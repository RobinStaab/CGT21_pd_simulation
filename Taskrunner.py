
import multiprocessing as mp
from queue import Empty
import time
from Simulator import Simulator
from test_simulator import generate_players

class SimulatorProcess(mp.Process):

    def __init__(self, task_queue, result_queue, step_size=100) -> None:
        mp.Process.__init__(self)
        self.task_queue = task_queue
        self.result_queue = result_queue
        self.step_size = step_size
        
    def run(self):
        sim = None
        proc_name = self.name
        while True:
            try:
                next_task = self.task_queue.get(False)  # Non-blocking get 
                if next_task.msg_type == "RESTART":
                    # Reset the simulation here
                    player_cfgs = generate_players( next_task.msg_content['strategy'],
                                                    next_task.msg_content['num_players'],
                                                    next_task.msg_content['play_window'],
                                                    next_task.msg_content['migrate_window'],
                                                    next_task.msg_content['imit_prob'],
                                                    next_task.msg_content['migrate_prob'])
                    sim = Simulator(    next_task.msg_content['grid_x'],
                                        next_task.msg_content['grid_y'],
                                        next_task.msg_content['num_players'],
                                        next_task.msg_content['play_window'],
                                        next_task.msg_content['migrate_window'],
                                        player_cfgs,
                                        next_task.msg_content['T'],
                                        next_task.msg_content['R'],
                                        next_task.msg_content['S'], 
                                        next_task.msg_content['P'])
                    print(f"Restarted Simulation with new CFG { next_task.msg_content['grid_x']} x { next_task.msg_content['grid_y']}")
                elif next_task.msg_type == "EXIT":
                    # Poison pill means shutdown
                    print('{}: Exiting'.format(proc_name))
                    break
            except Empty:
                #print("Continue to work")
                #time.sleep(2)
                pass

            
            if sim is not None:
                start_t = time.time()
                sim.simulate(self.step_size)
                
                print(f"Done with step: {time.time()-start_t} - Epoch: {sim.total_epoch}")
                start_t = time.time()
                answer = {'grid': sim.grid}     # TODO compute full output state at this point
                print(f"Queue is full: {self.result_queue.full()}")
                self.result_queue.put(answer, False)
                print(f"Continue runner {time.time()-start_t}")


class ProcessMsg:

    def __init__(self, msg_type: str, msg_content: dict):
        self.msg_type = msg_type
        self.msg_content = msg_content


if __name__ == '__main__':
    # Establish communication queues
    tasks = mp.Queue()
    results = mp.Queue()

    msg_dict = {
            'T' : 1.5,
            'R' : 1,
            'S' : 0.5,
            'P' : 0.8,
            'strategy'        : "random",
            'grid_x'          : 20,
            'grid_y'          : 20,
            'num_players'     : 350,
            'play_window'     : 1,
            'migrate_window'  : 3,
            'imit_prob'       : 0.8,
            'migrate_prob'    : 0.8,
            'epochs'          : 1000
    }


    # Start the Simulator process
    num_servers = 1 #mp.cpu_count() * 2
    print('Creating {} consumers'.format(num_servers))
    consumers = [SimulatorProcess(tasks, results) for i in range(num_servers) ]
    for w in consumers:
        w.start()

    # Enqueue jobs
    num_jobs = 5
    for i in range(num_jobs):
        tasks.put(ProcessMsg("RESTART", msg_content=msg_dict))
        time.sleep(2)

    # Add a poison pill for each consumer
    for i in range(num_servers):
        tasks.put(ProcessMsg("EXIT", msg_content=msg_dict))

    # Start printing results
    while num_jobs:
        result = results.get()
        print('Result:', result)
        num_jobs -= 1