from StatementParseClasses import Statement
from ParserClasses import ParsingStructure

class StatementsParse(ParsingStructure):
    parsing_structure_type = "statements"
    def __init__(self, *args):
        self.objects = []
        for arg in args:
            if isinstance(arg, StatementParse):
                self.objects.append(arg)
            else:
                break # This one is special because it could have nothing at all, returning an empty list for objects

from StatementParse import StatementParse