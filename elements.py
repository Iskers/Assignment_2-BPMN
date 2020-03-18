# start


class ProjectElements:
    pass


class Node(ProjectElements):
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

    @staticmethod
    def factory(type_, *args):
        if type_ == "Gate":
            return Gate(*args)
        elif type_ == "Task":
            return Task(*args)
        else:
            raise Exception("Invalid node type")


class Container(ProjectElements):
    @staticmethod
    def factory(type_, *args):
        if type_ == "Lane":
            return Lane(*args)
        elif type_ == "Project":
            return Project(*args)
        else:
            raise Exception("Invalid container type")


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


class Lane(Container):
    def __init__(self, name, workload):
        self._name = name
        self._workload = workload


class Project(Container):
    def __init__(self, name):
        self._name = name


class PrecedenceConstraint(ProjectElements):
    precedence_constraints = {}

    def __init__(self, source: Node, target: Node):
        self._source = source
        self._target = target

        if not self.precedence_constraints[self.source]:
            self.precedence_constraints[self.source] = {}
        if not self.precedence_constraints[self.target]:
            self.precedence_constraints[self.target] = {}

        self.precedence_constraints[self.source]["To"] = self.target
        self.precedence_constraints[self.target]["From"] = self.source

    def __del__(self):
        previous = self.precedence_constraints[self.source]["From"]
        next_ = self.precedence_constraints[self.source]["To"]
        self.precedence_constraints[previous]["To"] = next_
        self.precedence_constraints[next_]["From"] = previous
        del self.precedence_constraints[self.source]

    @property
    def source(self):
        return self._source

    @property
    def target(self):
        return self._target

