# start
import simulation_tools as st


class ProjectElement:
    pass


class Node(ProjectElement):
    _list_of_nodes = []

    def __init__(self, name, start_date, completion_date, project_nodes):
        self._name = name
        self._start_date = start_date
        self._completion_date = completion_date
        self._project_nodes = project_nodes
        self._project_nodes.append(self)

    def __del__(self):
        self._project_nodes.remove(self)

    @property
    def predecessors(self):
        index = self._project_nodes.index(self)
        return self._project_nodes[:index]

    @property
    def successors(self):
        index = self._project_nodes.index(self)
        return self._project_nodes[index:]

    @staticmethod
    def factory(type_, *args):
        if type_ == "Gate":
            return Gate(*args)
        elif type_ == "Task":
            return Task(*args)
        else:
            raise Exception("Invalid node type")


class Gate(Node):
    def __init__(self, name, start_date, completion_date, project_nodes):
        super().__init__(name, start_date, completion_date, project_nodes)


class Task(Node):
    def __init__(self, name, start_date, completion_date, project_nodes, minimum_duration, maximum_duration):
        super().__init__(name, start_date, completion_date, project_nodes)
        self.minimum_duration = minimum_duration
        self.maximum_duration = maximum_duration
        self._expected_duration = -1
        self._duration = -1

    @property
    def duration(self):
        if self._duration < 0:
            return self.generate_duration()
        else:
            return self._duration

    def generate_expected_duration(self, workload):
        return self.minimum_duration + (self.maximum_duration - self.minimum_duration) * workload

    def generate_duration(self):

        st.DurationGenerators.task_duration_generator(self, )

class Container(ProjectElement):
    def __init__(self):
        self._container = []
        self._precedence_constraints = PrecedenceConstraintsContainer()

    @property
    def container(self):
        return self._container

    @staticmethod
    def factory(type_, *args):
        if type_ == "Lane":
            return Lane(*args)
        elif type_ == "Project":
            return Project(*args)
        else:
            raise Exception("Invalid container type")

    def add_node(self, *args, **kwargs):
        type_ = args[0]
        args = args[1:]
        node = Node.factory(args[0], *args)
        self.container.append(node)
        self._precedence_constraints.add_constraint()


class Lane(Container):
    def __init__(self, name, workload):
        super().__init__()
        self._name = name
        self._workload = workload


class Project(Container):
    def __init__(self, name):
        super().__init__()
        self._name = name

    def add_lane(self, *args):
        lane = Lane(*args)
        self.container.append(lane)


class PrecedenceConstraintsContainer(ProjectElement):

    def __init__(self):
        self._container = {}

    @property
    def container(self):
        return self._container

    def add_constraint(self, source: Node, target: Node):
        self.container[source]["To"] = target
        self.container[target]["From"] = source

    def remove_constraint(self, source):
        previous = self.container[source]["From"]
        next_ = self.container[source]["To"]
        self.container[previous]["To"] = next_
        self.container[next_]["From"] = previous
        del self.container[source]


class PrecedenceConstraint(ProjectElement):
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
