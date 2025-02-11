# Manifesto da Função `soma`

## Autor
Mário Rafael Figueiredo da Silva

## Data
2025-02-8

## Ficheiro
[ficheiro código](sum.py)


## Descrição
A função "soma" lê uma string com o objetivo de somar todos os algarismos presentes na mesma. Este comportamente deve ser desativado quando se encontra o comando "OFF" e novamente ativado se o comando for "ON". Sempre que surgir o caracter "=" deve ser impresso o valor somado até ao momento.

## Funcionamento
1. **Leitura de números**: 
A função percorre a string, caracter por caracter, e acumula algarismos consecutivos para formar números completos. Também são tratados números negativos cajo surja o caracter "-" antes do mesmo.
2. **Controlo da Soma**:
   Inicialmente o comportamento é iniciado como "True". Quando a função depara-se com um "OFF" este comportamento é alterado para "False" e deixa de realizar quaisquer somas.
3. **Processamento dos números**:
   O processamento dos números dá-se assim que é encontrado um caracter diferente de um algarismo.

## Exemplo
### Input:
```python
texto = "12teste34 ON56OFF 78ON90 = 5 OFF10 = ON20="
soma(texto)
```

### Saida Esperada:
```python
191
196
216
```

