import os


class Coen:
    def __init__(self, project_directory):
        self.project_name = os.path.basename(project_directory)
        self.project_directory = project_directory

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

    def build(self):
        pass
