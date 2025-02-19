def ler_csv(ficheiro):
    with open(ficheiro, 'r', encoding='utf-8') as f:
        linhas = f.readlines()

    cabecalho = linhas[0].strip().split(';')  
    dados = []

    temp_linha = "" 
    dentro_aspas = False  
    linhas_completas = []  

    for linha in linhas[1:]: 
        linha = linha.rstrip()

        if dentro_aspas:
            temp_linha += " " + linha  
        else:
            temp_linha = linha  

        qtd_aspas = temp_linha.count('"')

        if qtd_aspas % 2 == 0:
            linhas_completas.append(temp_linha)
            dentro_aspas = False
        else:
            dentro_aspas = True

    for linha in linhas_completas:
        valores = []
        temp = ""
        dentro_campo_aspas = False

        for i, char in enumerate(linha):            
            if char == '"':
                if i < len(linha) - 1 and linha[i + 1] == '"':  
                    temp += '"' 
                else:
                    dentro_campo_aspas = not dentro_campo_aspas
            elif char == ';' and not dentro_campo_aspas:
                valores.append(temp.strip())  
                temp = ""  
            else:
                temp += char  
        valores.append(temp.strip())  
        dados.append(valores)

    return cabecalho, dados


def processar_dados(dados):
    compositores = sorted(set(dado[4] for dado in dados if len(dado) > 4)) 

    obras_por_periodo = {}
    for dado in dados:
        if len(dado) >= 4:
            periodo = dado[3]
            titulo = dado[0]

            if periodo not in obras_por_periodo:
                obras_por_periodo[periodo] = []
            obras_por_periodo[periodo].append(titulo)

    obras_por_periodo = {p: sorted(obras) for p, obras in obras_por_periodo.items()}
    contagem_por_periodo = {p: len(obras) for p, obras in obras_por_periodo.items()}

    return compositores, contagem_por_periodo, obras_por_periodo


def main():
    ficheiro = "obras.csv"
    cabecalho, dados = ler_csv(ficheiro)

    compositores, contagem_por_periodo, obras_por_periodo = processar_dados(dados)

    print("Lista dos compositores:\n")
    print(compositores)

    print("\n\nQuantidade de obras por período:\n")
    print(contagem_por_periodo)

    print("\n\nNome das obras de cada período:\n")
    print(obras_por_periodo)


if __name__ == "__main__":
    main()
