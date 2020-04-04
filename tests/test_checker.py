from unittest import TestCase
import src.parsers as prs
import elements as ele
import checker as chk


class TestChecker(TestCase):
    def setUp(self) -> None:
        self.parser = prs.BPMNParser()
        self.checker = chk.Checker()

    def test_check_project(self):
        project = self.parser.parse("ControlSystemProject.xml", "xml", False)
        self.assertTrue(self.checker.check_project(project))

    def test_check_project_invalid(self):
        with self.assertRaises(Exception):
            project = self.parser.parse("InvalidControlSystemProject.xml", "xml", False)
            self.checker.check_project(project)
