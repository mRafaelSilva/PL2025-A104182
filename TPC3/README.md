# Manifesto da Função `converter`

## Autor
Mário Rafael Figueiredo da Silva

## Data
2025-02-28

## Ficheiro
[ficheiro código](converter.py)


## Descrição
A função converter transforma texto escrito em Markdown para HTML, convertendo corretamente cabeçalhos, formatação de texto (negrito e itálico), listas numeradas, links e imagens. O programa lê um texto de entrada, e retorna a versão correspondente em HTML.

## Funcionamento

1. **Leitura do texto Markdown**: 
   O programa continua a leitura do texto, inserido no terminal, até uma linha vazia ser inserida.

2. **Conversão de Markdown para HTML**:
    Cabeçalhos #, ## e ### são convertidos para `<h1>`, `<h2>` e `<h3>`.

    - Texto em **negrito** é convertido para `<b>`...`</b>`.

    - Texto em *itálico* é convertido para `<i>`...`</i>`.

    - Listas numeradas são transformadas em elementos `<ol>` e `<li>`.

    - Links `[texto](URL)` são transformados em `<a href="URL">texto</a>`.

    - Imagens `![texto](URL)` são transformadas em `<img src="URL" alt="texto"/>`.

3. **Impressão do HTML gerado**:
    O HTML formatado é impresso no terminal.
## Exemplo
### Input:
```python
# Título Principal
## Subtítulo
### Sub-subtítulo

Texto com **negrito** e *itálico*.

1. Primeiro item
2. Segundo item
3. Terceiro item

Pagina WEB [Google](http://www.google.com).

Imagem: ![Teste](http://ola.com/img.jpg) 
```

### Saida Esperada:
```python
<h1>Título Principal</h1>
<h2>Subtítulo</h2>
<h3>Sub-subtítulo</h3>

Texto com <b>negrito</b> e <i>itálico</i>.

<ol>
<li>Primeiro item</li>
<li>Segundo item</li>
<li>Terceiro item</li>
</ol>

Pagina WEB <a href="http://www.google.com">Google</a>.

Imagem: <img src="http://ola.com/img.jpg" alt="Teste"/>
```

