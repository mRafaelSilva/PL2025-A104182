def check(tokens, pos, token_type):
    if tokens[pos][0] == token_type:
        return pos + 1
    else:
        raise ValueError("Erro 2")

def factor(tokens, pos):
    token = tokens[pos]
    if token[0] == 'NUM':
        valor = int(token[1])
        pos = check(tokens, pos, 'NUM')
        return valor, pos
    elif token[0] == 'AP':
        pos = check(tokens, pos, 'AP')
        resultado, pos = expr(tokens, pos)
        pos = check(tokens, pos, 'FP')
        return resultado, pos
    else:
        raise ValueError("Erro 1")

def term(tokens, pos):
    resultado, pos = factor(tokens, pos)
    while tokens[pos][0] in ('MULT', 'DIV'):
        op = tokens[pos][0]
        pos = check(tokens, pos, op)
        valor, pos = factor(tokens, pos)
        if op == 'MULT':
            resultado *= valor
        else:
            resultado //= valor  
    return resultado, pos

def expr(tokens, pos):

    resultado, pos = term(tokens, pos)
    while tokens[pos][0] in ('SOM', 'SUB'):
        op = tokens[pos][0]
        pos = check(tokens, pos, op)
        valor, pos = term(tokens, pos)
        if op == 'SOM':
            resultado += valor
        else:
            resultado -= valor
    return resultado, pos

def parse(tokens):
    resultado, pos = expr(tokens, 0)
    if tokens[pos][0] != 'EOF':
        raise ValueError("Erro 3")
    return resultado
