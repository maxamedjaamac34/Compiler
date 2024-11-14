from StatementParseClasses import Statement

class StatementParse(Statement):
    parsing_structure_type = "statement"
    def __init__(self, statement, *args):
        # *args lets it take trailing tokens
        if isinstance(statement, LetStatementParse) or isinstance(statement, IfStatementParse) or isinstance(statement, WhileStatementParse) or isinstance(statement, DoStatementParse) or isinstance(statement, ReturnStatementParse):
            self.objects = [statement]
        else:
            raise ValueError("statement should be a letStatement, ifStatement, whileStatement, doStatement, or returnStatement")

from LetStatementParse import LetStatementParse
from IfStatementParse import IfStatementParse
from WhileStatementParse import WhileStatementParse
from DoStatementParse import DoStatementParse
from ReturnStatementParse import ReturnStatementParse