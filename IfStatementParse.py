from StatementParseClasses import Statement
from ParserClasses import Token

class IfStatementParse(Statement):
    parsing_structure_type = "ifStatement"
    def __init__(self, if_statement, open_parenthesis, expression, close_parenthesis, open_brace, *args):
        if not (isinstance(if_statement, Token) and if_statement.tokenType == "keyword" and if_statement.tokenValue == "if"):
            raise ValueError("if must be keyword Token if")
        if not (isinstance(open_parenthesis, Token) and open_parenthesis.tokenType == "symbol" and open_parenthesis.tokenValue == "("):
            raise ValueError("open_parenthesis must be symbol Token (")
        if not (isinstance(expression, Token) and expression.tokenType == "identifier"):
            raise ValueError("expression must be ExpressionParse object")
        if not (isinstance(close_parenthesis, Token) and close_parenthesis.tokenType == "symbol" and close_parenthesis.tokenValue == ")"):
            raise ValueError("close_parenthesis must be symbol Token )")
        if not (isinstance(open_brace, Token) and open_brace.tokenType == "symbol" and open_brace.tokenValue == "{"):
            raise ValueError("open_brace must be symbol Token {")
        self.objects = [if_statement, open_parenthesis, expression, close_parenthesis, open_brace]
        close_brace = False
        else_statement = False
        else_open_brace = False
        else_close_brace = False
        for arg in args:
            if not close_brace:
                if isinstance(arg, Token) and arg.tokenType == "symbol" and arg.tokenValue == "}":
                    close_brace = True
                    self.objects.append(arg)
                elif isinstance(arg, StatementParse):
                    self.objects.append(arg)
                else:
                    raise ValueError("arg must be StatementParse object or }")
            elif isinstance(arg, Token) and arg.tokenType == "keyword" and arg.tokenValue == "else" and not else_statement:
                else_statement = True
                self.objects.append(arg)
            elif isinstance(arg, Token) and arg.tokenType == "symbol" and arg.tokenValue == "{" and else_statement and not else_open_brace:
                else_open_brace = True
                self.objects.append(arg)
            if else_open_brace and not else_close_brace:
                if isinstance(arg, Token) and arg.tokenType == "symbol" and arg.tokenValue == "}":
                    else_close_brace = True
                    self.objects.append(arg)
                if isinstance(arg, StatementParse):
                    self.objects.append(arg)
                else:
                    raise ValueError("arg must be StatementParse object or }")
            else:
                pass
        if not close_brace:
            raise ValueError("if statement needs close brace")

from StatementParse import StatementParse