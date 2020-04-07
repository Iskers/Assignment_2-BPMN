from unittest import TestCase

from src.printer import BPMNPrinter
from src.parsers import BPMNParser
import elements


class TestBPMNPrinter(TestCase):
    def setUp(self) -> None:
        self.parser_ = BPMNParser()
        self.printer = BPMNPrinter()
        self.project = self.parser_.parse("ControlSystemProject.xml", "xml", False)

    def test__xml_printer(self):
        self.printer.print("test_print.xml", "xml", False, self.project)

    def test_xml_printer_match(self):
        self.printer.print("test_print.xml", "xml", False, self.project)
        test_project = self.parser_.parse("test_print.xml", "xml", False)
