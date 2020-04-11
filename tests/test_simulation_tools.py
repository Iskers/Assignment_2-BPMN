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


class TestDateGenerator(TestCase):
    def setUp(self) -> None:
        self.project = src.test_tools.project_setup()

    def test_generate_dates(self):
        simulation_tools.DateGenerator.generate_project_completion_date(self.project)


class TestMonteCarloSimulation(TestCase):
    def setUp(self) -> None:
        self.project = src.test_tools.project_setup()

    def test_monte_carlo_basic(self):
        se = simulation_tools.MonteCarloSimulation.Monte_Carlo_Basic(self.project, 10000)
        pass


class TestLabelStudy(TestCase):
    def setUp(self) -> None:
        self.project = src.test_tools.project_setup()

    def test_generate_basic_label(self):
        se, oe = simulation_tools.LabelStudy.generate_basic_label(self.project, "MidProject", 50)
        pass

    def test_generate_multiple_labels(self):
        results, dates = simulation_tools.LabelStudy.generate_multiple_labels(self.project, "MidProject", 51, 100)
        pass