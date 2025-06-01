class StackMachineCodeGenerator:
    def __init__(self):
        self.code = []
        self.label_counter = 0
        self.string_heap = {}  
        self.local_vars = {}   
        self.global_vars = {}  
        self.var_types = {}    
        self.array_info = {}   
        self.functions = {}    
        self.current_scope = 'global'
        self.local_offset = 0
        self.global_offset = 0
        
    def new_label(self, prefix="L"):
        """Para gerar as labels únicas de jump"""
        self.label_counter += 1
        return f"{prefix}{self.label_counter}"
    
    def emit(self, instruction):
        """Acrescentar a instrução"""
        self.code.append(instruction.lower())
    
    def generate(self, ast):
        """Só inicializa"""
        self.visit(ast)
        self.emit("stop")
        return "\n".join(self.code)
    
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
    
    def visit_program(self, node):
        """Programas: ('program', name, declarations, compound_statement)"""
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
    
    def visit_var_decl(self, node):
        """Declarações de variáveis: ('var_decl', var_specs)"""
        _, var_specs = node
        
        for var_spec in var_specs:
            self.visit(var_spec)
    
    def visit_var_spec(self, node):
        """Especificação de variáveis: ('var_spec', id_list, type_spec)"""
        _, id_list, type_spec = node
        
        # Extrai o tipo da variável
        var_type = self._extract_type(type_spec)
        
        for var_name in id_list:
            # Se for array
            if isinstance(type_spec, tuple) and len(type_spec) >= 4 and type_spec[0] == 'array_type':
                # Declaracao: ('array_type', start, end, element_type)
                self._handle_array_declaration_v2(var_name, type_spec)
            else:
                # variável simples
                self.var_types[var_name] = var_type
                
                if self.current_scope == 'global':
                    self.global_vars[var_name] = self.global_offset
                    self.global_offset += 1
                else:
                    self.local_vars[var_name] = self.local_offset
                    self.local_offset += 1

    def _handle_array_declaration_v2(self, var_name, type_spec):
        """('array_type', start, end, element_type)"""

        _, start_val, end_val, element_type = type_spec
        
        size = end_val - start_val + 1
        
        # Store array info
        self.array_info[var_name] = {
            'size': size,
            'start_index': start_val,
            'element_type': element_type if isinstance(element_type, str) else str(element_type)
        }
        
        self.emit(f"alloc {size}")
        
        if self.current_scope == 'global':
            self.emit(f"storeg {self.global_offset}")
            self.global_vars[var_name] = self.global_offset
            self.global_offset += 1
        else:
            self.emit(f"storel {self.local_offset}")
            self.local_vars[var_name] = self.local_offset
            self.local_offset += 1
        
        self.var_types[var_name] = 'array'


    def _extract_type(self, type_spec):
        """extrair o tipo"""
        if isinstance(type_spec, tuple):
            if type_spec[0] == 'type':
                return type_spec[1].lower()
            elif type_spec[0] == 'array':
                return 'array'
            return type_spec[0].lower()
        elif isinstance(type_spec, str):
            return type_spec.lower()
        return 'unknown'
    
    
    def visit_compound(self, node):
        """comando em si"""
        _, statements = node
        
        if statements:
            for stmt in statements:
                if stmt is not None:
                    self.visit(stmt)


    def visit_assign(self, node):
        """Visit assignment: ('assign', variable, expression)"""
        _, var, expr = node
        
        if var[0] == 'var':
            var_name = var[1]
            
            self.visit(expr)
            
            # Armazena na posição correta
            if var_name in self.local_vars:
                self.emit(f"storel {self.local_vars[var_name]}")
            elif var_name in self.global_vars:
                self.emit(f"storeg {self.global_vars[var_name]}")
            else:
                # Special case for function return value
                if var_name in self.functions:
                    self.emit("storel -1")  # Store in return position
                else:
                    raise Exception(f"Variável não definida -> {var_name}")

               # atibuir a um elemento do array     
        elif var[0] == 'array_access':
            array_name, index_expr = var[1], var[2]
            
            if array_name in self.local_vars:
                self.emit(f"pushl {self.local_vars[array_name]}")
            elif array_name in self.global_vars:
                self.emit(f"pushg {self.global_vars[array_name]}")
            else:
                raise Exception(f"Undefined array: {array_name}")
            
            # gerar iíndice
            if array_name in self.array_info:
                start_idx = self.array_info[array_name]['start_index']
                if start_idx != 1:  # Pascal arrays typically start at 1
                    self.visit(index_expr)
                    self.emit(f"pushi {start_idx}")
                    self.emit("sub")  # Convert to 0-based index
                else:
                    self.visit(index_expr)
                    self.emit("pushi 1")
                    self.emit("sub")  # Convert from 1-based to 0-based
            else:
                self.visit(index_expr)
                self.emit("pushi 1")
                self.emit("sub")  # Default: convert from 1-based to 0-based
            
            self.visit(expr)
            
            # Faz a atribuição no array [ endereço_base, índice, valor ]
            self.emit("storen")

    def visit_var(self, node):
        """Referência a variável: ('var', name)"""
        _, name = node
        
        if name in self.local_vars:
            self.emit(f"pushl {self.local_vars[name]}")
        elif name in self.global_vars:
            self.emit(f"pushg {self.global_vars[name]}")
        else:
            raise Exception(f"Undefined variable: {name}")
    
    def visit_array_access(self, node):
        """Acesso a arrays: ('array_access', name, index)"""
        _, name, index = node
        
        # verifica se é string para usar o CHARAT
        if name in self.var_types and self.var_types[name] == 'string':
            # Push endereço da string
            if name in self.local_vars:
                self.emit(f"pushl {self.local_vars[name]}")
            elif name in self.global_vars:
                self.emit(f"pushg {self.global_vars[name]}")
            else:
                raise Exception(f"Undefined variable: {name}")
            
            # Push index
            self.visit(index)
            self.emit("pushi 1")
            self.emit("sub")  # Convert from 1-based to 0-based indexing
            
            self.emit("charat")
            
        else:
            # Se não é um array
            if name in self.local_vars:
                self.emit(f"pushl {self.local_vars[name]}")
            elif name in self.global_vars:
                self.emit(f"pushg {self.global_vars[name]}")
            else:
                raise Exception(f"Undefined array: {name}")
            
            if name in self.array_info:
                start_idx = self.array_info[name]['start_index']
                if start_idx != 1:
                    self.visit(index)
                    self.emit(f"pushi {start_idx}")
                    self.emit("sub")  # Convert to 0-based index
                else:
                    self.visit(index)
                    self.emit("pushi 1")
                    self.emit("sub")  # Convert from 1-based to 0-based
            else:
                self.visit(index)
                self.emit("pushi 1")
                self.emit("sub")  # Default: convert from 1-based to 0-based
            
            self.emit("loadn")
    
    def visit_const(self, node):
        """Constante: ('const', value)"""
        _, value = node
        
        if isinstance(value, int):
            self.emit(f"pushi {value}")
        elif isinstance(value, float):
            self.emit(f"pushf {value}")
        elif isinstance(value, str):
            # Trata valores booleanos representados como string
            clean_value = value.strip().lower()
            if clean_value == 'true':
                self.emit("pushi 1")
            elif clean_value == 'false':
                self.emit("pushi 0")
            else:
                # String literal - precisa de ser guardada como string
                escaped_value = value.replace('"', '\\"')
                self.emit(f'pushs "{escaped_value}"')
        elif value in ['true', 'false']:
            self.emit(f"pushi {1 if value == 'true' else 0}")
    
    def visit_func_call(self, node):
        """Chamada de função: ('func_call', name, args)"""
        _, name, args = node
        
        if name == 'length':
            if args:
                arg = args[0]
                if arg[0] == 'var':
                    var_name = arg[1]
                    if var_name in self.local_vars:
                        self.emit(f"pushl {self.local_vars[var_name]}")
                    elif var_name in self.global_vars:
                        self.emit(f"pushg {self.global_vars[var_name]}")
                    else:
                        raise Exception(f"Undefined variable: {var_name}")
                else:
                    self.visit(arg)
                self.emit("strlen")
        else:
            if args:
                for arg in reversed(args):
                    self.visit(arg)

            # Chama função
            self.emit(f"pusha {name}")
            self.emit("call")
    
    def visit_if(self, node):
        """IFt: ('if', condition, then_stmt, else_stmt)"""
        _, condition, then_stmt, else_stmt = node
        
        # passa para a condição
        self.visit(condition)
        
        if else_stmt is None:
            # if
            end_label = self.new_label("endif")
            self.emit(f"jz {end_label}")
            self.visit(then_stmt)
            self.emit(f"{end_label}:")
        else:
            # If-else
            else_label = self.new_label("else")
            end_label = self.new_label("endif")
            
            self.emit(f"jz {else_label}")
            self.visit(then_stmt)
            self.emit(f"jump {end_label}")
            self.emit(f"{else_label}:")
            self.visit(else_stmt)
            self.emit(f"{end_label}:")
    
    def visit_for(self, node):
        _, var, start, direction, end, body = node

        # Inicializar variável de controlo
        self.visit(start)
        if var in self.local_vars:
            self.emit(f"storel {self.local_vars[var]}")
        else:
            self.emit(f"storeg {self.global_vars[var]}")

        loop_label = self.new_label("label")
        end_label = self.new_label("label")

        self.emit(f"{loop_label}:")

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
            raise Exception(f"Unknown for direction: {direction}")

        self.emit(f"jz {end_label}")

        # Corpo do ciclo
        self.visit(body)

        # Incremento/decremento
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

    
    def visit_write(self, node):
        """Write: ('write', expressions) - output without newline"""
        _, expressions = node
        
        if expressions:
            for expr in expressions:
                self.visit(expr)
                
                expr_type = self._get_expression_type(expr)
                
                if expr_type in ['integer', 'int']:
                    self.emit("writei")
                elif expr_type in ['real', 'float']:
                    self.emit("writef")
                else:  # string or unknown
                    self.emit("writes")
    
    def visit_writeln(self, node):
        """Writeln: ('writeln', expressions)"""
        _, expressions = node
        
        if expressions:
            for expr in expressions:
                self.visit(expr)
                
                expr_type = self._get_expression_type(expr)
                
                if expr_type in ['integer', 'int']:
                    self.emit("writei")
                elif expr_type in ['real', 'float']:
                    self.emit("writef")
                else:  # string or unknown
                    self.emit("writes")
        
        self.emit("writeln")
    
    def _get_expression_type(self, expr):
        if isinstance(expr, tuple):
            if expr[0] == 'var':
                var_name = expr[1]
                return self.var_types.get(var_name, 'unknown')
            elif expr[0] == 'const':
                value = expr[1]
                if isinstance(value, int):
                    return 'integer'
                elif isinstance(value, float):
                    return 'real'
                elif isinstance(value, str):
                    return 'string'
            elif expr[0] in ['+', '-', '*', '/', 'div', 'mod']:
                return 'integer'
        return 'unknown'
    
    def visit_readln(self, node):
        """readLn : ('readln', variables)"""
        _, variables = node
        
        for var in variables:
            if var[0] == 'var':
                var_name = var[1]
                var_type = self.var_types.get(var_name, 'string')
                
                # dá sempre o string address da heap
                self.emit("read")
                
                if var_type in ['integer', 'int']:
                    self.emit("atoi")  
                elif var_type in ['real', 'float']:
                    self.emit("atof")  
                
                # Store in variable
                if var_name in self.local_vars:
                    self.emit(f"storel {self.local_vars[var_name]}")
                elif var_name in self.global_vars:
                    self.emit(f"storeg {self.global_vars[var_name]}")
                    
            elif var[0] == 'array_access':
                array_name, index_expr = var[1], var[2]
                
                # ORDEM CORRETA: primeiro endereço, depois índice, depois valor
                if array_name in self.local_vars:
                    self.emit(f"pushl {self.local_vars[array_name]}")
                elif array_name in self.global_vars:
                    self.emit(f"pushg {self.global_vars[array_name]}")
                else:
                    raise Exception(f"Undefined array: {array_name}")
                
                # gera o indice
                if array_name in self.array_info:
                    start_idx = self.array_info[array_name]['start_index']
                    if start_idx != 1:
                        self.visit(index_expr)
                        self.emit(f"pushi {start_idx}")
                        self.emit("sub")  # Convert to 0-based index
                    else:
                        self.visit(index_expr)
                        self.emit("pushi 1")
                        self.emit("sub")  # Convert from 1-based to 0-based
                else:
                    self.visit(index_expr)
                    self.emit("pushi 1")
                    self.emit("sub")  # Default: convert from 1-based to 0-based
                
                #(vai para o topo da pilha)
                self.emit("read")
                
                if array_name in self.array_info:
                    element_type = self.array_info[array_name]['element_type']
                    if element_type in ['integer', 'int']:
                        self.emit("atoi")
                    elif element_type in ['real', 'float']:
                        self.emit("atof")
                else:
                    self.emit("atoi")
                
                # Stack: [endereço_array, índice, valor_convertido]
                self.emit("storen")
    
    def visit_binary_op(self, node):
        op, left, right = node
        
        # se for comparação de caracteres
        if op == '=' and self._is_char_comparison(left, right):
            self._handle_char_comparison(left, right)
            return
        
        self.visit(left)
        self.visit(right)
        
        if op == '+':
            self.emit("add")
        elif op == '-':
            self.emit("sub")
        elif op == '*':
            self.emit("mul")
        elif op == '/':
            self.emit("div")
        elif op == 'div':
            self.emit("div")
        elif op == 'mod':
            self.emit("mod")
        elif op == '=':
            self.emit("equal")
        elif op == '<>':
            self.emit("equal")
            self.emit("not")
        elif op == '<':
            self.emit("inf")
        elif op == '<=':
            self.emit("infeq")
        elif op == '>':
            self.emit("sup")
        elif op == '>=':
            self.emit("supeq")
        elif op == 'and':
            self.emit("and")
        elif op == 'or':
            self.emit("or")
    
    def visit_while(self, node):
        """while: ('while', condition, body)"""
        _, condition, body = node

        loop_label = self.new_label("while")
        end_label = self.new_label("endwhile")

        self.emit(f"{loop_label}:")
        
        self.visit(condition)
        self.emit(f"jz {end_label}")

        self.visit(body)

        self.emit(f"jump {loop_label}")
        self.emit(f"{end_label}:")

    def _is_char_comparison(self, left, right):
        return (isinstance(left, tuple) and left[0] == 'array_access' and 
                isinstance(right, tuple) and right[0] == 'const' and 
                isinstance(right[1], str) and len(right[1]) == 1)

    def _handle_char_comparison(self, left, right):
        self.visit(left)
        
        char = right[1]
        ascii_code = ord(char)
        self.emit(f"pushi {ascii_code}")
        
        # Compare ASCII codes
        self.emit("equal")


def generate_code_from_ast(ast):
    generator = StackMachineCodeGenerator()
    return generator.generate(ast)
