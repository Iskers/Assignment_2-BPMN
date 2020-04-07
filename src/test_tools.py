import src.parsers as prs
import elements


def project_setup():
    parser_ = prs.BPMNParser()
    project = parser_.parse("ControlSystemProject.xml", "xml", False)
    return project
