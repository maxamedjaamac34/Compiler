import xml.etree.ElementTree as ET
from xmlParse import JackClass, JackSubroutine, JackVarDec, xml_parse

class ClassSymbolTables:
    subroutine_symbol_tables = []
    def __init__(self, jack_class: JackClass):
        self.class_symbol_table = {"this":{"name": "this", "type": jack_class.name, "kind": "arg", "value": None}}
        for i in jack_class.var_decs:
            self.class_symbol_table.update({i.name, {"name": i.name, "type": i.type, "kind": i.kind, "value": None}})
        for i in jack_class.subroutines:
            subroutine_symbol_table = {"subroutine_name": i.name}
            for j in i.var_decs:
                subroutine_symbol_table.update({j.name, {"name": j.name, "type": j.type, "kind": j.kind, "value": None}})
            self.subroutine_symbol_tables.append(subroutine_symbol_table)

wheel_class = JackClass("Wheel")
wheel_symbol_tables = ClassSymbolTables(wheel_class)
print(wheel_symbol_tables.class_symbol_table)
print(wheel_symbol_tables.subroutine_symbol_tables)