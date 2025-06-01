class SemanticAnalyzer:
    def __init__(self):
        self.functions = {
            'length': {
                 'params': [('x', 'string')],
                 'return': 'integer'
             }
        }
        self.symbols = {}
        self.current_scope = 'global'
        self.errors = []  # Para registar erros

    def analyze(self, tree):
        if tree[0] == 'program':
            _, name, declarations, main = tree
            self.visit_declarations(declarations)
            self.visit_statement(main)
        return 1 if self.errors else 0

    def visit_declarations(self, declarations):
        for decl in declarations:
            if decl[0] == 'var_decl':
                for spec in decl[1]:
                    self.visit_var_spec(spec)
            elif decl[0] == 'function':
                self.visit_function_decl(decl)

    def visit_var_spec(self, spec):
        _, ids, typ = spec
        for var in ids:
            if var in self.symbols:
                self.errors.append(f"Erro: variável '{var}' já declarada")
            else:
                self.symbols[var] = typ

    def visit_function_decl(self, node):
        _, name, params, ret_type, decls, body = node
        if name in self.functions:
            self.errors.append(f"Erro: função '{name}' já foi definida")
        else:
            self.functions[name] = {
                'params': [(v, t) for (_, ids, t) in params for v in ids],
                'return': ret_type
            }
        old_symbols = self.symbols.copy()
        for (_, ids, t) in params:
            for var in ids:
                self.symbols[var] = t
        
        self.symbols[name] = ret_type  
        
        for d in decls:
            if d[0] == 'var_decl':
                for spec in d[1]:
                    self.visit_var_spec(spec)
        self.visit_statement(body)
        self.symbols = old_symbols

    def visit_statement(self, stmt):
        if stmt is None:
            return
        if stmt[0] == 'compound':
            for s in stmt[1]:
                self.visit_statement(s)
        elif stmt[0] == 'assign':
            _, var, expr = stmt
            self.check_assignment(var, expr)
        elif stmt[0] == 'proc_call':
            self.check_proc_call(stmt)
        elif stmt[0] == 'if':
            self.visit_expr(stmt[1])
            self.visit_statement(stmt[2])
            if stmt[3]: self.visit_statement(stmt[3])
        elif stmt[0] in ('while', 'repeat'):
            self.visit_expr(stmt[1])
            self.visit_statement(stmt[2])
        elif stmt[0] == 'for':
            _, var, start, direction, end, body = stmt
            self.visit_expr(start)
            self.visit_expr(end)
            self.visit_statement(body)
        elif stmt[0] in ('write', 'writeln', 'read', 'readln'):
            for arg in stmt[1]:
                if stmt[0].startswith('read'):
                    self.check_variable(arg)
                else:
                    self.visit_expr(arg)

    def check_assignment(self, var, expr):
        if var[0] == 'var':
            name = var[1]
            if name not in self.symbols:
                self.errors.append(f"Erro: variável '{name}' não declarada")
            else:
                tipo_var = self.symbols[name]
                tipo_expr = self.visit_expr(expr)
                if tipo_expr and tipo_var != tipo_expr:
                    self.errors.append(f"Erro: incompatibilidade de tipos em '{name} := ...' ({tipo_var} ← {tipo_expr})")

    def visit_expr(self, expr):
        if expr[0] == 'const':
            val = expr[1]
            if isinstance(val, int): return 'integer'
            if isinstance(val, float): return 'real'
            if isinstance(val, bool): return 'boolean'
            if val in ['true', 'false']: return 'boolean'
            if isinstance(val, str):
                return 'char' if len(val) == 1 else 'string'
        elif expr[0] == 'array_access':
            varname = expr[1]
            index_expr = expr[2]
            if varname not in self.symbols:
                self.errors.append(f"Erro: variável '{varname}' não declarada")
                return None
            tipo = self.symbols[varname]
            index_type = self.visit_expr(index_expr)
            if index_type != 'integer':
                self.errors.append(f"Erro: índice de array deve ser integer, encontrado {index_type}")
            if tipo == 'string':
                return 'char'
            elif isinstance(tipo, tuple) and tipo[0] == 'array_type':
                return tipo[3]
            else:
                self.errors.append(f"Erro: tipo '{tipo}' não permite acesso indexado (esperado array ou string)")
                return None

        elif expr[0] == 'var':
            var = expr[1]
            return self.symbols.get(var, None)
        elif expr[0] == 'func_call':
            fname = expr[1]
            args = expr[2]
            if fname not in self.functions:
                self.errors.append(f"Erro: função '{fname}' não definida")
                return None
            func_info = self.functions[fname]
            if len(args) != len(func_info['params']):
                self.errors.append(f"Erro: número incorreto de argumentos para função '{fname}'")
            for i, arg in enumerate(args):
                tipo_arg = self.visit_expr(arg)
                expected = func_info['params'][i][1]
                if tipo_arg != expected:
                    self.errors.append(f"Erro: tipo do argumento {i+1} de '{fname}' é {tipo_arg}, esperado {expected}")
            return func_info['return']
        elif isinstance(expr, tuple) and len(expr) == 3:
            op, left, right = expr
            tipo_left = self.visit_expr(left)
            tipo_right = self.visit_expr(right)
            if op in ('=', '<>', '<', '<=', '>', '>='):
                if tipo_left != tipo_right:
                    self.errors.append(f"Erro: comparação '{op}' entre tipos incompatíveis: {tipo_left} e {tipo_right}")
                return 'boolean'
            elif op in ('and', 'or'):
                if tipo_left != 'boolean' or tipo_right != 'boolean':
                    self.errors.append(f"Erro: operação lógica '{op}' entre tipos incompatíveis: {tipo_left} e {tipo_right}")
                return 'boolean'
            else:
                if tipo_left != tipo_right:
                    self.errors.append(f"Erro: operação aritmética '{op}' entre tipos incompatíveis: {tipo_left} e {tipo_right}")
                return tipo_left
        elif isinstance(expr, tuple) and len(expr) == 2:
            op, subexpr = expr
            tipo_subexpr = self.visit_expr(subexpr)
            if op == 'not':
                if tipo_subexpr != 'boolean':
                    self.errors.append(f"Erro: operação 'not' aplicada a tipo {tipo_subexpr}, esperado boolean")
                return 'boolean'
            return tipo_subexpr
        return None

    def check_variable(self, var):
        if var[0] == 'var':
            if var[1] not in self.symbols:
                self.errors.append(f"Erro: variável '{var[1]}' usada antes da declaração")
