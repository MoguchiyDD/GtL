# Developer && Owner: МогучийДД (MoguchiyDD)
# LICENSE: MIT License which is located in the text file LICENSE
#
# Goal: Check for a New VERSION of The SOFTWARE
# Result: The VERSION of The Released SOFTWARE
#
# Past Modification: Editing The «GetVersion» CLASS (LOGGER)
# Last Modification: Editing The «GetVersion» CLASS (INTERNET)
# Modification Date: 2024.02.15, 08:24 PM
#
# Create Date: 2024.01.25, 02:27 PM


from PySide6.QtCore import Qt
from PySide6.QtWidgets import QWidget

from .filesystem import Logger
from .values import StringsValues
from .messages import activate_message_box

from bs4 import BeautifulSoup
from urllib3 import PoolManager
from requests import head

from re import findall

from os import getenv


# ------------ Web Parsing ------------

class GetVersion(QWidget):
    """
    This CLASS is Engaged in HARD-CODED WEB PARSING of The SITE and Gets
    The VERSION of THE SOFTWARE
    ---
    FUNCTIONS:
    - get_version() -> tuple[bool, str, str] : Finds Out The LATEST VERSION of
    The SOFTWARE and Compares it with The CURRENT VERSION of The SOFTWARE
    """

    def __init__(
        self,
        language_char: str,
        parent: QWidget | None = None,
        flags: Qt.WindowType = Qt.WindowType.Widget
    ) -> None:
        super(GetVersion, self).__init__(parent, flags)
        self.setParent(parent)

        self.language_char = language_char.lower() + "_"
        self.basedir = parent.basedir
        self.str_val = StringsValues(self.basedir)
        self.logs = Logger(self.basedir)

        self.soup = None

        is_net = availability_internet(1)
        if not is_net:
            activate_message_box(
                self.basedir,
                self.language_char + "error_net_title",
                self.language_char + "error_net_text",
                "net.svg",
                self
            )
            text = "There is no connection to the Internet to check "
            text += "the new release"
            self.logs.write_logger(self.logs.LoggerLevel.LOGGER_ERROR, text)
        else:
            try:
                url = self.str_val.string_values("app_version_tags")
                https = PoolManager()
                response = https.request("GET", url)
                self.soup = BeautifulSoup(response.data, "html.parser")
            except:  # ERROR
                activate_message_box(
                    self.basedir,
                    self.language_char + "error_version_title",
                    self.language_char + "error_version_text",
                    "net.svg",
                    self
                )
                text = "Didn't open the required URL page to check "
                text += "the new release"
                self.logs.write_logger(
                    self.logs.LoggerLevel.LOGGER_ERROR,
                    text
                )

    def get_version(self) -> tuple[bool, str, str]:
        """
        Finds Out The LATEST VERSION of The SOFTWARE and Compares it with
        The CURRENT VERSION of The SOFTWARE
        ---
        RESULT: (New Version (True) | Current Version (False),
        Short NAME of VERSION | "", Full NAME of VERSION | "")
        """

        if self.soup is not None:
            href = self.str_val.string_values("app_version_find")
            tags = self.soup.find(
                lambda tag: (tag.name == "a" and
                             "/".join(tag.get("href").split("/")[:-1]) == href)
            )

            # TAG
            tag_version = tags.text.split("-")[0]
            int_tag_version = int("".join(findall(r"[\d]+", tag_version)))

            # ENV
            env_version = getenv("VERSION")
            int_env_version = int("".join(findall(r"[\d]+", env_version)))

            if (int_tag_version > int_env_version):  # New Version
                activate_message_box(  # SUCCESS
                    self.basedir,
                    self.language_char + "success_version_title",
                    self.language_char + "success_version_text",
                    "version.svg",
                    self
                )

                text = "Notifying the user about the availability of a new "
                text += "version of the GtL program"
                self.logs.write_logger(
                    self.logs.LoggerLevel.LOGGER_SUCCESS, text
                )

                result = (True, tag_version[1:], tags.text)
                return result

        result = (False, "", "")
        return result

# -------------------------------------


def availability_internet(timeout: int) -> bool:
    """
    Checks INTERNET Access on The CURRENT DEVICE

    ---
    PARAMETERS:
    - timeout: int -> TIME for Checking
    ---
    RESULT: Checking for ACCESS to The INTERNET (True / False)
    """

    try:
        head("https://www.google.com/", timeout=timeout)
    except:
        return False

    return True
