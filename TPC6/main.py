from calc_lexer import tokenize
from calc_parser import parse

def main():
    while True:
        try:
            text = input(">> ")
            if text.lower() in ('exit'):
                break

            tokens = tokenize(text)
            resultado = parse(tokens)
            print(f"Resultado: {resultado}")

        except Exception as e:
            print(f"Erro: {e}")

if __name__ == "__main__":
    main()
