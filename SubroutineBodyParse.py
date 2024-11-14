from ProgramStructureParseClasses import ProgramStructure
from ParserClasses import Token
from StatementParse import StatementParse
from VarOrClassVarDecParse import VarDecParse, ClassVarDecParse

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