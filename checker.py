import elements as ele


class Checker:
    def __init__(self):
        pass

    @classmethod
    def check_project(cls, project):
        """
        :param project:
        :return:
        """
        start = 0
        stop = 0
        for node in project.project_nodes:
            node = project.project_nodes[node]
            if isinstance(node, ele.Gate):
                con = project.precedence_constraints[node]
                if len(project.precedence_constraints[node]["From"]) < 1:
                    start += 1
                if len(project.precedence_constraints[node]["To"]) < 1:
                    stop += 1
            elif isinstance(node, ele.Lane):
                start, stop = cls._check_lane(node, start, stop)

            if start > 1 or stop > 1:
                raise Exception(f"Too many start or stop gates.")
        return True

    @staticmethod
    def _check_lane(lane, start, stop):
        for node in lane.project_nodes:
            if isinstance(node, ele.Gate):
                if len(lane.precedence_constraints[node.name]["From"]) < 1:
                    start += 1
                if len(lane.precedence_constraints[node.name]["To"]) < 1:
                    stop += 1
        return start, stop
