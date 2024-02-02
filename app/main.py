# Developer && Owner: МогучийДД (MoguchiyDD)
# LICENSE: MIT License which is located in the text file LICENSE
#
# Goal: Launch Working SOFTWARE
# Result: Opens The Finished SOFTWARE in The ACTIVE WINDOW
#
# Past Modification: Editing The «MainWindow» BLOCK (FOOTER)
# Last Modification: Editing The «MainWindow» BLOCK (LOGGER)
# Modification Date: 2024.02.02, 04:21 PM
#
# Create Date: 2023.10.23, 11:28 AM


from PySide6.QtCore import QObject, Qt, Slot, Signal
from PySide6.QtGui import QScreen, QFontDatabase, QIcon
from PySide6.QtWidgets import QApplication, QMainWindow, QWidget, QVBoxLayout

from models.releases import GetVersion
from models.filesystem import FileSystem, Logger
from models.values import StringsValues
from models.messages import activate_message_box
from models.header import Header
from models.content import Content
from models.footer import Footer

from threading import Thread
from schedule import every, run_pending, cancel_job
from dotenv import load_dotenv
from time import sleep

from sys import argv, exit
from os import getenv, path

basedir = path.dirname(__file__)
load_dotenv()


# ------------ SOFTWARE ------------

class MainWindow(QMainWindow):
    """
    The MAIN CLASS that Runs The All SOFTWARE

    ---
    PARAMETERS:
    - parent: QWidget | None = None -> Widget PARENT for this CLASS
    (AFTER THAT, THIS CURRENT CLASS WILL BECOME A CHILD OF THE PARENT)
    - f: Qt.WindowType = Qt.WindowType.Window -> Window-System (Window)
    """

    MIN_WIDTH = 1024
    MIN_HEIGHT = 600

    def __init__(
        self,
        parent: QWidget | None = None,
        flags: Qt.WindowType = Qt.WindowType.Window
    ) -> None:
        super(MainWindow, self).__init__(parent, flags)

        global basedir
        self.basedir = basedir
        self.str_val = StringsValues(self.basedir)
        self.logs = Logger()

        self.data_settings_file = self.__ram_settegins_file()  # RAM
        self.language = self.__language(  # LANGUAGE
            self.data_settings_file["language"]
        )
        version = GetVersion(self.language[0], self).get_version()
        self.__main(  # TITLE, SIZE, CENTER WINDOW && FONTS
            version[0], version[1]
        )
        self.__content(version[2])  # CONTENT

        # INSTALL
        self.widget = QWidget()
        self.widget.setLayout(self.main_layout)
        self.setCentralWidget(self.widget)

        # For New VERSION
        if version[0] is False:
            self.schedule = RunSchedule(self.language[0], self)
            self.schedule.signal_checking_release.connect(
                self.__check_and_activate_release
            )

    def __main(self, is_version: bool, number_version: str) -> None:
        """
        Settings for TITLE, WINDOW SIZE, WINDOW POSITION and FONT

        ---
        PARAMETERS:
        - is_version: bool -> New Version (True) | Current Version (False)
        - number_version: str -> Short NAME of VERSION | ""
        """

        # TITLE
        window_title = self.str_val.string_values("app_title")
        title = window_title + " — " + getenv("VERSION")

        # VERSION
        if is_version:
            text_version = self.str_val.string_values(
                self.language[0].lower() + "_" + "version_title"
            ).upper()
            window_title_version = f"({ text_version }: { number_version })"
            self.setWindowTitle(title + " " + window_title_version)
        else:
            self.setWindowTitle(title)

        self.setMinimumSize(self.MIN_WIDTH, self.MIN_HEIGHT)  # SIZE

        # CENTER WINDOW
        center = QScreen.availableGeometry(
            QApplication.primaryScreen()
        ).center()
        geo = self.frameGeometry()
        geo.moveCenter(center)
        self.move(geo.topLeft())

        # FONTS
        QFontDatabase.addApplicationFont(
            path.join(basedir, "fonts/Lora", "Lora-Bold.ttf")
        )
        QFontDatabase.addApplicationFont(
            path.join(basedir, "fonts/Lora", "Lora-Regular.ttf")
        )
        QFontDatabase.addApplicationFont(
            path.join(basedir, "fonts/Ubuntu", "Ubuntu-B.ttf")
        )
        QFontDatabase.addApplicationFont(
            path.join(basedir, "fonts/Ubuntu", "Ubuntu-R.ttf")
        )

    def __content(self, number_version: str) -> None:
        """
        Fills LAYOUT within The LAYERS

        ---
        PARAMETERS:
        - number_version -> Full NAME of VERSION | ""
        """

        self.main_layout = QVBoxLayout()
        self.main_layout.setContentsMargins(0, 0, 0, 0)
        self.header = Header(
            self.language[0], self.language[1], number_version, self
        )
        self.content = Content(self.language[0], self.header, self)
        Footer(self.language[0], self)

    def __ram_settegins_file(self) -> dict[str, any]:
        """
        Checks and Gets DATA from 1 SETTINGS FILE (JSON)

        ---
        RESULT: DICTIONARY from SETTINGS FILE (JSON)
        """

        def __info_message() -> None:
            """
            Displaying a MESSAGE about Updating The SETTINGS FILE and RAM
            """

            activate_message_box(
                self.basedir,
                "ru_info_msg_data_title",
                "ru_info_msg_data_text",
                "info.svg",
                self
            )
            self.logs.write_logger(
                self.logs.LoggerLevel.LOGGER_INFO,
                "Fixing a damaged program settings file"
            )

        def __update_data() -> dict[str, any]:
            """
            Updating The SETTINGS FILE and RAM, as well as Displaying a MESSAGE
            about DATA Update
            ---
            RESULT: The DATA from The SETTINGS FILE
            """

            filesystem.write_file_settings()
            data_settings_file = filesystem.TEMPLATE
            __info_message()  # INFO MESSAGE BOX

            return data_settings_file

        filesystem = FileSystem(self.basedir)
        data_settings_file = filesystem.read_file_settings()

        is_error_filesystem = filesystem._failed_isfile()
        if is_error_filesystem is True:  # Error : No FILE
            __info_message()  # INFO MESSAGE BOX
        else:  # Checking KEYS
            valid_keys = filesystem._valid_true_keys(
                list(data_settings_file.keys())
            )
            valid_values = filesystem._valid_true_values(data_settings_file)
            if (valid_keys is False) or (valid_values is False):  # Error
                data_settings_file = __update_data()

        return data_settings_file

    def __language(self, language: str) -> tuple[str]:
        """
        Selects The LANGUAGE for The SOFWARE

        ---
        PARAMETERS:
        - language: str -> The LANGUAGE (for Select)
        ---
        RESULT: ("RU", "Русский") || ("EN", "English")
        """

        match language:
            case "RU":
                result = ("RU", "Русский")
            case "EN":
                result = ("EN", "English")

        return result

    @Slot()
    def __check_and_activate_release(
        self, language: str, parent: QWidget
    ) -> None:
        """
        Check and Activate The New VERSION (GUI)

        ---
        PARAMETERS:
        - language: str -> The «RU» or The «EN»
        - parent: MainWindow -> Reference to The CLASS «MainWindow»
        """

        def rename_window_title(short_name_version: str) -> None:
            """
            Renames The TITLE of The MAIN WINDOW

            ---
            PARAMETERS:
            - short_name_version: str -> For Example, 1.1.0
            """

            window_title = self.str_val.string_values("app_title")
            title = window_title + " — " + getenv("VERSION")
            text_version = self.str_val.string_values(
                self.language[0].lower() + "_" + "version_title"
            ).upper()
            title_version = f"({ text_version }: { short_name_version })"
            self.setWindowTitle(title + " " + title_version)

        def show_button_header(full_name_version: str) -> None:
            """
            Shows and Overrides The ACTION of a BUTTON in The HEADER

            ---
            PARAMETERS:
            - full_name_version: str -> For Example, v1.1.0-stable
            """

            # Update URL
            self.header.version = full_name_version
            text_version = self.str_val.string_values("app_version")
            text_version += "/" + self.header.version

            # Shows and Overrides The ACTION of a BUTTON
            self.header.btn_updates.clicked.disconnect()
            self.header.btn_updates.clicked.connect(
                lambda _: self.header.open_url(
                    text_version, "error_msg_url_text_version"
                )
            )
            self.header.btn_updates.show()

        version = GetVersion(language, parent).get_version()
        is_new_version = version[0]
        if is_new_version:
            short_name_version = version[1]
            full_name_version = version[2]

            rename_window_title(short_name_version)  # Title
            show_button_header(full_name_version)  # Header

            self.schedule.is_activate = False

# ----------------------------------


# ------------ SCHEDULE ------------

class RunSchedule(QObject):
    """
    Every 10 HOURS, Checks through The THREAD for The RELEASE of a New VERSION.
    If a New VERSION is RELEASED, then The THREAD will Close After The SIGNAL
    has been Fully Processed.
    ---
    PARAMETERS:
    - language: str -> The «RU» or The «EN»
    - parent: MainWindow -> Reference to The CLASS «MainWindow»
    """

    signal_checking_release = Signal(str, QWidget)

    def __init__(self, language: str, parent: MainWindow) -> None:
        super().__init__()

        self.is_activate = True

        self.thread = Thread(
            target=self.run,
            name="THREAD_RELEASE",
            args=(language, parent),
            daemon=True
        )
        self.thread.start()

    def run(self, language: str, parent: MainWindow) -> None:
        """
        Runs a THREAD

        ---
        PARAMETERS:
        - language: str -> The «RU» or The «EN»
        - parent: MainWindow -> Reference to The CLASS «MainWindow»
        """

        def release() -> None:
            """
            Checking for a New VERSION
            """

            self.signal_checking_release.emit(language, parent)

        job = every(10).hours.do(release)
        while self.is_activate:
            run_pending()
            sleep(1)

            if self.is_activate is False:
                cancel_job(job)

# ----------------------------------


if __name__ == "__main__":
    app = QApplication(argv)
    app.setWindowIcon(
        QIcon(path.join(basedir, "icons/favicons", "favicon_256x256.ico"))
    )

    with open(path.join(basedir, "qss", "main.qss"), "r") as qss_file:
        app.setStyleSheet(qss_file.read())

    window = MainWindow()
    window.show()

    exit(app.exec())
