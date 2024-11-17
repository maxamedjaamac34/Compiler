from ParserClasses import Token, ParsingStructureNotFound
from StatementParseClasses import Statement
from ExpressionParseClasses import SubroutineCallParse

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

class DoStatementParse(Statement):
    """a do statement is do subroutineCall ;"""
    parsing_structure_type = "doStatement"
    def __init__(self, *args): # do subroutineCall ;
        arg_l = []
        for arg in args:
            arg_l.append(arg) #creates a list of all the arguments
        self.objects = []
        
        # first argument must be do keyword Token
        if isinstance(arg_l[0], Token) and arg_l[0].tokenType == "keyword" and arg_l[0].tokenValue == "do":
            self.objects.append(arg_l[0])
        else:
            raise ParsingStructureNotFound("First argument must be do")
        
        # *arg_l[1:] must make a valid SubroutineCall
        try:
            subroutine_call = SubroutineCallParse(*arg_l[1:])
        except ParsingStructureNotFound:
            raise ParsingStructureNotFound("*arg_l[1:] must make a valid SubroutineCall")
        arg_l[1:] = [subroutine_call] + arg_l[len(subroutine_call.objects)+1:]
        
        # arg_l[2] must be ; symbol Token
        if isinstance(arg_l[2], Token) and arg_l[2].tokenType == "symbol" and arg_l[2].tokenValue == ";":
            self.objects.append(arg_l[2])
        else:
            raise ParsingStructureNotFound("arg_l[2] must be ; symbol Token")


class ReturnStatementParse(Statement):
    parsing_structure_type = "returnStatement"
    def __init__(self, *args):
        arg_l = []
        for arg in args:
            arg_l.append(arg)
        if not (isinstance(arg_l[0], Token) and arg_l[0].tokenType == "keyword" and arg_l[0].tokenValue == "return"):
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

from StatementParseClasses import StatementParse
from ExpressionParseClasses import SubroutineCallParse

do_statement_example = [
    Token(21, 1, "keyword", "do"), # <keyword> do </keyword>
    Token(21, 2, "identifier", "draw"), # <identifier> draw </identifier>
    Token(21, 3, "symbol", "("), # <symbol> ( </symbol>
    Token(21, 4, "symbol", ")"), # <symbol> ) </symbol>
    Token(21, 5, "symbol", ";"), # <symbol> ; </symbol>
]

print(DoStatementParse(*do_statement_example))