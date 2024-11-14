from ProgramStructureParseClasses import ProgramStructure
from ParserClasses import Token
from StatementParse import StatementParse
from VarOrClassVarDecParse import VarDecParse, ClassVarDecParse

class SubroutineBodyParse(ProgramStructure):
    parsing_structure_type = "subroutineBody"
    def __init__(self, *args):
        
        statements = False # whether a statements object has been given (can no longer give more var decs
        end_brace = False
        #start_brace = False # whether an end brace has been given,, not sure if we need this
        self.objects = []
        
        for arg in args:

            if (isinstance(arg, Token) and arg.tokenType == "symbol" and arg.tokenValue == "{"):
                #start_brace = True
                self.objects.append(arg)

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
                raise ValueError("Subroutine body must be {varDec* statement*}")
        if not end_brace:
            raise ValueError("Subroutine body must end with }")
        if not statements:
            raise ValueError("Subroutine body must have statements")