# start
import simulation_tools as st


class ProjectElement:
    pass


class Node(ProjectElement):
    _list_of_nodes = []

    def __init__(self, name, project_nodes):
        self._name = name
        self._start_date = -1
        self._completion_date = -1
        self._project_nodes = project_nodes
        self._project_nodes.append(self)

    def __del__(self):
        self._project_nodes.remove(self)

    def __str__(self):
        return self.name

    @property
    def name(self):
        return self._name

    @property
    def predecessors(self):
        index = self._project_nodes.index(self)
        return self._project_nodes[:index]

    @property
    def successors(self):
        index = self._project_nodes.index(self)
        return self._project_nodes[index + 1:]

    @staticmethod
    def factory(type_, **kwargs):
        if type_ == "Gate":
            return Gate(**kwargs)
        elif type_ == "Task":
            return Task(**kwargs)
        else:
            raise Exception("Invalid node type")


class Gate(Node):
    def __init__(self, name, project_nodes):
        super().__init__(name, project_nodes)


class Task(Node):
    def __init__(self, name, minimum_duration: float, maximum_duration: float, project_nodes):
        super().__init__(name, project_nodes)
        self.minimum_duration = float(minimum_duration)
        self.maximum_duration = float(maximum_duration)

    # Todo remove
    '''
        self._expected_duration = -1
        self._duration = -1

    # Can only be generated in a lane context
    @property
    def duration(self):
        if self._duration < 0:
            raise Exception("No duration")
        else:
            return self._duration

    @duration.setter
    def duration(self, value):
        self._duration = value

    def generate_expected_duration(self, workload):
        return self.minimum_duration + (self.maximum_duration - self.minimum_duration) * workload

    def generate_duration(self, workload):
        self._expected_duration = self.generate_expected_duration(workload)
        duration = st.DurationGenerators.task_duration_generator(self.minimum_duration, self.maximum_duration,
                                                                 self._expected_duration)
        self.duration = duration
    '''


class Container(ProjectElement):
    def __init__(self, name):
        self._name = name
        self._container = []
        self._precedence_constraints = PrecedenceConstraintsContainer()
        self._nodes = []

    def __str__(self):
        return self.name

    def __iter__(self):
        return iter(self.container)

    @property
    def container(self):
        return self._container

    @property
    def name(self):
        return self._name

    @property
    def nodes(self):
        return self._nodes

    @property
    def precedence_constraints(self):
        return self._precedence_constraints

    @staticmethod
    def factory(type_, *args):
        if type_ == "Lane":
            return Lane(*args)
        elif type_ == "Project":
            return Project(*args)
        else:
            raise Exception("Invalid container type")

    def add_node(self, **kwargs):
        kwargs = self.key_treatment(kwargs)
        node = Node.factory(**kwargs, project_nodes=self.nodes)
        self.container.append(node)

    @staticmethod
    def key_treatment(dictionary):
        for key in dictionary:
            if "-" in key:
                temp_name = key.replace("-", "_")
                dictionary[temp_name] = dictionary.pop(key)
        return dictionary

    def add_constraint(self, source, target):
        self.precedence_constraints.add_constraint(source, target)

    # Todo remove
    def add_lane(self, param):
        pass


class Lane(Container):
    def __init__(self, name):
        super().__init__(name)
        self._workload = -1

    # Todo remove
    '''
    @property
    def workload(self):
        if self._workload < 0:
            self._workload = st.DurationGenerators.lane_workload_generator(self)
        return self._workload
    '''


class Project(Container):
    def __init__(self, name):
        super().__init__(name)

    def add_lane(self, **kwargs):
        lane = Lane(**kwargs)
        self.container.append(lane)
        return lane


class PrecedenceConstraintsContainer(ProjectElement):
    def __init__(self):
        self._container = {}

    def __iter__(self):
        return iter(self.container)

    def __str__(self):
        return self.container

    @property
    def container(self):
        return self._container

    def add_constraint(self, source: Node, target: Node):
        if source not in self.container:
            self.container[source] = {"To": [], "From": []}
        if target not in self.container:
            self.container[target] = {"To": [], "From": []}
        self.container[source]["To"].append(target)
        self.container[target]["From"].append(source)

    def remove_constraint(self, source):
        previous = self.container[source]["From"]
        next_ = self.container[source]["To"]
        self.container[previous]["To"] = next_
        self.container[next_]["From"] = previous
        del self.container[source]

    def __getitem__(self, item):
        return self.container[item]


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
