from StatementParseClasses import Statement
from ParserClasses import Token

class DoStatementParse(Statement):
    parsing_structure_type = "doStatement"
    def __init__(self, do, subroutine_call, semicolon, *args): # args does nothing, this is so it can accept trailing tokens
        if not (isinstance(do, Token) and do.tokenType == "keyword" and do.tokenValue == "do"):
            raise ValueError("do must be keyword Token 'do'")
        if not (isinstance(subroutine_call, SubroutineCallParse)):
            raise ValueError("subroutine_call must be a SubroutineCallParse object")
        if not (isinstance(semicolon, Token) and semicolon.tokenType == "symbol" and semicolon.tokenValue == ";"):
            raise ValueError("semicolon must be symbol Token ';'")
        self.objects = [do, subroutine_call, semicolon]

from SubroutineCallParse import SubroutineCallParse