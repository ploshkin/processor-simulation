from simpy.resources.resource import PriorityRequest


class RequestProcessor(PriorityRequest):
    def __init__(self, processor, process_type, priority):
        self.type = process_type
        super().__init__(resource=processor, priority=priority)


class Process:
    def __init__(self, env, type, pid):
        self._env = env
        self.type = type
        self._exec_time = self._env.exec_times[self.type]
        self.pid = pid
        self._processor = self._env.processor
        self.wait_time = 0
        self.completed = False
        self._priority = 0
        self._env.fp.write('New process {} appeared at time {}\n'.format(self, self._env.now))

    def __format__(self, format_spec):
        return '<pid={}, type={}>'.format(self.pid, self.type)

    def run(self, priority):
        self._priority = priority
        with RequestProcessor(self._processor, self.type, self._priority) as req:
            self.wait_time = -self._env.now
            yield req

            self.wait_time += self._env.now
            self._env.fp.write('Process {} start running at {}\n'.format(self, self._env.now))
            yield self._env.process(self.exec())

    def exec(self):
        if self._env.is_quantum(self._priority) and self._exec_time > self._env.quantum:
            self._env.fp.write('Quantum assigned for process {}\n'.format(self))
            yield self._env.timeout(self._env.quantum)
            self._env.process(self.run(self._priority))
        else:
            yield self._env.timeout(self._exec_time)



