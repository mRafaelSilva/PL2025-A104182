import ply.lex as lex

tokens = (
    # bloco principal
    'PROGRAM', 'BEGIN', 'END',

    # tipos e variáveis
    'VAR', 'ARRAY', 'OF', 'INTEGER', 'REAL', 'BOOLEAN', 'CHAR', 'STRINGTYPE',

    'IF', 'THEN', 'ELSE',
    'WHILE', 'DO',
    'FOR', 'TO', 'DOWNTO',
    'REPEAT', 'UNTIL',

    # funções e procedimentos
    'FUNCTION', 'PROCEDURE',

    # input e output
    'WRITELN', 'WRITE', 'READLN', 'READ',

    'LENGTH',

    # operadores
    'ASSIGN', 'PLUS', 'MINUS', 'TIMES', 'DIVIDE',
    'EQUAL', 'NEQUAL', 'LT', 'LE', 'GT', 'GE',
    'MOD', 'DIV',
    'AND', 'OR', 'NOT',

    # símbolos
    'LPAREN', 'RPAREN',
    'LBRACKET', 'RBRACKET',
    'COLON', 'SEMICOLON', 'DOT', 'COMMA',

    'ID', 'INT', 'REALNUM', 'STRING', 'CHARLIT',

    'TRUE', 'FALSE',

    # comentários
    'COMMENT'
)

states = (
    ('comment', 'exclusive'),
)

t_ignore = ' \t'
t_comment_ignore = ''


def t_PROGRAM(t):
    r'[Pp][Rr][Oo][Gg][Rr][Aa][Mm]'
    return t

def t_FUNCTION(t):
    r'[Ff][Uu][Nn][Cc][Tt][Ii][Oo][Nn]'
    return t

def t_PROCEDURE(t):
    r'[Pp][Rr][Oo][Cc][Ee][Dd][Uu][Rr][Ee]'
    return t

def t_BEGIN(t):
    r'[Bb][Ee][Gg][Ii][Nn]'
    return t

def t_DOWNTO(t):
    r'[Dd][Oo][Ww][Nn][Tt][Oo]'
    return t

def t_REPEAT(t):
    r'[Rr][Ee][Pp][Ee][Aa][Tt]'
    return t

def t_WRITELN(t):
    r'[Ww][Rr][Ii][Tt][Ee][Ll][Nn]'
    return t

def t_INTEGER(t):
    r'[Ii][Nn][Tt][Ee][Gg][Ee][Rr]'
    return t

def t_BOOLEAN(t):
    r'[Bb][Oo][Oo][Ll][Ee][Aa][Nn]'
    return t

def t_STRINGTYPE(t):
    r'[Ss][Tt][Rr][Ii][Nn][Gg]'
    return t

def t_LENGTH(t):
    r'[Ll][Ee][Nn][Gg][Tt][Hh]'
    return t

def t_READLN(t):
    r'[Rr][Ee][Aa][Dd][Ll][Nn]'
    return t

def t_ARRAY(t):
    r'[Aa][Rr][Rr][Aa][Yy]'
    return t

def t_UNTIL(t):
    r'[Uu][Nn][Tt][Ii][Ll]'
    return t

def t_FALSE(t):
    r'[Ff][Aa][Ll][Ss][Ee]'
    return t

def t_WRITE(t):
    r'[Ww][Rr][Ii][Tt][Ee]'
    return t

def t_WHILE(t):
    r'[Ww][Hh][Ii][Ll][Ee]'
    return t

def t_THEN(t):
    r'[Tt][Hh][Ee][Nn]'
    return t

def t_ELSE(t):
    r'[Ee][Ll][Ss][Ee]'
    return t

def t_TRUE(t):
    r'[Tt][Rr][Uu][Ee]'
    return t

def t_REAL(t):
    r'[Rr][Ee][Aa][Ll]'
    return t

def t_CHAR(t):
    r'[Cc][Hh][Aa][Rr]'
    return t

def t_READ(t):
    r'[Rr][Ee][Aa][Dd]'
    return t

def t_END(t):
    r'[Ee][Nn][Dd]'
    return t

def t_VAR(t):
    r'[Vv][Aa][Rr]'
    return t

def t_FOR(t):
    r'[Ff][Oo][Rr]'
    return t

def t_AND(t):
    r'[Aa][Nn][Dd]'
    return t

def t_NOT(t):
    r'[Nn][Oo][Tt]'
    return t

def t_DIV(t):
    r'[Dd][Ii][Vv]'
    return t

def t_MOD(t):
    r'[Mm][Oo][Dd]'
    return t

def t_IF(t):
    r'[Ii][Ff]'
    return t

def t_OF(t):
    r'[Oo][Ff]'
    return t

def t_OR(t):
    r'[Oo][Rr]'
    return t

def t_DO(t):
    r'[Dd][Oo]'
    return t

def t_TO(t):
    r'[Tt][Oo]'
    return t

# operadores e símbolos
t_ASSIGN    = r':='
t_LE        = r'<='
t_GE        = r'>='
t_NEQUAL    = r'<>'
t_EQUAL     = r'='
t_LT        = r'<'
t_GT        = r'>'
t_PLUS      = r'\+'
t_MINUS     = r'-'
t_TIMES     = r'\*'
t_DIVIDE    = r'/'
t_LPAREN    = r'\('
t_RPAREN    = r'\)'
t_LBRACKET  = r'\['
t_RBRACKET  = r'\]'
t_COLON     = r':'
t_SEMICOLON = r';'
t_DOT       = r'\.'
t_COMMA     = r','


def t_COMMENT(t):
    r'\{[^}]*\}'
    t.lexer.lineno += t.value.count('\n')
    pass


def t_LPAREN_STAR(t):
    r'\(\*'
    t.lexer.comment_level = 1
    t.lexer.push_state('comment')

def t_comment_LPAREN_STAR(t):
    r'\(\*'
    t.lexer.comment_level += 1

def t_comment_STAR_RPAREN(t):
    r'\*\)'
    t.lexer.comment_level -= 1
    if t.lexer.comment_level == 0:
        t.lexer.pop_state()

def t_comment_newline(t):
    r'\n+'
    t.lexer.lineno += len(t.value)

def t_comment_content(t):
    r'[^(*\*)\n]+'
    pass

def t_comment_error(t):
    t.lexer.skip(1)


def t_REALNUM(t):
    r'\d+\.\d+([eE][+-]?\d+)?'
    try:
        t.value = float(t.value)
    except ValueError:
        print(f"Invalid real number: {t.value}")
        t.value = 0.0
    return t

def t_INT(t):
    r'\d+'
    try:
        t.value = int(t.value)
    except ValueError:
        print(f"Invalid integer: {t.value}")
        t.value = 0
    return t


def t_STRING(t):
    r"'(?:''|[^']){2,}'"

    t.value = t.value[1:-1].replace("''", "'")
    return t


def t_CHARLIT(t):
    r"'[^']'"

    t.value = t.value[1:-1]
    return t


def t_CHARLIT_ESCAPED(t):
    r"''''"
    t.value = "'"
    t.type = 'CHARLIT'
    return t


def t_ID(t):
    r'[a-zA-Z_][a-zA-Z0-9_]*'
    return t

# nova linha
def t_newline(t):
    r'\n+'
    t.lexer.lineno += len(t.value)

# erro
def t_error(t):
    print(f"Illegal character '{t.value[0]}' at line {t.lexer.lineno}")
    t.lexer.skip(1)


lexer = lex.lex()

def analyze_file(filename):
    """Analyze a Pascal file"""
    try:
        with open(filename, 'r', encoding='utf-8') as f:
            data = f.read()
        
        lexer.input(data)
        tokens_found = []
        
        while True:
            try:
                tok = lexer.token()
                if not tok:
                    break
                tokens_found.append(tok)
                print(f"Line {tok.lineno}: {tok.type} = {repr(tok.value)}")
            except lex.LexError as e:
                print(f"Lexical error: {e}")
                break
                
        return tokens_found
        
    except FileNotFoundError:
        print(f"File '{filename}' not found")
        return []
    except Exception as e:
        print(f"Error reading file: {e}")
        return []

def get_input():
    
    while True:
        try:
            data = input('>>> ')
        except EOFError:
            break
            
        if data.lower() == 'quit':
            break
        elif data.lower().startswith('file '):
            filename = data[5:].strip()
            analyze_file(filename)
            continue
        elif data == '':
            continue
            
        lexer.input(data)
        while True:
            try:
                tok = lexer.token()
                if not tok:
                    break
                print(f"{tok.type} = {repr(tok.value)}")
            except lex.LexError as e:
                print(f"Lexical error: {e}")
                break

if __name__ == "__main__":
    get_input()
