from simpy import Environment
from simpy.resources.resource import PriorityResource
from process import Process
from numpy.random import randint, rand, seed, normal
from numpy import maximum, minimum
from os.path import curdir, join, isdir
from os import listdir, mkdir


def get_priorities(exec_times, is_priorities):
    priorities = [1 for k in range(len(exec_times))]
    min_time = min(exec_times)
    max_time = max(exec_times)

    if is_priorities:
        for k in range(len(exec_times)):
            priorities[k] = (exec_times[k] - min_time) / (max_time - min_time)

    return priorities


def quantile(lst, weight):
    weight = maximum(0, minimum(1, weight))  # weight e [0, 1]
    return sorted(lst)[int(len(lst) * weight - 1)]


class System(Environment):
    def __init__(self, end_time, exec_times, weight, is_priorities=True, distribution='uniform', mean=5):
        super().__init__()
        self._end_time = end_time
        self._n_types = len(exec_times)
        self.exec_times = exec_times
        self.priorities = get_priorities(exec_times=self.exec_times, is_priorities=is_priorities)
        self.processor = PriorityResource(env=self, capacity=1)
        self._process_count = [0 for k in range(self._n_types)]
        self._processes = []
        self.__total_queues_len = [0 for k in range(self._n_types)]
        self.quantum = quantile(lst=self.exec_times, weight=weight)
        self.fp = self.get_fp()
        if distribution != 'uniform' and distribution != 'normal':
            print('Error: distribution "{}" does not supported'.format(distribution))
            distribution = 'uniform'
        self._distribution = distribution
        if mean <= 0:
            print('Error: mean value must be > 0')
            mean = 5
        self._mean = mean

        self.fp.write('Execution times: {}\n'.format(self.exec_times))
        self.fp.write('Quantum duration: {}\n'.format(self.quantum))

    def get_fp(self):
        log_dir = join(curdir, 'log')
        if not isdir(log_dir):
            mkdir(log_dir)
        idx = len(listdir(log_dir)) + 1
        fp = open(join(log_dir, 'log.txt'.format(idx)), 'w')
        return fp

    @property
    def _wait_time(self):  # TODO
        val = 0
        if self._distribution == 'normal':
            while val <= 0:
                val = int(normal(loc=self._mean, scale=(self._mean-1)/3))
        elif self._distribution == 'uniform':
            val = randint(1, self._mean*2)
        return val

    def avg_times(self):
        avg = []
        for k in range(self._n_types):
            process_list_k = [process.wait_time for process in self._processes if process.type == k]
            if len(process_list_k) > 0:
                time = sum(process_list_k) / len(process_list_k)
            else:
                time = 0
            avg.append(time)

        print('Average waiting times: {}\n'.format(avg))
        return avg

    @property
    def avg_queues_len(self):
        if self.now >= self._end_time:
            return [queue_len / self._end_time for queue_len in self.__total_queues_len]
        else:
            return [queue_len / self.now for queue_len in self.__total_queues_len]

    def queues_len(self):
        queue = [req.type for req in self.processor.put_queue]
        return [queue.count(k) for k in range(self._n_types)]

    def add_len(self, queues_len):
        for k in range(self._n_types):
            self.__total_queues_len[k] += queues_len[k]

    def source_processes(self):
        time_to_next = 0
        # generate and execute processes
        while self.now < self._end_time:
            if time_to_next == 0:
                time_to_next = self._wait_time
                process = Process(env=self, type=randint(self._n_types), pid=sum(self._process_count))
                self._processes.append(process)
                self._process_count[process.type] += 1
                self.process(process.run(self.priorities[process.type]))
            else:
                self.add_len(self.queues_len())
                yield self.timeout(1)
                time_to_next -= 1
        # execute remaining processes
        while sum(self.queues_len()):
            yield self.timeout(1)

    def is_quantum(self, priority):
        val = rand()
        if val < priority * 0.2:
            return True
        else:
            return False
