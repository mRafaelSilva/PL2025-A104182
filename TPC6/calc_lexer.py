import re

PADROES_TOKENS = [
    (r'\d+', 'NUM'),      
    (r'\+', 'SOM'),       
    (r'-', 'SUB'),         
    (r'\*', 'MULT'),       
    (r'/', 'DIV'),         
    (r'\(', 'AP'),     
    (r'\)', 'FP')      
]

def tokenize(texto):
    tokens = []
    while texto:
        texto = texto.lstrip()
        for padrao, tipo in PADROES_TOKENS:
            match = re.match(padrao, texto)
            if match:
                tokens.append((tipo, match.group()))
                texto = texto[len(match.group()):]
                break
        else:
            raise ValueError(f"Caractere inválido: {texto[0]}")
    tokens.append(("EOF", ""))
    return tokens
