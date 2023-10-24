# Developer && Owner: МогучийДД (MoguchiyDD)
# LICENSE: MIT License which is located in the text file LICENSE
#
# Goal: Parse XML Files
# Result: Returning The RESULT through an ATTRIBUTE with The NAME
#
# Past Modification: Checking CODE The PEP8
# Last Modification: Editing The «string_values» FUNCTION (SOURCE PARSE)
# Modification Date: 2023.10.23, 08:50 PM
#
# Create Date: 2023.10.23, 03:23 PM


from xml.etree.ElementTree import parse


# ------------ STRINGS ------------

def string_values(attribute_name: str) -> str:
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

    try:
        xml = parse(str("app/values/strings.xml"))
    except FileNotFoundError:
        xml = None
    except TypeError:
        xml = None

    if xml is not None:
        resources = xml.getroot()
        for strings in resources:
            string = strings.find("[@name=\"" + attribute_name + "\"]")
            if string is not None:
                text = string.text
                if isinstance(text, str) is True:
                    result = text
                    break

    return result

# ---------------------------------