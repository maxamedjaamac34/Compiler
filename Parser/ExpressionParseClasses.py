
from ParserClasses import Token, ParsingStructure, ParsingStructureNotFound


# class list for import statements:
# ExpressionParse, TermParse, SubroutineCallParse, ExpressionListParse, OpParse, UnaryOpParse, KeywordConstantParse

class Expression(ParsingStructure):
    pass

class ExpressionParse(ParsingStructure):
    parsing_structure_type = "expression"
    # Placeholder - expressions are replaced with identifiers in the Expressionless versions of test files
    def __init__(self, *args):
        arg_l = list(args)
        if not arg_l:
            raise ParsingStructureNotFound ("you didn't pass anything in")
        self.objects = []
        last_term = False # This flag states if the last argument was a term.
        # If it is true, the next argument should be an op.
        # If it is false, the next argument should be a term.
        for i in range(len(arg_l)):
            if last_term:
                try:
                    op = OpParse(*arg_l[i:])
                except ParsingStructureNotFound:
                    break
                last_term = False
                self.objects.append(op)
                arg_l[i:] = [op] + arg_l[i+len(op.objects):]
            else:
                try:
                    term = TermParse(*arg_l[i:])
                except ParsingStructureNotFound:
                    break
                last_term = True
                self.objects.append(term)
                arg_l[i:] = [term] + arg_l[i+len(term.objects):]
        if not last_term:
            raise ParsingStructureNotFound ("The last object in the expression must be a term")

class TermParse(Expression):
    parsing_structure_type = "term"
    # This one is the part that's not LL1
    def __init__(self, *args):
        try:
            term = self.varname_expression(*args)
        except ParsingStructureNotFound:
            pass
        try:
            term = self.parentheses_expression(*args)
        except ParsingStructureNotFound:
            pass
        try:
            term = self.unary_op_term()
        except ParsingStructureNotFound:
            pass
        try:
            term = self.subroutine_call()
        except ParsingStructureNotFound:
            pass
        try:
            term = self.var_name(*args)
        except ParsingStructureNotFound:
            pass
        try:
            term = self.token_term(*args)
        except ParsingStructureNotFound:
            raise ParsingStructureNotFound ("No term found")
        self.objects = term


    # Functions of term return list of the objects in the term
    def varname_expression(self, *args):
        # varName [ expression ]
        arg_l = list(args)
        objects = []
        try:
            var_name = VarNameParse(*arg_l)
        except ParsingStructureNotFound:
            raise ParsingStructureNotFound ("first arg must be a varName")
        objects.append(var_name)
        if isinstance(arg_l[1], Token) and arg_l[1].tokenType =="symbol" and arg_l[1].tokenValue == "[":
            objects.append(arg_l[1])
        else:
            raise ParsingStructureNotFound ("second arg must be symbol token [")
        try:
            expression = ExpressionParse(*arg_l[2:])
        except ParsingStructureNotFound:
            raise ParsingStructureNotFound ("third arg to the end of the list must make valid ExpressionParse")
        objects.append(expression)
        arg_l[2:] = [expression] + arg_l[2+len(expression.objects):] # this makes it consume the tokens
        if isinstance(arg_l[3], Token) and arg_l[3].tokenType =="symbol" and arg_l[3].tokenValue == "]":
            objects.append(arg_l[3])
        else:
            raise ParsingStructureNotFound ("second arg must be symbol token ]")
        return objects

    def parentheses_expression(self, *args):
        # ( expression )
        arg_l = list(args)
        objects = []
        if isinstance(arg_l[0], Token) and arg_l[0].tokenType == "symbol" and arg_l[0].tokenValue == "(":
            objects.append(arg_l[0])
        else:
            raise ParsingStructureNotFound ("first arg must be symbol token (")
        try:
            expression = ExpressionParse(*arg_l[1:])
        except ParsingStructureNotFound:
            raise ParsingStructureNotFound ("second arg to end of list must be valid ExpressionParse")
        objects.append(expression)
        arg_l[1:] = [expression] + arg_l[1+len(expression.objects):]
        if isinstance(arg_l[2], Token) and arg_l[2].tokenType == "symbol" and arg_l[2].tokenValue == ")":
            objects.append(arg_l[2])
        else:
            raise ParsingStructureNotFound("third arg must be symbol token )")
        return objects

    def unary_op_term(self, *args):
        # unaryOp term
        arg_l = list(args)
        try:
            unary_op = UnaryOpParse(*arg_l)
        except ParsingStructureNotFound:
            raise ParsingStructureNotFound ("first arg must be a unary_op")
        arg_l = [unary_op] + arg_l[len(unary_op.objects):]
        try:
            term = TermParse(*arg_l[1:])
        except ParsingStructureNotFound:
            raise ParsingStructureNotFound ("second arg must be a term")
        return [unary_op, term]
    def subroutine_call(self, *args):
        # subroutineCall
        try:
            subroutine_call = SubroutineCallParse(*args)
        except ParsingStructureNotFound:
            raise ParsingStructureNotFound ("No subroutine call found")
        return [subroutine_call]
    def var_name(self, *args):
        # varName
        try:
            var_name = VarNameParse(*args)
        except ParsingStructureNotFound:
            raise ParsingStructureNotFound ("Not a VarNameParse")
        return [var_name]
    def token_term(self, *args):
        # Token of type keyword, stringConstant, or integerConstant
        arg_l = list(args)
        token_types = ["keyword", "stringConstant", "integerConstant"]
        if isinstance(arg_l[0], Token) and arg_l[0].tokenType in token_types:
            return [arg_l[0]]
        else:
            raise ParsingStructureNotFound (f"not a Token of types {token_types}")

class OpParse(Expression):
    parsing_structure_type = "op"
    def __init__(self, op, *args): # args does nothing, this is so it can accept trailing tokens
        if not args:
            raise ParsingStructureNotFound ("you didn't pass anything in")
        if op is Token and op.tokenType == "symbol" and op.tokenValue in ["+", "-", "*", "/", "&", "|", "<", ">", "="]:
            self.objects = [op]
        else:
            raise ParsingStructureNotFound("op must be symbol Token + - * / & | < > =")

class UnaryOpParse(Expression):
    parsing_structure_type = "unaryOp"
    def __init__(self, *args): # args does nothing, this is so it can accept trailing tokens
        arg_l = list(args)
        if not arg_l:
            raise ParsingStructureNotFound ("you didn't pass anything in")
        if arg_l[0] is Token and arg_l[0].tokenType == "symbol" and arg_l[0].tokenValue in ["-", "~"]:
            self.objects = arg_l
        else:
            raise ParsingStructureNotFound("Unary operator must be symbol Token - or ~")

class KeywordConstantParse(Expression):
    parsing_structure_type = "keywordConstant"
    def __init__(self, op, *args): # args does nothing, this is so it can accept trailing tokens
        if not args:
            raise ParsingStructureNotFound ("you didn't pass anything in")
        if op is Token and op.tokenType == "keyword" and op.tokenValue in ["true", "false", "null", "this"]:
            self.objects = op
        else:
            raise ParsingStructureNotFound("Keyword constant must be keyword Token true, false, null, this")

class SubroutineCallParse(Expression):
    parsing_structure_type = "subroutineCall"
    def __init__(self, *args):
        arg_l = []
        for arg in args:
            arg_l.append(arg)
        if not arg_l:
            raise ParsingStructureNotFound ("you didn't pass anything in")
        self.objects = []
        if isinstance(arg_l[0], Token) and arg_l[0].tokenType == "identifier":
            pass # we do not know if this is className or varName or subroutineName yet.
        else:
            raise ParsingStructureNotFound("arg_l[0] must be an identifier Token")

        class_or_var = False
        if isinstance(arg_l[1], Token) and arg_l[1].tokenType == "symbol" and arg_l[1].tokenValue == "(":
            self.objects.append(SubroutineNameParse(arg_l[0])) # Now we know that arg_l[0] is SubroutineName
            self.objects.append(arg_l[1])
        elif isinstance(arg_l[1], Token) and arg_l[1].tokenType == "symbol" and arg_l[1].tokenValue == ".":
            self.objects.append(arg_l[0]) # It will remain ambiguous if this is a class or var name, oh well
            self.objects.append(arg_l[1])
            class_or_var = True
        else:
            raise ParsingStructureNotFound("arg_l[1] must be . or (")

        if class_or_var: # Rest of structure is subroutineName ( expressionList? )
            # arg_l[2] must be SubroutineName
            try:
                subroutine_name = SubroutineNameParse(*arg_l[2:])
            except ParsingStructureNotFound:
                raise ParsingStructureNotFound("*arg_l[2:] must make a valid subroutineName")
            arg_l[2:] = [subroutine_name] + arg_l[2+len(subroutine_name.objects):]
            self.objects.append(subroutine_name)

            # arg_l[3] must be (
            if isinstance(arg_l[3], Token) and arg_l[3].tokenType == "symbol" and arg_l[3].tokenValue == "(":
                self.objects.append(arg_l[3])
            else:
                raise ParsingStructureNotFound("*arg_l[3] must be symbol Token (")

            close_paren_index = 5 # If there is an expressionList, this is 5. Else, it's 4
            # arg_l[4] could be expressionList but this is optional
            try:
                expression_list = ExpressionListParse(*arg_l[4:])
                arg_l[4:] = [expression_list] + arg_l[4 + len(expression_list.objects):]
                self.objects.append(expression_list)
            except ParsingStructureNotFound:
                close_paren_index = 4

            # arg_l[close_paren_index] must be symbol token )
            if isinstance(arg_l[close_paren_index], Token) and arg_l[close_paren_index].tokenType == "symbol" and arg_l[close_paren_index].tokenValue == ")":
                self.objects.append(arg_l[close_paren_index])
            else:
                raise ParsingStructureNotFound(f"*arg_l[{close_paren_index}] must be symbol Token )")

        else: # Rest of structure is expressionList )
            close_paren_index = 3 # if there is an expressionList, this is 3. Else, it's 2
            # *arg[2:] could make a valid expressionList or it could be empty
            try:
                expression_list = ExpressionListParse(*arg_l[2:])
                arg_l[2:] = [expression_list] + arg_l[2+len(expression_list.objects):]
            except ParsingStructureNotFound:
                close_paren_index = 2

            # arg_l[3] must be symbol Token )
            if isinstance(arg_l[close_paren_index], Token) and arg_l[close_paren_index].tokenType == "symbol" and arg_l[close_paren_index].tokenValue == ")":
                self.objects.append(arg_l[close_paren_index])
            else: raise ParsingStructureNotFound(f"*arg_l[{close_paren_index}] must be symbol Token )")

class ExpressionListParse(Expression):
    parsing_structure_type = "expressionList"
    def __init__(self, *args):
        arg_l = []
        for arg in args:
            arg_l.append(arg)
        if not arg_l:
            raise ParsingStructureNotFound ("you didn't pass anything in")
        expression = False # is the previous object an expression?
        comma = True # Is the previous object a comma? Assume a starting comma so first expression can be treated same as any else
        self.objects = []
        for arg in arg_l:
            if arg is None:
                break
            if isinstance(arg, Token) and arg.tokenType == "symbol" and arg.tokenValue == "," and expression:
                expression = False
                comma = True
                self.objects.append(arg)
            elif comma:
                try:
                    expression_ob = ExpressionParse(arg)
                    expression = True
                    self.objects.append(expression_ob)
                except ParsingStructureNotFound:
                    pass
            elif expression: # so that this can accept trailing tokens
                break
            else:
                raise ParsingStructureNotFound("expressionList must be in the form of expression, expression, ...")
        if comma:
            raise ParsingStructureNotFound("expressionList shouldn't end with ,")

# subroutine_call_example = [
#     Token(21, 2, "identifier", "draw"), # <identifier> draw </identifier>
#     Token(21, 3, "symbol", "("), # <symbol> ( </symbol>
#     Token(21, 4, "symbol", ")"), # <symbol> ) </symbol>
#     ]
#
# print(ExpressionParse(*subroutine_call_example))

from ProgramStructureParseClasses import SubroutineNameParse, VarNameParse