# Developer && Owner: МогучийДД (MoguchiyDD)
# LICENSE: MIT License which is located in the text file LICENSE
#
# Goal: Writing and Reading IMPORTANT FILES
# Result: AUTOMATED SYSTEM with FILES
#
# Past Modification: Editing The «FileSystem» CLASS (__check_existence_folder)
# Last Modification: Editing The «FileSystem» CLASS (write_file_settings)
# Modification Date: 2023.11.04, 01:07 AM
#
# Create Date: 2023.11.01, 10:01 PM


from json import dumps, loads
from os import path, chdir, mkdir


# ------------ FILE SYSTEM ------------

class FyleSystem:
    """
    Storage of SYSTEM FILES

    ---
    PARAMETERS:
    - path_main_file: str -> The «basedir» VARIABLE from The «app/main.py» FILE
    ---
    FUNCTIONS:
    - write_file_settings(self, data: dict[str, any]) -> None :
    Writes The SETTINGS FILE
    - read_file_settings(self) -> dict[str, any] : Reads The SETTINGS FILE
    """

    FOLDER = ".settings"
    FILE_SETTINGS = ".settings.json"
    TEMPLATE = {
        "dash": True,
        "block": ". ? !"
    }

    def __init__(self, path_main_file: str) -> None:
        self.basedir = path_main_file

        self.path_file_system = path.dirname(__file__)
        self.path_folder_settings = path.join(path_main_file, self.FOLDER)
        self.path_file_settings = path.join(
            self.path_folder_settings, self.FILE_SETTINGS
        )

        self.__check_existence_folder()

    def __check_existence_folder(self) -> None:
        """
        Creates 1 FOLDER for The SETTINGS FILE if The FOLDER does not Exist and
        Writes The Finished TEMPLATE inside The FILE
        """

        if path.exists(self.path_folder_settings) is False:
            chdir(self.basedir)
            mkdir(self.FOLDER)
            chdir("..")
            self.write_file_settings(self.TEMPLATE)

    def write_file_settings(self, data: dict[str, any]) -> None:
        """
        Writes The SETTINGS FILE

        ---
        PARAMETERS:
        - data: dict[str, any] -> The DATA for SETTINGS FILE
        """

        with open(self.path_file_settings, "w+") as f:
            f.write(dumps(data))

    def read_file_settings(self) -> dict[str, any]:
        """
        Reads The SETTINGS FILE

        ---
        RESULT: The DATA from SETTINGS FILE
        """

        with open(self.path_file_settings, "r") as f:
            data = f.read()

        return loads(data)

# -------------------------------------
