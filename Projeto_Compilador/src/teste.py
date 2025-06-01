from pascal_lex import lexer
from pascal_sin import parser
from pascal_semantic import SemanticAnalyzer
from code_generator import generate_code_from_ast

# Lê o ficheiro teste.pas
with open('teste.pas', 'r') as f:
    code = f.read()

# Testa o lexer primeiro
print("=== TOKENS ===")
lexer.input(code)
while tok := lexer.token():
    print(tok)

print("\n=== PARSING ===")
# Testa o parser
result = parser.parse(code)
if result:
    print("Parsing successful!")
    print("AST:", result)
else:
    print("Parsing failed!")

print("\n=== ANÁLISE SEMÂNTICA ===")
if result:
    sem = SemanticAnalyzer()
    erro = sem.analyze(result)

    if erro:
        print("Foram encontrados erros semânticos:")
        for e in sem.errors:
            print("-", e)
        print("\nCódigo não foi gerado")
    else:
        print("\n=== GERAÇÃO DE CÓDIGO ===")
        generated_code = generate_code_from_ast(result)

        with open("codigo.txt", "w") as out_file:
            out_file.write(generated_code)
            print("Código guardado em 'codigo.txt'\n")
else:
    print("Sem análise semântica (sintaxe falhou)")
