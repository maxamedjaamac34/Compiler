import xml.etree.ElementTree as ET

OP_TO_VM = {
    "+": "add",
    "-": "sub",
    "*": "call Math.multiply 2",
    "/": "call Math.divide 2",
    "&": "and",
    "|": "or",
    "<": "lt",
    ">": "gt",
    "=": "eq"
}

UNARY_OP_TO_VM = {
    "-": "neg",
    "~": "not"
}

class Expression:
    def __init__(self, exp):
        self.objects = []
        for child in exp:
            if child.tag == 'term':
                self.objects.append(Term(child))
            if child.tag == 'op':
                self.objects.append(Op(child))

class Term:
    def __init__(self, term):
        self.objects = []
        for child in term:
            if child.tag == 'expression':
                self.objects.append(Expression(child))
            elif child.tag == 'subroutineCall':
                self.objects.append(SubroutineCall(child))
            elif child.tag == 'unaryOp':
                self.objects.append(UnaryOp(child))
            elif child.tag == 'term':
                self.objects.append(Term(child))
            else:
                self.objects.append(child)

class SubroutineCall:
    def __init__(self, subroutine_call):
        self.name = ""
        self.objects = []
        for child in subroutine_call:
            if child.tag == 'expressionList':
                self.objects.append(ExpressionList(child))
            elif child.text in ['(', ')']:
                self.objects.append(child)
            else:
                self.name = self.name + child.text
                self.objects.append(child)

class ExpressionList:
    def __init__(self, expression_list):
        self.objects = []
        for child in expression_list:
            if child.tag == 'expression':
                self.objects.append(Expression(child))
            else:
                self.objects.append(child)

class Op:
    def __init__(self, op):
        self.objects = []
        for child in op:
            self.objects.append(child)

class UnaryOp:
    def __init__(self, unary_op):
        self.objects = []
        for child in unary_op:
            self.objects.append(child)

def expression_code_gen(root):
    expression = Expression(root)
    code_lines = []

    term = expression.objects[0]
    if isinstance(term.objects[0], UnaryOp):
        code_lines.append(expression_code_gen(term.objects[1:]))
        code_lines.append(UNARY_OP_TO_VM[term.objects[0].text])
    elif isinstance(term.objects[0], SubroutineCall):
        num_args = 0
        for child in term.objects[0].objects:
            if isinstance(child, ExpressionList):
                for j in child.objects:
                    if isinstance(j, Expression):
                        code_lines.append(expression_code_gen(j.objects))
                        num_args += 1
        code_lines.append("call " + term.objects[0].name + " " + num_args)
    elif isinstance(term, Term) and isinstance(term.objects[1], Op) and isinstance(term.objects[2], Term):
        code_lines.append(expression_code_gen(term.objects))
        code_lines.append(expression_code_gen(expression.objects[2].objects))
        code_lines.append(OP_TO_VM[expression.objects[1].objects[0].text])
    elif term.objects[0].tag in ['identifier', 'keyword']:
        # todo: look up term.objects[0].text in symbol table and put memory segment + index in push statement
        code_lines.append("push " + term.objects[0].text)
    elif term.objects[0].tag == 'integerConstant':
        code_lines.append("push constant " + term.objects[0].text)
    return code_lines

tree = ET.parse('Expression.xml')
root = tree.getroot()
print(expression_code_gen(root))
