from ProgramStructureParseClasses import ProgramStructure
from ParserClasses import Token

class VarNameParseN(ProgramStructure):
    parsing_structure_type = "varName"
    def __init__(self, identifier: Token, *args):
        # args does nothing, this is so it accepts trailing tokens
        if identifier.tokenType != "identifier":
            raise ValueError("varName's identifier must be an identifier")
        self.objects = [identifier]