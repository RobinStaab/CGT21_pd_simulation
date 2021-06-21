import numpy as np
import test_simulator
from Simulator import Simulator
import os
from tqdm.contrib.concurrent import process_map
from analysis import *
from random import randint, seed
from itertools import repeat

def read_file(file_name):
    experiments = []
    nr_experiments = 0
    with open(file_name, mode='r') as csv_file:
        lines = csv_file.read().splitlines() 
        for line in lines:
            if len(line) == 0:
                continue
            elif line[0] == '#':
                experiments.append({'name': line[1:], 'params': {}, 'players': [], 'changed_keys': {}})
                read_ind = 1
                nr_experiments = nr_experiments + 1
                nr_players = 0
            elif read_ind == 1:
                param_keys = line.split(', ')
                read_ind = read_ind + 1
            elif read_ind == 2:
                param_values = line.split(', ')
                assert len(param_keys)==len(param_values), f"Missing values in parameters of experiment {nr_experiments}"
                for key_i in range(len(param_keys)):
                    experiments[-1]['params'][param_keys[key_i]] = param_values[key_i]
                read_ind = read_ind + 1
            elif read_ind == 3:
                read_ind = 0
                keys = line.split(', ')
                nr_keys = len(keys)
            else:
                values = line.split(', ')
                assert len(values)==nr_keys, f"Missing values in player {nr_players} of experiment {nr_experiments}"
                params = {}
                for i in range(nr_keys):
                    params[keys[i]] = values[i]
                params['id'] = nr_players
                experiments[-1]['players'].append(params)
                nr_players = nr_players + 1
    return experiments

def expand_players(experiments):
    for exp_i in range(len(experiments)):
        keys = list(experiments[exp_i]['players'][0].keys())
        for pl_i in range(len(experiments[exp_i]['players'])):
            for key_i in range(len(keys)):
                param = experiments[exp_i]['players'][pl_i][keys[key_i]]
                if  isinstance(param, str) and (';' in param or ':' in param):
                    expanded_exp = []
                    if ':' in param:
                        values = param.split(':')
                    else:
                        start, end, step = param.split(';')
                        values = np.arange(float(start), float(end)+float(step), float(step))
                    for value in values:
                        temp_exp = experiments[exp_i].copy()
                        temp_exp['players'] = experiments[exp_i]['players'].copy()
                        temp_exp['players'][pl_i] = experiments[exp_i]['players'][pl_i].copy()
                        if not pl_i in temp_exp['changed_keys']:
                            temp_exp['changed_keys'][pl_i] = []
                        if not keys[key_i] in temp_exp['changed_keys'][pl_i]:
                            temp_exp['changed_keys'][pl_i].append(keys[key_i])
                        temp_exp['players'][pl_i][keys[key_i]] = value
                        expanded_exp.append(temp_exp)
                    if exp_i != 0:
                        expanded_exp = experiments[:exp_i] + expanded_exp
                    if exp_i != len(experiments)-1:
                        expanded_exp = expanded_exp + experiments[exp_i+1:]
                    return expand_players(expanded_exp)
    return experiments

def convert_values(experiments):
    for exp in experiments:
        for param in exp['params']:
            if param in ['T', 'R', 'S', 'P']:
                exp['params'][param] = float(exp['params'][param])
            elif param in ['grid_x', 'grid_y', 'epochs', 'runs']:
                exp['params'][param] = int(float(exp['params'][param]))
            elif param in ['infinite']:
                exp['params'][param] = exp['params'][param] == 'True'
            else:
                assert False, f"Parameter {key} not implemented for experiments"
        for player in exp['players']:
            for key in player.keys():
                if key in ['strat']:
                    continue
                elif key in ['id', 'nr']:
                    player[key] = int(float(player[key]))
                elif key in ['imit_prob', 'migrate_prob', 'omega']:
                    player[key] = float(player[key])
                else:
                    assert False, f"Key {key} not implemented for experiments"
        #add changed keys to name
        player_changes = []
        for p_i in range(len(exp['players'])):
            changes = []
            if p_i in exp['changed_keys']:
                for key in exp['changed_keys'][p_i]:
                    changes.append(f'{key}-{exp["players"][p_i][key]}')
                player_changes.append(f"{p_i}:{'_'.join(changes)}")
        exp['name'] = exp['name'] + ''.join([f'_({change})' for change in player_changes])

    return experiments

def class_name(player):
    return f"{player['strat']}_imitP-{player['imit_prob']}_migrateP-{player['migrate_prob']}_omega-{player['omega']}"
   
def run_experiment(experiment):
    player_cfgs = []
    classes = []
    strategies = []
    num_players = 0
    for player in experiment['players']:
        player_class = class_name(player)
        for i in range(player['nr']):
            player_cfgs.append(test_simulator.generate_player(player['strat'], player_class, 1, 3, player['imit_prob'], player['migrate_prob'], player['omega']))
        num_players = num_players + player['nr']
        if player_class not in classes:
            classes.append(player_class)
        if player['strat'] not in strategies:
            strategies.append(player['strat'])

    nr_results = 5
    nr_runs = experiment['params']['runs']
    results = [[] for i in range(nr_results)]
    averages = []
    for r in range(nr_runs):

        sim = Simulator(experiment['params']['grid_x'], experiment['params']['grid_y'], num_players, 1, 3, player_cfgs, experiment['params']['T'], experiment['params']['R'], experiment['params']['S'], experiment['params']['P'], experiment['params']['infinite'], rand_seed=randint(0,13371337))
        sim.simulate(experiment['params']['epochs'], visualize=False)
        state = sim.get_state()

        t, df_dpc, fig_dpc = defection_per_class_over_time(sim.get_state(), strategies, visualize=False)
        results[0].append(df_dpc)
        t2, df_cd, fig_cd   = class_distribution_over_time(sim.map_history, strategies, visualize=False)
        results[1].append(df_cd)
        t3, df_cvc, fig_cvc = class_vs_class_over_time(sim.get_state(), strategies, visualize=False)
        results[2].append(df_cvc)
        t4, df_ppc, fig_ppcot = payoff_per_class_over_time(sim.get_state(), strategies, visualize=False)
        results[3].append(df_ppc)
        t5, df_poo, fig_poo = percentage_of_optimum(sim.get_state(), experiment['params']['T'], strategies, visualize=False)
        results[4].append(df_poo)
    
    for res in range(nr_results):
        #print(results[res])
        for run in range(nr_runs):
            if run == 0:
                sum = results[res][run]
            else:
                sum = sum + results[res][run]
            
        averages.append(sum/nr_runs)
        #print(averages[-1])
    
    if not os.path.exists('data'):
        os.makedirs('data')
    exp_dir = f"data/{experiment['name']}"
    if not os.path.exists(exp_dir):
        os.makedirs(exp_dir)

    figs = {}
    averages[0].to_csv(f'{exp_dir}/dpc.csv')
    figs['dpc'] = vis_dpc(averages[0])
    averages[1].to_csv(f'{exp_dir}/cd.csv')
    figs['cd'] = vis_cd(averages[1])
    averages[2].to_csv(f'{exp_dir}/cvc.csv')
    figs['cvc'] = vis_cvc(averages[2])
    averages[3].to_csv(f'{exp_dir}/ppc.csv')
    figs['ppc'] = vis_ppc(averages[3])
    averages[4].to_csv(f'{exp_dir}/poo.csv')
    figs['poo'] = vis_poo(averages[4])
    for fig in figs:
        if html:
            figs[fig].write_html(f'{exp_dir}/{fig}.html')
        if png: 
            figs[fig].write_image(f'{exp_dir}/{fig}.png')
    
    

if __name__ == "__main__":
    seed(42)
    global html 
    global png 
    html = True
    png = False  #write_image doesn't work on WSL1 -> had to set it to False :-(

    experiments = read_file('experiments.csv')
    experiments = expand_players(experiments)
    experiments = convert_values(experiments)
    if False:
        for exp in experiments:
            print(exp)

    process_map(run_experiment, experiments) #max_workers=8