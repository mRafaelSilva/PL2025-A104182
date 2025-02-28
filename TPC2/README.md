# Manifesto da Função `ler_csv`

## Autor
Mário Rafael Figueiredo da Silva

## Data
2025-02-25

## Ficheiro
[ficheiro código](exercicio.py)


## Descrição
A função "ler_csv" lê um ficheiro CSV e extrai os dados contidos no mesmo, tratando corretamente campos que possam estar entre aspas para evitar erros na separação dos valores. A partir destes dados, o programa realiza uma análise para identificar compositores únicos, contar a quantidade de obras por período e lista os títulos das obras de cada período.

## Funcionamento
1. **Leitura do ficheiro CSV:**: 
   O ficheiro é lido linha por linha. Os valores são separados pelo delimitador ';', tratando corretamente os campos que contêm aspas.
2. **Tratamento de campos entre aspas**:
    O programa concatena as linhas - caso haja aspas abertas - e fecha-as quando um par completo é identificado.
3. **Processamento dos dados**:
    Extrai-se a lista de compositores distintos a partir da coluna correspondente.
    Organiza-se a contagem de obras por período.
    Gera-se uma listagem das obras por período, ordenadas alfabeticamente.

## Exemplo
### Input:
```python
Título;Ano;Género;Período;Compositor
"Sinfonia nº 5";1808;Sinfonia;Clássico;Beethoven
"Requiem";1791;Requiem;Clássico;Mozart
"O Messias";1741;Oratório;Barroco;Haendel
"Concerto para Violino";1878;Concerto;Romantismo;Tchaikovsky    
```

### Saida Esperada:
```python
Lista dos compositores:
['Beethoven', 'Haendel', 'Mozart', 'Tchaikovsky']

Quantidade de obras por período:
{'Clássico': 2, 'Barroco': 1, 'Romantismo': 1}

Nome das obras de cada período:
{'Clássico': ['Requiem', 'Sinfonia nº 5'], 'Barroco': ['O Messias'], 'Romantismo': ['Concerto para Violino']}
```

