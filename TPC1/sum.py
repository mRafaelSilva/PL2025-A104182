def soma(texto):
    soma = 0
    comportamento = True
    numero = ""
    i = 0
    n = len(texto)

    while i < n:
        c = texto[i]

        if c == "-":
            if numero == "":
                numero = "-"
            else:
                if comportamento and numero not in ["", "-"]:
                    soma += int(numero)
                numero = "-" 
        elif c.isdigit():
            numero += c  
        else:
            if numero not in ["", "-"]:
                if comportamento:
                    soma += int(numero)
                numero = ""

            if texto[i:i+2] == "ON":
                comportamento = True
                i += 1  
            elif texto[i:i+3] == "OFF":
                comportamento = False
                i += 2  
            elif c == "=":
                print(soma)

        i += 1

    if numero not in ["", "-"]:
        if comportamento:
            soma += int(numero)

texto = "12teste34 ON56OFF 78ON90-1 = 5 OFF10 = ON20="
soma(texto)
