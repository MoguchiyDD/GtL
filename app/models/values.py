# Developer && Owner: МогучийДД (MoguchiyDD)
# LICENSE: MIT License which is located in the text file LICENSE
#
# Goal: Parse XML Files
# Result: Returning The RESULT through an ATTRIBUTE with The NAME
#
# Past Modification: Adding The «StringsValues» CLASS
# Last Modification: Adding The «StringsValues» CLASS («strings_values_idx»)
# Modification Date: 2023.10.30, 02:33 PM
#
# Create Date: 2023.10.23, 03:23 PM


from xml.etree.ElementTree import parse


# ------------ STRINGS ------------

class StringsValues:
    """
    Responsible for Taking STRINGS from The «app/values/strings.xml» FILE

    ---
    FUNCTIONS:
    - string_values(attribute_name: str) -> str : From The FILE
    "app/values/string.sml" it produces The RESULT through The ATTRIBUTE "name"
    - strings_values_idx(attribute_name: str, idx: int) -> str : From The FILE
    "app/values/string.sml" it produces The RESULT through The ATTRIBUTE "name"
    + Finds The Search WORD
    """

    def __init__(self) -> None:
        try:
            self.xml = parse(str("app/values/strings.xml"))
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

    def strings_values_idx(self, attribute_name: str, idx: int) -> str:
        """
        From The FILE "app/values/string.sml" it produces The RESULT through
        The ATTRIBUTE "name" + Finds The Search WORD
        ---
        PARAMETERS:
        - attribute_name: str -> ATTRIBUTE with The NAME
        - idx: int -> INDEX of The Search WORD
        ---
        RESULT: ("", "", "") || ("FIND WORD", "1 PART", "2 PART")
        """

        result = ("", "", "")

        val = self.string_values(attribute_name)
        len_val = len(val)
        if (len_val >= 1) and (idx < len_val):
            list_val = val.split(" ")
            find_word = list_val[idx]
            parts = val.split(find_word)
            result = (find_word, parts[0], parts[1])

        return result

# ---------------------------------
