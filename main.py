import os

import src.test_tools
import src.parsers
import src.path_finder as pf

import elements
import simulation_tools
import checker
import page_generator


# Create utility classes
parser = src.parsers.BPMNParser()
page_generator = page_generator.HTMLPageGenerator()


def default_project_study():
    # Define project origin file.
    file_name = "ControlSystemProject.xml"

    format_ = file_name.split(".")
    format_ = format_[-1]

    # Create project class instance
    # The parse function takes in file format and
    project = parser.parse(file_name, format_, False)

    try:
        checker.Checker.check_project(project)

    except Exception as fault:
        print(f"Cant use project, {fault}")

    else:
        # Generate page with default template and store_location
        # The time limit dates are set here, they can be changed by editing dates

        # ex:
        # page_generator.default_page_generation(project, height_range=(2, 10, 9), velocity_range=(0.1, 2.0, 0.1))
        dates = (51, 52, 53)

        # default_page_generation(project, sim_count, gate_name, dates)
        page_generator.default_page_generation(project, 1000, "MidProject", dates)

        while True:
            open_file_query = input("Do you want to open the study?[y / n]")

            if not open_file_query or open_file_query == "y":
                os.system(str(pf.PathFinder.get_file_path("study.html", "templates")))
                break
            elif open_file_query == "n":
                break
            else:
                pass


if __name__ == '__main__':
    default_project_study()

