from ExpressionParseClasses import Expression
from ParserClasses import Token, ParsingStructure

class ExpressionParse(ParsingStructure):
    parsing_structure_type = "expression"
    # Placeholder - expressions are replaced with identifiers in the Expressionless versions of test files
    def __init__(self, identifier, *args): # args does nothing, just so it can accept trailing tokens
        if isinstance(identifier, Token) and identifier.tokenType == "identifier":
            self.objects = [identifier]
        else:
            raise ValueError("identifier must be an identifier Token")
