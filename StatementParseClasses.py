from ParserClasses import ParsingStructure, ParsingStructureNotFound


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
        arg_l = list(args)
        self.objects = []
        for i in range(len(arg_l)):
            try:
                statement = StatementParse(*arg_l[i:])
                self.objects.append(statement)
                arg_l[i:] = [statement] + arg_l[len(statement.objects)+i:]
            except ParsingStructureNotFound:
                break

from LetIfWhileDoReturn import LetStatementParse, IfStatementParse, WhileStatementParse, DoStatementParse, ReturnStatementParse