# Manifesto da Função `soma`

## Autor
Mário Rafael Figueiredo da Silva

## Data
2025-02-08


## Descrição
A função `soma` lê uma string com o objetivo de somar todos os algarismos presentes na mesma. Este comportamente deve ser desativado quando se encontra o comando "OFF" e novamente ativado se o comando for "ON". Sempre que surgir o caracter "=" deve ser impresso o valor somado até ao momento.

## Funcionamento
1. **Identificação inicial de tokens**: Fazemos uso de expressões regulares para retirar os comandos especiais e os algarismos.
2. **Processamento dos tokens**:
   - Se o token for um número e o modo de soma estiver ativo, o valor é adicionado à soma total.
   - Se o token for `=`, a soma acumulada até aquele momento é imprimida no terminal.

## Exemplo
### Input:
```python
texto = "12teste34 ON56OFF 78ON90 = 5 OFF10 = ON20="
soma(texto)

