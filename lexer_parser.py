from sly import Lexer, Parser

from nodes import TYPE_DICT, Block, Content, Line
from utils import fix_string, rgb_to_hex

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
    NAME = r'[a-zA-Z_][a-zA-Z0-9_]*'
    STRING = r'".+"'

    @_(r'\d+')
    def NUMBER(self, t):
        t.value = int(t.value)
        return t

    @_(r'\n+')
    def newline(self, t):
        self.lineno += t.value.count('\n')

    def error(self, t):
        print(f"Illegal character {t.value[0]} in line {self.lineno}")
        self.index += 1

class BlockParser(Parser):
    tokens = BlockLexer.tokens

    @_('file')
    def input(self, p):
        return p.file 

    @_('lines')
    def file(self, p):
        return [p.lines]

    @_('lines file')
    def file(self, p):
        (p.file).append(p.lines)
        return p.file

    @_('BLOCK NAME "{" block_content "}"')
    def lines(self, p):
        return Block(p.NAME, p.block_content)

    @_('LINE NAME "{" line_content "}"')
    def lines(self, p):
        return Line(p.NAME, p.line_content)

    @_('block_line')
    def block_content(self, p):
        return Content().add(*p.block_line)

    @_('block_line block_content')
    def block_content(self, p):
        return (p.block_content).add(*p.block_line)

    @_('COLOR ":" "(" tuple ")"')
    def block_line(self, p):
        return ("fillcolor", p.tuple)

    @_('TYPE_NAME ":" TYPE')
    def block_line(self, p):
        return ("shape",TYPE_DICT[p.TYPE])

    @_('TEXT ":" STRING')
    def block_line(self, p):
        return ("label", fix_string(p.STRING))

    @_('FRAME ":" "(" tuple ")"')
    def block_line(self, p):
        return ("color",p.tuple)

    @_('NUMBER "," NUMBER "," NUMBER')
    def tuple(self, p):
        return f"{rgb_to_hex((p.NUMBER0,p.NUMBER1,p.NUMBER2))}"

    @_('line_line')
    def line_content(self, p):
        return Content().add(*p.line_line)

    @_('line_line line_content')
    def line_content(self, p):
        return (p.line_content).add(*p.line_line)
    
    @_('COLOR ":" "(" tuple ")"')
    def line_line(self, p):
        return ("color", p.tuple)

    @_('TEXT ":" STRING')
    def line_line(self, p):
        return ("label", fix_string(p.STRING))

    @_('CONNECT ":" connect_nt')
    def line_line(self, p):
        return ("edge", p.connect_nt)

    @_('any ">" NAME')
    def connect_nt(self, p):
        connections  = [(begin, p.NAME) for begin in p.any]
        return  connections

    @_('NAME "<" any')
    def connect_nt(self, p):
        connections  = [(begin,p.NAME) for begin in p.any]
        return connections

    @_('NAME')
    def any(self, p):
        return [p.NAME]

    @_('NAME "," any')
    def any(self, p):
        (p.any).append(p.NAME)
        return p.any

    def error(self, p):
        if p:
            print(f"Syntax error at token {p.type} ({p.value}), line {p.lineno}")
        else:
            print("Unexpected end of input")

def run_main(input, output):
    lexer = BlockLexer()
    parser = BlockParser()

    with open(input, "r") as f:
        data = f.read()
        elements = parser.parse(lexer.tokenize(data))
        elements.reverse()
        
        with open(output, 'w') as f:
            f.write("digraph BlockSchema {\n")
            f.write("node [style=filled]; \n")
            for elem in elements:
                f.write(elem.to_string())
            f.write("}\n")
