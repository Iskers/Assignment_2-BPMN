class Node:
    _list_of_nodes = []

    def __init__(self, name, start_date, completion_date):
        self._name = name
        self._start_date = start_date
        self._completion_date = completion_date
        self._list_of_nodes.append(self)

    def __del__(self):
        self._list_of_nodes.remove(self)

    @property
    def predecessors(self):
        index = self._list_of_nodes.index(self)
        return self._list_of_nodes[:index]

    @property
    def successors(self):
        index = self._list_of_nodes.index(self)
        return self._list_of_nodes[index:]


class Container:
    @staticmethod
    def factory(type_, *args):
        if type_ == "Lane":
            return Lane(args)
        if type_ == "Project":
            return Project(args)


class Gate(Node):
    def __init__(self, name, start_date, completion_date):
        super().__init__(name, start_date, completion_date)


class Task(Node):
    def __init__(self, name, minimum_duration, maximum_duration, workload):
        super().__init__(name)
        self._expected_duration = self.calculate_expected_duration(minimum_duration, maximum_duration, workload)

    @staticmethod
    def calculate_expected_duration(minimum_duration, maximum_duration, workload):
        return minimum_duration + (maximum_duration - minimum_duration) * workload


class PrecedenceConstraint:
    def __init__(self, before: Node, after: Node):
        pass


class Lane(Container):
    def __init__(self, name, workload):
        self._name = name
        self._workload = workload


class Project(Container):
    def __init__(self, name):
        self._name = name
