from datetime import date
from maquinaVenda import MaquinaVenda

def main():
    maquina = MaquinaVenda()
    hoje = date.today().strftime("%Y-%m-%d")
    print(f"maq: {hoje}, Stock carregado, Estado atualizado.")
    print("maq: Bom dia. Estou disponível para atender o seu pedido.")
    
    while True:
        comando = input(">> ").strip().upper()
        if comando == "SAIR":
            maquina.return_change()
            print("maq: Até à próxima")
            break
        maquina.process_command(comando)

if __name__ == "__main__":
    main()