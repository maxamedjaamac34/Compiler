from ProgramStructureParseClasses import ProgramStructure
from ParserClasses import Token

class TypeParseN(ProgramStructure):
    parsing_structure_type = "type"
    def __init__(self, type_name, *args):
        # args does nothing, this is so it accepts trailing tokens
        if type_name is Token:
            if type_name.tokenType == "identifier":
                self.objects = [type_name]
            if type_name.tokenType != "keyword":
                raise ValueError("type must be a keyword if it is a Token")
            if type_name.tokenValue != ("int" or "char" or "boolean"):
                raise ValueError("type must be 'int', 'char', or 'boolean' if it is a keyword Token")
            else:
                self.objects = [type_name]
        else:
            raise ValueError("type must be either a Token or a ClassNameParse")