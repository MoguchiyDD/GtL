# Developer && Owner: МогучийДД (MoguchiyDD)
# LICENSE: MIT License which is located in the text file LICENSE
#
# Goal: Writing and Reading IMPORTANT FILES
# Result: AUTOMATED SYSTEM with FILES
#
# Past Modification: Editing The «Logger» CLASS (DOCS)
# Last Modification: Editing The «FileSystem» CLASS (LANGUAGE && LOGGER)
# Modification Date: 2024.02.02, 08:52 PM
#
# Create Date: 2023.11.01, 10:01 PM


from json import dumps, loads
from datetime import datetime, timezone

from os import path, chdir, mkdir, getcwd
from os.path import isfile


# ------------- VARIABLES -------------

class FileVariables:
    """
    - FOLDER : Folder with DATA for The SOFTWARE in The FILE SYSTEM
    - FILE_SETTINGS : File for SOFTWARE SETTINGS
    - FILE_LANGUAGE : File for Saving The SOFTWARE LANGUAGE
    - FILE_LOGS : File for LOGGING The SOFTWARE
    """

    FOLDER = ".data"
    FILE_SETTINGS = ".settings.json"
    FILE_LANGUAGE = ".lang.txt"
    FILE_LOGS = ".logs.txt"

# -------------------------------------


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
    - read_file_settings(self) -> dict[str, any] : Reads The SETTINGS FILE
    - write_file_settings(self, data: dict[str, any]=TEMPLATE) -> None :
    Writes The SETTINGS FILE
    - read_file_language(language: str=TEMPLATE_LANGUAGE_VALUE) -> str :
    Reads The LANGUAGE FILE
    - write_file_language(language: str) -> None : Writes The LANGUAGE FILE
    """

    # KEYS
    TEMPLATE_TITLE_KEY = "title"
    TEMPLATE_LIST_KEY = "list"
    TEMPLATE_DASH_KEY = "dash"
    TEMPLATE_BLOCK_KEY = "block"
    TEMPLATE_LANGUAGE_KEY = "language"
    TEMPLATE_NOTIFICATION_KEY = "notification"
    TEMPLATE_ANIMATION_KEY = "animation"

    # VALUES
    TEMPLATE_TITLE_VALUE = False
    TEMPLATE_LIST_VALUE = False
    TEMPLATE_DASH_VALUE = True
    TEMPLATE_BLOCK_VALUE = [".", "?", "!"]
    TEMPLATE_LANGUAGE_VALUE = "RU"
    TEMPLATE_NOTIFICATION_VALUE = False
    TEMPLATE_ANIMATION_VALUE = False

    # TEMPLATE
    TEMPLATE = {
        TEMPLATE_TITLE_KEY: TEMPLATE_TITLE_VALUE,
        TEMPLATE_LIST_KEY: TEMPLATE_LIST_VALUE,
        TEMPLATE_DASH_KEY: TEMPLATE_DASH_VALUE,
        TEMPLATE_BLOCK_KEY: TEMPLATE_BLOCK_VALUE,
        TEMPLATE_LANGUAGE_KEY: TEMPLATE_LANGUAGE_VALUE,
        TEMPLATE_NOTIFICATION_KEY: TEMPLATE_NOTIFICATION_VALUE,
        TEMPLATE_ANIMATION_KEY: TEMPLATE_ANIMATION_VALUE
    }
    TEMPLATE_KEYS = TEMPLATE.keys()

    def __init__(
        self, path_main_file: str,
        overwrite_file: bool = False
    ) -> None:
        variables = FileVariables()
        self.FOLDER = variables.FOLDER
        self.FILE_SETTINGS = variables.FILE_SETTINGS
        self.FILE_LANGUAGE = variables.FILE_LANGUAGE
        
        self.basedir = path_main_file
        self.is_create_folder = False
        self.failed_isfile = False

        self.path_folder_settings = path.join(path_main_file, self.FOLDER)
        self.path_file_settings = path.join(
            self.path_folder_settings, self.FILE_SETTINGS
        )
        self.path_file_language = path.join(
            self.path_folder_settings, self.FILE_LANGUAGE
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
            elif key == self.TEMPLATE_NOTIFICATION_KEY:  # notification
                _cnt_result = __bool(value, _cnt_result)
            elif key == self.TEMPLATE_ANIMATION_KEY:  # animation
                _cnt_result = __bool(value, _cnt_result)

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

    def write_file_settings(self, data: dict[str, any]=TEMPLATE) -> None:
        """
        Writes The SETTINGS FILE

        ---
        PARAMETERS:
        - data: dict[str, any]=TEMPLATE -> The DATA for SETTINGS FILE
        """

        with open(self.path_file_settings, "w+") as f:
            f.write(dumps(data, ensure_ascii=False))

    def read_file_language(self, language: str=TEMPLATE_LANGUAGE_VALUE) -> str:
        """
        Reads The LANGUAGE FILE

        ---
        PARAMETERS:
        - language: str="RU" -> Symbols for LANGUAGE
        ---
        RESULT: The SYMBOLS for LANGUAGE from LANGUAGE FILE
        """

        if path.exists(self.path_file_language) is False:
            self.write_file_language(language)

        with open(self.path_file_language, "r+") as f:
            language = f.read()

        return language

    def write_file_language(self, language: str) -> None:
        """
        Writes The LANGUAGE FILE

        ---
        PARAMETERS:
        - language: str -> Symbols for LANGUAGE
        """

        with open(self.path_file_language, "w+") as f:
            f.write(language)

# -------------------------------------


# -------------- LOGGER ---------------

class Logger(FileSystem):
    """
    Writes LOGGING to «.data/logs.txt» FILE

    ---
    CLASSES:
    - LoggerLevel : Logging Level (INFO, SUCCESS || ERROR)
    ---
    PARAMETERS:
    - path_main_file: str -> The «basedir» VARIABLE from The «app/main.py» FILE
    ---
    FUNCTIONS:
    - write_logger(level: LoggerLevel, text: str) -> None : Writes The LOGGER
    """

    class LoggerLevel:
        """
        Logging Level (INFO, SUCCESS || ERROR)
        """

        LOGGER_INFO = "INFO"
        LOGGER_SUCCESS = "SUCCESS"
        LOGGER_ERROR = "ERROR"

    def __init__(self, path_main_file: str) -> None:
        self.basedir = path_main_file

        variables = FileVariables()
        self.FOLDER = variables.FOLDER
        self.FILE_LOGS = variables.FILE_LOGS

        self.path_folder_logger = path.join(path_main_file, self.FOLDER)
        self.path_logger = path.join(self.path_folder_logger, self.FILE_LOGS)

    def write_logger(self, level: LoggerLevel, text: str) -> None:
        """
        Writes The LOGGER

        ---
        PARAMETERS:
        - level: LoggerLevel -> Logging Level (INFO, SUCCESS || ERROR)
        - text: str -> Logging Text
        """

        if path.exists(self.path_folder_logger) is False:
            chdir(self.basedir)
            mkdir(self.FOLDER)

        date = datetime.now(timezone.utc).strftime("%Z %Y.%m.%d, %H:%M:%S")
        logger = date + " : " + level.upper() + " : " + text + "\n"

        with open(self.path_logger, "a+") as f:
            f.write(logger)

# -------------------------------------
