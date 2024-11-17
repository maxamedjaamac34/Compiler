from ParserClasses import Token, ParsingStructureNotFound
from StatementParseClasses import Statement, StatementsParse
from ExpressionParseClasses import SubroutineCallParse, ExpressionParse


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
    def __init__(self, *args):
        arg_l = list(args)
        self.objects = []
        # if (expression) {statements}
        # optional: else {statements}
        if isinstance(arg_l[0], Token) and arg_l[0].tokenType == "keyword" and arg_l[0].tokenValue == "if":
            self.objects.append(arg_l[0])
        else:
            raise ParsingStructureNotFound("first arg must be a keyword token if")
        if isinstance(arg_l[1], Token) and arg_l[1].tokenType == "symbol" and arg_l[1].tokenValue == "(":
            self.objects.append(arg_l[1])
        else:
            raise ParsingStructureNotFound("second arg must be a symbol token ( ")
        try:
            expression = ExpressionParse(*arg_l[2:])
            self.objects.append(expression)
            arg_l[2:] = [expression] + arg_l[len(expression.objects)+2:]
        except ParsingStructureNotFound:
            raise ParsingStructureNotFound("*arg_l[2:] must be a valid ExpressionParse")
        # {statements}
        if isinstance(arg_l[3], Token) and arg_l[3].tokenType == "symbol" and arg_l[3].tokenValue == "{":
            self.objects.append(arg_l[3])
        else:
            raise ParsingStructureNotFound("fourth arg must be symbol token {")
        # Statements might be empty
        close_brace_index = 5 # If statements is empty this becomes 4
        try:
            statements = StatementsParse(*arg_l[4:])
            self.objects.append(statements)
            arg_l[4:] = [statements] + arg_l[len(statements.objects)+4:]
        except ParsingStructureNotFound:
            close_brace_index = 4
        if isinstance(arg_l[close_brace_index], Token) and arg_l[close_brace_index].tokenType == "symbol" and arg_l[close_brace_index].tokenValue == "}":
            self.objects.append(arg_l[close_brace_index])
        else:
            raise ParsingStructureNotFound(f"{close_brace_index+1}th arg must be symbol token close brace") # needs to be +1 because zero based index
        if isinstance(arg_l[close_brace_index+1], Token) and arg_l[close_brace_index+1].tokenType == "keyword" and arg_l[close_brace_index+1].tokenValue == "else":
            self.objects.append(arg_l[close_brace_index+1])
        else:
            return
        # { statements }
class WhileStatementParse(Statement):
    parsing_structure_type = "whileStatement"
    def __init__(self, *args):
        arg_l = list(args)
        self.objects = []
        # while ( expression ) { statements }
        if isinstance(arg_l[0], Token) and arg_l[0].tokenType == "keyword" and arg_l[0].tokenValue == "while":
            self.objects.append(arg_l[0])
        else:
            raise ParsingStructureNotFound("first arg must be keyword Token while")
        if isinstance(arg_l[1], Token) and arg_l[1].tokenType == "symbol" and arg_l[1].tokenValue == "(":
            self.objects.append(arg_l[1])
        else:
            raise ParsingStructureNotFound("second arg must be symbol Token (")
        try:
            expression = ExpressionParse(*arg_l[2:])
            self.objects.append(expression)
            arg_l[2:] = [expression] + arg_l[len(expression.objects)+2:]
        except ParsingStructureNotFound:
            raise ParsingStructureNotFound("*arg_l[2:] must make valid ExpressionParse object")
        if isinstance(arg_l[3], Token) and arg_l[3].tokenType == "symbol" and arg_l[3].tokenValue == "{":
            self.objects.append(arg_l[3])
        else:
            raise ParsingStructureNotFound("*arg_l[3] must be symbol Token {")
        try:
            statements = StatementsParse(*arg_l[4:])
        except ParsingStructureNotFound:
            raise ParsingStructureNotFound("*arg_l[4] must make valid Statements object")
        self.objects.append(statements)
        arg_l[4:] = [statements] + arg_l[len(statements.objects)+4:]
        if isinstance(arg_l[5], Token) and arg_l[5].tokenType == "symbol" and arg_l[5].tokenValue == "}":
            raise ParsingStructureNotFound("*arg_l[5] must be symbol Token }")


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
        self.objects.append(subroutine_call)
        
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
        self.objects = []
        if isinstance(arg_l[0], Token) and arg_l[0].tokenType == "keyword" and arg_l[0].tokenValue == "return":
            self.objects.append(arg_l[0])
        else:
            raise ParsingStructureNotFound("arg_l[0] must be keyword Token return")
        if isinstance(arg_l[1], Token) and arg_l[1].tokenType == "symbol" and arg_l[1].tokenValue == ";":
            self.objects.append(arg_l[1])
        else:
            try:
                expression = ExpressionParse(*arg_l[1:])
            except ParsingStructureNotFound:
                raise ParsingStructureNotFound("*arg_l[1:] must make a valid ExpressionParse or arg[1] must be ; symbol Token")
            self.objects.append(expression)
            arg_l[1:] = [expression] + arg_l[len(expression.objects)+1:]
            if isinstance(arg_l[2], Token) and arg_l[2].tokenType == "symbol" and arg_l[2].tokenValue == ";":
                self.objects.append(arg_l[2])
            else:
                raise ParsingStructureNotFound("arg_l[2] must be symbol Token ;")

from StatementParseClasses import StatementParse
from ExpressionParseClasses import SubroutineCallParse

do_statement_example = [
    Token(21, 1, "keyword", "do"), # <keyword> do </keyword>
    Token(21, 2, "identifier", "draw"), # <identifier> draw </identifier>
    Token(21, 3, "symbol", "("), # <symbol> ( </symbol>
    Token(21, 4, "symbol", ")"), # <symbol> ) </symbol>
    Token(21, 5, "symbol", ";"), # <symbol> ; </symbol>
]

return_statement_example = [
    Token(1,1,"keyword", "return"),
    Token(1,1,"identifier", "x"),
    Token(1,1,"symbol", ";"),
]

print(DoStatementParse(*do_statement_example))