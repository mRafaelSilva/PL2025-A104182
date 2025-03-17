import json
import ply.lex as lex
import re
from produto import Produto

class MaquinaVenda:
    def __init__(self):
        self.stock = []
        self.balance = 0
        self.load_stock()
        self.lexer = self.build_lexer()
    
    def build_lexer(self):
        tokens = ('LISTAR', 'MOEDA', 'SELECIONAR', 'SAIR', 'MOEDAS', 'CODIGO_PRODUTO', 'COMMA', 'DOT')
        
        t_LISTAR = r'LISTAR'
        t_MOEDA = r'MOEDA'
        t_SELECIONAR = r'SELECIONAR'
        t_SAIR = r'SAIR'
        t_MOEDAS = r'\d+[eEcC]'
        t_CODIGO_PRODUTO = r'[A-Z]\d+'
        t_COMMA = r','
        t_DOT = r'\.'

        t_ignore = ' \t'

        def t_error(t):
            print(f"Caractere desconhecido '{t.value[0]}'")
            t.lexer.skip(1)

        lexer = lex.lex()
        return lexer

    def load_stock(self):
        try:
            with open("stock.json", "r") as f:
                data = json.load(f)
                self.stock = [Produto(**item) for item in data]
        except FileNotFoundError:
            self.stock = []

    def save_stock(self):
        with open("stock.json", "w") as f:
            json.dump([vars(p) for p in self.stock], f, indent=4)

    def process_command(self, command):
        self.lexer.input(command)
        tokens = []
        while True:
            tok = self.lexer.token()
            if not tok:
                break
            tokens.append(tok)

        if not tokens:
            print("maq: Comando inválido")
            return

        handlers = {
            'LISTAR': self.list_products,
            'MOEDA': lambda: self.handle_moeda(tokens[1:]),
            'SELECIONAR': lambda: self.handle_select(tokens[1:] if len(tokens) > 1 else [])
        }

        cmd = tokens[0].type
        action = handlers.get(cmd, lambda: print("maq: Comando inválido"))
        action()

    def list_products(self):
        print("maq:")
        header = "{:<6} | {:<15} | {:<12} | {:<8}".format("COD", "NOME", "QUANTIDADE", "PREÇO")
        print(header)
        print("-" * len(header))
        for p in self.stock:
            price_cents = int(p.preco * 100)
            print("{:<6} | {:<15} | {:<12} | {:<8}".format(p.cod, p.nome, p.quant, f"{price_cents}"))

    def handle_moeda(self, tokens):
        moedas = [tok.value for tok in tokens if tok.type == 'MOEDAS']
        total_added = 0
        for moeda in moedas:
            value = self.parse_moeda(moeda)
            self.balance += value
            total_added += 1
        self.print_balance()

    def handle_select(self, tokens):
        if not tokens or tokens[0].type != 'CODIGO_PRODUTO':
            print("maq: Código inválido")
            return
        self.select_product(tokens[0].value)

    def parse_moeda(self, moeda_str):
        value = int(moeda_str[:-1])
        unit = moeda_str[-1].lower()
        return value * 100 if unit == 'e' else value

    def print_balance(self):
        euros, cents = divmod(self.balance, 100)
        saldo_str = f"{euros}e{cents:02d}c" if euros else f"{cents}c"
        print(f"maq: Saldo = {saldo_str}")

    def select_product(self, code):
        produto = next((p for p in self.stock if p.cod == code), None)
        if not produto:
            print("maq: Produto não existe")
            return
        if produto.quant == 0:
            print("maq: Produto esgotado")
            return
        price_cents = int(produto.preco * 100)
        if self.balance < price_cents:
            print("maq: Saldo insuficiente para satisfazer o seu pedido")
            print(f"maq: Saldo = {self.balance//100}e{self.balance%100}c; Pedido = {price_cents}c")
            return
        produto.quant -= 1
        self.balance -= price_cents
        print(f'maq: Pode retirar o produto dispensado "{produto.nome}"')
        self.print_balance()
        self.save_stock()

    def return_change(self):
        moedas_disponiveis = [100, 50, 20, 10, 5]
        change = {}
        remaining = self.balance

        for moeda in moedas_disponiveis:
            count, remaining = divmod(remaining, moeda)
            if count:
                change[moeda] = count

        if change:
            change_str = ", ".join([f"{count}x {moeda//100}e" if moeda >= 100 else f"{count}x {moeda}c"
                                    for moeda, count in change.items()])
            print(f"maq: Pode retirar o troco: {change_str}")
        self.balance = 0
