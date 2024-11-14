from ProgramStructureParseClasses import ProgramStructure
from ParserClasses import Token

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
            if isinstance(arg, Token) and arg.tokenType == "symbol" and arg.tokenValue == ";" and var_dec and not semicolon:
                semicolon = True
                self.objects.append(arg)
            elif isinstance(arg, Token) and arg.tokenType == "symbol" and arg.tokenValue == "," and var_dec and not semicolon:
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