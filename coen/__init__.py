import os
import json


class Coen:
    def __init__(self, project_directory):
        self.project_name = os.path.basename(project_directory)
        self.project_directory = project_directory

        self.content = ""

        if not os.path.exists(self.project_directory):
            os.makedirs(self.project_directory)

        if not os.path.exists(self.get_coen_file_path()):
            with open(self.get_coen_file_path(), "w") as f:
                f.writelines(
                    [
                        "{\n",
                        f"  \"name\": \"{self.project_name}\",\n",
                        f"  \"author\": \"\"\n",
                        "}\n",
                    ]
                )

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
            case _:
                print(f"Unknown Command: {self.current_command}")

    def build_content(self):
        with open(self.get_main_file_path(), "r") as main_file:
            lines = main_file.readlines()
            for line in lines:
                self.current_statement = line

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

        os.system(
            f"cd {self.get_intermediates_directory_path()} && pdflatex main.tex")

    def build_tex(self):
        self.build_content()
        info = json.load(open(self.get_coen_file_path()))

        with open(self.get_tex_file_path(), "w") as tex_file:
            title = info.get('name', '').replace('_', '\\_')
            author = info.get('author', '').replace('_', '\\_')

            tex_file.writelines(
                [
                    f"\\documentclass{{article}}\n",
                    "\n",
                    f"\\title{{{title}}}\n",
                    f"\\author{{{author}}}\n",
                    f"\\date{{{info.get('date', '')}}}\n",
                    "\n",
                    f"\\begin{{document}}\n",
                    f"\\maketitle\n",
                    f"\n",
                    self.content,
                    f"\n",
                    f"\\end{{document}}\n",
                ]
            )
