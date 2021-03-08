'''
Generates bash script to run grid search for each task/model over hyperparameters

Right now is super simple and mostly hard coded. Grid tweaked at top of file.
'''

import os
import itertools

COMMAND_TEMPLATE = 'CUDA_VISIBLE_DEVICES={} python main.py --optim {} --lrdecay {} --momentum {} --lr {}\n'
TOTAL_GPU=4

LR_RANGE = [50.0, 30.0, 10.0, 1.0, 0.1]
OPTIMIZERS = {
    'nesterov': [5.0, 1.0, 0.1, 0.05],
    #'sgd': [100.0, 50.0, 30.0, 10.0, 1.0, 0.1],
    #'aggmo': [100.0, 50.0, 30.0, 10.0, 1.0, 0.1]
}
DECAYS = [0.5]
MOM = [0.9, 0.99]

FIlENAME = 'run_jobs_{}.sh'

def generate_job_strings():
    jobs = {}
    j = 0
    for i in range(TOTAL_GPU):
        jobs[i] = []

    for optim, lrates in OPTIMIZERS.items():
        for lr in lrates:
            for decay in DECAYS:
                for mom in MOM:
                    job = COMMAND_TEMPLATE.format(j % TOTAL_GPU, optim, decay, mom, lr)
                    jobs[j % TOTAL_GPU].append(job)
                    j+=1
    return jobs


if __name__ == '__main__':
    jobs = generate_job_strings()
    for gpu_id, jobs in jobs.items():
        with open(FIlENAME.format(gpu_id), 'w') as f:
            f.writelines(jobs)
