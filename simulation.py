from system import System
from numpy import mean, std
from numpy.random import randint, seed
from os.path import curdir, join, isdir
from shutil import rmtree
from graph import graph_std_vs_n_proc, graph_std_vs_quantum
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


def simulate(n_iterations):
    # seed(0)

    # mean standard deviation of queue length vs. number of types
    list_mean_deviations = []
    priorities_flags = [True, False]

    for is_priorities in priorities_flags:
        n_processes = [n for n in range(2, 21)]
        mean_deviations = []
        for n_proc in n_processes:
            print(n_proc)
            deviations = []
            for i in range(n_iterations):
                exec_times = generate_exec_times(n=n_proc, min_time=10, max_time=100)
                system = System(end_time=1000, exec_times=exec_times, weight=0.6,
                                is_priorities=is_priorities, distribution='normal')
                system.process(system.source_processes())
                system.run(until=20000)
                deviations.append(std(system.avg_queues_len))

                print(system.avg_queues_len)
                print(std(system.avg_queues_len))

            mean_deviations.append(mean(deviations))

        list_mean_deviations.append(mean_deviations)

    graph_std_vs_n_proc(x=[n_processes for i in range(len(priorities_flags))], y=list_mean_deviations,
                        labels=priorities_flags, distribution='normal')

    # mean standard deviation of queue length vs. weight
    # weights = arange(0.05, 1.05, 0.05)
    # mean_deviations = []
    # for quantum_weight in weights:
    #     print(quantum_weight)
    #     deviations = []
    #     for i in range(n_iterations):
    #         exec_times = generate_exec_times(n=12, min_time=10, max_time=100)
    #         system = System(end_time=1000, exec_times=exec_times, weight=quantum_weight, is_priorities=True)
    #         system.process(system.source_processes())
    #         system.run(until=20000)
    #         deviations.append(std(system.avg_queues_len))
    #     mean_deviations.append(mean(deviations))
    # graph_std_vs_quantum(x=weights, y=mean_deviations)

simulate(10)
