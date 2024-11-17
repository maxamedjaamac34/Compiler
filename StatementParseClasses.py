from ParserClasses import ParsingStructure

# class list for import statements:
# StatementParse, StatementsParse

class Statement(ParsingStructure):
    pass # statements, statement, letStatement, ifStatement, whileStatement, doStatement, returnStatement

class StatementParse(Statement):
    parsing_structure_type = "statement"
    def __init__(self, statement, *args):
        # *args lets it take trailing tokens
        if isinstance(statement, LetStatementParse) or isinstance(statement, IfStatementParse) or isinstance(statement, WhileStatementParse) or isinstance(statement, DoStatementParse) or isinstance(statement, ReturnStatementParse):
            self.objects = [statement]
        else:
            raise ValueError("statement should be a letStatement, ifStatement, whileStatement, doStatement, or returnStatement")

class StatementsParse(ParsingStructure):
    parsing_structure_type = "statements"
    def __init__(self, *args):
        self.objects = []
        for arg in args:
            if isinstance(arg, StatementParse):
                self.objects.append(arg)
            else:
                break # This one is special because it could have nothing at all, returning an empty list for objects

from LetIfWhileDoReturn import LetStatementParse, IfStatementParse, WhileStatementParse, DoStatementParse, ReturnStatementParse