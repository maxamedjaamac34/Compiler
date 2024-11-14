from ProgramStructureParseClasses import ProgramStructure
from ParserClasses import Token
from VarOrClassVarDecParse import ClassVarDecParse
from SubroutineDecParse import SubroutineDecParse

class ClassParse(ProgramStructure):
    def __init__(self, class_keyword, class_name, open_brace, *args):
        # class is the only parsing structure that does NOT accept trailing tokens because each file should be only one class
        if not (isinstance(class_keyword, Token) and class_keyword.tokenType == "keyword" and class_keyword.tokenValue == "class"):
            raise ValueError("class_keyword must be the keyword Token 'class'")
        if not (isinstance(class_name, Token) and class_name.tokenType == "identifier"):
            raise ValueError("class_name must be a ClassNameParse object")
        if not (isinstance(open_brace, Token) and open_brace.tokenType == "symbol" and open_brace.tokenValue == "{"):
            raise ValueError("open_brace must be the symbol token {")
        self.objects = [class_keyword, class_name, open_brace]
        subroutine_decs = False # whether subroutines have already been detected
        close_brace = False # whether a close brace has already been detected
        for arg in args:
            if arg is ClassVarDecParse and not subroutine_decs and not close_brace:
                self.objects.append(arg)
            elif arg is SubroutineDecParse and not close_brace:
                subroutine_decs = True
                self.objects.append(arg)
            elif arg is Token and arg.tokenType == "symbol" and arg.tokenValue == "}" and not close_brace:
                close_brace = True
                self.objects.append(arg)
            else:
                raise ValueError("classes are in the format of class className {classVarDecs*, subroutineDecs*}")
        if not close_brace:
            raise ValueError("Class must end with }")

    def to_xml(self):#to make xml
        xml_output = "<class>\n"
        for obj in self.objects:
            if isinstance(obj, Token):
                xml_output += f"<{obj.tokenType}> {obj.tokenValue} </{obj.tokenType}>\n"
            elif hasattr(obj, 'to_xml'):
                xml_output += obj.to_xml()
        xml_output += "</class>\n"
        return xml_output
