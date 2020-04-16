import elements
import simulation_tools
import src.test_tools
import sklearn
import checker
import os

from sklearn import linear_model
import page_generator as pg
import src.path_finder as pf

# Create utility classes
page_generator = pg.HTMLPageGenerator()


def default_project_study():
    # Define project origin file.
    file_name = "task_project.tsv"

    format_ = file_name.split(".")
    format_ = format_[-1]

    # Create project class instance
    # The parse function takes in file format and
    basic_project = src.test_tools.project_setup()

    # You can change project attributes here before the check
    # ex:
    # project.inside_diameter = 0.1

    try:
        checker.Checker.check_project(basic_project)

    except Exception as fault:
        print(f"Cant use project, {fault}")

    else:
        # Generate page with default template and store_location
        # Set the height range if your project has more than one vertical pipe.

        # ex:
        # page_generator.default_page_generation(project, height_range=(2, 10, 9), velocity_range=(0.1, 2.0, 0.1))

        # Se README for how to disable warning
        dates = (51, 52, 53)

        page_generator.default_page_generation(basic_project, 1000, "MidProject", dates)

        while True:
            open_file_query = input("Do you want to open the study?[y / n]")

            if not open_file_query or open_file_query == "y":
                os.system(str(pf.PathFinder.get_file_path("study.html", "templates")))
                break
            elif open_file_query == "n":
                break
            else:
                pass


'''
def project_study_with_user_input():
    file_name = input("Input the name of the project file: ")
    default_folder_query = input("Default location for projects is in the data folder.\nIf not, input the location of "
                                 "the project file: ")

    accepted_types = ("tsv", "xml")
    if file_name.endswith(accepted_types):
        format_ = file_name.split(".")
        format_ = format_[-1]
    else:
        format_ = input("Input the format of the file: ")

    try:
        if default_folder_query:
            file_name = default_folder_query + file_name
            project = parser.parse(file_name, format_, True)
        else:
            project = parser.parse(file_name, format_, False)

    except Exception as fault:
        print(f"Couldn't parse file. {fault}")

    else:
        try:
            circ.projectControl.control_project(project)

        except Exception as fault:
            print(f"Cant use project, {fault}")

        else:
            # Generate page with default template and store_location
            template_query = input("Input template file name. Press enter for default: ")
            target_query = input("Input target file name. Press enter for default: ")

            if not template_query and not target_query:
                page_generator.default_page_generation(project, base_velocity=10, height_range=(1, 100, 90),
                                                       efficiency_range=(0.1, 1, 90), velocity_range=(1, 10, 1),
                                                       diameter_range=(0.1, 1, 10))

            elif not template_query:
                page_generator.export_project_study_in_HTML(project, template_query, "study.html")
            elif not target_query:
                page_generator.export_project_study_in_HTML(project, "study-template.html", target_query)
            else:
                page_generator.export_project_study_in_HTML(project, template_query, target_query)

            while True:
                open_file_query = input("Do you want to open the study?[y / n] ")
                if not open_file_query or open_file_query == "y":
                    os.system(str(pf.PathFinder.get_file_path("study.html", "templates")))
                    break
                elif open_file_query == "n":
                    break
                else:
                    pass
'''

if __name__ == '__main__':
    # basic_project = src.test_tools.project_setup()
    default_project_study()

    # default_project_study()
    # results = simulation_tools.AlgorithmStudy.three_dates(basic_project, "MidProject", dates, 1000)

    # project_study_with_user_input()
    pass
