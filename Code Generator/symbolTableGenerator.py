import xml.etree.ElementTree as ET
from xmlParse import JackClass, JackSubroutine, JackVarDec, xml_parse

class ClassSymbolTables:
    subroutine_symbol_tables = []
    def __init__(self, jack_class: JackClass):
        self.class_symbol_table = {"this":{"name": "this", "type": jack_class.name, "kind": "argument", "index": 0}}
        field_counter = 0
        static_counter = 0
        for i in jack_class.var_decs:
            if i.kind == "static":
                index = static_counter
                static_counter += 1
            else:
                index = field_counter
                field_counter += 1
            self.class_symbol_table.update({i.name: {"name": i.name, "type": i.type, "kind": i.kind, "index": index}})
        for i in jack_class.subroutines:
            subroutine_symbol_table = {"subroutine_name": i.name}
            argument_counter = 0
            var_counter = 0
            for j in i.var_decs:
                if j.kind == "argument":
                    index = argument_counter
                    argument_counter += 1
                else:
                    index = var_counter
                    var_counter += 1
                subroutine_symbol_table.update({j.name: {"name": j.name, "type": j.type, "kind": j.kind, "index": index}})
            self.subroutine_symbol_tables.append(subroutine_symbol_table)

wheel_class = xml_parse("Wheel")
wheel_symbol_tables = ClassSymbolTables(wheel_class)
print(wheel_symbol_tables.class_symbol_table)
print(wheel_symbol_tables.subroutine_symbol_tables)