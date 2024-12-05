from sly import Lexer, Parser

class BlockLexer(Lexer):
    tokens = { BLOCK, LINE, NAME, NUMBER, COLOR, TEXT, FRAME, TYPE_NAME, CONNECT, STRING, TYPE}
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
        self.names = { }

    @_('file')
    def input(self,p):
        ...
    
    # @_('EOF')
    # def input(self,p):
    #     ...

    @_('lines')
    def file(self, p):
        ...

    @_('lines file')
    def file(self, p):
        ...
    @_('BLOCK NAME "{" block_content "}"')
    def lines(self, p):
        ...

    @_('LINE NAME "{" line_content "}"')
    def lines(self, p):
        ...
    
    @_('block_line')
    def block_content(self,p):
        ...
    
    @_('block_line block_content')
    def block_content(self,p):
        ...

    @_('COLOR ":" "(" tuple ")"')
    def block_line(self,p):
        ...
    
    @_('TYPE_NAME ":" TYPE')
    def block_line(self,p):
        ...

    @_('TEXT ":" STRING')
    def block_line(self,p):
        ...

    @_('FRAME ":" "(" tuple ")"')
    def block_line(self,p):
        ...

    @_('NUMBER "," NUMBER "," NUMBER')
    def tuple(self,p):
        ...
    
    @_('line_line')
    def line_content(self, p):
        ...
    
    @_('line_line line_content')
    def line_content(self,p):
        ...

    @_('COLOR ":" "(" tuple ")"')
    def line_line(self,p):
        ...
    
    @_('TEXT ":" STRING')
    def line_line(self,p):
        ...
    @_('CONNECT ":" connect_nt')
    def line_line(self,p):
        ...
    @_('any ">" NAME')
    def connect_nt(self,p):
        ...
    @_('NAME "<" any')
    def connect_nt(self,p):
        ...

    @_('NAME')
    def any(self,p):
        ...
    @_('NAME "," any')
    def any(self,p):
        ...

    def error(self, p):
        print(f"Error parsing {p}")

if __name__ == '__main__':
    lexer = BlockLexer()
    parser = BlockParser()

    with open("ex.db", "r") as f:
        parser.parse(lexer.tokenize(f.read()))
