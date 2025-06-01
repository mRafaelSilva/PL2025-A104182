<p align="center">
  <img src="capa.png" alt="Capa do Relatório" width="300"/>
</p>

<h2 align="center">Universidade do Minho</h2>

<h3 align="center">Unidade Curricular de Processamento de Linguagens</h3>
<h4 align="center">Ano Letivo 2024/2025</h4>

<p align="center">
  <strong>Engenharia Informática</strong>
</p>

<br/>

<h2 align="center">Construção de um Compilador para Pascal Standard</h2>

<br/><br/>

### Grupo 38:

- **Filipa Oliveira da Silva** (A104167)  
- **Maria Cleto Rocha** (A104441)  
- **Mário Rafael Figueiredo da Silva** (A104182)

<br/><br/>


## **1. Introdução**

O presente relatório descreve o desenvolvimento e a construção de um compilador da linguagem **Pascal**, realizado no âmbito da unidade curricular **Processamento de Linguagens**. O principal objetivo do projeto foi aplicar, de forma prática, os conhecimentos teóricos adquiridos ao longo do semestre — desde a definição formal de linguagens até à implementação das fases clássicas de um compilador: **análise léxica**, **sintática** e **semântica**, entre outras.

 O compilador foi desenvolvido em **Python**, recorrendo à biblioteca **PLY (Python Lex-Yacc)**, que permite a construção de analisadores léxicos e sintáticos baseados em expressões regulares e gramáticas LALR(1), respetivamente.

O projeto foi desenvolvido de forma modular e em grupo, com a responsabilidade dividida entre os membros. 

A arquitetura do compilador é composta pelas seguintes fases:

- **Análise léxica**: responsável por reconhecer os tokens da linguagem (identificadores, operadores, palavras reservadas, etc.), convertendo o código-fonte numa sequência de unidades lexicais;
- **Análise sintática**: responsável por validar a estrutura gramatical do programa, construindo uma **árvore sintática abstrata (AST)** baseada nas regras da gramática;
- **Análise semântica**: responsável por verificar se o programa respeita regras contextuais da linguagem.

O compilador suporta **variáveis de tipos básicos** (`integer`, `boolean`, `string`), **arrays unidimensionais**, **funções e procedimentos com parâmetros**, bem como estruturas de controlo como `if`, `while`, `for`, e chamadas a funções e instruções de entrada/saída (`read`, `write`, entre outras).

<br/><br/>


## **2. Análise Léxica**

&nbsp;&nbsp;&nbsp;&nbsp;Após uma pesquisa dos elementos que poderiam surgir num código pascal, decidimos criar os seguintes tokens:


### **2.1. Tokens**
```python
# bloco principal
  'PROGRAM', 'BEGIN', 'END',

# tipos e variáveis
  'VAR', 'ARRAY', 'OF', 'INTEGER', 'REAL', 'BOOLEAN', 'CHAR', 'STRINGTYPE',

# controlo de decisões
  'IF', 'THEN', 'ELSE',
  'WHILE', 'DO',
  'FOR', 'TO', 'DOWNTO',
  'REPEAT', 'UNTIL',

# funções e procedimentos
  'FUNCTION', 'PROCEDURE',

# input e output
  'WRITELN', 'WRITE', 'READLN', 'READ',

  'LENGTH',

# operadores
  'ASSIGN', 'PLUS', 'MINUS', 'TIMES', 'DIVIDE',
  'EQUAL', 'NEQUAL', 'LT', 'LE', 'GT', 'GE',
  'MOD', 'DIV',
  'AND', 'OR', 'NOT',

# símbolos
  'LPAREN', 'RPAREN',
  'LBRACKET', 'RBRACKET',
  'COLON', 'SEMICOLON', 'DOT', 'COMMA',

  'ID', 'INT', 'REALNUM', 'STRING', 'CHARLIT',

  'TRUE', 'FALSE',

# comentários
  'COMMENT'
```
A definição dos tokens é fundamental para que o analisador léxico consiga reconhecer os diversos elementos da *linguagem Pascal*. De forma a explicar melhor o porquê de termos criado cada um destes, decidimos dividi-los por grupos baseando-se no contexto.

- *Bloco principal:* os tokens ```PROGRAM, BEGIN e END``` delimitam a estrutura base de um programa Pascal. São importantes para marcar o início e o fim do código executável.
- *Tipos e variáveis:* os tokens ```VAR, ARRAY, OF, INTEGER, REAL, BOOLEAN, CHAR e STRINGTYPE``` permitem reconhecer declarações de variáveis e os tipos.
- *Controlo de decisões:* tokens como ```IF, THEN, ELSE, WHILE, DO, FOR, TO, DOWNTO, REPEAT e UNTIL``` representam instruções de decisão e loops.
- *Funções e procedimentos:* os tokens ```FUNCTION e PROCEDURE``` servem para identificar outros blocos de código. Apesar de os termos definido, não conseguimos torna-los funcionais quando geramos código.
- *Entrada e saída:* ```WRITELN, WRITE, READLN e READ``` são tokens específicos para operações de input/output.
- *Outros auxiliares:* o token ```LENGTH``` foi incluído para suportar operações comuns sobre strings e arrays.
- *Operadores:* os tokens como ```ASSIGN, PLUS, MINUS, DIVIDE, MOD, AND, OR```,entre outros, cobrem as operações aritméticas, relacionais e lógicas.
- *Símbolos e literais:* tokens como ```LPAREN, COLON, COMMA, STRING, CHARLIT, INT e REALNUM``` representam os símbolos de pontuação, constantes e identificadores.
- *Booleanos:* ```TRUE e FALSE``` são os valores true e false que surgem como bool.
- *Comentários:* o token ```COMMENT``` permite que o lexer reconheça e ignore texto comentado.


### **2.2. Estados**

Além disso, definimos também um estado para comentário, podendo assim ler os comentários do género "(*...*)" e não causar problemas com interpretações erradas.
```
states = (
    ('comment', 'exclusive'),
)
```
A <b>gestão dos estados</b> é feita através das funções <b>t_LPAREN_STAR(), t_comment_LPAREN_STAR() e t_comment_STAR_RPAREN()</b> que servem para, iniciar, prolongar e sair do estado respetivamente.

### **2.3. Regras**

<div align="center">

| Função           | Expressão Regex                     |
|------------------|--------------------------------------|
| `t_PROGRAM`      | `[Pp][Rr][Oo][Gg][Rr][Aa][Mm]`       |
| `t_FUNCTION`     | `[Ff][Uu][Nn][Cc][Tt][Ii][Oo][Nn]`    |
| `t_PROCEDURE`    | `[Pp][Rr][Oo][Cc][Ee][Dd][Uu][Rr][Ee]` |
| `t_BEGIN`        | `[Bb][Ee][Gg][Ii][Nn]`               |
| `t_DOWNTO`       | `[Dd][Oo][Ww][Nn][Tt][Oo]`           |
| `t_REPEAT`       | `[Rr][Ee][Pp][Ee][Aa][Tt]`           |
| `t_WRITELN`      | `[Ww][Rr][Ii][Tt][Ee][Ll][Nn]`       |
| `t_INTEGER`      | `[Ii][Nn][Tt][Ee][Gg][Ee][Rr]`       |
| `t_BOOLEAN`      | `[Bb][Oo][Oo][Ll][Ee][Aa][Nn]`       |
| `t_STRINGTYPE`   | `[Ss][Tt][Rr][Ii][Nn][Gg]`           |
| `t_LENGHT`      | `[Ll][Ee][Nn][Gg][Tt][Hh]`       |
| `t_READLN`     | `[Rr][Ee][Aa][Dd][Ll][Nn]`    |
| `t_ARRAY`    | `[Aa][Rr][Rr][Aa][Yy]` |
| `t_UNTIL`        | `[Uu][Nn][Tt][Ii][Ll]`               |
| `t_FALSE`       | `[Ff][Aa][Ll][Ss][Ee]`           |
| `t_WRITE`       | `[Ww][Rr][Ii][Tt][Ee]`           |
| `t_WHILE`      | `[Ww][Hh][Ii][Ll][Ee]`       |
| `t_THEN`      | `[Tt][Hh][Ee][Nn]`       |
| `t_ELSE`      | `[Ee][Ll][Ss][Ee]`       |
| `t_TRUE`   | `[Tt][Rr][Uu][Ee]`           |
| `t_REAL`      | `[Rr][Ee][Aa][Ll]`       |
| `t_CHAR`     | `[Cc][Hh][Aa][Rr]`    |
| `t_READ`    | `[Rr][Ee][Aa][Dd]` |
| `t_END`        | `[Ee][Nn][Dd]`               |
| `t_VAR`       | `[Vv][Aa][Rr]`           |
| `t_FOR`       | `[Ff][Oo][Rr]`           |
| `t_AND`      | `[Aa][Nn][Dd]`       |
| `t_NOT`      | `[Nn][Oo][Tt]`       |
| `t_DIV`      | `[Dd][Ii][Vv]`       |
| `t_MOD`   | `[Mm][Oo][Dd]`           |
| `t_IF`      | `[Ii][Ff]`       |
| `t_OF`     | `[Oo][Ff]`    |
| `t_OR`    | `[Oo][Rr]` |  
| `t_DO`        | `[Dd][Oo]`|
| `t_TO`       | `[Tt][Oo]` |
| `t_COMMENT`     | `\{[^}]*\}`|
| `t_LPAREN_STAR`    | `\(\*` |  
| `t_comment_LPAREN_STAR`        | `\(\*`|
| `t_comment_STAR_RPAREN`       | `\*\)`|
| `t_comment_newline`    | `\n+` |  
| `t_comment_content`        | `[^(*\*)\n]`|
</div>

Para além destas, também temos as regras de todos os operadores e símbolos possiveís <b>(" :-, +, <>, ; "...)</b> definidas.

Após confirmarmos o bom funcionamento desta abordagem, fazendo uso dos exemplos fornecidos pela equipa docente, avançamos para a análise sintática.


## 3. Análise Sintática
O analisador sintático é responsável por verificar se a sequência de tokens produzida pelo analisador léxico segue a sintaxe da linguagem Pascal. Para isso, foi utilizada a biblioteca **PLY** (Python Lex-Yacc) que implementa um parser **LALR(1)**. Este tipo de parser oferece a geração automática de tabelas de análise sintática, deteção de *conflitos shift/reduce e reduce/reduce*, mecanismos de tratamento de erros e suporte a precedências. 

### 3.1. Gramática 

#### 1. Programa Principal
```
Programa → PROGRAM ID SEMICOLON Declaracoes Comando_composto DOT
         | PROGRAM ID SEMICOLON Comando_composto DOT
```
#### 2. Declarações
```
Declaracoes → Declaracoes Declaracao
            | Declaracao

Declaracao → Declaracao_var
           | Declaracao_funcao
           | Declaracao_procedimento
```
#### 3. Declaração de variáveis
```
Declaracao_var → VAR Lista_var

Lista_var → Lista_var Especificacao_var
          | Especificacao_var

Especificacao_var → Lista_id COLON Especificacao_tipo SEMICOLON

Lista_id → Lista_id COMMA ID
         | ID

Especificacao_tipo → INTEGER | REAL | BOOLEAN | CHAR | STRINGTYPE | Tipo_array

Tipo_array → ARRAY LBRACKET INT DOT DOT INT RBRACKET OF Especificacao_tipo
```
#### 4. Funções e Procedimentos
```
Declaracao_funcao → Cabecalho_funcao Declaracoes Comando_composto SEMICOLON
                  | Cabecalho_funcao Comando_composto SEMICOLON

Cabecalho_funcao → FUNCTION ID LPAREN Lista_parametros RPAREN COLON Especificacao_tipo SEMICOLON
                 | FUNCTION ID COLON Especificacao_tipo SEMICOLON

Declaracao_procedimento → Cabecalho_procedimento Declaracoes Comando_composto SEMICOLON
                        | Cabecalho_procedimento Comando_composto SEMICOLON

Cabecalho_procedimento → PROCEDURE ID LPAREN Lista_parametros RPAREN SEMICOLON
                       | PROCEDURE ID SEMICOLON

Lista_parametros → Lista_parametros SEMICOLON Especificacao_parametro
                 | Especificacao_parametro

Especificacao_parametro → Lista_id COLON Especificacao_tipo
```
#### 5. Comandos
```
Comando_composto → BEGIN Lista_comandos END

Lista_comandos → Lista_comandos SEMICOLON Comando
               | Comando
               | ε

Comando → Atribuicao
        | Procedimento
        | Comando_composto
        | If
        | While
        | For
        | Repeat
        | Write
        | Read
        | ε
```
#### 6. Tipos de Comandos Específicos
```
Atribuicao → Variavel ASSIGN Expressao_bool

Variavel → ID
         | ID LBRACKET Expressao_bool RBRACKET

Procedimento → ID LPAREN Lista_expressoes RPAREN
             | ID LPAREN RPAREN
             | ID

If → IF Expressao_bool THEN Comando
   | IF Expressao_bool THEN Comando ELSE Comando

While → WHILE Expressao_bool DO Comando

For → FOR ID ASSIGN Expressao_bool TO Expressao_bool DO Comando
    | FOR ID ASSIGN Expressao_bool DOWNTO Expressao_bool DO Comando

Repeat → REPEAT Lista_comandos UNTIL Expressao_bool

Write → WRITE LPAREN Lista_expressoes RPAREN
      | WRITELN LPAREN Lista_expressoes RPAREN
      | WRITELN LPAREN RPAREN
      | WRITELN

Read → READ LPAREN Lista_variaveis RPAREN
     | READLN LPAREN Lista_variaveis RPAREN

Lista_variaveis → Lista_variaveis COMMA Variavel
                | Variavel

Lista_expressoes → Lista_expressoes COMMA Expressao_bool
                 | Expressao_bool
```
#### 7. Expressões
```
Expressao_bool → Expressao
               | Expressao Operador_relacional Expressao

Operador_relacional → EQUAL | NEQUAL | LT | LE | GT | GE

Expressao → Termo
          | Expressao Operador_aditivo Termo

Operador_aditivo → PLUS | MINUS | OR

Termo → Fator
      | Termo Operador_multiplicativo Fator

Operador_multiplicativo → TIMES | DIVIDE | DIV | MOD | AND

Fator → Constante
      | Variavel
      | LPAREN Expressao_bool RPAREN
      | Funcao
      | PLUS Fator
      | MINUS Fator
      | NOT Fator

Constante → INT | REALNUM | STRING | CHARLIT | TRUE | FALSE

Funcao → ID LPAREN Lista_expressoes RPAREN
       | ID LPAREN RPAREN
       | LENGTH LPAREN Expressao_bool RPAREN
```
### 3.2. Implementação das Produções
Cada produção da gramática foi implementada como uma função Python, seguindo a convenção do PLY, onde o nome da função começa por ```p_``` seguido do nome do *não-terminal*. A produção em si é descrita na *docstring* da função, e a ação semântica correspondente é definida no corpo da função. Esta ação constrói um nó da **árvore sintática abstrata** (AST), utilizando tuplos para representar estruturas compostas.
Por exemplo, a produção responsável pela definição de arrays é:
```python
def p_array_type(p):
    '''array_type : ARRAY LBRACKET INT DOT DOT INT RBRACKET OF type_spec'''
    p[0] = ('array_type', p[3], p[6], p[9])
```
Esta regra permite reconhecer declarações como ```array[1..10] of integer``` e gerar o nó ```('array_type', 1, 10, 'integer')``` na árvore sintática. 

### 3.3. Precedências
Foi necessário definir explicitamente a precedência dos operadores para evitar ambiguidades e garantir que a análise sintática reflete a semântica correta das expressões. Isto é feito através da diretiva ```precedence``` fornecida pelo PLY:
```python
precedence = (
    ('right', 'ELSE'),        
    ('left', 'OR'),
    ('left', 'AND'),
    ('right', 'NOT'),
    ('left', 'EQUAL', 'NEQUAL', 'LT', 'LE', 'GT', 'GE'),
    ('left', 'PLUS', 'MINUS'),
    ('left', 'TIMES', 'DIVIDE', 'DIV', 'MOD'),
    ('right', 'UNARY'),       
)
```
Esta ordem estabelece uma hierarquia entre:
- operadores relacionais (```=```,```<```,```>```, etc.);
- operadores lógicos (```and```, ```or```, ```not```);
- operadores aritméticos (```+```, ```-```, ```*```, ```/```, ```div```, ```mod```);
- operadores unários (```+```, ```-``` aplicados a um único operando);

A distinção entre operadores *binários* e *unários* é particularmente importante na regra **fator**, onde os operadores ```+```, ```-``` e ```not``` podem atuar sobre uma única expressão:
```python
def p_fator(p):
    '''fator : const
            | variable
            | LPAREN expr_bool RPAREN
            | func_call
            | PLUS fator %prec UNARY
            | MINUS fator %prec UNARY
            | NOT fator'''
    if len(p) == 2:
        p[0] = p[1]
    elif p[1] == '(':
        p[0] = p[2]
    else:
        p[0] = (p[1], p[2])
```
Aqui, o uso de ```%prec UNARY``` indica explicitamente que o ```PLUS``` e o ```MINUS``` usados nesta produção têm a precedência definida pelo símbolo ```UNARY```, que está mais acima na hierarquia que os operadores binários correspondentes. O uso adequado de precedências evita conflitos *shift/reduce* e assegura que a estrutura sintática das expressões é coerente com a semântica esperada da linguagem.

### 3.4. Construção da AST
A **AST** é construída de forma incremental durante a análise sintática, onde cada produção contribui com um nó que representa a construção correspondente do programa. A árvore gerada contém apenas informação relevante para as fases seguintes do compilador, como a análise semântica e geração de código.

### 3.5. Tratamento de Erros
O analisador sintático inclui uma função ```p_error``` que permite identificar erros de sintaxe e reportá-los de forma clara:
```python
def p_error(p):
    if p:
        print(f"Erro de sintaxe no token {p.type} ('{p.value}') na linha {p.lineno}")
    else:
        print("Erro de sintaxe: fim inesperado do ficheiro")
```
Este mecanismo permite detetar tokens inesperados, estruturas incompletas ou fins de ficheiros prematuros. Desta forma, o compilador consegue interromper a análise com uma mensagem informativa.


## 4. Análise Semântica

No nosso trabalho, a análise semântica é uma fase fundamental do processo de compilação, pois verifica a **a declaração de variáveis, o tipo de dados e a coerência do código** de um programa, garantindo dessa maneira que está em conformidade com as regras semânticas da linguagem ***Pascal***. Esta etapa completa a análise léxica e sintática feitas anteriormente, detetando erros que não são visíveis apenas com base na estrutura do código.

No compilador, a análise semântica foi implementada na classe `SemanticAnalyzer`, que percorre a **árvore sintática abstrata (AST)** gerada pelo parser e valida os seguintes aspetos:

- Declaração e uso correto de variáveis;
- Verificação de tipos em expressões e atribuições;
- Verificação de chamadas a funções e procedimentos;
- Coerência no acesso a arrays e strings;
- Correção de operações aritméticas, relacionais e lógicas.

---

### 4.1. Estrutura da Análise

A classe `SemanticAnalyzer` mantém duas estruturas principais de suporte:

- ***symbols***: uma tabela de símbolos (dicionário) onde são guardadas as variáveis declaradas e os seus tipos.
- ***functions***: uma tabela de funções, com os seus parâmetros e tipo de retorno. Inicialmente, inclui a função built-in ***length***.

A análise começa no nó principal `program` da AST. A travessia da árvore é realizada com funções auxiliares, tais como `visit_declarations`, `visit_statement` e `visit_expr`, que processam recursivamente cada subestrutura do programa.

---

### 4.2. Declaração de Variáveis e Visibilidade

Cada variável é registada na tabela de símbolos com o respetivo tipo, sendo verificada a duplicação de nomes. Por exemplo, no seguinte código Pascal:

```pascal
var x: integer;
    x: boolean;
```

Gera o erro:
```
Erro: variável 'x' já declarada
```

No caso das funções, os parâmetros são registados como variáveis locais. Ao entrar no corpo da função, o analisador guarda a tabela de símbolos anterior, adiciona os novos símbolos e, no final, restaura o contexto anterior, respeitando e certificando dessa forma que **cada função tem, de facto, as suas próprias variáveis**.

---

### 4.3. Atribuições e Verificação de tipos

A função `check_assignment` valida se a variável à esquerda de uma atribuição foi realmente declarada e se o tipo da expressão à direita é de facto compatível com o tipo da variável.

Por exemplo, neste excerto de código:

```pascal
var x: integer;
begin
  x := true;
end.
```

A saída do analisador:
```
Erro: incompatibilidade de tipos em 'x := ...' (integer ← boolean)
```

Esta verificação cobre tanto variáveis simples como acessos a arrays:
```pascal
var a: array[1..5] of integer;
begin
  a[1] := 'abc';
end.
```

Erro detetado:
```
Erro: incompatibilidade de tipos em 'a := ...' (integer ← string)
```

---

### 4.4. Expressões e Operadores

A função `visit_expr` trata expressões compostas, como operações binárias e unárias, validando dessa forma:

- Tipos compatíveis nos operandos;
- Operações permitidas para cada tipo;
- Resultado esperado da operação.

Por exemplo:
```pascal
var b: boolean;
begin
  b := 1 + true;
end.
```

Origina:
```
Erro: operação aritmética '+' entre tipos incompatíveis: integer e boolean
```

Além disso, operações lógicas como `and`, `or` e `not` são verificadas para garantir que recebem apenas operandos booleanos:
```pascal
var x: integer;
begin
  if x and true then
    writeln('erro');
end.
```

Erro:
```
Erro: operação lógica 'and' entre tipos incompatíveis: integer e boolean
```

---

### 4.5. Chamadas a Funções e Procedimentos

As chamadas a funções são validadas com base na tabela `functions`, verificando:

- Existência da Função;
- Número de Argumentos;
- Tipos dos Argumentos.

Por exemplo:
```pascal
var s: string;
begin
  writeln(length(123));
end.
```

Saída:
```
Erro: tipo do argumento 1 de 'length' é integer, esperado string
```

Além disso, o compilador também impede redefinições de funções:
```pascal
function length(x: string): integer;
begin
  length := 0;
end;
```

Erro:
```
Erro: função 'length' já foi definida
```

---

### 4.6. Instruções de Entrada e Saída

As instruções `read`, `readln`, `write` e `writeln` são também tratadas semanticamente. No caso da leitura (`read`, `readln`), o argumento deve ser uma **variável existente**, caso contrário é gerado erro:

```pascal
begin
  read(x);
end.
```

Resultado:
```
Erro: variável 'x' não declarada
```

Na escrita (`write`, `writeln`), os argumentos são processados como expressões, e os tipos não precisam de ser homogéneos, mas devem ser válidos.

## **5. Conversão para código**

&nbsp;&nbsp;&nbsp;&nbsp;Depois de todas as confirmações feitas podemos passar para a conversão de código. Nesta etapa, recebemos o resultado que a análise sintática devolve e, a partir daí, começamos a criar a sequência de instruções que deve ser passada ao EMWVM. 
Ao iniciar a classe, definimos as seguintes variáveis:
<b>

```python
  self.code = [] // guardamos aqui o código gerado
  self.label_counter = 0 // para gerar as labels únicas
  self.local_vars = {}  // dicionários, valor é offset
  self.global_vars = {}  // 
  self.var_types = {} // tipos
  self.array_info = {} // limites e tipo
  self.functions = {}    
  self.current_scope = 'global'
  self.local_offset = 0
  self.global_offset = 0
```

Inicialmente começamos por passar a árvore completa à função visit. Esta função é a responsável pela lógica central da geração de código uma vez que chama a função adequada para gerar as instruções.
</b>

<b>

### 5.1. Funções gerais

```python
  def visit(self, node):
      """Visita o nodo"""
      if isinstance(node, tuple):
          node_type = node[0]
          
          # Se for um operador
          if node_type in ['+', '-', '*', '/', 'div', 'mod', '=', '<>', '<', '<=', '>', '>=', 'and', 'or']:
              return self.visit_binary_op(node)
          
          # outros métodos
          method_name = f"visit_{node_type}"
          if hasattr(self, method_name):
              return getattr(self, method_name)(node)
          else:
              raise Exception(f"Unknown node type: {node_type}")
      elif isinstance(node, list):
          for item in node:
              self.visit(item)
      else:
          return node
```
</b>

Uma vez que, nos nossos exemplos, todas as funções iniciam com a palavra <b> program </b>, segue também, em seguida, a definição da função <b> visit_program ():


```python
  def visit_program(self, node):
      """Visit program node: ('program', name, declarations, compound_statement)"""
      _, name, declarations, compound_stmt = node
      
      # inicializar os pointers da stack
      self.emit("pushi 0")  # reserva espaço 
      self.emit("pushi 0")  # reserva base frame, Assim dá para escrever e ler sem colisão.
      self.emit("start") # inicializa FP
      
      # processar declarações de variaveis
      if declarations:
          for decl in declarations:
              self.visit(decl)
      
      # processa o código
      self.visit(compound_stmt)
```
</b>

Nesta função, começamos por reservar espaço para não ocorrem conflitos e colisões e, de seguida, reservamos o local do FP para definir o início do bloco das variáveis. Com a emissão do <b> start </b>, inicializamos o FP.
Depois de todas estas etapas passamos para o processamento das declarações de variáveis e do restante código.

De forma a não tornar o relatório muito extensivo optamos por não colocar aqui todas as funções <b> "visit" </b> e apenas iremos abordar as mais importantes, como ,por exemplo, o loop for.

### 5.2. visit_for

A função <b> visit_for </b> trata da geração de código para ciclos for. Primeiro, avalia-se o valor inicial e guarda-se na variável de controlo. Depois, criam-se duas labels: uma para o início do ciclo e outra para o final (para saber onde saltar caso a condição falhe).

```python
  # Inicializar variável de controlo
  self.visit(start)
  if var in self.local_vars:
      self.emit(f"storel {self.local_vars[var]}")
  else:
      self.emit(f"storeg {self.global_vars[var]}")

  loop_label = self.new_label("label")
  end_label = self.new_label("label")

  self.emit(f"{loop_label}:")
```

    A seguir, gera-se a condição que verifica se a variável já atingiu o valor final. No caso de <b>to</b>, verifica se a variável é menor ou igual (infeq); no caso de <b>downto</b>, se é maior ou igual (supeq). Se a condição for falsa, salta diretamente para o final do ciclo.

    Se a condição for verdadeira, executa-se o corpo do ciclo. Depois, incrementa-se ou decrementa-se a variável de controlo, conforme o tipo de ciclo. Por fim, volta-se a saltar para o início do ciclo para repetir o processo. Quando a condição já não for satisfeita, o programa segue para a label final, saindo do ciclo.

```python
# Condição: i <= end ou i >= end
if var in self.local_vars:
    self.emit(f"pushl {self.local_vars[var]}")
else:
    self.emit(f"pushg {self.global_vars[var]}")
self.visit(end)

if direction == 'to':
    self.emit("infeq")
elif direction == 'downto':
    self.emit("supeq")
else:
    raise Exception(f"Erro no for: {direction}")

self.emit(f"jz {end_label}")

# Corpo do ciclo
self.visit(body)

# Incrementar/diminuir
if var in self.local_vars:
    self.emit(f"pushl {self.local_vars[var]}")
else:
    self.emit(f"pushg {self.global_vars[var]}")

self.emit("pushi 1")
if direction == 'to':
    self.emit("add")
else:
    self.emit("sub")

if var in self.local_vars:
    self.emit(f"storel {self.local_vars[var]}")
else:
    self.emit(f"storeg {self.global_vars[var]}")

self.emit(f"jump {loop_label}")
self.emit(f"{end_label}:")
```

Para além das que já foram mencionadas anteriormente, o nosso código está adaptado para lidar com todas as funcionalidades mais simples <b>(+, -, *, /, <=..)</b> como também com os if's, constantes, arrays, assigns...

É importante referir que, apesar de captarmos os tokens e realizarmos a sintática dos procedures e das funções, não nos foi possível implementar essa funcionalidade nesta fase de geração de código.

## 7. Conclusão

Em suma, a implementação deste Compilador para Pascal constituiu uma excelente oportunidade para aplicar de forma concreta os conceitos teóricos abordados na respetiva unidade curricular. Foi possível compreender em profundidade o funcionamento interno de um compilador, desde a leitura do código-fonte até à verificação das suas propriedades semânticas.

Cada fase revelou desafios distintos: 
- a **análise léxica** exigiu modelação precisa dos padrões lexicais; 
- **a análise sintática** obrigou à definição de uma gramática LALR(1) adequada; 
- e a **análise semântica** assegurou a coerência contextual através da verificação de declarações, tipos e chamadas a funções. 


Apesar do bom funcionamento nas três fases principais, não foi possível concluir a 100% a geração de código simbólico para a Máquina Virtual, especialmente a funcionalidade do Exemplo 7. Esta extensão revelou-se mais complexa, exigindo infraestrutura adicional para integração com a AST e ambientes semânticos.

Por fim, acreditamos que o projeto cumpriu os objetivos essenciais, demonstrando que a arquitetura está preparada para extensões futuras. Foi uma experiência fundamental para consolidar conhecimentos sobre compiladores, linguagens formais e programação modular.
