import random


class Generators:
    pass


class DurationGenerators(Generators):

    def __init__(self):
        super().__init__()
        pass

    @classmethod
    def project_duration_generator(cls, project):
        project_duration = 0
        for lane in project:
            project_duration += cls.lane_duration_generator(lane)
        return project_duration

    @staticmethod
    def lane_duration_generator(lane):
        lane_duration = 0
        for task in lane:
            task.generate_duration(lane.workload)
            lane_duration += task.duration
        return lane_duration

    @staticmethod
    def task_duration_generator(min_, max_, mode):
        return random.triangular(min_, max_, mode)

    @staticmethod
    def lane_workload_generator(lane):
        return random.random()


class MonteCarloSimulation:
    pass

    def __init__(self):
        pass
