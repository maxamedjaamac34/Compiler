from StatementParseClasses import Statement
from ParserClasses import Token

class LetStatementParse(Statement):
    parsing_structure_type = "letStatement"
    def __init__(self, let, var_name, *args):
        if not (isinstance(let, Token) and let.tokenType == "keyword" and let.tokenValue == "let"):
            raise ValueError("let must be keyword Token let")
        if not (isinstance(var_name, Token) and var_name.tokenType == "identifier"):
            raise ValueError("var_name must be a VarNameParse object")
        self.objects = [let, var_name]
        open_bracket = False
        optional_expression = False
        close_bracket = False
        equal = False
        expression = False
        semicolon = False
        for arg in args:

            # sacrificing efficiency for explicitness and readability by predefining
            # the requirements for each type of to be valid at each point in variable assignments
            bool_open_bracket = not open_bracket and not optional_expression and not close_bracket and not equal and not expression and not semicolon
            bool_optional_expression = open_bracket and not optional_expression and not close_bracket and not equal and not expression and not semicolon
            bool_close_bracket = open_bracket and optional_expression and not close_bracket and not equal and not expression and not semicolon
            bool_equal = not equal and not expression and not semicolon
            bool_expression = equal and not expression and not semicolon
            bool_semicolon = equal and expression and not semicolon

            if isinstance(arg, Token) and arg.tokenType == "symbol" and arg.tokenValue == "[" and bool_open_bracket:
                open_bracket = True
                self.objects.append(arg)
            elif isinstance(arg, Token) and arg.tokenType == "identifier" and bool_optional_expression:
                optional_expression = True
                self.objects.append(arg)
            elif isinstance(arg, Token) and arg.tokenType == "symbol" and arg.tokenValue == "]" and bool_close_bracket:
                close_bracket = True
                self.objects.append(arg)
            elif isinstance(arg, Token) and arg.tokenType == "symbol" and arg.tokenValue == "=" and bool_equal:
                equal = True
                self.objects.append(arg)
            elif isinstance(arg, Token) and arg.tokenType == "identifier" and bool_expression:
                expression = True
                self.objects.append(arg)
            elif isinstance(arg, Token) and arg.tokenType == "symbol" and arg.tokenValue == ";" and bool_semicolon:
                semicolon = True
                self.objects.append(arg)
            elif semicolon: # so that this can accept trailing tokens
                break
        if not equal and not expression and not semicolon:
            raise ValueError("let statements require = expression ;")


