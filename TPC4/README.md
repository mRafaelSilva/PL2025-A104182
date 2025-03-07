# Manifesto da Função `analisador-léxico`

## Autor
Mário Rafael Figueiredo da Silva

## Data
2025-03-07

## Ficheiro
[ficheiro código](analisador-lexico.py)


## Descrição
A função "analisador-lexico" analisa e extrai tokens de uma query, identificando campos estruturais importantes. O programa lê a query de entrada e retorna uma lista de tokens já com a classificação adequada.

## Funcionamento

1. **Leitura da Query**: 
   O programa solicita ao utilizador que introduza uma query no terminal.

2. **Tokenização**:
    -Palavras-chave (select, where, LIMIT) são identificadas.

    -Variáveis (?nome, ?desc) são reconhecidas pelo prefixo ?.

    -Strings são extraídas corretamente.

    -Números (1000) são reconhecidos.

    -Símbolos especiais ({, }, ., :) são tratados adequadamente.

3. **Impressão dos Tokens**:
    A lista de tokens extraídos da query é impressa no terminal.

## Exemplo
### Input:
```python
# Título Principal
## Subtítulo
### Sub-subtítulo

select ?nome ?desc where {
?s a dbo:MusicalArtist.
?s foaf:name "Chuck Berry"@en .
?w dbo:artist ?s.
?w foaf:name ?nome.
?w dbo:abstract ?desc
} LIMIT 1000
```

### Saida Esperada:
```python
('SELECT', 'select')
('VAR', '?nome')
('VAR', '?desc')
('WHERE', 'where')
('SYMBOL', '{')
('VAR', '?s')
('ERROR', 'a')
('URI', 'dbo:MusicalArtist')
('SYMBOL', '.')
('VAR', '?s')
('URI', 'foaf:name')
('STRING', '"Chuck Berry"@en')
('SYMBOL', '.')
('VAR', '?w')
('URI', 'dbo:artist')
('VAR', '?s')
('SYMBOL', '.')
('VAR', '?w')
('URI', 'foaf:name')
('VAR', '?nome')
('SYMBOL', '.')
('VAR', '?w')
('URI', 'dbo:abstract')
('VAR', '?desc')
('SYMBOL', '}')
('LIMIT', 'LIMIT')
('NUMBER', '1000')
```

