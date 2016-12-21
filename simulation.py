from system import System
from numpy import std
from numpy.random import randint, seed
from os.path import curdir, join, isdir
from shutil import rmtree
from graph import graph_std_vs_n_proc
from time import sleep


def delete_log():
    if isdir(join(curdir, 'log')):
        rmtree(join(curdir, 'log'))


def generate_exec_times(n, min_time, max_time):
    exec_times = []
    while len(exec_times) < n:
        exec_time = randint(min_time, max_time)
        if exec_times.count(exec_time) == 0:
            exec_times.append(exec_time)
    return exec_times


def simulate():
    exec_times = generate_exec_times(n=7, min_time=10, max_time=100)
    system = System(end_time=1000, exec_times=exec_times, weight=0.5,
                    is_priorities=True, distribution='uniform', mean=7)
    system.process(system.source_processes())
    system.run(until=20000)

    print('Average queues length: {}'.format(system.avg_queues_len))
    print('Average waiting times: {}'.format(system.avg_times()))
    print('Standard deviation of queue length: {}'.format(std(system.avg_queues_len)))

simulate()
