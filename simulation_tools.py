import random


class Generators:
    pass


class DurationGenerators(Generators):

    def __init__(self):
        super().__init__()
        pass

    def project_duration_generator(self, project):
        project_duration = 0
        for lane in project:
            project_duration += self.lane_duration_generator(lane)
        return project_duration

    def lane_duration_generator(self, lane):
        lane_duration = 0
        for task in lane:
            lane_duration += self.task_duration_generator(task)
        return lane_duration

    @staticmethod
    def task_duration_generator(min_, max_, mode):
        return random.triangular(min_, max_, mode)
