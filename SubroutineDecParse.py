from ProgramStructureParseClasses import ProgramStructure
from ParserClasses import Token
from ParameterListParse import ParameterListParse
from SubroutineBodyParse import SubroutineBodyParse

class SubroutineDecParse(ProgramStructure):
    parsing_structure_type = "subroutineDec"
    def __init__(self, subroutine, void_or_type, subroutine_name, open_parenthesis, *args):
        # args does nothing, this is so it accepts trailing tokens
        if not (isinstance(subroutine, Token) and subroutine.tokenType == "keyword" and subroutine.tokenValue in ["constructor", "function", "method"]):
            raise ValueError("Subroutine must be the keyword constructor, function, or method")
        if not (isinstance(void_or_type, Token) and (void_or_type.tokenType == "keyword" and void_or_type.tokenValue == "void") or void_or_type.tokenType == "identifier"):
            raise ValueError("void_or_type must be the keyword token void or a type")
        if not (isinstance(subroutine_name, Token) and subroutine_name.tokenType == "identifier"):
            raise ValueError("subroutine_name must be a SubroutineNameParse object")
        if not (isinstance(open_parenthesis,Token) and open_parenthesis.tokenType == "symbol" and open_parenthesis.tokenValue == "("):
            raise ValueError("open_parenthesis must be symbol Token '('")
        self.objects = [subroutine, void_or_type, subroutine_name, open_parenthesis]
        close_parenthesis = False # whether there has been a close parenthesis or not
        subroutine_body = False # whether there has been a subroutineBody or not
        for arg in args:
            if isinstance(arg, ParameterListParse) and not close_parenthesis and not subroutine_body:
                self.objects.append(arg)
            elif isinstance(arg, Token) and arg.tokenType == "symbol" and arg.tokenValue == ")":
                close_parenthesis = True
                self.objects.append(arg)
            elif isinstance(arg, SubroutineBodyParse) and close_parenthesis and not subroutine_body:
                subroutine_body = True
                self.objects.append(arg)
            elif close_parenthesis and subroutine_body:
                break
            else:
                raise ValueError("args must be ) parameterList? subroutineBody")