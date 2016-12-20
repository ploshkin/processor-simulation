from system import System
from numpy import mean, std
from numpy.random import randint, seed


def generate_exec_times(n, min_time, max_time):
    exec_times = []
    while len(exec_times) < n:
        exec_time = randint(min_time, max_time)
        if exec_times.count(exec_time) == 0:
            exec_times.append(exec_time)
    return exec_times


def simulate(n_iterations):
    seed(0)
    exec_times = generate_exec_times(n=10, min_time=10, max_time=100)
    deviations = []
    for i in range(n_iterations):
        system = System(end_time=1000, exec_times=exec_times, weight=0.6, is_priorities=False)
        system.process(system.source_processes())
        system.run(until=20000)
        deviations.append(std(system.avg_queues_len))
        print(std(system.avg_queues_len))

    print('mean deviation = {}'.format(mean(deviations)))

simulate(100)
