from ExpressionParseClasses import Expression
from ParserClasses import Token
from ExpressionListParse import ExpressionListParse

class SubroutineCallParse(Expression):
    parsing_structure_type = "subroutineCall"
    def __init__(self, *args):
        self.objects = []
        if isinstance(args[0], Token) and args[0].tokenType == "identifier":
            self.objects.append(args[0])
            expression = False # parse for expression list in here
            comma = True # parse for expression list in here
            if isinstance(args[1], Token) and args[1].tokenType == "symbol" and args[1].tokenValue == ".":
                self.objects.append(args[1])
                subroutine_name = False
                open_parenthesis = False
                close_parenthesis = False
                expression = False  # expression list checking
                comma = True  # expression list checking
                for arg in args[2:]:
                    if isinstance(arg,
                                  Token) and arg.tokenType == "identifier" and not subroutine_name and not open_parenthesis and not close_parenthesis:
                        subroutine_name = True
                        self.objects.append(arg)
                    elif isinstance(arg,
                                    Token) and arg.tokenType == "symbol" and arg.tokenValue == "(" and subroutine_name and not open_parenthesis and not close_parenthesis:
                        open_parenthesis = True
                        self.objects.append(arg)
                    elif subroutine_name and open_parenthesis and not close_parenthesis:
                        if isinstance(arg, Token) and arg.tokenType == "symbol" and arg.tokenValue == ")":
                            close_parenthesis = True
                            self.objects.append(arg)
                        elif isinstance(arg, Token) and (arg.tokenType == "identifier" or arg.tokenType == "keyword") and comma:
                            expression = True
                            comma = False
                            self.objects.append(arg)
                        elif isinstance(arg, Token) and arg.tokenType == "symbol" and arg.tokenValue == "," and expression:
                            expression = False
                            comma = True
                            self.objects.append(arg)
                        else:
                            raise ValueError("subroutine call must close its parentheses")
                    elif subroutine_name and open_parenthesis and close_parenthesis:
                        break  # so this can accept trailing tokens
                    else:
                        raise ValueError(
                            "If subroutine call starts with a class name or var name, it must be in the form of (className|varName) . subroutineName ( expressionList )")

            elif isinstance(args[1], Token) and args[1].tokenType == "symbol" and args[1].tokenValue == "(":
                close_parenthesis = False
                self.objects.append(args[1])
                for arg in args[2:]:
                    if not close_parenthesis:
                        if isinstance(arg, Token) and arg.tokenType == "symbol" and arg.tokenValue == ")":
                            close_parenthesis = True
                            self.objects.append(arg)
                        elif isinstance(arg, Token) and (arg.tokenType == "identifier" or arg.tokenType == "keyword") and comma:
                            expression = True
                            comma = False
                            self.objects.append(arg)
                        elif isinstance(arg, Token) and arg.tokenType == "symbol" and arg.tokenValue == "," and expression:
                            expression = False
                            comma = True
                            self.objects.append(arg)
                        else:
                            raise ValueError("subroutine call must close its parentheses")
                    elif close_parenthesis: # So that this can accept trailing tokens
                        break
                    else:
                        raise ValueError("If subroutine call starts with a subroutine name, it must be in the form of subroutineName ( expressionList ) ")
            else:
                raise ValueError("subroutine name should be followed by a ( or a .")
        else:
            raise ValueError ("Subroutine call must start with an identifier Token")
