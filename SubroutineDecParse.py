from ProgramStructureParseClasses import ProgramStructure
from ParserClasses import Token
from ParameterListParse import ParameterListParse
from SubroutineBodyParse import SubroutineBodyParse

class SubroutineDecParse(ProgramStructure):
    parsing_structure_type = "subroutineDec"
    def __init__(self, subroutine, void_or_type, subroutine_name, open_parenthesis, parameter_list, close_parenthesis, subroutine_body, *args):
        # args does nothing, this is so it accepts trailing tokens
        if not (isinstance(subroutine, Token) and subroutine.tokenType == "keyword" and subroutine.tokenValue in ["constructor", "function", "method"]):
            raise ValueError("Subroutine must be the keyword constructor, function, or method")
        if not (isinstance(void_or_type, Token) and (void_or_type.tokenType == "keyword" and void_or_type.tokenValue == "void") or void_or_type.tokenType == "identifier"):
            raise ValueError("void_or_type must be the keyword token void or a type")
        if not (isinstance(subroutine_name, Token) and subroutine_name.tokenType == "identifier"):
            raise ValueError("subroutine_name must be a SubroutineNameParse object")
        if not (isinstance(open_parenthesis,Token) and open_parenthesis.tokenType == "symbol" and open_parenthesis.tokenValue == "("):
            raise ValueError("open_parenthesis must be symbol Token '('")
        if not isinstance(parameter_list, ParameterListParse):
            raise ValueError("parameter_list must be ParameterListParse object")
        if not (isinstance(close_parenthesis, Token) and close_parenthesis.tokenType == "symbol" and close_parenthesis.tokenValue == ")"):
            raise ValueError("close_parenthesis must be symbol Token ')'")
        if not isinstance(subroutine_body, SubroutineBodyParse):
            raise ValueError("subroutine_body must be SubroutineBodyParse object")
        self.objects = [subroutine, void_or_type, open_parenthesis, parameter_list, close_parenthesis, subroutine_body]