'''
Generates bash script to run grid search for each task/model over hyperparameters

Right now is super simple and mostly hard coded. Grid tweaked at top of file.
'''

import os

COMMAND_TEMPLATE = '--gres=gpu:1 -l -c 2 -p gpuc -J \'lstm-gsrch\' python main.py --optim {} --lrdecay {} --lr {}\n'
LR_RANGE = [100.0, 50.0, 30.0, 10.0, 1.0, 0.1]
OPTIMIZERS = {
    'adam': [100.0, 50.0, 30.0, 10.0, 1.0, 0.1],
    'sgd': [100.0, 50.0, 30.0, 10.0, 1.0, 0.1],
    'aggmo': [100.0, 50.0, 30.0, 10.0, 1.0, 0.1]
}
DECAYS = [0.1, 0.5, 1.0]

FIlENAME = 'run_jobs.sh'

def generate_job_strings():
    jobs = []
    for optim, lrates in OPTIMIZERS.items():
        for lr in lrates:
            for decay in DECAYS:
                command = COMMAND_TEMPLATE.format(optim, decay, lr)
                jobs.append(command)
    return jobs

if __name__ == '__main__':
    jobs = generate_job_strings()
    with open(FIlENAME, 'w') as f:
        f.writelines(jobs)
