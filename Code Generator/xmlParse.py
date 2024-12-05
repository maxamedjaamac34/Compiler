import xml.etree.ElementTree as ET

class JackVarDec:
    def __init__(self, kind, type, name):
        self.kind = kind
        self.type = type
        self.name = name
        return

class JackClass:
    var_decs = []
    subroutines = []
    def __init__(self, name):
        self.name = name

class JackSubroutine:
    var_decs = []
    statements = []
    def __init__(self, kind, type, name):
        self.kind = kind
        self.type = type
        self.name = name

def xml_parse(filename):
    tree = ET.parse(filename + '.xml')
    root = tree.getroot()
    class_name = root[1].text
    jack_class = JackClass(class_name)
    for child in root:
        if child.tag in ["varDec", "classVarDec"]:
            #                                     kind           type           name
            jack_class.var_decs.append(JackVarDec(child[0].text, child[1].text, child[2].text))
        if child.tag == "subroutineDec":
            #                 function/method/constructor  type           name
            jack_subroutine = JackSubroutine(child[0], child[1].text, child[2].text)
            for s_child in child: # s_child = subroutineDec child
                if s_child.tag == "parameterList":
                    for i in range(len(s_child.iterchildren())):
                        if i == 0:
                            continue
                        if s_child[i].tag == "identifier" and s_child[i-1].tag in ["identifier", "keyword"]:
                            jack_subroutine.var_decs.append(JackVarDec("argument", s_child[i-1].text, s_child[i].text))
                if s_child.tag == "varDec":
                    jack_subroutine.var_decs.append(JackVarDec(s_child[0].text, s_child[1].text, s_child[2].text))
                if s_child.tag in ["ifStatement", "letStatement", "whileStatement", "doStatement", "returnStatement"]:
                    jack_subroutine.statements.append(child)
            jack_class.subroutines.append(jack_subroutine)
    return jack_class
