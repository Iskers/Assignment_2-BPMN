import random, numpy, sklearn
from matplotlib import pyplot
from sklearn.neural_network import MLPClassifier
from sklearn.naive_bayes import GaussianNB

import elements
from src.path_finder import *


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
    def Monte_Carlo_Basic(cls, project: elements.Project, sim_count, file_name) -> tuple:
        project_attributes = {}
        durations = cls.generate_project_durations(project, sim_count)
        project_attributes["durations"] = durations
        project_attributes["mean duration"] = durations.mean()
        project_attributes["standard deviation"] = durations.std()
        project_attributes["minimum duration"] = durations.min()
        project_attributes["maximum duration"] = durations.max()
        project_attributes["Quantile median"] = numpy.quantile(durations, 0.5)
        project_attributes["Quantile 0.9"] = numpy.quantile(durations, 0.9)

        pyplot.hist(durations, 25)
        pyplot.title("histogram")
        pyplot.xlabel("Durations")
        pyplot.ylabel("Cases")
        path = PathFinder.get_folder_path("templates")
        file_path = f"{path}/{file_name}"
        pyplot.savefig(file_path)
        return file_name, project_attributes

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

        # #0-Successful failures discovered  #1-Successful successes discovered, #2-Successes
        successful_predictions = [0, 0, 0]
        # #0-Failures not discovered  #1-Successes not discovered, #2-Fails
        failed_predictions = [0, 0, 0]

        # #0-Failures, #1 - Successes
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


class AlgorithmStudy:

    @classmethod
    def three_algorithms(cls, project, gate_name, date, labels):
        training_labels, training_sample = LabelStudy.generate_multiple_labels(project,
                                                                               gate_name, date, labels)

        results = {}

        first_model = GaussianNB()
        first_model.fit(training_sample, training_labels)
        print("Logistic Regression: Training set learned")

        predicted_labels = first_model.predict(training_sample)
        results["Gaussian"] = LabelStudy.generate_results(predicted_labels, training_labels)

        second_model = sklearn.svm.SVC()
        second_model.fit(training_sample, training_labels)

        second_predicted_labels = second_model.predict(training_sample)

        results["SVC"] = LabelStudy.generate_results(second_predicted_labels, training_labels)

        third_model = MLPClassifier()
        third_model.fit(training_sample, training_labels)

        third_predicted_labels = third_model.predict(training_sample)

        results["MLPClassifier"] = LabelStudy.generate_results(third_predicted_labels, training_labels)
        return results

    @classmethod
    def dates_with_models(cls, project, gate_name, dates: tuple, labels):
        results = {}
        for date in dates:
            results[date] = cls.three_algorithms(project, gate_name, date, labels)
        return results

    @classmethod
    def models_with_dates(cls, project, gate_name, dates: tuple, labels:int):
        results = {}
        for date in dates:
            training_labels, training_sample = LabelStudy.generate_multiple_labels(project, gate_name, date, labels)
            first_model = GaussianNB()
            cls.model_run_through(first_model, "Gaussian", results, training_sample, training_labels)
            second_model = sklearn.svm.SVC()
            cls.model_run_through(second_model, "SVC", results, training_sample, training_labels)
            third_model = MLPClassifier()
            cls.model_run_through(third_model, "MLPClassifier", results, training_sample, training_labels)

    @classmethod
    def model_run_through(cls, model, model_name: str, results, training_sample, training_labels):
        model.fit(training_sample, training_labels)
        predicted_labels = model.predict(training_sample)
        results[model_name] = LabelStudy.generate_results(training_sample)
        return results
