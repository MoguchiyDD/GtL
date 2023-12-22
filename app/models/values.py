# Developer && Owner: МогучийДД (MoguchiyDD)
# LICENSE: MIT License which is located in the text file LICENSE
#
# Goal: Parse XML Files
# Result: Returning The RESULT through an ATTRIBUTE with The NAME
#
# Past Modification: Editing The «StringsValues» CLASS («strings_values_idx»)
# Last Modification: Correction of CODE from LOGICAL ERRORS
# Modification Date: 2023.12.22, 06:54 PM
#
# Create Date: 2023.10.23, 03:23 PM


from xml.etree.ElementTree import parse
from os import path


# ------------ STRINGS ------------

class StringsValues:
    """
    Responsible for Taking STRINGS from The «app/values/strings.xml» FILE

    ---
    PARAMETERS:
    - basedir: str -> Directory COMPONENT of a PATHNAME
    ---
    FUNCTIONS:
    - string_values(attribute_name: str) -> str : From The FILE
    "app/values/string.sml" it produces The RESULT through The ATTRIBUTE "name"
    - strings_values_idx(attribute_name: str, idx: int) ->
    tuple[tuple[str], str, str] : From The FILE "app/values/string.sml"
    it produces The RESULT through The ATTRIBUTE "name" + Finds The Search WORD
    """

    def __init__(self, basedir: str) -> None:
        try:
            self.xml = parse(path.join(basedir, "values", "strings.xml"))
        except FileNotFoundError:
            self.xml = None
        except TypeError:
            self.xml = None

    def string_values(self, attribute_name: str) -> str:
        """
        From The FILE "app/values/string.sml" it produces The RESULT through
        The ATTRIBUTE "name"
        ---
        PARAMETERS:
        - attribute_name: str -> ATTRIBUTE with The NAME
        ---
        RESULT: "" || "..."
        """

        result = ""

        if self.xml is not None:
            resources = self.xml.getroot()
            for strings in resources:
                string = strings.find("[@name=\"" + attribute_name + "\"]")
                if string is not None:
                    text = string.text
                    if isinstance(text, str) is True:
                        result = text
                        break

        return result

    def strings_values_idx(
        self, attribute_name: str, *idx: int
    ) -> tuple[tuple[str], str, str]:
        """
        From The FILE "app/values/string.sml" it produces The RESULT through
        The ATTRIBUTE "name" + Finds The Search WORD
        ---
        PARAMETERS:
        - attribute_name: str -> ATTRIBUTE with The NAME
        - idx: int -> INDEX of The Search WORD
        ---
        RESULT: ((""), "", "") || (("FIND WORD"), "1 PART", "2 PART")
        """

        result = ((""), "", "")

        val = self.string_values(attribute_name)
        len_val = len(val)
        if (len_val >= 1):
            list_val = val.split()

            parts = []
            find_parts = []

            old_idx = 0
            for i in idx:
                one_part = [word for word in list_val[old_idx:i]]
                find_parts.append(" " + list_val[i] + " ")
                parts.append(" ".join(one_part))
                one_part = []
                old_idx = i + 1

            parts.append(" ".join(list_val[idx[-1] + 1:]))
            parts.insert(0, tuple(find_parts))
            result = tuple(parts)

        return result

# ---------------------------------
