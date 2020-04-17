import re
import src.file_handler as fh
import src.path_finder as pf
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
            model_title = self._serialize_message("h3", f"Study using {model} model")
            model_body = ""
            performances = []
            for date in results:
                # Date title
                model_body += self._serialize_message("h4", f"Time limit: {date}")
                tables = ""
                tables += self._first_table(results, date, model)
                tables += self._second_table(results, date, model)
                model_body += self._serialize_message_with_options("div", tables, "id=\"tables\"")
                performances.append(self._model_stats_per_date(model, date, results))

            model_performance = self._model_stats(performances)
            model_stats = self._serialize_message("li", f"Model performs with {round(model_performance * 100, 2)}"
                                                        f"% accuracy")
            model_body = model_title + model_stats + model_body
            model_body = self._serialize_message_with_options("div", model_body, "id=\"model\"")
            body += model_body
        return title + body

    @staticmethod
    def _model_stats_per_date(model, date, results):
        successes = results[date][model][0][2]
        tries = successes + results[date][model][1][2]
        performance = successes / tries
        return performance

    @staticmethod
    def _model_stats(performances: list):
        sum_ = 0
        for i in range(len(performances)):
            sum_ += performances[i]
        return sum_ / len(performances)

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

    @staticmethod
    def _print_project(project):
        return ""

    def _print_core_attributes(self, project, sim_count):
        return self.serializer.serialize_core_attributes(project, sim_count)

    @staticmethod
    def _print_img(project):
        return ""

    def _print_model_study(self, project, gate_name, dates, sim_count):
        return self.serializer.serialize_model_study(project, gate_name, dates, sim_count)
