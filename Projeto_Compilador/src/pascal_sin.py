import ply.yacc as yacc
from pascal_lex import tokens


# Operadores unários têm maior prioridade do que operadores binários 

precedence = (
    ('right', 'ELSE'),                                           # Para resolver o conflito do  'dangling else'
    ('left', 'OR'),                                              # Operador lógico OR
    ('left', 'AND'),                                             # Operador lógico AND    
    ('right', 'NOT'),                                            # Operador lógico NOT       
    ('left', 'EQUAL', 'NEQUAL', 'LT', 'LE', 'GT', 'GE'),         # Operadores relacionais
    ('left', 'PLUS', 'MINUS'),                                   # Operadores aditivos (binários)
    ('left', 'TIMES', 'DIVIDE', 'DIV', 'MOD'),                   # Operadores multiplicativos
    ('right', 'UNARY'),                                          # Operadores unários (+, -) com `%prec UNARY`     
)

# PROGRAMA PRINCIPAL 

def p_program(p):
    '''program : PROGRAM ID SEMICOLON declarations compound_statement DOT
               | PROGRAM ID SEMICOLON compound_statement DOT'''
    if len(p) == 7:
        p[0] = ('program', p[2], p[4], p[5])
    else:
        p[0] = ('program', p[2], [], p[4])


# == DECLARAÇÕES ==

def p_declarations(p):
    '''declarations : declarations declaration
                   | declaration'''
    if len(p) == 2:
        p[0] = [p[1]]
    else:
        p[0] = p[1] + [p[2]]

def p_declaration(p):
    '''declaration : var_declaration
                  | function_declaration
                  | procedure_declaration'''
    p[0] = p[1]

# Declaração de variáveis
def p_var_declaration(p):
    '''var_declaration : VAR var_list'''
    p[0] = ('var_decl', p[2])

def p_var_list(p):
    '''var_list : var_list var_spec
                | var_spec'''
    if len(p) == 2:
        p[0] = [p[1]]
    else:
        p[0] = p[1] + [p[2]]

def p_var_spec(p):
    '''var_spec : id_list COLON type_spec SEMICOLON'''
    p[0] = ('var_spec', p[1], p[3])

def p_id_list(p):
    '''id_list : id_list COMMA ID
               | ID'''
    if len(p) == 2:
        p[0] = [p[1]]
    else:
        p[0] = p[1] + [p[3]]

# Tipos básicos
def p_type_spec(p):
    '''type_spec : INTEGER
                 | REAL
                 | BOOLEAN
                 | CHAR
                 | STRINGTYPE
                 | array_type'''
    p[0] = p[1]

def p_array_type(p):
    '''array_type : ARRAY LBRACKET INT DOT DOT INT RBRACKET OF type_spec'''
    p[0] = ('array_type', p[3], p[6], p[9])


# FUNÇÕES E PROCEDIMENTOS

def p_function_declaration(p):
    '''function_declaration : function_header declarations compound_statement SEMICOLON
                           | function_header compound_statement SEMICOLON'''
    if len(p) == 5:
        p[0] = ('function', p[1][0], p[1][1], p[1][2], p[2], p[3])
    else:
        p[0] = ('function', p[1][0], p[1][1], p[1][2], [], p[2])

def p_function_header(p):
    '''function_header : FUNCTION ID LPAREN param_list RPAREN COLON type_spec SEMICOLON
                      | FUNCTION ID COLON type_spec SEMICOLON'''
    if len(p) == 9:
        p[0] = (p[2], p[4], p[7])  # nome, parâmetros, tipo_retorno
    else:
        p[0] = (p[2], [], p[4])    # nome, sem parâmetros, tipo_retorno

def p_procedure_declaration(p):
    '''procedure_declaration : procedure_header declarations compound_statement SEMICOLON
                            | procedure_header compound_statement SEMICOLON'''
    if len(p) == 5:
        p[0] = ('procedure', p[1][0], p[1][1], p[2], p[3])
    else:
        p[0] = ('procedure', p[1][0], p[1][1], [], p[2])

def p_procedure_header(p):
    '''procedure_header : PROCEDURE ID LPAREN param_list RPAREN SEMICOLON
                       | PROCEDURE ID SEMICOLON'''
    if len(p) == 7:
        p[0] = (p[2], p[4])  # nome, parâmetros
    else:
        p[0] = (p[2], [])    # nome, sem parâmetros

def p_param_list(p):
    '''param_list : param_list SEMICOLON param_spec
                  | param_spec'''
    if len(p) == 2:
        p[0] = [p[1]]
    else:
        p[0] = p[1] + [p[3]]

def p_param_spec(p):
    '''param_spec : id_list COLON type_spec'''
    p[0] = ('param', p[1], p[3])


# COMANDOS

def p_compound_statement(p):
    '''compound_statement : BEGIN statement_list END'''
    p[0] = ('compound', p[2])

def p_statement_list(p):
    '''statement_list : statement_list SEMICOLON statement
                     | statement
                     | empty''' 
    if len(p) == 2:
        if p[1] is None:
            p[0] = []
        else:
            p[0] = [p[1]]
    else:
        if p[3] is None:
            p[0] = p[1] if p[1] else []
        else:
            p[0] = (p[1] if p[1] else []) + [p[3]]

def p_statement(p):
    '''statement : assignment_statement
                | procedure_call
                | compound_statement
                | if_statement
                | while_statement
                | for_statement
                | repeat_statement
                | write_statement
                | read_statement
                | empty'''
    p[0] = p[1]

def p_empty(p):
    '''empty :'''
    p[0] = None

# Atribuição
def p_assignment_statement(p):
    '''assignment_statement : variable ASSIGN expr_bool'''
    p[0] = ('assign', p[1], p[3])

def p_variable(p):
    '''variable : ID
                | ID LBRACKET expr_bool RBRACKET'''
    if len(p) == 2:
        p[0] = ('var', p[1])
    else:
        p[0] = ('array_access', p[1], p[3])

# Chamada de procedimento
def p_procedure_call(p):
    '''procedure_call : ID LPAREN expression_list RPAREN
                     | ID LPAREN RPAREN
                     | ID'''
    if len(p) == 2:
        p[0] = ('proc_call', p[1], [])
    elif len(p) == 4:
        p[0] = ('proc_call', p[1], [])
    else:
        p[0] = ('proc_call', p[1], p[3])


# CONTROLO DE FLUXO

def p_if_statement(p):
    '''if_statement : IF expr_bool THEN statement
                   | IF expr_bool THEN statement ELSE statement'''
    if len(p) == 5:
        p[0] = ('if', p[2], p[4], None)
    else:
        p[0] = ('if', p[2], p[4], p[6])

def p_while_statement(p):
    '''while_statement : WHILE expr_bool DO statement'''
    p[0] = ('while', p[2], p[4])

def p_for_statement(p):
    '''for_statement : FOR ID ASSIGN expr_bool TO expr_bool DO statement
                    | FOR ID ASSIGN expr_bool DOWNTO expr_bool DO statement'''
    p[0] = ('for', p[2], p[4], p[5], p[6], p[8])

def p_repeat_statement(p):
    '''repeat_statement : REPEAT statement_list UNTIL expr_bool'''
    p[0] = ('repeat', p[2], p[4])


# I/O STATEMENTS

def p_write_statement(p):
    '''write_statement : WRITE LPAREN expression_list RPAREN
                      | WRITELN LPAREN expression_list RPAREN
                      | WRITELN LPAREN RPAREN
                      | WRITELN'''
    if len(p) == 2:
        p[0] = ('writeln', [])
    elif len(p) == 4:
        p[0] = ('writeln', [])
    else:
        p[0] = (p[1].lower(), p[3])

def p_read_statement(p):
    '''read_statement : READ LPAREN variable_list RPAREN
                     | READLN LPAREN variable_list RPAREN'''
    p[0] = (p[1].lower(), p[3])

def p_variable_list(p):
    '''variable_list : variable_list COMMA variable
                    | variable'''
    if len(p) == 2:
        p[0] = [p[1]]
    else:
        p[0] = p[1] + [p[3]]

def p_expression_list(p):
    '''expression_list : expression_list COMMA expr_bool
                      | expr_bool'''
    if len(p) == 2:
        p[0] = [p[1]]
    else:
        p[0] = p[1] + [p[3]]


# HIERARQUIA DE EXPRESSÕES

# Nível 1: Expressões Booleanas (operadores relacionais)
def p_expr_bool(p):
    '''expr_bool : expr
                | expr op_rel expr'''
    if len(p) == 2:
        p[0] = p[1]
    else:
        p[0] = (p[2], p[1], p[3])

def p_op_rel(p):
    '''op_rel : EQUAL
             | NEQUAL
             | LT
             | LE
             | GT
             | GE'''
    p[0] = p[1]

# Nível 2: Expressões Aritméticas (operadores aditivos)
def p_expr(p):
    '''expr : termo
           | expr op_ad termo'''
    if len(p) == 2:
        p[0] = p[1]
    else:
        p[0] = (p[2], p[1], p[3])

def p_op_ad(p):
    '''op_ad : PLUS
            | MINUS
            | OR'''
    p[0] = p[1]

# Nível 3: Termos (operadores multiplicativos)
def p_termo(p):
    '''termo : fator
            | termo op_mul fator'''
    if len(p) == 2:
        p[0] = p[1]
    else:
        p[0] = (p[2], p[1], p[3])

def p_op_mul(p):
    '''op_mul : TIMES
             | DIVIDE
             | DIV
             | MOD
             | AND'''
    p[0] = p[1]


# Nível 4: Fatores 

# Fatores são os elementos mais básicos de uma expressão. Os operadores unários +, - e NOT aplicam-se diretamente sobre um fator, 
# funcionando como inversão do sinal ou negação lógica. É definida a precedência UNARY para as regras PLUS fator e MINUS fator, 
# permitindo que o parser interprete corretamente expressões como -x + y, avaliando primeiro o operador unário

def p_fator(p):
    '''fator : const
            | variable
            | LPAREN expr_bool RPAREN
            | func_call
            | PLUS fator %prec UNARY
            | MINUS fator %prec UNARY
            | NOT fator'''
    if len(p) == 2:
        p[0] = p[1]
    elif len(p) == 4 and p[1] == '(':
        p[0] = p[2]
    else:
        p[0] = (p[1], p[2])

# Constantes
def p_const(p):
    '''const : INT
            | REALNUM
            | STRING
            | CHARLIT
            | TRUE
            | FALSE'''
    p[0] = ('const', p[1])

# Chamadas de função
def p_func_call(p):
    '''func_call : ID LPAREN expression_list RPAREN
                | ID LPAREN RPAREN
                | LENGTH LPAREN expr_bool RPAREN'''
    if len(p) == 4:
        p[0] = ('func_call', p[1], [])
    elif p[1].lower() == 'length':
        p[0] = ('func_call', 'length', [p[3]])
    else:
        p[0] = ('func_call', p[1], p[3])


# TRATAMENTO DE ERROS

def p_error(p):
    if p:
        print(f"Erro de sintaxe no token {p.type} ('{p.value}') na linha {p.lineno}")
        print(f"Posição no token: {p.lexpos}")
    else:
        print("Erro de sintaxe: fim inesperado do ficheiro")


# PARSER

parser = yacc.yacc()

# Analisa o código Pascal e retorna a árvore sintática
def parse_pascal_code(code, debug=False):
    try:
        result = parser.parse(code, debug=debug)
        return result
    except Exception as e:
        print(f"Erro durante análise: {e}")
        return None

# Analisa um ficheiro Pascal
def parse_file(filename):
    try:
        with open(filename, 'r', encoding='utf-8') as f:
            code = f.read()
        
        print(f"A analisar ficheiro: {filename}")
        result = parse_pascal_code(code)
        
        if result:
            print("Análise sintática concluída com sucesso!")
            return result
        else:
            print("Erro na análise sintática")
            return None
            
    except FileNotFoundError:
        print(f"Ficheiro '{filename}' não encontrado")
        return None
    except Exception as e:
        print(f"Erro ao ler ficheiro: {e}")
        return None

if __name__ == "__main__":
    import sys
    
    if len(sys.argv) > 1:
        filename = sys.argv[1]
        parse_file(filename)
    else:
        print("Uso: python pascal_parser.py <ficheiro.pas>")
        print("Ou importe como módulo: from pascal_parser import parse_pascal_code")