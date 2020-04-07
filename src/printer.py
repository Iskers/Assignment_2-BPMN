import xml.etree.ElementTree as et
from xml.dom import minidom

from src import file_handler as fh, path_finder as pf
import elements


class Printer:
    """
    This is a class for parsing text in the tsv, csv, and xml formats using a file handler.

    :param separator: Separator for the parsing text, default is tabulation.
    :type separator: str
    """

    def __init__(self, separator='\t'):
        self._separator = separator
        pass

    @property
    def separator(self):
        """Get or set the current separator"""
        return self._separator

    @separator.setter
    def separator(self, separator):
        self._separator = separator

    def print(self, file_name: str, format_: str, true_path: bool = True, *args):
        """
        Takes inn a file and appends it to a given circuit. If the file is in the data folder the filename can be given
        only with the name of the file. This function can parse tsv and xml formats.

        :param str file_name: Source file
        :param str format_: Format of file. Accepts "tsv" and "xml".
        :param bool true_path: Boolean value to indicate if object is in data folder.
        :raises Exception: Invalid format.
        """
        if not true_path:
            file_name = pf.PathFinder.get_file_path(file_name=file_name, folder_name="data")

        with fh.File(file_name, "w") as file_target:
            if format_ == "tsv":
                return self._tsv_printer(file_target, *args)
            elif format_ == "xml":
                return self._xml_printer(file_target, *args)
            elif format_ == "csv":
                self.separator = ","
                return self._tsv_printer(file_target, *args)
            else:
                raise Exception("Invalid format")

    def _tsv_printer(self, file_target, *args):
        return 0

    def _xml_printer(self, file_target, *args):
        return 0

    @staticmethod
    def _xml_document_loader(file_target) -> et.ElementTree:
        xml_document = et.parse(file_target)
        return xml_document


# noinspection PyMethodOverriding
class BPMNPrinter(Printer):
    def __init__(self):
        super().__init__()

    def _xml_printer(self, file_target, project):
        tree = self._project_brancher(project)
        string = et.tostring(tree)
        reparsed = minidom.parseString(string)
        file_target.write(reparsed.toprettyxml(indent="  "))

    def _project_brancher(self, project) -> et.ElementTree:
        root = et.Element("project", name=project.name)
        for element in project.container:
            self._element_brancher_recursive(root, element)
        self._precedence_brancher(root, project)
        return root

    def _element_brancher_recursive(self, root, element: et.Element):
        if isinstance(element, elements.Gate):
            self._gate_brancher(root, element)
        elif isinstance(element, elements.Task):
            self._task_brancher(root, element)
        elif isinstance(element, elements.Lane):
            self._lane_brancher(root, element)

    def _lane_brancher(self, root, lane):
        lane_root = et.SubElement(root, "lane", name=lane.name)

        for node in lane.container:
            self._element_brancher_recursive(lane_root, node)

        self._precedence_brancher(lane_root, lane)

    @staticmethod
    def _gate_brancher(root, gate):
        return et.SubElement(root, "gate", name=gate.name)

    @staticmethod
    def _task_brancher(root, task):
        return et.SubElement(root, "task", {"name": task.name, "minimum-duration": task.minimum_duration,
                                            "maximum-duration": task.maximum_duration})

    @staticmethod
    def _precedence_brancher(root, container: elements.Container):
        for node in container.precedence_constraints:
            for to in container.precedence_constraints[node]["To"]:
                et.SubElement(root, "precedence-constraint", {"source": node, "target": to})

    def _tsv_line_printer(self, line: str, project):
        """Takes a line and appends it to a circuit"""
        line = fh.File.line_treatment(line, self.separator)
        project.add_part_from_string(line)

    def _xml_recursive(self, context: elements.Container, root):
        type_ = root.tag
        if type_ == "precedence-constraint":
            context.add_constraint(source=root.attrib["source"], target=root.attrib["target"])
            return
        if type_ == "lane":
            context.add_lane(*root.attrib)
            # a = list(root)
            for child in root:
                self._xml_recursive(context, child)
        elif type_ == "gate":
            context.add_node(type_="Gate", **root.attrib)
            return
        elif type_ == "task":
            context.add_node(type_="Task", **root.attrib)
            return
        else:
            raise Exception("Invalid type")
