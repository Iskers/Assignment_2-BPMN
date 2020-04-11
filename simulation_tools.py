import random, numpy, sklearn
from matplotlib import pyplot

import elements


class Generators:
    pass


class DurationGenerators(Generators):

    def __init__(self):
        super().__init__()
        pass

    @classmethod
    def project_duration_generator(cls, project):
        project_duration = 0
        for element in project:
            if isinstance(element, elements.Lane):
                project_duration += cls.lane_duration_generator(element)
        return project_duration

    @classmethod
    def lane_duration_generator(cls, lane):
        lane_duration = 0
        workload = cls.lane_workload_generator()
        for task in lane:
            lane_duration += cls.task_duration_generator(task, workload)
        return lane_duration

    @staticmethod
    def task_duration_generator(task, workload):
        expected_duration = task.minimum_duration + (task.maximum_duration - task.minimum_duration) * workload
        return random.triangular(task.minimum_duration, task.maximum_duration, expected_duration)

    @staticmethod
    def lane_workload_generator():
        return random.random()


class DateGenerator(Generators):
    duration_generator = DurationGenerators()

    @classmethod
    def generate_project_completion_date(cls, project):
        end_gate = cls.get_end_gate(project)
        workloads = cls.generate_task_workloads(project)
        task_durations = cls.generate_task_durations(project, workloads)
        return cls.generate_predecessing_completion_dates(end_gate, task_durations, project)

    @classmethod
    def generate_gate_due_date(cls, project: elements.Project, gate_name):
        gate = project.project_nodes[gate_name]
        workloads = cls.generate_task_workloads(project)
        task_durations = cls.generate_task_durations(project, workloads)
        due_date = cls.generate_predecessing_completion_dates(gate, task_durations, project)
        return due_date

    @classmethod
    def generate_predecessing_completion_dates(cls, node, task_durations, project):
        """
        :param node: Last node of project
        :param task_durations: Durations of nodes in project
        :param project: Project in which to analyze
        :return:
        """
        if node == cls.get_start_gate(project):
            node.start_date = 0
            node.completion_date = 0
            return node.completion_date

        if node.completion_date != -1:
            return node.completion_date
        else:
            if node.start_date == -1:
                previous_nodes = cls.get_previous_nodes(node, project)

                for previous_node in previous_nodes:
                    cls.generate_predecessing_completion_dates(previous_node, task_durations, project)
                    if previous_node.completion_date > node.start_date:
                        node.start_date = previous_node.completion_date
            node.completion_date = node.start_date + task_durations[node]
            return node.completion_date

    @classmethod
    def get_all_previous_nodes(cls, node, project):
        if node == cls.get_start_gate(project):
            return {}

        else:
            previous_nodes = set(cls.get_previous_nodes(node, project))
            for previous_node in previous_nodes:
                previous_nodes = previous_nodes.union(cls.get_all_previous_nodes(previous_node, project))
                # previous_nodes = previous_nodes + cls.get_all_previous_nodes(previous_node, project)
            return previous_nodes

    @classmethod
    def get_previous_nodes(cls, node, project):
        previous_nodes = []
        try:
            previous_nodes = previous_nodes + project.precedence_constraints[node]["From"]
        except:
            pass

        for element in project.container:
            if isinstance(element, elements.Lane):
                try:
                    previous_nodes = previous_nodes + element.precedence_constraints[node]["From"]
                except:
                    pass
        return previous_nodes

    @classmethod
    def get_start_gate(cls, project):
        for node in project.project_nodes:
            node = project.project_nodes[node]
            if isinstance(node, elements.Gate):
                if len(project.precedence_constraints[node]["From"]) == 0:
                    return node

    @classmethod
    def get_end_gate(cls, project):
        for node in project.project_nodes:
            node = project.project_nodes[node]
            if isinstance(node, elements.Gate):
                if len(project.precedence_constraints[node]["To"]) == 0:
                    return node

    @classmethod
    def generate_task_durations(cls, project, workloads):
        durations = {}
        for node in project.project_nodes:
            node = project.project_nodes[node]
            if isinstance(node, elements.Gate):
                durations[node] = 0
            else:
                durations[node] = cls.duration_generator.task_duration_generator(node, workloads[node])
        return durations

    @classmethod
    def generate_task_workloads(cls, project):
        lane_workloads = cls.generate_lane_workloads(project)
        workload = {}
        for element in project.container:
            if isinstance(element, elements.Lane):
                for node in element.container:
                    workload[node] = lane_workloads[element]
        return workload

    @classmethod
    def generate_lane_workloads(cls, project):
        workload_dictionary = {}
        for element in project.container:
            if isinstance(element, elements.Lane):
                workload_dictionary[element] = DurationGenerators.lane_workload_generator()
        return workload_dictionary

    @classmethod
    def get_predecessing_completion_dates(cls, node, project):
        previous_nodes = cls.get_all_previous_nodes(project.project_nodes[node], project)
        dates = numpy.zeros(len(previous_nodes))
        i = 0
        for previous_node in previous_nodes:
            dates[i] = previous_node.completion_date
            i += 1
        return dates

    @classmethod
    def project_reset(cls, project):
        for node in project.project_nodes:
            node = project.project_nodes[node]
            node.completion_date = -1
            node.start_date = -1


class MonteCarloSimulation:
    def __init__(self):
        pass

    @classmethod
    def Monte_Carlo_Basic(cls, project: elements.Project, sim_count):
        durations = cls.generate_project_durations(project, sim_count)
        mean_duration = durations.mean()
        standard_deviation = durations.std()
        minimum_duration = durations.min()
        maximum_duration = durations.max()
        quantile_median = numpy.quantile(durations, 0.5)
        quantile_top = numpy.quantile(durations, 0.9)
        pyplot.hist(durations, 25)
        pyplot.title("histogram")
        pyplot.show()
        pass

    @staticmethod
    def generate_project_durations(project: elements.Project, sim_count):
        durations = numpy.zeros(sim_count)
        for i in range(sim_count):
            durations[i] = DateGenerator.generate_project_completion_date(project)
            DateGenerator.project_reset(project)
        return durations

    def linear_study(self, some_val):
        pass

    @classmethod
    def generate_basic_result(cls, project, gate_name, maximum_duration):
        duration = DateGenerator.generate_gate_due_date(project, gate_name)

        if duration < maximum_duration:
            return 1
        else:
            return 0


class LabelStudy:
    pass

    @classmethod
    def generate_basic_label(cls, project, gate_name, maximum_duration):
        result = MonteCarloSimulation.generate_basic_result(project, gate_name, maximum_duration)
        dates = DateGenerator.get_predecessing_completion_dates(gate_name, project)
        return result, dates

    @classmethod
    def generate_multiple_labels(cls, project, gate_name, maximum_duration, labels):
        results = []
        dates = []
        for i in range(labels):
            result, date = cls.generate_basic_label(project, gate_name, maximum_duration)
            results.append(result)
            dates.append(date)
            DateGenerator.project_reset(project)
        return results, dates

    @classmethod
    def generate_results(cls, predicted_labels, solutions_labels):
        successful_predictions = [0, 0, 0]
        failed_predictions = [0, 0, 0]
        solution_data = [0, 0]
        predicted_data = [0, 0]

        for i in range(len(solutions_labels)):
            if predicted_labels[i] == solutions_labels[i]:
                cls.compare(solutions_labels[i], successful_predictions)
                successful_predictions[2] += 1
            else:
                cls.compare(solutions_labels[i], failed_predictions)
                failed_predictions[2] += 1
            cls.compare(solutions_labels[i], solution_data)
            cls.compare(predicted_labels[i], predicted_data)

        return successful_predictions, failed_predictions, solution_data, predicted_data

    @staticmethod
    def compare(boolean, list_):
        if boolean == 0:
            list_[0] += 1
        else:
            list_[1] += 1
        return list_


