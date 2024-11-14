from ProgramStructureParseClasses import ProgramStructure
from ParserClasses import Token

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
                raise ValueError("*args must be comma symbol Token, TypeParse, and VarNameParse alternating")