from ParserClasses import ParsingStructure, ParsingStructureNotFound, Token
from ProgramStructureParseClasses import SubroutineNameParse

# class list for import statements:
# StatementParse, StatementsParse

class Statement(ParsingStructure):
    pass # statements, statement, letStatement, ifStatement, whileStatement, doStatement, returnStatement

class StatementParse(Statement):
    parsing_structure_type = "statement"
    def __init__(self, statement, *args):
        # *args lets it take trailing tokens
        arg_l = list(args)
        try:
            statement = LetStatementParse(*arg_l)
        except ParsingStructureNotFound:
            try:
                statement = IfStatementParse(*arg_l)
            except ParsingStructureNotFound:
                try:
                    statement = WhileStatementParse(*arg_l)
                except ParsingStructureNotFound:
                    try:
                        statement = DoStatementParse(*arg_l)
                    except ParsingStructureNotFound:
                        try:
                            statement = ReturnStatementParse(*arg_l)
                        except ParsingStructureNotFound:
                            raise ParsingStructureNotFound("statement should be a letStatement, ifStatement, whileStatement, doStatement, or returnStatement")
        self.objects = [statement]

class StatementsParse(ParsingStructure):
    parsing_structure_type = "statements"
    def __init__(self, *args):
        theres_statements = False
        arg_l = list(args)
        self.objects = []
        for i in range(len(arg_l)):
            try:
                statement = StatementParse(*arg_l[i:])
                self.objects.append(statement)
                arg_l[i:] = [statement] + arg_l[len(statement.objects)+i:]
                theres_statements = True
            except ParsingStructureNotFound:
                if theres_statements:
                    break
                else:
                    raise ParsingStructureNotFound("There's no statements")

#Now implemling the let statement parsing
class LetStatementParse(Statement):
    """Handles parsing for let statements: grammar of let stat: 'let' varName '['expression']' '=' expression ';'"""
    parsing_structure_type = "letStatement"

    def __init__(self, *args):
        # Conveting args to a list for easy handling
        arg_l = list(args)
        self.objects = []  # To store parsed objects for the let statement

        # check there are tokens given
        if not arg_l:
            raise ParsingStructureNotFound("letStatement not found: you've passed nothing into here")

        # First token must be the 'let' keyword
        if isinstance(arg_l[0], Token) and arg_l[0].tokenType == "keyword" and arg_l[0].tokenValue == "let":
            self.objects.append(arg_l[0])  # Append the 'let' keyword token to objects
        else:
            raise ParsingStructureNotFound("First token must be 'let' keyword")

        # Second token must be the variable name aka (identifier)
        if isinstance(arg_l[1], Token) and arg_l[1].tokenType == "identifier":
            self.objects.append(arg_l[1])  # Append the variable name token to objects
        else:
            raise ParsingStructureNotFound("arg_l[1]th token must be an identifier (variable name)")

        # Keep track of the current position in the argument list
        current_index = 2

        # checking if there's an array access using [expression]
        if (
            current_index < len(arg_l)
            and isinstance(arg_l[current_index], Token)
            and arg_l[current_index].tokenType == "symbol"
            and arg_l[current_index].tokenValue == "["
        ):
            # Append the '[' symbol token to objects
            self.objects.append(arg_l[current_index])
            current_index += 1  # Move to the next token

            # Parse the expression inside the brackets
            try:
                array_expression = ExpressionParse(*arg_l[current_index:])
                self.objects.append(array_expression)  # Append the parsed array expression
                current_index += len(array_expression.objects)  # Move past the parsed expression
            except ParsingStructureNotFound:
                raise ParsingStructureNotFound("Invalid expression inside array brackets")

            # Closing bracket must be present
            if (
                current_index < len(arg_l)
                and isinstance(arg_l[current_index], Token)
                and arg_l[current_index].tokenType == "symbol"
                and arg_l[current_index].tokenValue == "]"
            ):
                self.objects.append(arg_l[current_index])  # Append the ']' barket symbol token to objects
                current_index += 1  # Movingg to the next token
            else:
                raise ParsingStructureNotFound("You are missing closing ']' for array access")

        # Next token must be the '=' symbol
        if (
            current_index < len(arg_l)
            and isinstance(arg_l[current_index], Token)
            and arg_l[current_index].tokenType == "symbol"
            and arg_l[current_index].tokenValue == "="
        ):
            self.objects.append(arg_l[current_index])  # Append the '=' symbol token to objects
            current_index += 1  # Move to the next token
        else:
            raise ParsingStructureNotFound("arg_l[current_index]th must be '=' symbol after variable name or array access")

        # Parse the expression after the equal sing '=' ...
        try:
            expression = ExpressionParse(*arg_l[current_index:])
            self.objects.append(expression)  # add the parsed expression ob objects list
            current_index += len(expression.objects)  # Move past the parsed expression
        except ParsingStructureNotFound:
            raise ParsingStructureNotFound("Invalid expression after '=' in let statement")

        # Last token must be the ';' symbol
        if (
            current_index < len(arg_l)
            and isinstance(arg_l[current_index], Token)
            and arg_l[current_index].tokenType == "symbol"
            and arg_l[current_index].tokenValue == ";"
        ):
            self.objects.append(arg_l[current_index])  # Append the ';' symbol token to objects
        else:
            raise ParsingStructureNotFound("Missing ';' at the end of let statement")





class IfStatementParse(Statement):
    parsing_structure_type = "ifStatement"
    def __init__(self, *args):
        arg_l = list(args)
        self.objects = []
        # if (expression) {statements}
        # optional: else {statements}
        if not arg_l:
            raise ParsingStructureNotFound("ifStatement not found: you've passed nothing into here")
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
        if isinstance(arg_l[3], Token) and arg_l[3].tokenType == "symbol" and arg_l[3].tokenValue == ")":
            self.objects.append(arg_l[3])
        else:
            raise ParsingStructureNotFound("fourth arg must be symbol token ( ")
        # {statements}
        if isinstance(arg_l[4], Token) and arg_l[4].tokenType == "symbol" and arg_l[4].tokenValue == "{":
            self.objects.append(arg_l[4])
        else:
            raise ParsingStructureNotFound("fifth arg must be symbol token {")
        # Statements might be empty
        close_brace_index = 6 # If statements is empty this becomes 5
        try:
            statements = StatementsParse(*arg_l[5:])
            self.objects.append(statements)
            arg_l[5:] = [statements] + arg_l[len(statements.objects)+5:]
        except ParsingStructureNotFound:
            close_brace_index = 5
        if isinstance(arg_l[close_brace_index], Token) and arg_l[close_brace_index].tokenType == "symbol" and arg_l[close_brace_index].tokenValue == "}":
            self.objects.append(arg_l[close_brace_index])
        else:
            raise ParsingStructureNotFound(f"{close_brace_index+1}th arg must be symbol token close brace") # needs to be +1 because zero based index
        try:
            if isinstance(arg_l[close_brace_index+1], Token) and arg_l[close_brace_index+1].tokenType == "keyword" and arg_l[close_brace_index+1].tokenValue == "else":
                self.objects.append(arg_l[close_brace_index+1])
            else:
                return
        except IndexError: # if there's no else
            return
        # { statements }
        if isinstance(arg_l[close_brace_index+2], Token) and arg_l[close_brace_index+2].tokenType == "symbol" and arg_l[close_brace_index+2].tokenValue == "{":
            self.objects.append(arg_l[close_brace_index+2])
        else:
            raise ParsingStructureNotFound(f"{close_brace_index+3}th arg must be symbol token open brace")
        # statements can be empty
        else_close_index = close_brace_index + 4 # if there is no statements, this is close_brace_index+3
        try:
            statements = StatementsParse(*arg_l[close_brace_index+3:])
            self.objects.append(statements)
            arg_l[close_brace_index+3:] = [statements] + [len(statements.objects)+close_brace_index+3]
        except ParsingStructureNotFound:
            else_close_index = close_brace_index + 3
        if isinstance(arg_l[else_close_index], Token) and arg_l[else_close_index].tokenType == "symbol" and arg_l[else_close_index].tokenValue == "}":
            self.objects.append(arg_l[else_close_index])
        else:
            raise ParsingStructureNotFound("Last token must be }")


class WhileStatementParse(Statement):  # while ( expression ) { statements }
    parsing_structure_type = "whileStatement"

    def __init__(self, *args):
        arg_l = list(args)
        self.objects = []
       
        if not arg_l:
            raise ParsingStructureNotFound("whileStatement not found: you've passed nothing into here")
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
            arg_l[2:] = [expression] + arg_l[len(expression.objects) + 2:]
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
        arg_l[4:] = [statements] + arg_l[len(statements.objects) + 4:]
        if isinstance(arg_l[5], Token) and arg_l[5].tokenType == "symbol" and arg_l[5].tokenValue == "}":
            raise ParsingStructureNotFound("*arg_l[5] must be symbol Token }")


class DoStatementParse(Statement): #do draw()
    """a do statement is do subroutineCall ;"""
    parsing_structure_type = "doStatement"

    def __init__(self, *args):  # do subroutineCall ;
        arg_l = []
        for arg in args:
            arg_l.append(arg)  # creates a list of all the arguments
        self.objects = []
        if not arg_l:
            raise ParsingStructureNotFound("doStatement not found: you've passed nothing into here")

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
        arg_l[1:] = [subroutine_call] + arg_l[len(subroutine_call.objects) + 1:]
        self.objects.append(subroutine_call)

        # arg_l[2] must be ; symbol Token
        if isinstance(arg_l[2], Token) and arg_l[2].tokenType == "symbol" and arg_l[2].tokenValue == ";":
            self.objects.append(arg_l[2])
        else:
            raise ParsingStructureNotFound("arg_l[2] must be ; symbol Token")

class ReturnStatementParse(Statement): # retur; or return x;
    parsing_structure_type = "returnStatement"
    def __init__(self, *args):
        arg_l = []
        for arg in args:
            arg_l.append(arg)
        self.objects = []
        if not arg_l:
            raise ParsingStructureNotFound("whileStatement not found: you've passed nothing into here")
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

from ExpressionParseClasses import SubroutineCallParse, ExpressionParse


if_statement_example = [
    Token(1,1,"keyword", "if"),
    Token(1,1,"symbol", "("),
    Token(1,1,"identifier", "x"),
    Token(1,1,"symbol", ")"),
    Token(1,1,"symbol", "{"), # <symbol> ) </symbol>
    Token(21, 5, "symbol", ";"), # <symbol> ; </symbol>
    Token(1,1,"symbol", "}"),
]

return_statement_example = [
    Token(1,1,"keyword", "return"),
    Token(1,1,"identifier", "x"),
    Token(1,1,"symbol", ";"),
]

do_statement_example = [
    Token(21, 1, "keyword", "do"), # <keyword> do </keyword>
    Token(21, 2, "identifier", "draw"), # <identifier> draw </identifier>
    Token(21, 3, "symbol", "("), # <symbol> ( </symbol>
    Token(21, 4, "symbol", ")"), # <symbol> ) </symbol>
    Token(21, 5, "symbol", ";"), # <symbol> ; </symbol>
]

print(IfStatementParse(*if_statement_example))

