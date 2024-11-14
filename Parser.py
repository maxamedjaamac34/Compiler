from SubroutineBodyParse import SubroutineBodyParse
from ParserClasses import Token
from ClassParse import ClassParse
from VarOrClassVarDecParse import VarDecParse
from ParameterListParse import ParameterListParse
from IfStatementParse import IfStatementParse
from LetStatementParse import LetStatementParse
from ReturnStatementParse import ReturnStatementParse
from WhileStatementParse import WhileStatementParse
from DoStatementParse import DoStatementParse
from SubroutineDecParse import SubroutineDecParse
from VarOrClassVarDecParse import ClassVarDecParse
from SubroutineCallParse import SubroutineCallParse
from ExpressionListParse import ExpressionListParse
from StatementParse import StatementParse
from StatementsParse import StatementsParse
from ExpressionParse import ExpressionParse

# try/except statements galore

# This could be repetitive so let's make a function that does the trying
# try_parse tries to parse a class with any number of positional arguments
# It inputs every list objects[0:], objects[1:], objects[2:]...
# The class should return errors if there is not a valid parsing structure of that type at the front of the list, but will accept trailing tokens
# And the class has a self.objects list item, here called matched.objects
# This specification works with every ParsingStructure class except for ClassParse, which will be handled separately
# If it works for a given sublist, replace the elements of objects that match with matched.objects with matched, and break the for loop
# If it doesn't work in the for loop, pass. If no list works, just return objects
def try_parse(parse_class, objects: list, print_try_progress):
    # print_try_progress is true if you want to print progress, false otherwise
    for l in range(len(objects)):
        try:
            parse_objects = objects[l:]
            matched = parse_class(*parse_objects)
            if print_try_progress:
                print(f"{parse_class} object found at index {l}")
            for i in matched.objects: # Removes the first instance of each object in matched.objects from objects
                # If the classes were written correctly, this should just be removing stuff from the start of the list
                for j in parse_objects:
                    if i == j:
                        parse_objects.remove(j)
                        break
            if not (isinstance(matched, StatementsParse) and matched.objects == []):
                objects = objects[:l] + parse_objects
                objects.insert(l, matched) # Adds the instance of parse_class that matched refers to, to the front of the list
                if isinstance(matched, StatementParse):
                    continue
                else:
                    break
        except (ValueError, TypeError) as e:
            # Specific handling for ValueError and TypeError
            if print_try_progress:
                print(f"Parsing failed for {parse_class} at index {l}: {e}")
            pass
        except Exception as e:
            # Catch-all for any other exceptions
            if print_try_progress:
                print(f"Unexpected error for {parse_class} at index {l}: {e}")
            pass
    return objects

# Put it all together now
def parse_jack_class(tokens: list, print_parse_progress):
    # print_parse_progress is true if you want to print parse progress, false otherwise
    class_fully_parsed = False
    class_objects = tokens
    parsing_structures = [
        SubroutineBodyParse,
        SubroutineDecParse,
        ParameterListParse,
        VarDecParse,
        ClassVarDecParse,
        StatementParse,
        LetStatementParse,
        DoStatementParse,
        ReturnStatementParse,
        IfStatementParse,
        WhileStatementParse,
        SubroutineCallParse, # If not empty, requires type varName (, type varname)* ;

        # ExpressionListParse, # If not empty, requires expression (, expression)*
        # ExpressionParse, # Placeholder is trivial - only an identifier
        # SubroutineNameParse, # Trivial - only an identifier
        # TypeParse, # Trivial - only an identifier
        # VarNameParse, # Trivial - only an identifier
        # ClassNameParse, # Trivial - only an identifier
        # StatementsParse, # Trivial - will take any args and never raise an error (if it doesn't start with Statements, return empty list)
        # but that sort of trivial does not break try_parse
    ]

    for i in range(1000):
        try:
            if print_parse_progress:
                print("Trying to parse the class")
            class_parsed = ClassParse(*class_objects)
            class_fully_parsed = True
            print("huzzah! the class parsed!")
            print(str(class_parsed))
            return class_parsed
        except ValueError:
            for i in parsing_structures:
                if print_parse_progress:
                    print(f"Trying to make parsing structure {i} from current class_objects list")
                class_objects = try_parse(i, class_objects, print_parse_progress)
    for j in class_objects:
        print(str(j))


square_tokens = [
    Token(1,1,"keyword", "class"), # <keyword> class </keyword>
    Token(1, 2, "identifier", "Square"), # <identifier> Square </identifier>
    Token(1, 3, "symbol", "{"), # <symbol> { </symbol>
    Token(1, 4, "keyword", "field"), # <keyword> field </keyword>
    Token(1, 5, "keyword", "int"), # <keyword> int </keyword>
    Token(1, 6, "identifier", "x"), # <identifier> x </identifier>
    Token(1,1, "symbol", ","),
    Token(1,1, "identifier", "t"),
    Token(1, 7, "symbol", ","), # <symbol> , </symbol>
    Token(1, 8, "identifier", "y"), # <identifier> y </identifier>
    Token(1, 9, "symbol", ";"), # <symbol> ; </symbol>
    Token(2, 1, "keyword", "field"), # <keyword> field </keyword>
    Token(2, 2, "keyword", "int"), # <keyword> int </keyword>
    Token(2, 3, "identifier", "size"), # <identifier> size </identifier>
    Token(2, 4, "symbol", ";"), # <symbol> ; </symbol>
    Token(2, 5, "keyword", "constructor"), # <keyword> constructor </keyword>
    Token(2, 6, "identifier", "Square"), # <identifier> Square </identifier>
    Token(2, 7, "identifier", "new"), # <identifier> new </identifier>
    Token(2, 8, "symbol", "("), # <symbol> ( </symbol>
    Token(2, 9, "keyword", "int"), # <keyword> int </keyword>
    Token(3, 1, "identifier", "Ax"), # <identifier> Ax </identifier>
    Token(3, 2, "symbol", ","), # <symbol> , </symbol>
    Token(3, 3, "keyword", "int"), # <keyword> int </keyword>
    Token(3, 4, "identifier", "Ay"), # <identifier> Ay </identifier>
    Token(3, 5, "symbol", ","), # <symbol> , </symbol>
    Token(3, 6, "keyword", "int"), # <keyword> int </keyword>
    Token(3, 7, "identifier", "Asize"), # <identifier> Asize </identifier>
    Token(3, 8, "symbol", ")"), # <symbol> ) </symbol>
    Token(3, 9, "symbol", "{"), # <symbol> { </symbol>
    Token(4, 1, "keyword", "let"), # <keyword> let </keyword>
    Token(4, 2, "identifier", "x"), # <identifier> x </identifier>
    Token(4, 3, "symbol", "="), # <symbol> = </symbol>
    Token(4, 4, "identifier", "Ax"), # <identifier> Ax </identifier>
    Token(4, 5, "symbol", ";"), # <symbol> ; </symbol>
    Token(4, 6, "keyword", "let"), # <keyword> let </keyword>
    Token(4, 7, "identifier", "y"), # <identifier> y </identifier>
    Token(4, 8, "symbol", "="), # <symbol> = </symbol>
    Token(4, 9, "identifier", "Ay"), # <identifier> Ay </identifier>
    Token(5, 1, "symbol", ";"), # <symbol> ; </symbol>
    Token(5, 2, "keyword", "let"), # <keyword> let </keyword>
    Token(5, 3, "identifier", "size"), # <identifier> size </identifier>
    Token(5, 4, "symbol", "="), # <symbol> = </symbol>
    Token(5, 5, "identifier", "Asize"), # <identifier> Asize </identifier>
    Token(5, 6, "symbol", ";"), # <symbol> ; </symbol>
    Token(5, 7, "keyword", "do"), # <keyword> do </keyword>
    Token(5, 8, "identifier", "draw"), # <identifier> draw </identifier>
    Token(5, 9, "symbol", "("), # <symbol> ( </symbol>
    Token(6, 1, "symbol", ")"), # <symbol> ) </symbol>
    Token(6, 2, "symbol", ";"), # <symbol> ; </symbol>
    Token(6, 3, "keyword", "return"), # <keyword> return </keyword>
    Token(6, 4, "identifier", "x"), # <identifier> x </identifier>
    Token(6, 5, "symbol", ";"), # <symbol> ; </symbol>
    Token(6, 6, "symbol", "}"), # <symbol> } </symbol>
    Token(6, 7, "keyword", "method"), # <keyword> method </keyword>
    Token(6, 8, "keyword", "void"), # <keyword> void </keyword>
    Token(6, 9, "identifier", "dispose"), # <identifier> dispose </identifier>
    Token(7, 1, "symbol", "("), # <symbol> ( </symbol>
    Token(7, 1, "symbol", ")"), # <symbol> ) </symbol>
    Token(7, 2, "symbol", "{"), # <symbol> { </symbol>
    Token(7, 3, "keyword", "do"), # <keyword> do </keyword>
    Token(7, 4, "identifier", "Memory"), # <identifier> Memory </identifier>
    Token(7, 5, "symbol", "."), # <symbol> . </symbol>
    Token(7, 6, "identifier", "deAlloc"), # <identifier> deAlloc </identifier>
    Token(7, 7, "symbol", "("), # <symbol> ( </symbol>
    Token(7, 8, "keyword", "this"), # <keyword> this </keyword>
    Token(7, 9, "symbol", ")"), # <symbol> ) </symbol>
    Token(8, 1, "symbol", ";"), # <symbol> ; </symbol>
    Token(8, 2, "keyword", "return"), # <keyword> return </keyword>
    Token(8, 3, "symbol", ";"), # <symbol> ; </symbol>
    Token(8, 4, "symbol", "}"), # <symbol> } </symbol>
    Token(8, 5, "keyword", "method"), # <keyword> method </keyword>
    Token(8, 6, "keyword", "void"), # <keyword> void </keyword>
    Token(8, 7, "identifier", "draw"), # <identifier> draw </identifier>
    Token(8, 8, "symbol", "("), # <symbol> ( </symbol>
    Token(8, 9, "symbol", ")"), # <symbol> ) </symbol>
    Token(9, 1, "symbol", "{"), # <symbol> { </symbol>
    Token(9, 2, "keyword", "do"), # <keyword> do </keyword>
    Token(9, 3, "identifier", "Screen"), # <identifier> Screen </identifier>
    Token(9, 4, "symbol", "."), # <symbol> . </symbol>
    Token(9, 5, "identifier", "setColor"), # <identifier> setColor </identifier>
    Token(9, 6, "symbol", "("), # <symbol> ( </symbol>
    Token(9, 7, "identifier", "x"), # <identifier> x </identifier>
    Token(9, 8, "symbol", ")"), # <symbol> ) </symbol>
    Token(9, 9, "symbol", ";"), # <symbol> ; </symbol>
    Token(10, 1, "keyword", "do"), # <keyword> do </keyword>
    Token(10, 2, "identifier", "Screen"), # <identifier> Screen </identifier>
    Token(10, 3, "symbol", "."), # <symbol> . </symbol>
    Token(10, 4, "identifier", "drawRectangle"), # <identifier> drawRectangle </identifier>
    Token(10, 5, "symbol", "("), # <symbol> ( </symbol>
    Token(10, 6, "identifier", "x"), # <identifier> x </identifier>
    Token(10, 7, "symbol", ","), # <symbol> , </symbol>
    Token(10, 9, "identifier", "y"), # <identifier> y </identifier>
    Token(10, 9, "symbol", ","), # <symbol> , </symbol>
    Token(11, 1, "identifier", "x"), # <identifier> x </identifier>
    Token(11, 2, "symbol", ","), # <symbol> , </symbol>
    Token(11, 3, "identifier", "y"), # <identifier> y </identifier>
    Token(11, 4, "symbol", ")"), # <symbol> ) </symbol>
    Token(11, 5, "symbol", ";"), # <symbol> ; </symbol>
    Token(11, 6, "keyword", "return"), # <keyword> return </keyword>
    Token(11, 7, "symbol", ";"), # <symbol> ; </symbol>
    Token(11, 8, "symbol", "}"), # <symbol> } </symbol>
    Token(11, 9, "keyword", "method"), # <keyword> method </keyword>
    Token(12, 1, "keyword", "void"), # <keyword> void </keyword>
    Token(12, 2, "identifier", "erase"), # <identifier> erase </identifier>
    Token(12, 3, "symbol", "("), # <symbol> ( </symbol>
    Token(12, 4, "symbol", ")"), # <symbol> ) </symbol>
    Token(12, 5, "symbol", "{"), # <symbol> { </symbol>
    Token(12, 6, "keyword", "do"), # <keyword> do </keyword>
    Token(12, 7, "identifier", "Screen"), # <identifier> Screen </identifier>
    Token(12, 9, "symbol", "."), # <symbol> . </symbol>
    Token(12, 9, "identifier", "setColor"), # <identifier> setColor </identifier>
    Token(13, 1, "symbol", "("), # <symbol> ( </symbol>
    Token(13, 2, "identifier", "x"), # <identifier> x </identifier>
    Token(13, 3, "symbol", ")"), # <symbol> ) </symbol>
    Token(13, 4, "symbol", ";"), # <symbol> ; </symbol>
    Token(13, 5, "keyword", "do"), # <keyword> do </keyword>
    Token(13, 6, "identifier", "Screen"), # <identifier> Screen </identifier>
    Token(13, 7, "symbol", "."), # <symbol> . </symbol>
    Token(13, 8, "identifier", "drawRectangle"), # <identifier> drawRectangle </identifier>
    Token(13, 9, "symbol", "("), # <symbol> ( </symbol>
    Token(14, 1, "identifier", "x"), # <identifier> x </identifier>
    Token(14, 2, "symbol", ","), # <symbol> , </symbol>
    Token(14, 3, "identifier", "y"), # <identifier> y </identifier>
    Token(14, 4, "symbol", ","), # <symbol> , </symbol>
    Token(14, 5, "identifier", "x"), # <identifier> x </identifier>
    Token(14, 6, "symbol", ","), # <symbol> , </symbol>
    Token(14, 7, "identifier","y"), # <identifier> y </identifier>
    Token(14, 9, "symbol", ")"), # <symbol> ) </symbol>
    Token(14, 9, "symbol", ";"), # <symbol> ; </symbol>
    Token(15, 1, "keyword", "return"), # <keyword> return </keyword>
    Token(15, 2, "symbol", ";"), # <symbol> ; </symbol>
    Token(15, 3, "symbol", "}"), # <symbol> } </symbol>
    Token(15, 4, "keyword", "method"), # <keyword> method </keyword>
    Token(15, 5, "keyword", "void"), # <keyword> void </keyword>
    Token(15, 6, "identifier", "incSize"), # <identifier> incSize </identifier>
    Token(15, 7, "symbol", "("), # <symbol> ( </symbol>
    Token(15, 8, "symbol", ")"), # <symbol> ) </symbol>
    Token(15, 9, "symbol", "{"), # <symbol> { </symbol>
    Token(16, 1, "keyword", "if"), # <keyword> if </keyword>
    Token(16, 2, "symbol", "("), # <symbol> ( </symbol>
    Token(16, 3, "identifier", "x"), # <identifier> x </identifier>
    Token(16, 4, "symbol", ")"), # <symbol> ) </symbol>
    Token(16, 5, "symbol", "{"), # <symbol> { </symbol>
    Token(16, 6, "keyword", "do"), # <keyword> do </keyword>
    Token(16, 7, "identifier", "erase"), # <identifier> erase </identifier>
    Token(16, 9, "symbol", "("), # <symbol> ( </symbol>
    Token(16, 9, "symbol", ")"), # <symbol> ) </symbol>
    Token(17, 1, "symbol", ";"), # <symbol> ; </symbol>
    Token(17, 2, "keyword", "let"), # <keyword> let </keyword>
    Token(17, 3, "identifier", "size"), # <identifier> size </identifier>
    Token(17, 4, "symbol", "="), # <symbol> = </symbol>
    Token(17, 5, "identifier", "size"), # <identifier> size </identifier>
    Token(17, 6, "symbol", ";"), # <symbol> ; </symbol>
    Token(17, 7, "keyword", "do"), # <keyword> do </keyword>
    Token(17, 8, "identifier", "draw"), # <identifier> draw </identifier>
    Token(17, 9, "symbol", "("), # <symbol> ( </symbol>
    Token(18, 1, "symbol", ")"), # <symbol> ) </symbol>
    Token(18, 2, "symbol", ";"), # <symbol> ; </symbol>
    Token(18, 3, "symbol", "}"), # <symbol> } </symbol>
    Token(18, 4, "keyword", "return"), # <keyword> return </keyword>
    Token(18, 5, "symbol", ";"), # <symbol> ; </symbol>
    Token(18, 6, "symbol", "}"), # <symbol> } </symbol>
    Token(18, 7, "keyword", "method"), # <keyword> method </keyword>
    Token(18, 9, "keyword", "void"), # <keyword> void </keyword>
    Token(18, 10, "identifier", "decSize"), # <identifier> decSize </identifier>
    Token(19, 1, "symbol", "("), # <symbol> ( </symbol>
    Token(19, 2, "symbol", ")"), # <symbol> ) </symbol>
    Token(19, 3, "symbol", "{"), # <symbol> { </symbol>
    Token(19, 4, "keyword", "if"), # <keyword> if </keyword>
    Token(19, 5, "symbol", "("), # <symbol> ( </symbol>
    Token(19, 6, "identifier", "size"), # <identifier> size </identifier>
    Token(19, 7, "symbol", ")"), # <symbol> ) </symbol>
    Token(19, 8, "symbol", "{"), # <symbol> { </symbol>
    Token(19, 9, "keyword", "do"), # <keyword> do </keyword>
    Token(20, 1, "identifier", "erase"), # <identifier> erase </identifier>
    Token(20, 2, "symbol", "("), # <symbol> ( </symbol>
    Token(20, 3, "symbol", ")"), # <symbol> ) </symbol>
    Token(20, 4, "symbol", ";"), # <symbol> ; </symbol>
    Token(20, 5, "keyword", "let"), # <keyword> let </keyword>
    Token(20, 6, "identifier", "size"), # <identifier> size </identifier>
    Token(20, 7, "symbol", "="), # <symbol> = </symbol>
    Token(20, 9, "identifier", "size"), # <identifier> size </identifier>
    Token(20, 10, "symbol", ";"), # <symbol> ; </symbol>
    Token(21, 1, "keyword", "do"), # <keyword> do </keyword>
    Token(21, 2, "identifier", "draw"), # <identifier> draw </identifier>
    Token(21, 3, "symbol", "("), # <symbol> ( </symbol>
    Token(21, 4, "symbol", ")"), # <symbol> ) </symbol>
    Token(21, 5, "symbol", ";"), # <symbol> ; </symbol>
    Token(21, 6, "symbol", "}"), # <symbol> } </symbol>
    Token(21, 7, "keyword", "return"), # <keyword> return </keyword>
    Token(21, 8, "symbol", ";"), # <symbol> ; </symbol>
    Token(21, 9, "symbol", "}"), # <symbol> } </symbol>
    Token(22, 1, "keyword", "method"), # <keyword> method </keyword>
    Token(22, 2, "keyword", "void"), # <keyword> void </keyword>
    Token(22, 3, "identifier", "moveUp"), # <identifier> moveUp </identifier>
    Token(22, 4, "symbol", "("), # <symbol> ( </symbol>
    Token(22, 5, "symbol", ")"), # <symbol> ) </symbol>
    Token(22, 6, "symbol", "{"), # <symbol> { </symbol>
    Token(22, 7, "keyword", "if"), # <keyword> if </keyword>
    Token(22, 9, "symbol", "("), # <symbol> ( </symbol>
    Token(22, 1, "identifier", "y"), # <identifier> y </identifier>
    Token(23, 1, "symbol", ")"), # <symbol> ) </symbol>
    Token(23, 2, "symbol", "{"), # <symbol> { </symbol>
    Token(23, 3, "keyword", "do"), # <keyword> do </keyword>
    Token(23, 4, "identifier", "Screen"), # <identifier> Screen </identifier>
    Token(23, 5, "symbol", "."), # <symbol> . </symbol>
    Token(23, 6, "identifier", "setColor"), # <identifier> setColor </identifier>
    Token(23, 7, "symbol", "("), # <symbol> ( </symbol>
    Token(23, 8, "identifier", "x"), # <identifier> x </identifier>
    Token(23, 9, "symbol", ")"), # <symbol> ) </symbol>
    Token(24, 1, "symbol", ";"), # <symbol> ; </symbol>
    Token(24, 2, "keyword", "do"), # <keyword> do </keyword>
    Token(24, 3, "identifier", "Screen"), # <identifier> Screen </identifier>
    Token(24, 4, "symbol", "."), # <symbol> . </symbol>
    Token(24, 5, "identifier", "drawRectangle"), # <identifier> drawRectangle </identifier>
    Token(24, 6, "symbol", "("), # <symbol> ( </symbol>
    Token(24, 7, "identifier", "x"), # <identifier> x </identifier>
    Token(24, 9, "symbol", ","), # <symbol> , </symbol>
    Token(24, 1, "identifier", "y"), # <identifier> y </identifier>
    Token(25, 1, "symbol", ","), # <symbol> , </symbol>
    Token(25, 2, "identifier", "x"), # <identifier> x </identifier>
    Token(25, 3, "symbol", ","), # <symbol> , </symbol>
    Token(25, 4, "identifier", "y"), # <identifier> y </identifier>
    Token(25, 5, "symbol", ")"), # <symbol> ) </symbol>
    Token(25, 6, "symbol", ";"), # <symbol> ; </symbol>
    Token(25, 7, "keyword", "let"), # <keyword> let </keyword>
    Token(25, 8, "identifier", "y"), # <identifier> y </identifier>
    Token(25, 9, "symbol", "="), # <symbol> = </symbol>
    Token(26, 1, "identifier", "y"), # <identifier> y </identifier>
    Token(26, 2, "symbol", ";"), # <symbol> ; </symbol>
    Token(26, 3, "keyword", "do"), # <keyword> do </keyword>
    Token(26, 4, "identifier", "Screen"), # <identifier> Screen </identifier>
    Token(26, 5, "symbol", "."), # <symbol> . </symbol>
    Token(26, 6, "identifier", "setColor"), # <identifier> setColor </identifier>
    Token(26, 7, "symbol", "("), # <symbol> ( </symbol>
    Token(26, 9, "identifier", "x"), # <identifier> x </identifier>
    Token(26, 1, "symbol", ")"), # <symbol> ) </symbol>
    Token(27, 1, "symbol", ";"), # <symbol> ; </symbol>
    Token(27, 2, "keyword", "do"), # <keyword> do </keyword>
    Token(27, 3, "identifier", "Screen"), # <identifier> Screen </identifier>
    Token(27, 4, "symbol", "."), # <symbol> . </symbol>
    Token(27, 5, "identifier", "drawRectangle"), # <identifier> drawRectangle </identifier>
    Token(27, 6, "symbol", "("), # <symbol> ( </symbol>
    Token(27, 7, "identifier", "x"), # <identifier> x </identifier>
    Token(27, 8, "symbol", ","), # <symbol> , </symbol>
    Token(27, 9, "identifier", "y"), # <identifier> y </identifier>
    Token(28, 1, "symbol", ","), # <symbol> , </symbol>
    Token(28, 2, "identifier", "x"), # <identifier> x </identifier>
    Token(28, 3, "symbol", ","), # <symbol> , </symbol>
    Token(28, 4, "identifier", "y"), # <identifier> y </identifier>
    Token(28, 5, "symbol", ")"), # <symbol> ) </symbol>
    Token(28, 6, "symbol", ";"), # <symbol> ; </symbol>
    Token(28, 7, "symbol", "}"), # <symbol> } </symbol>
    Token(28, 9, "keyword", "return"), # <keyword> return </keyword>
    Token(28, 1, "symbol", ";"), # <symbol> ; </symbol>
    Token(29, 1, "symbol", "}"), # <symbol> } </symbol>
    Token(29, 2, "keyword", "method"), # <keyword> method </keyword>
    Token(29, 3, "keyword", "void"), # <keyword> void </keyword>
    Token(29, 4, "identifier", "moveDown"), # <identifier> moveDown </identifier>
    Token(29, 5, "symbol", "("), # <symbol> ( </symbol>
    Token(29, 6, "symbol", ")"), # <symbol> ) </symbol>
    Token(29, 7, "symbol", "{"), # <symbol> { </symbol>
    Token(29, 8, "keyword", "if"), # <keyword> if </keyword>
    Token(29, 9, "symbol", "("), # <symbol> ( </symbol>
    Token(30, 1, "identifier", "y"), # <identifier> y </identifier>
    Token(30, 2, "symbol", ")"), # <symbol> ) </symbol>
    Token(30, 3, "symbol", "{"), # <symbol> { </symbol>
    Token(30, 4, "keyword", "do"), # <keyword> do </keyword>
    Token(30, 5, "identifier", "Screen"), # <identifier> Screen </identifier>
    Token(30, 6, "symbol", "."), # <symbol> . </symbol>
    Token(30, 7, "identifier", "setColor"), # <identifier> setColor </identifier>
    Token(30, 9, "symbol", "("), # <symbol> ( </symbol>
    Token(30, 1, "identifier", "x"), # <identifier> x </identifier>
    Token(31, 1, "symbol", ")"), # <symbol> ) </symbol>
    Token(31, 2, "symbol", ";"), # <symbol> ; </symbol>
    Token(31, 3, "keyword", "do"), # <keyword> do </keyword>
    Token(31, 4, "identifier", "Screen"), # <identifier> Screen </identifier>
    Token(31, 5, "symbol", "."), # <symbol> . </symbol>
    Token(31, 6, "identifier", "drawRectangle"), # <identifier> drawRectangle </identifier>
    Token(31, 7, "symbol", "("), # <symbol> ( </symbol>
    Token(31, 8, "identifier", "x"), # <identifier> x </identifier>
    Token(31, 9, "symbol", ","), # <symbol> , </symbol>
    Token(32, 1, "identifier", "y"), # <identifier> y </identifier>
    Token(32, 2, "symbol", ","), # <symbol> , </symbol>
    Token(32, 3, "identifier", "x"), # <identifier> x </identifier>
    Token(32, 4, "symbol", ","), # <symbol> , </symbol>
    Token(32, 5, "identifier", "y"), # <identifier> y </identifier>
    Token(32, 6, "symbol", ")"), # <symbol> ) </symbol>
    Token(32, 7, "symbol", ";"), # <symbol> ; </symbol>
    Token(32, 9, "keyword", "let"), # <keyword> let </keyword>
    Token(32, 1, "identifier", "y"), # <identifier> y </identifier>
    Token(33, 1, "symbol", "="), # <symbol> = </symbol>
    Token(33, 2, "identifier", "y"), # <identifier> y </identifier>
    Token(33, 3, "symbol", ";"), # <symbol> ; </symbol>
    Token(33, 4, "keyword", "do"), # <keyword> do </keyword>
    Token(33, 5, "identifier", "Screen"), # <identifier> Screen </identifier>
    Token(33, 6, "symbol", "."), # <symbol> . </symbol>
    Token(33, 7, "identifier", "setColor"), # <identifier> setColor </identifier>
    Token(33, 8, "symbol", "("), # <symbol> ( </symbol>
    Token(33, 9, "identifier", "x"), # <identifier> x </identifier>
    Token(34, 1, "symbol", ")"), # <symbol> ) </symbol>
    Token(34, 2, "symbol", ";"), # <symbol> ; </symbol>
    Token(34, 3, "keyword", "do"), # <keyword> do </keyword>
    Token(34, 4, "identifier", "Screen"),  # <identifier> Screen </identifier>
    Token(34, 5, "symbol", "."), # <symbol> . </symbol>
    Token(34, 6, "identifier", "drawRectangle"), # <identifier> drawRectangle </identifier>
    Token(34, 7, "symbol", "("), # <symbol> ( </symbol>
    Token(34, 9, "identifier", "x"), # <identifier> x </identifier>
    Token(34, 1, "symbol", ","), # <symbol> , </symbol>
    Token(35, 1, "identifier", "y"), # <identifier> y </identifier>
    Token(35, 2, "symbol", ","), # <symbol> , </symbol>
    Token(35, 3, "identifier", "x"), # <identifier> x </identifier>
    Token(35, 4, "symbol", ","), # <symbol> , </symbol>
    Token(35, 5, "identifier", "y"), # <identifier> y </identifier>
    Token(35, 6, "symbol", ")"), # <symbol> ) </symbol>
    Token(35, 7, "symbol", ";"), # <symbol> ; </symbol>
    Token(35, 8, "symbol", "}"), # <symbol> } </symbol>
    Token(35, 9, "keyword", "return"), # <keyword> return </keyword>
    Token(36, 1, "symbol", ";"), # <symbol> ; </symbol>
    Token(36, 2, "symbol", "}"), # <symbol> } </symbol>
    Token(36, 3, "keyword", "method"), # <keyword> method </keyword>
    Token(36, 4, "keyword", "void"), # <keyword> void </keyword>
    Token(36, 5, "identifier", "moveLeft"), # <identifier> moveLeft </identifier>
    Token(36, 6, "symbol", "("), # <symbol> ( </symbol>
    Token(36, 7, "symbol", ")"), # <symbol> ) </symbol>
    Token(36, 9, "symbol", "{"), # <symbol> { </symbol>
    Token(36, 1, "keyword", "if"), # <keyword> if </keyword>
    Token(37, 1, "symbol", "("), # <symbol> ( </symbol>
    Token(37, 2, "identifier", "x"), # <identifier> x </identifier>
    Token(37, 3, "symbol", ")"), # <symbol> ) </symbol>
    Token(37, 4, "symbol", "{"), # <symbol> { </symbol>
    Token(37, 5, "keyword", "do"), # <keyword> do </keyword>
    Token(37, 6, "identifier", "Screen"), # <identifier> Screen </identifier>
    Token(37, 7, "symbol", "."), # <symbol> . </symbol>
    Token(37, 8, "identifier", "setColor"), # <identifier> setColor </identifier>
    Token(37, 9, "symbol", "("), # <symbol> ( </symbol>
    Token(38, 1, "identifier", "x"), # <identifier> x </identifier>
    Token(38, 2, "symbol", ")"), # <symbol> ) </symbol>
    Token(38, 3, "symbol", ";"), # <symbol> ; </symbol>
    Token(38, 4, "keyword", "do"), # <keyword> do </keyword>
    Token(38, 5, "identifier", "Screen"), # <identifier> Screen </identifier>
    Token(38, 6, "symbol", "."), # <symbol> . </symbol>
    Token(38, 7, "identifier", "drawRectangle"), # <identifier> drawRectangle </identifier>
    Token(38, 9, "symbol", "("), # <symbol> ( </symbol>
    Token(38, 1, "identifier", "x"), # <identifier> x </identifier>
    Token(39, 1, "symbol", ","), # <symbol> , </symbol>
    Token(39, 2, "identifier", "y"), # <identifier> y </identifier>
    Token(39, 3, "symbol", ","), # <symbol> , </symbol>
    Token(39, 4, "identifier", "x"), # <identifier> x </identifier>
    Token(39, 5, "symbol", ","), # <symbol> , </symbol>
    Token(39, 6, "identifier", "y"), # <identifier> y </identifier>
    Token(39, 7, "symbol", ")"), # <symbol> ) </symbol>
    Token(39, 8, "symbol", ";"), # <symbol> ; </symbol>
    Token(39, 9, "keyword", "let"), # <keyword> let </keyword>
    Token(40, 1, "identifier", "x"), # <identifier> x </identifier>
    Token(40, 2, "symbol", "="), # <symbol> = </symbol>
    Token(40, 3, "identifier", "x"), # <identifier> x </identifier>
    Token(40, 4, "symbol", ";"), # <symbol> ; </symbol>
    Token(40, 5, "keyword", "do"), # <keyword> do </keyword>
    Token(40, 6, "identifier", "Screen"), # <identifier> Screen </identifier>
    Token(40, 7, "symbol", "."), # <symbol> . </symbol>
    Token(40, 9, "identifier", "setColor"), # <identifier> setColor </identifier>
    Token(40, 1, "symbol", "("), # <symbol> ( </symbol>
    Token(41, 1, "identifier", "x"), # <identifier> x </identifier>
    Token(41, 2, "symbol", ")"), # <symbol> ) </symbol>
    Token(41, 3, "symbol", ";"), # <symbol> ; </symbol>
    Token(41, 4, "keyword", "do"), # <keyword> do </keyword>
    Token(41, 5, "identifier", "Screen"), # <identifier> Screen </identifier>
    Token(41, 6, "symbol", "."), # <symbol> . </symbol>
    Token(41, 7, "identifier", "drawRectangle"), # <identifier> drawRectangle </identifier>
    Token(41, 8, "symbol", "("), # <symbol> ( </symbol>
    Token(41, 9, "identifier", "x"), # <identifier> x </identifier>
    Token(42, 1, "symbol", ","), # <symbol> , </symbol>
    Token(42, 2, "identifier", "y"), # <identifier> y </identifier>
    Token(42, 3, "symbol", ","), # <symbol> , </symbol>
    Token(42, 4, "identifier", "x"), # <identifier> x </identifier>
    Token(42, 5, "symbol", ","), # <symbol> , </symbol>
    Token(42, 6, "identifier", "y"), # <identifier> y </identifier>
    Token(42, 7, "symbol", ")"), # <symbol> ) </symbol>
    Token(42, 9, "symbol", ";"), # <symbol> ; </symbol>
    Token(42, 1, "symbol", "}"), # <symbol> } </symbol>
    Token(43, 1, "keyword", "return"), # <keyword> return </keyword>
    Token(43, 2, "symbol", ";"), # <symbol> ; </symbol>
    Token(43, 3, "symbol", "}"), # <symbol> } </symbol>
    Token(43, 4, "keyword", "method"), # <keyword> method </keyword>
    Token(43, 5, "keyword", "void"), # <keyword> void </keyword>
    Token(43, 6, "identifier", "moveRight"), # <identifier> moveRight </identifier>
    Token(43, 7, "symbol", "("), # <symbol> ( </symbol>
    Token(43, 8, "symbol", ")"), # <symbol> ) </symbol>
    Token(43, 9, "symbol", "{"), # <symbol> { </symbol>
    Token(44, 1, "keyword", "if"), # <keyword> if </keyword>
    Token(44, 2, "symbol", "("), # <symbol> ( </symbol>
    Token(44, 3, "identifier", "x"), # <identifier> x </identifier>
    Token(44, 4, "symbol", ")"), # <symbol> ) </symbol>
    Token(44, 5, "symbol", "{"), # <symbol> { </symbol>
    Token(44, 6, "keyword", "do"), # <keyword> do </keyword>
    Token(44, 7, "identifier", "Screen"), # <identifier> Screen </identifier>
    Token(44, 9, "symbol", "."), # <symbol> . </symbol>
    Token(44, 1, "identifier", "setColor"), # <identifier> setColor </identifier>
    Token(45, 1, "symbol", "("), # <symbol> ( </symbol>
    Token(45, 2, "identifier", "x"), # <identifier> x </identifier>
    Token(45, 3, "symbol", ")"), # <symbol> ) </symbol>
    Token(45, 4, "symbol", ";"), # <symbol> ; </symbol>
    Token(45, 5, "keyword", "do"), # <keyword> do </keyword>
    Token(45, 6, "identifier", "Screen"), # <identifier> Screen </identifier>
    Token(45, 7, "symbol", "."), # <symbol> . </symbol>
    Token(45, 8, "identifier", "drawRectangle"), # <identifier> drawRectangle </identifier>
    Token(45, 9, "symbol", "("), # <symbol> ( </symbol>
    Token(46, 1, "identifier", "x"), # <identifier> x </identifier>
    Token(46, 2, "symbol", ","), # <symbol> , </symbol>
    Token(46, 3, "identifier", "y"), # <identifier> y </identifier>
    Token(46, 4, "symbol", ","), # <symbol> , </symbol>
    Token(46, 5, "identifier", "x"), # <identifier> x </identifier>
    Token(46, 6, "symbol", ","), # <symbol> , </symbol>
    Token(46, 7, "identifier", "y"), # <identifier> y </identifier>
    Token(46, 9, "symbol", ")"), # <symbol> ) </symbol>
    Token(46, 1, "symbol", ";"), # <symbol> ; </symbol>
    Token(47, 1, "keyword", "let"), # <keyword> let </keyword>
    Token(47, 2, "identifier", "x"), # <identifier> x </identifier>
    Token(47, 3, "symbol", "="), # <symbol> = </symbol>
    Token(47, 4, "identifier", "x"), # <identifier> x </identifier>
    Token(47, 5, "symbol", ";"), # <symbol> ; </symbol>
    Token(47, 6, "keyword", "do"), # <keyword> do </keyword>
    Token(47, 7, "identifier", "Screen"), # <identifier> Screen </identifier>
    Token(47, 8, "symbol", "."), # <symbol> . </symbol>
    Token(47, 9, "identifier", "setColor"), # <identifier> setColor </identifier>
    Token(48, 1, "symbol", "("), # <symbol> ( </symbol>
    Token(48, 2, "identifier", "x"), # <identifier> x </identifier>
    Token(48, 3, "symbol", ")"), # <symbol> ) </symbol>
    Token(48, 4, "symbol", ";"), # <symbol> ; </symbol>
    Token(48, 5, "keyword", "do"), # <keyword> do </keyword>
    Token(48, 6, "identifier", "Screen"), # <identifier> Screen </identifier>
    Token(48, 7, "symbol", "."), # <symbol> . </symbol>
    Token(48, 9, "identifier", "drawRectangle"), # <identifier> drawRectangle </identifier>
    Token(48, 1, "symbol", "("), # <symbol> ( </symbol>
    Token(49, 1, "identifier", "x"), # <identifier> x </identifier>
    Token(49, 2, "symbol", ","), # <symbol> , </symbol>
    Token(49, 3, "identifier", "y"), # <identifier> y </identifier>
    Token(49, 4, "symbol", ","), # <symbol> , </symbol>
    Token(49, 5, "identifier", "x"), # <identifier> x </identifier>
    Token(49, 6, "symbol", ","), # <symbol> , </symbol>
    Token(49, 7, "identifier", "y"), # <identifier> y </identifier>
    Token(49, 8, "symbol", ")"), # <symbol> ) </symbol>
    Token(49, 9, "symbol", ";"), # <symbol> ; </symbol>
    Token(50, 1, "symbol", "}"), # <symbol> } </symbol>
    Token(50, 2, "keyword", "return"), # <keyword> return </keyword>
    Token(50, 3, "symbol", ";"), # <symbol> ; </symbol>
    Token(50, 4, "symbol", "}"), # <symbol> } </symbol>
    Token(50, 5, "symbol", "}"), # <symbol> } </symbol>
]
#print("Tokens at start:", square_tokens[:5])
parse_jack_class(square_tokens, False)

