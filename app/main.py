# Developer && Owner: МогучийДД (MoguchiyDD)
# LICENSE: MIT License which is located in the text file LICENSE
#
# Goal: Launch Working SOFTWARE
# Result: Opens The Finished SOFTWARE in The ACTIVE WINDOW
#
# Past Modification: Checking CODE The PEP8
# Last Modification: Editing The «MainWindow» CLASS (VERSION)
# Modification Date: 2024.01.25, 10:56 PM
#
# Create Date: 2023.10.23, 11:28 AM


from PySide6.QtCore import Qt
from PySide6.QtGui import QScreen, QFontDatabase, QIcon
from PySide6.QtWidgets import QApplication, QMainWindow, QWidget, QVBoxLayout

from models.releases import GetVersion
from models.filesystem import FileSystem
from models.values import StringsValues
from models.messages import MessageBox
from models.header import Header
from models.content import Content
from models.footer import Footer

from dotenv import load_dotenv

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

        header = Header(
            self.language[0], self.language[1], number_version, self
        )
        Content(self.language[0], header, self)
        Footer(self)

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

            text_for_info_msg_data_title = self.str_val.string_values(
                "ru_info_msg_data_title"
            )
            text_for_info_msg_data_text = self.str_val.string_values(
                "ru_info_msg_data_text"
            )
            MessageBox(
                path.join(self.basedir, "icons", "info.svg"),
                text_for_info_msg_data_title,
                text_for_info_msg_data_text,
                self
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
            if (valid_keys is False) or (valid_values is False):  # ErrorS
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
