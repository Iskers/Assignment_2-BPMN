import re
import src.file_handler as fh
import src.path_finder as pf

# import module.study_ as stdy
import simulation_tools


class HTMLSerializer:
    def __init__(self):
        pass

    def serialize_project(self, project):
        title = f"<h2>{project}</h2>"
        body = ""
        for part in project:
            body = self._serialize_message("li", str(part))
        body = self._serialize_message("ul", body)
        return title + body

    def serialize_project_with_attributes(self, project):
        return ""

    '''
    def serialize_project_with_attributes(self, project):
        title = f"<h2>{self._sting_treatment(str(project))}</h2>"
        body = self._serialize_message("th", "Types: ")
        for part in project:
            if type(part).__name__ == "PipeStraight":
                body += self._serialize_message("th", "Pipe")
            elif type(part).__name__ == "PipeBend":
                body += self._serialize_message("th", "Bend")
            else:
                body += self._serialize_message("th", f"{type(part).__name__}")
        body = self._serialize_message("tr", body)

        # Zeta should not be on the project representation
        properties = {"ZETA"}

        for part in project:
            for evaluation_property, unused_value in vars(part).items():
                if evaluation_property not in properties:
                    property_print = self._sting_treatment(evaluation_property[1:])
                    inner_body = self._serialize_message_with_options("td", property_print, "id=\"property\"")
                    for inner_part in project:
                        if evaluation_property not in vars(inner_part):
                            inner_body += self._serialize_message_with_options("td", "", "id=\"empty_item_property\"")
                        else:
                            for item_property, value in vars(inner_part).items():
                                if item_property == evaluation_property:
                                    inner_body += self._serialize_message_with_options("td", value,
                                                                                       "id=\"item_property\"")
                    properties.add(evaluation_property)
                    body += self._serialize_message("tr", inner_body)

        body = self._serialize_message_with_options("table", body, "id=\"project\"")
        return title + body
    '''

    def serialize_core_attributes(self, project, sim_count: int):
        sim_count = sim_count * 10
        file_name, attributes = simulation_tools.MonteCarloSimulation.Monte_Carlo_Basic(project, sim_count,
                                                                                        "Histogram image.png")
        title = self._serialize_message("h2", f"Core attributes of project using basic Monte Carlo simulation "
                                              f"{sim_count} times")
        body = ""
        for key in attributes:
            if key == "durations":
                pass
            else:
                attribute = attributes[key]
                attribute = round(attribute, 2)
                body += self._serialize_message("li", f"{key} = {attribute}")

        image = self._serialize_image(file_name)

        return title + self._serialize_message("ul", body) + image

    def serialize_model_study(self, project, gate_name, dates, sim_count):
        global some_key
        results = simulation_tools.AlgorithmStudy.dates_with_models(project, gate_name, dates, sim_count)
        title = self._serialize_message("h2", f"Study of different regression models")
        body = ""
        for key in results:
            some_key = key

        for model in results[some_key]:
            model_body = self._serialize_message("h3", f"Study using {model}")
            for date in results:
                # Date title
                model_body += self._serialize_message("h4", f"Time limit: {date}")
                tables = ""
                tables += self._first_table(results, date, model)
                tables += self._second_table(results, date, model)
                model_body += self._serialize_message_with_options("div", tables, "id=\"tables\"")
                pass
            model_body = self._serialize_message_with_options("div", model_body,  "id=\"model\"")
            body += model_body
        return title + body

    def _first_table(self, results, date, model):
        # Create table header
        table = self._serialize_message_with_options("th", f"", "id=\"white\"")
        table += self._serialize_message("th", "Within time limit")
        table += self._serialize_message("th", "Not within time limit")
        table = self._serialize_message("tr", table)

        inner_table = self._serialize_message_with_options("td", f"solution", "id=\"property\"")
        inner_table += self._serialize_message("td", f"{str(results[date][model][2][1])}")
        inner_table += self._serialize_message("td", f"{str(results[date][model][2][0])}")
        inner_table = self._serialize_message("tr", inner_table)

        inner_table += self._serialize_message_with_options("td", f"prediction", "id=\"property\"")
        inner_table += self._serialize_message("td", f"{str(results[date][model][3][1])}")
        inner_table += self._serialize_message("td", f"{str(results[date][model][3][0])}")
        table += self._serialize_message("tr", inner_table)

        table = self._serialize_message_with_options("table", table, "id=\"table_type\"")
        return table

    def _second_table(self, results, date, model):
        # Create table header
        table = self._serialize_message_with_options("th", f"", "id=\"white\"")
        table += self._serialize_message("th", "Solution within time limit")
        table += self._serialize_message("th", "Solution not within time limit")
        table += self._serialize_message("th", "Both either within or not within time limit")
        table = self._serialize_message("tr", table)

        inner_table = self._serialize_message_with_options("td", f"successes", "id=\"property\"")
        inner_table += self._serialize_message("td", f"{str(results[date][model][0][1])}")
        inner_table += self._serialize_message("td", f"{str(results[date][model][0][0])}")
        inner_table += self._serialize_message("td", f"{str(results[date][model][0][2])}")
        inner_table = self._serialize_message("tr", inner_table)

        inner_table += self._serialize_message_with_options("td", f"failures", "id=\"property\"")
        inner_table += self._serialize_message("td", f"{str(results[date][model][1][1])}")
        inner_table += self._serialize_message("td", f"{str(results[date][model][1][0])}")
        inner_table += self._serialize_message("td", f"{str(results[date][model][1][2])}")
        table += self._serialize_message("tr", inner_table)

        table = self._serialize_message("table", table)
        return table

    '''
    def serialize_img_study(self, project, study, v_range, d_range, e_range, h_range):
        file_names = study.png_generator_plot(project, v_range, d_range, e_range, h_range)
        title = self._serialize_message("h2", "Plots of differing attributes and their effect on energy consumption")
        body = ""
        for file in file_names:
            body += self._serialize_image(file)
        body = self._serialize_message_with_options("div", body, "id=\"image_study\"")
        return title + body
    '''

    '''
    def serialize_all_boolean_studies(self, project, study_):
        title = self._serialize_message("h2", "Boolean study")
        valve_study, filter_study, velocities = study_.boolean_study(project)

        serialized_valve_string = self._serialize_boolean_study(valve_study, velocities, "Valve", "open")

        serialized_filter_string = self._serialize_boolean_study(filter_study, velocities, "Filter", "clean")

        # tables = self._serialize_message("table", serialized_valve_string + serialized_filter_string)
        tables = serialized_valve_string + serialized_filter_string
        return title + tables
    '''

    '''
    def serialize_core_attributes(self, project, velocity):
        study = stdy.Study(velocity)
        core_attributes = study.project_performance(project)

        title = self._serialize_message("h3", f"Core attributes of project with velocity of {velocity} [m/s]")
        warning = ""
        if core_attributes[0] > 10 ** 5:
            warning = "(Reynolds number exceeding 10^5. Flow calculation may not be precise)"
        body = self._serialize_message("li", f"Reynolds number = {round(core_attributes[0])} {warning}")
        flow_type = "Turbulent"
        if core_attributes[0] < 2300:
            flow_type = "Laminar"
        body += self._serialize_message("li", f"{flow_type} flow = {round(core_attributes[1], 4)} [m3/s]")
        body += self._serialize_message("li", f"Pressure losses due to height of project = {round(core_attributes[2])}"
                                              f" [N/m2]")
        body += self._serialize_message("li", f"Pressure losses due to friction in parts = "
                                              f"{round(core_attributes[3])} [N/m2]")
        body += self._serialize_message("li", f"Theoretical energy usage of project = {round(core_attributes[4], 2)}"
                                              f" [kW]")
        body += self._serialize_message("li", f"Actual energy usage of project = {round(core_attributes[5], 2)} [kW]")
        return title + self._serialize_message("ul", body)
    
    '''

    '''
    def _serialize_boolean_study(self, boolean_study, velocities, type_word, keyword: str):
        title = self._serialize_message("h3", f"Study of {type_word.lower()} setting at"
                                              f" different velocities")
        # Create table header
        serialized_valve_string = self._serialize_message("th", f"{type_word}s {keyword}: ")
        for key in boolean_study[0]:
            serialized_valve_string += self._serialize_message("th", num2words.num2words(sum(key)))

        serialized_valve_string = self._serialize_message("tr", serialized_valve_string)
        for i in range(len(velocities)):
            serialized_velocity_string = self._serialize_message("td", f"Velocity = {velocities[i]} [m/s]")
            for key in boolean_study[i]:
                serialized_velocity_string += self._serialize_message("td", f"{boolean_study[i][key]} [kW]")
            serialized_valve_string += self._serialize_message("tr", serialized_velocity_string)

        serialized_valve_string = self._serialize_message("table", serialized_valve_string)
        return title + serialized_valve_string
    '''

    @staticmethod
    def _serialize_message(tag: str, msg) -> str:
        body = HTMLSerializer._serialize_open_tag(tag)
        body += str(msg)
        body += HTMLSerializer._serialize_close_tag(tag)
        return body

    @staticmethod
    def _serialize_message_with_options(tag: str, msg, option):
        body = HTMLSerializer._serialize_open_tag_with_options(tag, option)
        body += str(msg)
        body += HTMLSerializer._serialize_close_tag(tag)
        return body

    @staticmethod
    def _serialize_open_tag(name):
        return f"<{name}>"

    @staticmethod
    def _serialize_open_tag_with_options(name, option):
        return f"<{name} {option}>"

    @staticmethod
    def _serialize_close_tag(name):
        return f"</{name}>"

    @staticmethod
    def _serialize_image(img_path):
        img_path = img_path.replace(" ", "%20")
        return f"<img src={img_path}>"

    @staticmethod
    def _serialize_image_with_options(img_path, option):
        img_path = img_path.replace(" ", "%20")
        return f"<img src={img_path} {option}>"

    @staticmethod
    def _sting_treatment(string):
        string = string.replace("_", " ")
        string = string.title()
        return string


class HTMLPageGenerator:
    def __init__(self):
        self.serializer = HTMLSerializer()
        self.path = pf.PathFinder.get_folder_path("templates")

    def default_page_generation(self, project, sim_count, gate_name, dates):
        self.export_project_study_in_HTML(project, "study-template.html", "study.html", sim_count, gate_name, dates)

    def export_project_study_in_HTML(self, project, template_file, target_file, sim_count, gate_name, dates):
        template_file = str(self.path) + "/" + template_file
        target_file = str(self.path) + "/" + target_file
        with fh.File(template_file, "r") as template:
            with fh.File(target_file, "w") as target:
                self._print_report(project, template, target, sim_count, gate_name, dates)

    def _print_report(self, project, template_stream, target_stream, sim_count, gate_name, dates):
        for line in template_stream:
            line = self._HTML_replacement(project, line, sim_count, gate_name, dates)
            target_stream.write(line + '\n')

    def _HTML_replacement(self, project, line: str, sim_count, gate_name, dates):
        line = line.rstrip()
        # Methods to be called to replace placeholder in template with some value.
        # Lambda takes in two arguments and gives back string.
        methods = {r'__BPMN__': lambda line_, project_: re.sub(r'__BPMN__', self._print_project(project_),
                                                               line_),
                   r'__core_attr__': lambda line_, project_: re.sub(r'__core_attr__',
                                                                    self._print_core_attributes(project_, sim_count),
                                                                    line_),
                   r'__model_study__': lambda line_, project_: re.sub(r'__model_study__',
                                                                      self._print_model_study(project_, gate_name,
                                                                                              dates, sim_count), line_),
                   r'__images__': lambda line_, project_: re.sub(r'__images__',
                                                                 self._print_img(project_), line_)
                   }
        for key in methods:
            if re.search(key, line):
                return methods[key](line, project)
        return line

    def _print_project(self, project):
        return ""
        # return self.serializer.serialize_project_with_attributes(project)

    def _print_core_attributes(self, project, sim_count):
        return self.serializer.serialize_core_attributes(project, sim_count)

    def _print_img(self, project):
        return ""
        # return self.serializer.serialize_img_study(project, self.study, v_range,
        #                                           d_range, e_range, h_range)

    def _print_model_study(self, project, gate_name, dates, sim_count):
        return self.serializer.serialize_model_study(project, gate_name, dates, sim_count)
        # return self.serializer.serialize_all_boolean_studies(project)
