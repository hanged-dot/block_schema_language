from sly import Lexer, Parser

class BlockLexer(Lexer):
    tokens = { BLOCK, LINE, NAME, NUMBER, COLOR, TEXT, FRAME, TYPE_NAME, CONNECT, STRING, TYPE }
    ignore = ' \t'
    literals = { '{','}','>','<',',',':','(',')' }

    # Tokens
    TYPE = r'\b(operation|condition|input/output|start/stop)\b'
    BLOCK = r'block'
    LINE = r'line'
    COLOR = r'color'
    TEXT = r'text'
    FRAME = r'frame'
    TYPE_NAME = r'type'
    CONNECT = r'connect'
    STRING = r'".+"'
    NAME = r'[a-zA-Z_][a-zA-Z0-9_]*'

    @_(r'\d+')
    def NUMBER(self, t):
        t.value = int(t.value)
        return t

    @_(r'\n+')
    def newline(self, t):
        self.lineno += t.value.count('\n')

    def error(self, t):
        print("Illegal character '%s'" % t.value[0])
        self.index += 1

class BlockParser(Parser):
    tokens = BlockLexer.tokens

    def __init__(self):
        self.names = {}
        self.blocks = []
        self.lines = []
        self.connections = []

    @_('file')
    def input(self, p):
        return p.file

    @_('lines')
    def file(self, p):
        return p.lines

    @_('lines file')
    def file(self, p):
        return p.lines + p.file

    @_('BLOCK NAME "{" block_content "}"')
    def lines(self, p):
        self.blocks.append({"name": p.NAME, "attributes": p.block_content})
        return []

    @_('LINE NAME "{" line_content "}"')
    def lines(self, p):
        self.lines.append({"name": p.NAME, "attributes": p.line_content})
        return []

    @_('block_line')
    def block_content(self, p):
        return [p.block_line]

    @_('block_line block_content')
    def block_content(self, p):
        return [p.block_line] + p.block_content

    @_('COLOR ":" "(" tuple ")"')
    def block_line(self, p):
        return {"color": p.tuple}

    @_('TYPE_NAME ":" TYPE')
    def block_line(self, p):
        return {"type": p.TYPE}

    @_('TEXT ":" STRING')
    def block_line(self, p):
        return {"text": p.STRING.strip('"')}

    @_('FRAME ":" "(" tuple ")"')
    def block_line(self, p):
        return {"frame": p.tuple}

    @_('NUMBER "," NUMBER "," NUMBER')
    def tuple(self, p):
        return (p.NUMBER0, p.NUMBER1, p.NUMBER2)

    @_('line_line')
    def line_content(self, p):
        return [p.line_line]

    @_('line_line line_content')
    def line_content(self, p):
        return [p.line_line] + p.line_content

    @_('COLOR ":" "(" tuple ")"')
    def line_line(self, p):
        return {"color": p.tuple}

    @_('TEXT ":" STRING')
    def line_line(self, p):
        return {"text": p.STRING.strip('"')}

    @_('CONNECT ":" connect_nt')
    def line_line(self, p):
        self.connections.append(p.connect_nt)
        return {"connect": p.connect_nt}

    @_('any ">" NAME')
    def connect_nt(self, p):
        return (p.any, "to", p.NAME)

    @_('NAME "<" any')
    def connect_nt(self, p):
        return (p.NAME, "to", p.any)

    @_('NAME')
    def any(self, p):
        return [p.NAME]

    @_('NAME "," any')
    def any(self, p):
        return [p.NAME] + p.any

    def error(self, p):
        print(f"Error parsing {p}")

if __name__ == '__main__':
    lexer = BlockLexer()
    parser = BlockParser()

    with open("ex.db", "r") as f:
        data = f.read()

    parser.parse(lexer.tokenize(data))

    # Generate DOT file
    with open("output.dot", "w") as dotfile:
        dotfile.write("digraph BlockSchema {\n")

        # Write blocks
        for block in parser.blocks:
            attributes = "\n".join(f"{key}={value}" for attr in block["attributes"] for key, value in attr.items())
            dotfile.write(f"  {block['name']} [label=\"{block['name']}\n{attributes}\"];\n")

        # Write lines
        for line in parser.lines:
            attributes = "\n".join(f"{key}={value}" for attr in line["attributes"] for key, value in attr.items())
            dotfile.write(f"  {line['name']} [label=\"{line['name']}\n{attributes}\"];\n")

        # Write connections
        for connection in parser.connections:
            source = "_".join(connection[0])
            target = connection[2]
            dotfile.write(f"  {source} -> {target};\n")

        dotfile.write("}\n")
