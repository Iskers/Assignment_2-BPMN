from unittest import TestCase
import src.test_tools
import simulation_tools


class TestDurationGenerators(TestCase):
    def setUp(self) -> None:
        self.project = src.test_tools.project_setup()

    def test_project_duration_generator(self):
        project_duration = simulation_tools.DurationGenerators.project_duration_generator(self.project)
        pass

    def test_lane_duration_generator(self):
        self.fail()

    def test_task_duration_generator(self):
        self.fail()
