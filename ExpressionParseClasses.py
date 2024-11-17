from ParserClasses import Token, ParsingStructure, ParsingStructureNotFound
from ProgramStructureParseClasses import SubroutineNameParse


# class list for import statements:
# ExpressionParse, TermParse, SubroutineCallParse, ExpressionListParse, OpParse, UnaryOpParse, KeywordConstantParse

class Expression(ParsingStructure):
    pass

class ExpressionParse(ParsingStructure):
    parsing_structure_type = "expression"
    # Placeholder - expressions are replaced with identifiers in the Expressionless versions of test files
    def __init__(self, *args): # args does nothing, just so it can accept trailing tokens
        if isinstance(args[0], Token) and args[0].tokenType == "identifier":
            self.objects = [args[0]]
        else:
            raise ParsingStructureNotFound("identifier must be an identifier Token")

class TermParse(Expression):
    parsing_structure_type = "term"
    # This one is the part that's not LL1

class OpParse(Expression):
    parsing_structure_type = "op"
    def __init__(self, op, *args): # args does nothing, this is so it can accept trailing tokens
        if op is Token and op.tokenType == "symbol" and op.tokenValue in ["+", "-", "*", "/", "&", "|", "<", ">", "="]:
            self.objects = [op]
        else:
            raise ValueError("op must be symbol Token + - * / & | < > =")

class UnaryOpParse(Expression):
    parsing_structure_type = "unaryOp"
    def __init__(self, op, *args): # args does nothing, this is so it can accept trailing tokens
        if op is Token and op.tokenType == "symbol" and op.tokenValue in ["-", "~"]:
            self.objects = op
        else:
            raise ValueError("Unary operator must be symbol Token - or ~")

class KeywordConstantParse(Expression):
    parsing_structure_type = "keywordConstant"
    def __init__(self, op, *args): # args does nothing, this is so it can accept trailing tokens
        if op is Token and op.tokenType == "keyword" and op.tokenValue in ["true", "false", "null", "this"]:
            self.objects = op
        else:
            raise ValueError("Keyword constant must be keyword Token true, false, null, this")

class SubroutineCallParse(Expression):
    parsing_structure_type = "subroutineCall"
    def __init__(self, *args):
        arg_l = []
        for arg in args:
            arg_l.append(arg)
        self.objects = []
        if isinstance(arg_l[0], Token) and arg_l[0].tokenType == "identifier":
            pass # we do not know if this is className or varName or subroutineName yet.
        else:
            raise ParsingStructureNotFound("arg_l[0] must be an identifier Token")

        class_or_var = False
        if isinstance(arg_l[1], Token) and arg_l[1].tokenType == "symbol" and arg_l[1].tokenValue == "(":
            self.objects.append(SubroutineNameParse(arg_l[0])) # Now we know that arg_l[0] is SubroutineName
            self.objects.append(arg_l[1])
            class_or_var = False
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
        if comma and self.objects != []:
            raise ParsingStructureNotFound("expressionList shouldn't end with ,")

subroutine_call_example = [
    Token(21, 2, "identifier", "draw"), # <identifier> draw </identifier>
    Token(21, 3, "symbol", "("), # <symbol> ( </symbol>
    Token(21, 4, "symbol", ")"), # <symbol> ) </symbol>
    ]

print(ExpressionParse(*subroutine_call_example))