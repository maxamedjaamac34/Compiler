from ProgramStructureParseClasses import ProgramStructure
from ParserClasses import Token

class SubroutineNameParseN(ProgramStructure):
    parsing_structure_type = "subroutineName"
    def __init__(self, identifier: Token, *args):
        # args does nothing, this is so it accepts trailing tokens
        if identifier.tokenType != "identifier":
            raise ValueError("subroutineName's identifier must be an identifier")
        self.objects = [identifier]