# Developer && Owner: МогучийДД (MoguchiyDD)
# LICENSE: MIT License which is located in the text file LICENSE
#
# Goal: Writing and Reading IMPORTANT FILES
# Result: AUTOMATED SYSTEM with FILES
#
# Past Modification: Editing The «FileSystem» CLASS («_valid_true_values»)
# Last Modification: Checking CODE The PEP8
# Modification Date: 2023.11.17, 11:47 PM
#
# Create Date: 2023.11.01, 10:01 PM


from json import dumps, loads
from os import path, chdir, mkdir
from os.path import isfile


# ------------ FILE SYSTEM ------------

class FileSystem:
    """
    Storage of SYSTEM FILES

    ---
    PARAMETERS:
    - path_main_file: str -> The «basedir» VARIABLE from The «app/main.py» FILE
    - overwrite_file: bool = False -> Overwrite The SETTINGS FILE if there is
    a PROBLEM with The KEYS
    ---
    FUNCTIONS:
    - _valid_true_keys(data: list[str]) -> bool : Checks The TITLE of The KEYS
    for Correct Spelling
    - _valid_true_values(data: dict[str, any]) -> bool : Checks The TITLE of
    The VALUES for Correct Spelling
    - _check_existence_folder(self) -> None : Creates 1 FOLDER for The SETTINGS
    FILE if The FOLDER does not Exist and Writes The Finished TEMPLATE inside
    The FILE
    - _failed_isfile() -> bool : Checks The «self.failed_isfile» VARIABLE to
    Trigger The Check when The FILE in The FOLDER did not Exist
    - write_file_settings(self, data: dict[str, any]=TEMPLATE) -> None :
    Writes The SETTINGS FILE
    - read_file_settings(self) -> dict[str, any] : Reads The SETTINGS FILE
    """

    # MAIN
    FOLDER = ".settings"
    FILE_SETTINGS = ".settings.json"

    # KEYS
    TEMPLATE_TITLE_KEY = "title"
    TEMPLATE_LIST_KEY = "list"
    TEMPLATE_DASH_KEY = "dash"
    TEMPLATE_BLOCK_KEY = "block"
    TEMPLATE_LANGUAGE_KEY = "language"

    # VALUES
    TEMPLATE_TITLE_VALUE = False
    TEMPLATE_LIST_VALUE = False
    TEMPLATE_DASH_VALUE = True
    TEMPLATE_BLOCK_VALUE = [".", "?", "!"]
    TEMPLATE_LANGUAGE_VALUE = "RU"

    # TEMPLATE
    TEMPLATE = {
        TEMPLATE_TITLE_KEY: TEMPLATE_TITLE_VALUE,
        TEMPLATE_LIST_KEY: TEMPLATE_LIST_VALUE,
        TEMPLATE_DASH_KEY: TEMPLATE_DASH_VALUE,
        TEMPLATE_BLOCK_KEY: TEMPLATE_BLOCK_VALUE,
        TEMPLATE_LANGUAGE_KEY: TEMPLATE_LANGUAGE_VALUE
    }
    TEMPLATE_KEYS = TEMPLATE.keys()

    def __init__(
        self, path_main_file: str,
        overwrite_file: bool = False
    ) -> None:
        self.basedir = path_main_file
        self.is_create_folder = False
        self.failed_isfile = False

        self.path_file_system = path.dirname(__file__)
        self.path_folder_settings = path.join(path_main_file, self.FOLDER)
        self.path_file_settings = path.join(
            self.path_folder_settings, self.FILE_SETTINGS
        )

        self._check_existence_folder()
        if self.is_create_folder is True:
            self.write_file_settings()
            self.is_create_folder = False

        if (overwrite_file) or (not isfile(self.path_file_settings)):
            self.write_file_settings()
            if overwrite_file is False:
                self.failed_isfile = True

    def _valid_true_keys(self, data: list[str]) -> bool:
        """
        Checks The TITLE of The KEYS for Correct Spelling

        ---
        PARAMETERS:
        - data: list[str] -> The DATA with CURRENT KEYS from RAM
        ---
        RESULT: True (RIGHT KEYS) || False (NOT RIGHT KEYS)
        """

        result = True

        for key in self.TEMPLATE_KEYS:
            try:
                data.index(key)
            except:
                result = False
                return result

        return result

    def _valid_true_values(self, data: dict[str, any]) -> bool:
        """
        Checks The TITLE of The VALUES for Correct Spelling

        ---
        PARAMETERS:
        - data: dict[str, any] -> The DATA with CURRENT DICTIONARY from RAM
        ---
        RESULT: True (RIGHT VALUES) || False (NOT RIGHT VALUES)
        """

        def __bool(value: bool, _cnt_result: int) -> int:
            """
            Checking a BOOLEAN VALUE

            ---
            PARAMETERS:
            - value: bool -> The VALUE from The KEY
            - _cnt_result: int -> Number of ERRORS to be LOGGED if ERRORS Exist
            ---
            RESULT: Number of ERRORS when Checking a VALUE by KEY
            """

            if isinstance(value, bool) is False:
                _cnt_result += 1

            return _cnt_result

        def __block(value: bool, _cnt_result: int) -> int:
            """
            Checking The VALUE of The «block» KEY

            ---
            PARAMETERS:
            - value: bool -> The VALUE from The KEY
            - _cnt_result: int -> Number of ERRORS to be LOGGED if ERRORS Exist
            ---
            RESULT: Number of ERRORS when Checking a VALUE by KEY
            """

            if isinstance(value, list) is False:
                _cnt_result += 1
            else:
                for val in value:
                    if isinstance(val, str) is False:
                        _cnt_result += 1

            return _cnt_result

        def __language(value: bool, _cnt_result: int) -> int:
            """
            Checking The VALUE of The «language» KEY

            ---
            PARAMETERS:
            - value: bool -> The VALUE from The KEY
            - _cnt_result: int -> Number of ERRORS to be LOGGED if ERRORS Exist
            ---
            RESULT: Number of ERRORS when Checking a VALUE by KEY
            """

            if value not in ["RU", "EN"]:
                _cnt_result += 1

            return _cnt_result

        result = True
        _cnt_result = 0

        for key, value in data.items():
            if key == self.TEMPLATE_TITLE_KEY:  # title
                _cnt_result = __bool(value, _cnt_result)
            elif key == self.TEMPLATE_LIST_KEY:  # list
                _cnt_result = __bool(value, _cnt_result)
            elif key == self.TEMPLATE_DASH_KEY:  # dash
                _cnt_result = __bool(value, _cnt_result)
            elif key == self.TEMPLATE_BLOCK_KEY:  # block
                _cnt_result = __block(value, _cnt_result)
            elif key == self.TEMPLATE_LANGUAGE_KEY:  # language
                _cnt_result = __language(value, _cnt_result)

        if _cnt_result >= 1:
            result = False

        return result

    def _check_existence_folder(self) -> None:
        """
        Creates 1 FOLDER for The SETTINGS FILE if The FOLDER does not Exist and
        Writes The Finished TEMPLATE inside The FILE
        """

        if path.exists(self.path_folder_settings) is False:
            chdir(self.basedir)
            mkdir(self.FOLDER)
            chdir("..")
            self.is_create_folder = True

    def _failed_isfile(self) -> bool:
        """
        Checks The «self.failed_isfile» VARIABLE to Trigger The Check when
        The FILE in The FOLDER did not Exist
        ---
        RESULT: True (NOT FILE) || False (HAVE FILE)
        """

        if self.failed_isfile:
            self.failed_isfile = False
            return True

        return False

    def write_file_settings(self, data: dict[str, any]=TEMPLATE) -> None:
        """
        Writes The SETTINGS FILE

        ---
        PARAMETERS:
        - data: dict[str, any]=TEMPLATE -> The DATA for SETTINGS FILE
        """

        with open(self.path_file_settings, "w+") as f:
            f.write(dumps(data, ensure_ascii=False))

    def read_file_settings(self) -> dict[str, any]:
        """
        Reads The SETTINGS FILE

        ---
        RESULT: The DATA from SETTINGS FILE
        """

        with open(self.path_file_settings, "r") as f:
            data = f.read()

        try:
            result = loads(data)
        except:
            result = {}

        return result

# -------------------------------------
