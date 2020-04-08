import random
import numpy
import sklearn


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

    def generate_start_date(self, node):
        pass

    def generate_completion_date(self, node):
        pass

class MonteCarloSimulation:
    def __init__(self):
        pass


    def linear_study(self, ):