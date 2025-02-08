import re

def soma(texto):
    soma = 0
    comportamento = True

    tokens = re.findall(r'ON|OFF|=|\d+', texto, re.IGNORECASE)

    for token in tokens:
        if token.upper() == "ON":
            comportamento = True
        elif token.upper() == "OFF":
            comportamento = False
        elif token == "=":
            print(soma)
        elif comportamento:  
            soma += int(token)


texto = "12teste34 ON56OFF 78ON90 = 5 OFF10 = ON20="
soma(texto)
