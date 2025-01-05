def rgb_to_hex(tuple_r):
    s_hex = "#"
    for i in tuple_r:
        s_hex += f"{(hex(i))[2:]:02s}"
    return '"'+s_hex+'"'

def fix_string(fix):
    fixed = fix[1:-1].replace('"','\\"')
    return f"\"{fixed}\""