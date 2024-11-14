from ParserClasses import Token, ParsingStructure

# class list for import statements:
# ExpressionParse, TermParse, SubroutineCallParse, ExpressionListParse, OpParse, UnaryOpParse, KeywordConstantParse

class Expression(ParsingStructure):
    pass

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