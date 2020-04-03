from unittest import TestCase
import src.parsers as prs


class TestBPMNParser(TestCase):
    def setUp(self) -> None:
        self.parser = prs.BPMNParser()

    def test__tsv_parser(self):
        self.fail()

    def test__tsv_line_parser(self):
        self.fail()

    def test__xml_parser(self):
        self.fail()

    def test__xml_recursive(self):
        self.parser.parse("ControlSystemProject.xml", "xml", False)
