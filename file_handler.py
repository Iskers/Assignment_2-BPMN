import sys


class File:
    """
    General file handler used as a context manager, i.e. using "with" statement.

    :param str file_name: Path and file name string.
    :param str mode: Mode to open file. Use characters read "r", write "w", append "a", or read-write "r+".
    """
    def __init__(self, file_name, mode):
        self.file_name = file_name
        self.mode = mode

    def __enter__(self):
        """
        To be used with the "with" statement, example:
            with File(file_name, mode) as some_var
                ... do something with file content. ...

        When finished un-indent and __exit__ is called.

        :raises OSError: If file can not be opened.
        :return: TextIO, which is a stream of text.
        """
        try:
            self.open_file = open(self.file_name, self.mode)
            return self.open_file
        except OSError:  # pragma: no cover
            sys.stderr.write(f"Could not open file: {self.file_name}" + '\n')
            sys.exit()

    def __exit__(self, *args):
        self.open_file.close()

    @staticmethod
    def line_treatment(line: str, separator: str) -> list:
        """Strips line and splits into list object."""
        line = line.rstrip()
        list_ = line.split(separator)
        return list_
