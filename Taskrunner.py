
from History import History
import multiprocessing as mp
import numpy as np
from queue import Empty
import time
from Simulator import Simulator
from test_simulator import generate_simple_players
from analysis import *

class SimulatorProcess(mp.Process):

    def __init__(self, task_queue, result_queue, step_size=50) -> None:
        mp.Process.__init__(self)
        self.task_queue = task_queue
        self.result_queue = result_queue
        self.step_size = step_size
        
    def run(self):
        sim = None
        proc_name = self.name
        state = 0       # 0 Not running # 1 Running # 2 Paused  
        history = []
        while True:
            try:
                next_task = self.task_queue.get(False)  # Non-blocking get 
                ####
                ## Receive Messages
                ####
                print(f"Received: {next_task.msg_type}")
                if next_task.msg_type == "RESTART":

                    self.strats = next_task.msg_content['strategies']
                    self.step_size =next_task.msg_content['step-size']
                    # Reset the simulation here
                    # print("WTF")
                    player_cfgs = generate_simple_players( next_task.msg_content['strategies'],
                                                    next_task.msg_content['counts'],
                                                    next_task.msg_content['play_window'],
                                                    next_task.msg_content['migrate_window'],
                                                    next_task.msg_content['imit_prob'],
                                                    next_task.msg_content['migrate_prob'],
                                                    next_task.msg_content['omega'])
                    # print("WTF")
                    sim = Simulator(next_task.msg_content['grid_x'],
                                    next_task.msg_content['grid_y'],
                                    next_task.msg_content['num_players'],
                                    next_task.msg_content['play_window'],
                                    next_task.msg_content['migrate_window'],
                                    player_cfgs,
                                    next_task.msg_content['T'],
                                    next_task.msg_content['R'],
                                    next_task.msg_content['S'], 
                                    next_task.msg_content['P'],
                                    False,
                                    next_task.msg_content['rand_seed'])
                    
                    history = []
                    state = 1
                    self.T = next_task.msg_content['T']

                    print(f"Restarted Simulation with new CFG { next_task.msg_content['grid_x']} x { next_task.msg_content['grid_y']} - Num_players: {next_task.msg_content['num_players']}")
                
                elif next_task.msg_type == "RESET":
                    
                    # Poison pill means shutdown
                    print('{}: Resetting the Simulation'.format(proc_name))
                    sim = None
                    history = []
                    state = 0
                
                elif next_task.msg_type == "TOGGLE":
                    
                    if state == 1:
                        # Poison pill means shutdown
                        print('{}: Pausing'.format(proc_name))
                        state = 2
                    elif state == 2:
                        if sim is None:
                            print(f"Cannot find prior simulation please start first.")
                        else:
                            print(f"Continuing the simulation")
                            state = 1
                    else:
                        print(f"Nothing to continue")

            except Empty :   # Might just sleep on empty queue
                if sim is None:
                    time.sleep(0.5)
                pass
            except AssertionError:
                sim = None
                state = 0

            try:
                if sim is not None and state == 1:
                    start_t = time.time()

                    print(f"Starting step: {state}")
                    sim.simulate(self.step_size)
                    
                    print(f"Done with step: {time.time()-start_t} - Epoch: {sim.total_epoch}")
                    start_t = time.time()

                    # Prepare the ouput 
                    def my_map(x):
                        if x == 0:
                            return x
                        else:
                            return self.strats.index(sim.players[int(x)-1].strategy.name)+1

                    #print(f"Counted players {len(np.nonzero(np.vectorize(my_map)(sim.grid))[0])}")
                    start_t = time.time()
                    
                    
                    # We want to have at most 50 time-points (epochs) in here 
                    sim_state = sim.get_state()

                    # TODO Actually could pre-sort by epoch here and make our live much easier 
                    curr_Epoch = sim.total_epoch
                    if(sim.total_epoch > 50):
                        selected_epochs = list(np.floor(np.linspace(0, sim.total_epoch, 50)))
                        selected_state = { }
                        """for p_id, p_val in sim_state.items():
                            for e_id, e_val in p_val.history.items():
                                for game in e_val:
                                    if game.epoch in selected_epochs:
                                        if selected_state.get(p_id) is None:
                                            selected_state[p_id] = History()
                                        if selected_state[p_id].history.get(e_id) is None:
                                            selected_state[p_id].history[e_id] = [ ]
                                        selected_state[p_id].history[e_id].append(game)"""
                        for p_id, p_val in sim_state.items():
                            for t_id, t_val in p_val.index_history.items():
                                if t_id in selected_epochs:
                                    if selected_state.get(p_id) is None:
                                            selected_state[p_id] = History()
                                    for e_id, e_val in t_val.items():
                                        if selected_state[p_id].history.get(e_id) is None:
                                            selected_state[p_id].history[e_id] = [ ]
                                        selected_state[p_id].history[e_id].extend(e_val)
                    else:
                        selected_state = sim_state
                    print(f"Done with reduction: {time.time()-start_t} - Epoch: {sim.total_epoch}")

                    start_t = time.time()
                    t1, df_dpcot, fig_dpc   = defection_per_class_over_time(selected_state,    self.strats, visualize=False)
                    t2, df_cd, fig_cd       = class_distribution_over_time(sim.map_history,     self.strats, visualize=False)
                    t3, df_cvc, fig_cvc     = class_vs_class_over_time(selected_state,         self.strats, visualize=False)
                    t4, df_ppcot, fig_ppcot = payoff_per_class_over_time(selected_state,       self.strats, visualize=False)
                    t5, df_poo, fig_poo     = percentage_of_optimum(selected_state, self.T,    self.strats, visualize=False)
                    print(f"Done with analysis: {time.time()-start_t} - Epoch: {sim.total_epoch}")

                    answer = { 'epoch': sim.total_epoch,
                            'grid' : np.vectorize(my_map)(sim.grid),
                            'df_dpc': df_dpcot,
                            'df_cd': df_cd,
                            'df_cvc': df_cvc,
                            'df_ppc': df_ppcot,
                            'df_poo': df_poo,
                            #'state': sim.get_state()   Kills it
                            }     # TODO compute full output state at this point

                    history.append(answer)
                    #print(f"Queue is full: {self.result_queue.full()}")
                    self.result_queue.put(answer, False)
                    #print(f"Continue runner {time.time()-start_t}")
            except Exception as e:   # Simply reset
                print(f"Broken: {e}")
                sim = None
                state = 0


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
            'epochs'          : 1000,
            'step-size'       : 20
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