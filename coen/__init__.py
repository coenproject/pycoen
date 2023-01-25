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

        if not os.path.exists(self.get_src_directory_path()):
            os.makedirs(self.get_src_directory_path())

        if not os.path.exists(self.get_main_file_path()):
            with open(self.get_main_file_path(), "w") as _:
                pass

        if not os.path.exists(self.get_intermediates_directory_path()):
            os.makedirs(self.get_intermediates_directory_path())

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
            case "import":
                pass
            case _:
                print(f"Unknown Command: {self.current_command}")

    def build_content(self):
        lines = self.coen_contents.split("\n")
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
        self.coen_contents = self.generate_combined_contents(
            self.get_main_file_path())

        print(self.coen_contents)

        self.build_tex()

        for _ in range(2):
            command = f"cd {self.get_intermediates_directory_path()} && pdflatex main.tex"
            os.system(command)

    def generate_combined_contents(self, path):
        current_content = ""
        with open(path, "r") as main_file:
            lines = main_file.readlines()

            for line in lines:
                self.current_statement = line.strip() + "\n"

                if self.current_statement.startswith("!import "):
                    self.current_command = self.current_statement.split()[
                        0][1:]
                    self.arguments = self.current_statement.split()[1:]
                    import_file_path = os.path.join(
                        os.path.dirname(path), ' '.join(self.arguments))
                    current_content += self.generate_combined_contents(
                        import_file_path)
                else:
                    current_content += self.current_statement
        return current_content

    def compile(self, path):
        with open(path, "r") as main_file:
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

                    # if self.current_statement.startswith("!import"):
                    #     self.current_command = self.current_statement.split()[
                    #         0][1:]
                    #     self.arguments = self.current_statement.split()[1:]
                    #     import_file_path = os.path.join(
                    #         os.path.dirname(path), ' '.join(self.arguments))
                    #     current_content += self.generate_combined_contents(
                    #         import_file_path)
                    # else:
                    #     current_content += self.current_statement

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
