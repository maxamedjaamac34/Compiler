from StatementParseClasses import Statement
from ParserClasses import Token

class ReturnStatementParse(Statement):
    parsing_structure_type = "returnStatement"
    def __init__(self, return_statement: Token, *args):
        if not (isinstance(return_statement, Token) and return_statement.tokenType == "keyword" and return_statement.tokenValue == "return"):
            raise ValueError("return_statement must 'return' keyword Token")
        self.objects = [return_statement]
        semicolon = False # Whether there has been a semicolon
        expression = False # Whether there has been an expression before this is evaluated
        for arg in args:
            if isinstance(arg, Token) and arg.tokenType == "identifier" and not semicolon and not expression:
                expression = True
                self.objects.append(arg)
            elif isinstance(arg, Token) and arg.tokenType == "symbol" and arg.tokenValue == ";" and not semicolon:
                semicolon = True
                self.objects.append(arg)
            elif semicolon: # so it can accept trailing tokens
                break
            else:
                raise ValueError("Return statement must be in the form of return expression? ;")
        if not semicolon:
            raise ValueError("Return statement must have ; at end")