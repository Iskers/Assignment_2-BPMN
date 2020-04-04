import elements as ele


class Checker:
    def __init__(self):
        pass

    @staticmethod
    def check_project(project):
        """
        :param project:
        :return:
        """
        start = 0
        stop = 0
        for node in project.nodes:
            if isinstance(node, ele.Gate):
                if len(project.precedence_constraints[node.name]["From"]) < 1:
                    start += 1
                if len(project.precedence_constraints[node.name]["To"]) < 1:
                    stop += 1
            if start > 1 or stop > 1:
                raise Exception(f"To start or stop gates.")
        return True
