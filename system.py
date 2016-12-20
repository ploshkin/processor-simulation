from simpy import Environment
from simpy.resources.resource import PriorityResource
from process import Process
from numpy.random import randint, rand, seed


def get_priorities(exec_times, is_priorities):
    priorities = [1 for k in range(len(exec_times))]
    min_time = min(exec_times)
    max_time = max(exec_times)

    if is_priorities:
        for k in range(len(exec_times)):
            priorities[k] = (exec_times[k] - min_time) / (max_time - min_time)

    return priorities


def quantile(lst, weight):
    return sorted(lst)[int(len(lst) * weight - 1)]


class System(Environment):
    def __init__(self, end_time, exec_times, weight, is_priorities=True):
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

    @property
    def _wait_time(self):  # TODO
        return randint(1, 10)

    @property
    def avg_times(self):
        avg = []
        for k in range(self._n_types):
            process_list_k = [process.wait_time for process in self._processes if process.type == k]
            if len(process_list_k) > 0:
                avg.append(sum(process_list_k) / len(process_list_k))
            else:
                avg.append(0)
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
                process = Process(self, randint(self._n_types), sum(self._process_count))
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
