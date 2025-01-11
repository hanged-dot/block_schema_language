import lexer_parser

def rgb_to_hex(tuple_r):
    s_hex = "#"
    for i in tuple_r:
        s_hex += f"{(hex(i))[2:]:02s}"
    return '"'+s_hex+'"'

def fix_string(fix):
    fixed = fix[1:-1].replace('"','\\"')
    return f"\"{fixed}\""

def check_if_nodes(node_1,node_2, list_elem):
    elems = [el.name for el in list_elem ]
    if node_1 not in elems:
        lexer_parser.EXCEPT = f"{node_1} not defined"
        return False
    if node_2 not in elems:
        lexer_parser.EXCEPT = f"{node_2} not defined"
        return False
    return True

