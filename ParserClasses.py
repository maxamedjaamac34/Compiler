# class list for import statements:
# Token, ParsingStructure

class Token:
    def __init__(self, line_no: int, column_no: int, token_type: str, token_value: str):
        self.lineNo = line_no
        self.columnNo = column_no
        self.tokenType = token_type
        self.tokenValue = token_value

    def __str__(self):
        return f"<{self.tokenType}> {self.tokenValue} </{self.tokenType}>"

class ParsingStructure:  # The base class for all structures that include token objects
    parsing_structure_type = "Generic Parsing Structure Name (you shouldn't see this)"
    objects = ["Generic Parsing Structure Objects (you shouldn't see this)"]

    def __str__(self):
        objects_string = ""
        for var in self.objects:
            for line in str(var).splitlines():
                objects_string = objects_string + "\n   " + line
        return f"""<{self.parsing_structure_type}>{objects_string}
</{self.parsing_structure_type}>"""

