import file_handler as fh
import path_finder as pf
import xml.etree.ElementTree as et

import elements


class Parser:
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

    def parse(self, file_name: str, format_: str, true_path: bool = True, *args):
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

        with fh.File(file_name, "r") as file_source:
            if format_ == "tsv":
                return self._tsv_parser(file_source, args)
            elif format_ == "xml":
                return self._xml_parser(file_source, args)
            elif format_ == "csv":
                self.separator = ","
                return self._tsv_parser(file_source, args)
            else:
                raise Exception("Invalid format")

    def _tsv_parser(self, file_source, *args):
        return 0

    def _xml_parser(self, file_source, *args):
        return 0

    '''
    def _tsv_parser(self, file_source, circuit: cir.Circuit) -> cir.Circuit:
        header = file_source.readline()
        header = fh.File.line_treatment(header, self.separator)

        for line in file_source:
            if "end\n" in line:
                break
            else:
                self._tsv_line_parser(line, circuit)

        circuit.name = header[1]
        return circuit

    def _tsv_line_parser(self, line: str, circuit: cir.Circuit):
        """Takes a line and appends it to a circuit"""
        line = fh.File.line_treatment(line, self.separator)
        circuit.add_part_from_string(line)

    def _xml_parser(self, file_source, circuit: cir.Circuit) -> cir.Circuit:
        xml_document = self._xml_document_loader(file_source)
        root = xml_document.getroot()
        circuit.name = root.attrib["name"]

        for child in root:
            type_ = child.tag
            part = cir.Part.factory_function(type_=type_, **child.attrib)
            circuit.add_part(part)

        return circuit
    '''

    @staticmethod
    def _xml_document_loader(file_source) -> et.ElementTree:
        xml_document = et.parse(file_source)
        return xml_document


# noinspection PyMethodOverriding
class BPMNParser(Parser):
    def __init__(self):
        super().__init__()

    def _tsv_parser(self, file_source, project) -> object:
        header = file_source.readline()
        header = fh.File.line_treatment(header, self.separator)

        if not project:
            project = elements.Project(header[1])

        for line in file_source:
            if "end\n" in line:
                break
            else:
                self._tsv_line_parser(line, project)
        return project

    def _tsv_line_parser(self, line: str, project):
        """Takes a line and appends it to a circuit"""
        line = fh.File.line_treatment(line, self.separator)
        project.add_part_from_string(line)

    def _xml_parser(self, file_source, project) -> object:
        xml_document = self._xml_document_loader(file_source)
        root = xml_document.getroot()
        if not project:
            project = elements.Project(root.attrib["name"])

        for child in root:
            type_ = child.tag
            part = cir.Part.factory_function(type_=type_, **child.attrib)
            project.add_part(part)

        return circuit
