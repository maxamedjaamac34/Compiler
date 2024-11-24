from ParserClasses import ParsingStructure, Token, ParsingStructureNotFound


# class list for import statements
# ClassParse, ClassVarDecParse, TypeParse, SubroutineDecParse, ParameterListParse, SubroutineNameParse, VarDecParse, VarNameParse

class ProgramStructure(ParsingStructure):  # ParsingStructures of Program Structures
    # class, classVarDec, type, subroutineDec, parameterList, subroutineBody, varDec, className, subroutineName, varName
    pass

class ClassParse(ProgramStructure):
    def __init__(self, class_keyword, class_name, open_brace, *args):
        # class is the only parsing structure that does NOT accept trailing tokens because each file should be only one class
        if not (isinstance(class_keyword, Token) and class_keyword.tokenType == "keyword" and class_keyword.tokenValue == "class"):
            raise ValueError("class_keyword must be the keyword Token 'class'")
        if not (isinstance(class_name, Token) and class_name.tokenType == "identifier"):
            raise ValueError("class_name must be a ClassNameParse object")
        if not (isinstance(open_brace, Token) and open_brace.tokenType == "symbol" and open_brace.tokenValue == "{"):
            raise ValueError("open_brace must be the symbol token {")
        self.objects = [class_keyword, class_name, open_brace]
        subroutine_decs = False # whether subroutines have already been detected
        close_brace = False # whether a close brace has already been detected
        for arg in args:
            if arg is ClassVarDecParse and not subroutine_decs and not close_brace:
                self.objects.append(arg)
            elif arg is SubroutineDecParse and not close_brace:
                subroutine_decs = True
                self.objects.append(arg)
            elif arg is Token and arg.tokenType == "symbol" and arg.tokenValue == "}" and not close_brace:
                close_brace = True
                self.objects.append(arg)
            else:
                raise ValueError("classes are in the format of class className {classVarDecs*, subroutineDecs*}")
        if not close_brace:
            raise ValueError("Class must end with }")

class ParameterListParse(ProgramStructure):
    parsing_structure_type = "parameterList"
    def __init__(self, *args):
        # This checks if the arguments are in (,type varName) order (but no starting comma)
        self.objects = []
        parameter_type = False
        var_dec = False
        comma = False #changed this to false as Iam assuming that no comma is needed for the first parameter
        valid_types = ["int", "char", "boolean"] #declaring the valid types that we need for Parameter List
        # so that both the starting parameter and the rest can be processed the same
        for arg in args:
            if isinstance(arg, Token) and arg.tokenType == "symbol" and arg.tokenValue == "," and not comma and not parameter_type and var_dec:
                var_dec = False
                comma = True
                self.objects.append(arg)
            elif isinstance(arg, Token) and arg.tokenType == "identifier" and comma and not parameter_type and not var_dec:
                comma = False
                parameter_type = True
                self.objects.append(arg)
            elif isinstance(arg, Token) and arg.tokenType == "keyword" and  arg.tokenValue in valid_types:
                comma = False
                parameter_type = True
                self.objects.append(arg)
            elif isinstance(arg, Token) and arg.tokenType == "identifier" and not comma and parameter_type and not var_dec:
                parameter_type = False
                var_dec = True
                self.objects.append(arg)
            elif var_dec:
                break # to accept trailing tokens
            else:
                raise ParsingStructureNotFound("*args must be comma symbol Token, TypeParse, and VarNameParse alternating")

class SubroutineBodyParse(ProgramStructure):
    parsing_structure_type = "subroutineBody"
    def __init__(self, start_brace, *args):
        if not (isinstance(start_brace, Token) and start_brace.tokenType == "symbol" and start_brace.tokenValue == "{"):
            # print(start_brace)
            raise ValueError("Subroutine body must start with symbol token {")
        end_brace = False # whether an end brace has been given
        self.objects = [start_brace]
        # print(self.objects)
        for arg in args:
            if isinstance(arg, Token) and arg.tokenType == "symbol" and arg.tokenValue == "}" and not end_brace:
                end_brace = True
                self.objects.append(arg)
            elif isinstance(arg, StatementParse) and not end_brace:
                self.objects.append(arg)
            elif (isinstance(arg, VarDecParse) or isinstance(arg, ClassVarDecParse)) and not end_brace:
                self.objects.append(arg)
            elif end_brace:
                break # to accept trailing tokens
            else:
                #print("could not make subroutine body")
                #print(str(arg))
                raise ValueError("Subroutine body must be {varDec* statement*}")
        if not end_brace:
            raise ValueError("Subroutine body must end with }")

class SubroutineDecParse(ProgramStructure):
    parsing_structure_type = "subroutineDec"
    def __init__(self, subroutine, void_or_type, subroutine_name, open_parenthesis, *args):
        # args does nothing, this is so it accepts trailing tokens
        if not (isinstance(subroutine, Token) and subroutine.tokenType == "keyword" and subroutine.tokenValue in ["constructor", "function", "method"]):
            raise ValueError("Subroutine must be the keyword constructor, function, or method")
        if not (isinstance(void_or_type, Token) and (void_or_type.tokenType == "keyword" and void_or_type.tokenValue == "void") or void_or_type.tokenType == "identifier"):
            raise ValueError("void_or_type must be the keyword token void or a type")
        if not (isinstance(subroutine_name, Token) and subroutine_name.tokenType == "identifier"):
            raise ValueError("subroutine_name must be a SubroutineNameParse object")
        if not (isinstance(open_parenthesis,Token) and open_parenthesis.tokenType == "symbol" and open_parenthesis.tokenValue == "("):
            raise ValueError("open_parenthesis must be symbol Token '('")
        self.objects = [subroutine, void_or_type, subroutine_name, open_parenthesis]
        close_parenthesis = False # whether there has been a close parenthesis or not
        subroutine_body = False # whether there has been a subroutineBody or not
        for arg in args:
            if isinstance(arg, ParameterListParse) and not close_parenthesis and not subroutine_body:
                self.objects.append(arg)
            elif isinstance(arg, Token) and arg.tokenType == "symbol" and arg.tokenValue == ")":
                close_parenthesis = True
                self.objects.append(arg)
            elif isinstance(arg, SubroutineBodyParse) and close_parenthesis and not subroutine_body:
                subroutine_body = True
                self.objects.append(arg)
            elif close_parenthesis and subroutine_body:
                break
            else:
                raise ValueError("args must be ) parameterList? subroutineBody")

class SubroutineNameParse(ProgramStructure):
    parsing_structure_type = "subroutineName"
    def __init__(self, *args):
        # args does nothing, this is so it accepts trailing tokens
        arg_l = []
        for arg in args:
            arg_l.append(arg)
        if arg_l[0].tokenType != "identifier":
            raise ParsingStructureNotFound("subroutineName's identifier must be an identifier")
        self.objects = [arg_l[0]]

class TypeParse(ProgramStructure):
    parsing_structure_type = "type"
    def __init__(self, type_name, *args):
        # args does nothing, this is so it accepts trailing tokens
        if type_name is Token:
            if type_name.tokenType == "identifier":
                self.objects = [type_name]
            if type_name.tokenType != "keyword":
                raise ValueError("type must be a keyword if it is a Token")
            if type_name.tokenValue != ("int" or "char" or "boolean"):
                raise ValueError("type must be 'int', 'char', or 'boolean' if it is a keyword Token")
            else:
                self.objects = [type_name]
        else:
            raise ValueError("type must be either a Token or a ClassNameParse")

class VarNameParse(ProgramStructure):
    parsing_structure_type = "varName"
    def __init__(self, *args):
        arg_l = list(args)
        if isinstance(arg_l[0], Token) and arg_l[0].tokenType == "identifier":
            self.objects = [arg_l[0]]
        else:
            raise ParsingStructureNotFound("first argument must be an identifier Token")

class VarOrClassVarDecParse(ProgramStructure):
    # Super class to VarDecParse and ClassVarDecParse because they are almost exactly the same
    def __init__(self, var, type_name, var_name, var_or_class_var, *args):
        # Pass in the semicolon before the other optional var declarations
        if var_or_class_var == "var":
            var_check = ["var"]
        else:
            var_check = ["static", "field"]
        if isinstance(var, Token) and not (var.tokenValue in var_check and var.tokenType == "keyword"):
            raise ValueError(f"var must be a keyword whose value is in {var_check}")
        if not (isinstance(type_name, Token) and (type_name.tokenType == "identifier" or type_name.tokenType == "keyword")):
            raise ValueError("type_name must be a identifier or keyword")
        if not (isinstance(var_name, Token) and var_name.tokenType == "identifier"):
            raise ValueError("var_name must be a identifier")
        self.objects = [var, type_name, var_name]
        var_dec = True # Whether the last token at the time of evaluating was a VarName
        comma = False # Whether the last token at the time of evaluating was a comma symbol Token
        semicolon = False # Whether the last token at the time of evaluating was a semicolon symbol Token
        for arg in args:
            if isinstance(arg, Token) and arg.tokenType == "symbol" and arg.tokenValue == "," and not semicolon:
                comma = True
                var_dec = False
                self.objects.append(arg)
            elif isinstance(arg, Token) and arg.tokenType == "identifier" and comma and not semicolon:
                var_dec = True
                comma = False
                self.objects.append(arg)
            elif semicolon:
                break # to accept trailing tokens
            else:
                #print(str(self))
                #print(arg.tokenType)
                #print(arg.tokenValue)
                raise ValueError("*args must be comma symbol Token and varNameParse alternating, ending with a semicolon")
        if not semicolon:
            raise ValueError("*args must end with a semicolon Token")

class VarDecParse(VarOrClassVarDecParse):
    parsing_structure_type = "varDec"
    def __init__(self, var, type_name, var_name, *args):
        super().__init__(var, type_name, var_name, "var", *args)

class ClassVarDecParse(VarOrClassVarDecParse):
    parsing_structure_type = "classVarDec"
    def __init__(self, var: Token, type_name, var_name, *args):
        super().__init__(var, type_name, var_name, "class_var", *args)

class ClassNameParse(ProgramStructure):
    parsing_structure_type = "className"
    def __init__(self, identifier: Token, *args):
        # args does nothing, this is so it accepts trailing tokens
        if identifier.tokenType != "identifier":
            raise ValueError("className's identifier must be an identifier")
        self.objects = [identifier]

from StatementParseClasses import StatementParse
from ExpressionParseClasses import TermParse


term_example = [
    Token(21, 1, "symbol", "["), # <symbol> [ </symbol>
    Token(21, 2, "identifier", "x"), # <identifier> x </identifier>
    Token(21, 3, "symbol", "<",), # <symbol> < </symbol>
    Token(21, 5, "symbol", "4"), # <integer> 5 </integer>
    Token(21, 5, "symbol", ";"), # <symbol> ; </symbol>
]

print(TermParse(*term_example))