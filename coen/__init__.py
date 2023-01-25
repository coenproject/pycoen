import os
import json


class Coen:
    def __init__(self, project_directory):
        self.project_name = os.path.basename(project_directory)
        self.project_directory = project_directory

        self.content = ""
        self.variables = dict()

        if not os.path.exists(self.project_directory):
            os.makedirs(self.project_directory)

        if not os.path.exists(self.get_coen_file_path()):
            default_info_file = open("./coen/resources/info", "r")
            default_info_contents = default_info_file.read()

            default_info_contents = default_info_contents.replace(
                "$TITLE", self.project_name)

            with open(self.get_coen_file_path(), "w") as f:
                f.write(default_info_contents)

        if not os.path.exists(self.get_src_directory_path()):
            os.makedirs(self.get_src_directory_path())

        if not os.path.exists(self.get_main_file_path()):
            with open(self.get_main_file_path(), "w") as _:
                pass

        if not os.path.exists(self.get_intermediates_directory_path()):
            os.makedirs(self.get_intermediates_directory_path())

    def get_coen_file_path(self):
        coen_file_path = os.path.join(self.project_directory, "coen.json")
        return coen_file_path

    def get_intermediates_directory_path(self):
        intermediates_directory_path = os.path.join(
            self.project_directory, "intermediates")
        return intermediates_directory_path

    def get_src_directory_path(self):
        src_directory_path = os.path.join(
            self.project_directory, "src")
        return src_directory_path

    def get_main_file_path(self):
        main_file_path = os.path.join(
            self.project_directory, "src", "main.coen")
        return main_file_path

    def get_tex_file_path(self):
        tex_file_path = os.path.join(
            self.project_directory, "intermediates", "main.tex")
        return tex_file_path

    def execute_command(self):
        match self.current_command.lower():
            case "section":
                self.content += f"\\section{{{' '.join(self.arguments)}}}\n"
            case "subsection":
                self.content += f"\\subsection{{{' '.join(self.arguments)}}}\n"
            case "set":
                self.variables[self.arguments[0]] = ' '.join(
                    self.arguments[1:])
            case _:
                print(f"Unknown Command: {self.current_command}")

    def build_content(self):
        self.set_info_variables()

        with open(self.get_main_file_path(), "r") as main_file:
            lines = main_file.readlines()
            for line in lines:
                self.current_statement = line.strip() + "\n"

                match self.current_statement[0]:
                    case "!":
                        self.current_command = self.current_statement.split()[
                            0][1:]
                        self.arguments = self.current_statement.split()[1:]
                        self.execute_command()
                    case _:
                        self.content += self.current_statement

    def build(self):
        self.build_tex()

        for _ in range(2):
            command = f"cd {self.get_intermediates_directory_path()} && pdflatex main.tex"
            os.system(command)

    def build_tex(self):
        self.build_content()

        template_file = open(self.variables.get("TEMPLATE"), "r")
        tex_content = template_file.read()

        tex_content = tex_content.replace("$CONTENT", self.content)

        print(self.variables)

        for key, value in self.variables.items():
            tex_content = tex_content.replace("$" + key, value)

        with open(self.get_tex_file_path(), "w") as tex_file:
            tex_file.write(tex_content)

    def set_info_variables(self):
        info = json.load(open(self.get_coen_file_path()))
        for key, value in info.items():
            self.variables[key.upper()] = value
