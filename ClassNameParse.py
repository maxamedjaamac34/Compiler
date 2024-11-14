from ProgramStructureParseClasses import ProgramStructure
from ParserClasses import Token

class ClassNameParseN(ProgramStructure):
    parsing_structure_type = "className"
    def __init__(self, identifier: Token, *args):
        # args does nothing, this is so it accepts trailing tokens
        if identifier.tokenType != "identifier":
            raise ValueError("className's identifier must be an identifier")
        self.objects = [identifier]