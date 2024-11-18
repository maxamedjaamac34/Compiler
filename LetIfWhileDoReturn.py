from ParserClasses import Token, ParsingStructureNotFound
from StatementParseClasses import Statement
from ExpressionParseClasses import SubroutineCallParse, ExpressionParse










from StatementParseClasses import StatementsParse
from ExpressionParseClasses import SubroutineCallParse

do_statement_example = [
    Token(21, 1, "keyword", "do"), # <keyword> do </keyword>
    Token(21, 2, "identifier", "draw"), # <identifier> draw </identifier>
    Token(21, 3, "symbol", "("), # <symbol> ( </symbol>
    Token(21, 4, "symbol", ")"), # <symbol> ) </symbol>
    Token(21, 5, "symbol", ";"), # <symbol> ; </symbol>
]

return_statement_example = [
    Token(1,1,"keyword", "return"),
    Token(1,1,"identifier", "x"),
    Token(1,1,"symbol", ";"),
]

