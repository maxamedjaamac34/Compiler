from StatementParseClasses import Statement
from ParserClasses import Token

class WhileStatementParse(Statement):
    parsing_structure_type = "whileStatement"
    def __init__(self, while_statement, open_parenthesis, expression, close_parenthesis, open_brace, *args):

        if not (isinstance(while_statement, Token) and while_statement.tokenType == "keyword" and while_statement.tokenValue == "while"):
            raise ValueError("while must be keyword Token while")
        if not (isinstance(open_parenthesis, Token) and open_parenthesis.tokenType == "symbol" and open_parenthesis.tokenValue == "("):
            raise ValueError("open_parenthesis must be symbol Token (")
        if not (isinstance(expression, Token) and expression.tokenType == "identifier"):
            raise ValueError("expression must be ExpressionParse object")
        if not (isinstance(close_parenthesis, Token) and close_parenthesis.tokenType == "symbol" and close_parenthesis.tokenValue == ")"):
            raise ValueError("close_parenthesis must be symbol Token )")
        if not (isinstance(open_brace, Token) and open_brace.tokenType == "symbol" and open_brace.tokenValue == "{"):
            raise ValueError("open_brace must be symbol Token {")
        self.objects = [while_statement, open_parenthesis, expression, close_parenthesis, open_brace]
        for arg in args:
            if isinstance(arg, Token) and arg.tokenType == "symbol" and arg.tokenValue == "}":
                self.objects.append(arg)
                break
            elif isinstance(arg, StatementParse):
                self.objects.append(arg)
            else:
                raise ValueError("arg must be StatementParse object or }")

from StatementParse import StatementParse

