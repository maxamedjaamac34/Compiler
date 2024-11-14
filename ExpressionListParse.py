from ExpressionParseClasses import Expression
from ParserClasses import Token

class ExpressionListParse(Expression):
    parsing_structure_type = "expressionList"
    def __init__(self, *args):
        expression = False # is the previous object an expression?
        comma = True # Is the previous object a comma? Assume a starting comma so first expression can be treated same as any else
        self.objects = []
        for arg in args:
            if arg is None:
                break
            if isinstance(arg, Token) and arg.tokenType == "symbol" and arg.tokenValue == "," and expression:
                expression = False
                comma = True
                self.objects.append(arg)
            elif isinstance(arg, Token) and arg.tokenType == "identifier" and comma:
                comma = False
                expression = True
                self.objects.append(arg)
            elif expression: # so that this can accept trailing tokens
                break
            else:
                raise ValueError("expressionList must be in the form of expression, expression, ...")
        if comma:
            raise ValueError("expressionList shouldn't end with ,")