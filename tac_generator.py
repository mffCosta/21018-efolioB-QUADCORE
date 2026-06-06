"""
tac_generator.py — Geração de código intermédio TAC para MOCP.
UC 21018 — Compilação, Universidade Aberta, 2025/2026
Grupo: QUADCORE
Autores: Maria Costa (2304361) | João Rodrigues (2203474) | Nuno Rolo (1900405) | Fábio Oliveira (1800960)

Gera Three Address Code (TAC) a partir da AST da linguagem MOCP.
"""

from ast_nodes import (
    ProgramNode,
    FunctionDefNode,
    BlockNode,
    VarDeclNode,
    VarSimpleDeclNode,
    VarInitDeclNode,
    VarSizedArrayDeclNode,
    VarUnsizedArrayDeclNode,
    VarArrayInitDeclNode,
    VarArrayExprInitDeclNode,
    AssignStmtNode,
    IfStmtNode,
    WhileStmtNode,
    ForStmtNode,
    ReturnStmtNode,
    ExprStmtNode,
    EmptyStmtNode,
    AssignExprNode,
    RelationalCondNode,
    NotCondNode,
    BinaryLogicalCondNode,
    ExprAsCondNode,
    BinaryExprNode,
    UnaryExprNode,
    CastExprNode,
    IdentifierNode,
    ArrayAccessNode,
    FunctionCallNode,
    IntLiteralNode,
    RealLiteralNode,
    StringLiteralNode,
)

from tac import (
    TACProgram,
    TACNameGenerator,
    tac_label,
    tac_goto,
    tac_if,
    tac_if_false,
    tac_assign,
    tac_binary,
    tac_unary_minus,
    tac_cast,
    tac_int_to_real,
    tac_real_to_int,
    tac_array_load,
    tac_array_store,
    tac_array_decl,
    tac_array_zero_init,
    tac_array_init,
    tac_param,
    tac_call,
    tac_return,
    tac_func_begin,
    tac_func_end,
    tac_declare,
    tac_getparam,
    tac_read,
    tac_readc,
    tac_reads,
    tac_write,
)


class TACGenerationError(Exception):
    pass


class TACGenerator:
    """
    Gera TAC a partir da AST.

    O gerador assume que a análise semântica já foi executada.
    """

    def __init__(self):
        self.function_returns = {}
        self.function_params = {}
        self.program = TACProgram()
        self.names = TACNameGenerator()
        self.current_function = None

        # Tipos das variaveis conhecidas, usados para inserir conversoes
        # numericas explicitas (int_to_real / real_to_int) no TAC.
        self.var_types = {}
        self.global_var_types = {}

        self.input_functions = {"ler", "lerc", "lers"}
        self.output_functions = {"escrever", "escreverc", "escrevers", "escreverv"}

    # =====================================================
    # Apoio à geração de temporários
    # =====================================================

    def _new_temp(self) -> str:
        """
        Cria um temporário novo e regista-o no conjunto de temporários do
        programa TAC. Esse registo permite à otimização distinguir, sem
        ambiguidade, temporários de variáveis do utilizador.
        """
        temp = self.names.new_temp()
        self.program.temporaries.add(temp)
        return temp

    # =====================================================
    # API principal
    # =====================================================

    def generate(self, ast: ProgramNode) -> TACProgram:
        self.program = TACProgram()
        self.names = TACNameGenerator()
        self.var_types = {}
        self.global_var_types = {}

        self.function_returns = {
            func.name: func.return_type
            for func in ast.functions
        }

        self.function_returns.update({
            "ler": "inteiro",
            "lerc": "inteiro",
            "lers": "inteiro[]",
            "escrever": "vazio",
            "escreverc": "vazio",
            "escrevers": "vazio",
            "escreverv": "vazio",
        })

        # Parametros das funcoes do utilizador (definicoes e prototipos), para
        # converter argumentos para o tipo do parametro no ponto da chamada.
        self.function_params = {
            func.name: func.params for func in ast.functions
        }
        for proto in ast.prototypes:
            self.function_params.setdefault(proto.name, proto.params)

        self.visit_program(ast)

        return self.program

    # =====================================================
    # Programa / funções
    # =====================================================

    def visit_program(self, node: ProgramNode) -> None:
        for decl in node.global_decls:
            self.visit_var_decl(decl)

        # Tipos globais ficam visiveis em todas as funcoes.
        self.global_var_types = dict(self.var_types)

        for func in node.functions:
            self.visit_function(func)

    def visit_function(self, node: FunctionDefNode) -> None:
        self.current_function = node.name
        self.var_types = dict(self.global_var_types)

        self.program.add(tac_func_begin(node.name))

        # Rececao explicita dos parametros: cada parametro e declarado e
        # depois lido da area de chamada com 'getparam i'. Assim o TAC fica
        # auto-contido e a convencao de chamadas torna-se verificavel, sem
        # depender de suposicoes implicitas sobre onde ficam os argumentos.
        for index, param in enumerate(node.params):
            if param.name:
                self.var_types[param.name] = self._param_type(param)
                self.program.add(tac_declare(param.name))
                self.program.add(tac_getparam(param.name, index))

        self.visit_block(node.body)

        self.program.add(tac_func_end(node.name))

        self.current_function = None

    def visit_block(self, node: BlockNode) -> None:
        for decl in node.declarations:
            self.visit_var_decl(decl)

        for stmt in node.statements:
            self.visit_stmt(stmt)

    # =====================================================
    # Declarações
    # =====================================================

    def visit_var_decl(self, node: VarDeclNode) -> None:
        var_type = node.var_type

        for item in node.items:
            if isinstance(item, VarSimpleDeclNode):
                self.var_types[item.name] = var_type
                self.program.add(tac_declare(item.name))
                default = "0.0" if var_type == "real" else "0"
                self.program.add(tac_assign(item.name, default))

            elif isinstance(item, VarInitDeclNode):
                self.var_types[item.name] = var_type
                self.program.add(tac_declare(item.name))
                value = self.visit_expr(item.value)
                value = self._convert(value, self._type_of(item.value), var_type)
                self.program.add(tac_assign(item.name, value))

            elif isinstance(item, VarSizedArrayDeclNode):
                self.var_types[item.name] = f"{var_type}[]"
                self.program.add(tac_array_decl(item.name, str(item.size)))
                # Materializa a inicializacao por omissao a 0 (spec MOCP) no
                # proprio TAC, em vez de a deixar implicita na declaracao.
                self.program.add(tac_array_zero_init(item.name, str(item.size)))

            elif isinstance(item, VarUnsizedArrayDeclNode):
                self.var_types[item.name] = f"{var_type}[]"
                self.program.add(tac_array_decl(item.name, "?"))

            elif isinstance(item, VarArrayInitDeclNode):
                self.var_types[item.name] = f"{var_type}[]"
                self.program.add(tac_array_decl(item.name, str(len(item.values))))

                for index, expr in enumerate(item.values):
                    value = self.visit_expr(expr)
                    value = self._convert(value, self._type_of(expr), var_type)
                    self.program.add(tac_array_init(item.name, str(index), value))

            elif isinstance(item, VarArrayExprInitDeclNode):
                self.var_types[item.name] = f"{var_type}[]"
                self.program.add(tac_array_decl(item.name, "?"))
                value = self.visit_expr(item.value)
                self.program.add(tac_assign(item.name, value))

            else:
                raise TACGenerationError(
                    f"Declaração sem tratamento TAC: {type(item).__name__}"
                )

    # =====================================================
    # Instruções
    # =====================================================

    def visit_stmt(self, stmt) -> None:
        if isinstance(stmt, AssignStmtNode):
            self.visit_assignment(stmt.target, stmt.value)

        elif isinstance(stmt, IfStmtNode):
            self.visit_if(stmt)

        elif isinstance(stmt, WhileStmtNode):
            self.visit_while(stmt)

        elif isinstance(stmt, ForStmtNode):
            self.visit_for(stmt)

        elif isinstance(stmt, ReturnStmtNode):
            self.visit_return(stmt)

        elif isinstance(stmt, ExprStmtNode):
            self.visit_expr_stmt(stmt)

        elif isinstance(stmt, EmptyStmtNode):
            pass

        elif isinstance(stmt, BlockNode):
            self.visit_block(stmt)

        else:
            raise TACGenerationError(
                f"Instrução sem tratamento TAC: {type(stmt).__name__}"
            )

    def visit_assignment(self, target, value_expr) -> None:
        value = self.visit_expr(value_expr)
        value_type = self._type_of(value_expr)

        if isinstance(target, IdentifierNode):
            value = self._convert(value, value_type, self.var_types.get(target.name))
            self.program.add(tac_assign(target.name, value))

        elif isinstance(target, ArrayAccessNode):
            index = self.visit_expr(target.index)
            value = self._convert(value, value_type, self._element_type(target.name))
            self.program.add(tac_array_store(target.name, index, value))

        else:
            raise TACGenerationError(
                f"Destino de atribuição inválido: {type(target).__name__}"
            )

    def visit_assign_expr(self, expr: AssignExprNode) -> None:
        self.visit_assignment(expr.target, expr.value)

    def visit_if(self, stmt: IfStmtNode) -> None:
        else_label = self.names.new_label()
        end_label = self.names.new_label()

        condition = self.visit_cond_expr(stmt.condition)
        self.program.add(tac_if_false(condition, else_label))

        self.visit_block(stmt.then_block)

        if stmt.else_block is not None:
            self.program.add(tac_goto(end_label))
            self.program.add(tac_label(else_label))
            self.visit_block(stmt.else_block)
            self.program.add(tac_label(end_label))
        else:
            self.program.add(tac_label(else_label))

    def visit_while(self, stmt: WhileStmtNode) -> None:
        start_label = self.names.new_label()
        end_label = self.names.new_label()

        self.program.add(tac_label(start_label))

        condition = self.visit_cond_expr(stmt.condition)
        self.program.add(tac_if_false(condition, end_label))

        self.visit_block(stmt.body)

        self.program.add(tac_goto(start_label))
        self.program.add(tac_label(end_label))

    def visit_for(self, stmt: ForStmtNode) -> None:
        start_label = self.names.new_label()
        end_label = self.names.new_label()

        if stmt.init is not None:
            self.visit_assign_expr(stmt.init)

        self.program.add(tac_label(start_label))

        if stmt.condition is not None:
            condition = self.visit_cond_expr(stmt.condition)
            self.program.add(tac_if_false(condition, end_label))

        self.visit_block(stmt.body)

        if stmt.update is not None:
            self.visit_assign_expr(stmt.update)

        self.program.add(tac_goto(start_label))
        self.program.add(tac_label(end_label))

    def visit_return(self, stmt: ReturnStmtNode) -> None:
        if stmt.value is None:
            self.program.add(tac_return())
        else:
            value = self.visit_expr(stmt.value)
            return_type = self.function_returns.get(self.current_function)
            value = self._convert(value, self._type_of(stmt.value), return_type)
            self.program.add(tac_return(value))

    def visit_expr_stmt(self, stmt: ExprStmtNode) -> None:
        self.visit_expr(stmt.expr)

    # =====================================================
    # Condições
    # =====================================================

    def visit_cond_expr(self, cond) -> str:
        if isinstance(cond, ExprAsCondNode):
            return self.visit_expr(cond.expr)

        if isinstance(cond, RelationalCondNode):
            left = self.visit_expr(cond.left)
            right = self.visit_expr(cond.right)
            temp = self._new_temp()
            self.program.add(tac_binary(temp, left, cond.operator, right))
            return temp

        if isinstance(cond, NotCondNode):
            value = self.visit_cond_expr(cond.operand)
            temp = self._new_temp()
            self.program.add(tac_binary(temp, value, "==", "0"))
            return temp

        if isinstance(cond, BinaryLogicalCondNode):
            if cond.operator == "&&":
                return self._visit_logical_and(cond)

            if cond.operator == "||":
                return self._visit_logical_or(cond)

            raise TACGenerationError(
                f"Operador lógico desconhecido: {cond.operator}"
            )

        raise TACGenerationError(
            f"Condição sem tratamento TAC: {type(cond).__name__}"
        )

    def _visit_logical_and(self, cond: BinaryLogicalCondNode) -> str:
        """
        Gera TAC com curto-circuito para 'esq && dir'.

        O operando direito so e avaliado quando o esquerdo for verdadeiro,
        evitando efeitos laterais indesejados (chamadas de funcao, acessos
        a vetor, etc.) quando o resultado ja esta determinado pelo esquerdo.
        O resultado e normalizado para 0/1 num temporario.
        """
        false_label = self.names.new_label()
        end_label = self.names.new_label()
        result = self._new_temp()

        left = self.visit_cond_expr(cond.left)
        self.program.add(tac_if_false(left, false_label))

        right = self.visit_cond_expr(cond.right)
        self.program.add(tac_if_false(right, false_label))

        self.program.add(tac_assign(result, "1"))
        self.program.add(tac_goto(end_label))
        self.program.add(tac_label(false_label))
        self.program.add(tac_assign(result, "0"))
        self.program.add(tac_label(end_label))

        return result

    def _visit_logical_or(self, cond: BinaryLogicalCondNode) -> str:
        """
        Gera TAC com curto-circuito para 'esq || dir'.

        O operando direito so e avaliado quando o esquerdo for falso. O
        resultado e normalizado para 0/1 num temporario.
        """
        true_label = self.names.new_label()
        end_label = self.names.new_label()
        result = self._new_temp()

        left = self.visit_cond_expr(cond.left)
        self.program.add(tac_if(left, true_label))

        right = self.visit_cond_expr(cond.right)
        self.program.add(tac_if(right, true_label))

        self.program.add(tac_assign(result, "0"))
        self.program.add(tac_goto(end_label))
        self.program.add(tac_label(true_label))
        self.program.add(tac_assign(result, "1"))
        self.program.add(tac_label(end_label))

        return result

    # =====================================================
    # Expressões
    # =====================================================

    def visit_expr(self, expr) -> str:
        if isinstance(expr, IdentifierNode):
            return expr.name

        if isinstance(expr, ArrayAccessNode):
            index = self.visit_expr(expr.index)
            temp = self._new_temp()
            self.program.add(tac_array_load(temp, expr.name, index))
            return temp

        if isinstance(expr, FunctionCallNode):
            return self.visit_function_call(expr)

        if isinstance(expr, BinaryExprNode):
            left = self.visit_expr(expr.left)
            right = self.visit_expr(expr.right)
            left, right = self._promote_operands(expr, left, right)
            temp = self._new_temp()
            self.program.add(tac_binary(temp, left, expr.operator, right))
            return temp

        if isinstance(expr, UnaryExprNode):
            value = self.visit_expr(expr.operand)
            temp = self._new_temp()
            self.program.add(tac_unary_minus(temp, value))
            return temp

        if isinstance(expr, CastExprNode):
            value = self.visit_expr(expr.expr)
            temp = self._new_temp()
            self.program.add(tac_cast(temp, value, expr.target_type))
            return temp

        if isinstance(expr, IntLiteralNode):
            return str(expr.value)

        if isinstance(expr, RealLiteralNode):
            return str(expr.value)

        if isinstance(expr, StringLiteralNode):
            return self._format_string_literal(expr.value)

        raise TACGenerationError(
            f"Expressão sem tratamento TAC: {type(expr).__name__}"
        )

    def visit_function_call(self, call: FunctionCallNode) -> str:
        if call.name == "ler":
            temp = self._new_temp()
            self.program.add(tac_read(temp))
            return temp

        if call.name == "lerc":
            temp = self._new_temp()
            self.program.add(tac_readc(temp))
            return temp

        if call.name == "lers":
            temp = self._new_temp()
            self.program.add(tac_reads(temp))
            return temp

        if call.name in self.output_functions:
            args = [self.visit_expr(arg) for arg in call.args]

            if len(args) == 0:
                self.program.add(tac_call(call.name, 0, None))
            else:
                for arg in args:
                    self.program.add(tac_write(call.name, arg))

            return ""

        # Avalia cada argumento e converte-o para o tipo do parametro
        # correspondente antes de o passar (conversao no ponto da chamada).
        params = self.function_params.get(call.name)
        args = []
        for index, arg in enumerate(call.args):
            place = self.visit_expr(arg)
            if params is not None and index < len(params) and not params[index].is_array:
                place = self._convert(
                    place, self._type_of(arg), params[index].param_type
                )
            args.append(place)

        for arg in args:
            self.program.add(tac_param(arg))

        return_type = self.function_returns.get(call.name, "inteiro")

        if return_type == "vazio":
            self.program.add(tac_call(call.name, len(args), None))
            return ""

        temp = self._new_temp()
        self.program.add(tac_call(call.name, len(args), temp))
        return temp

    # =====================================================
    # Conversões numéricas explícitas
    # =====================================================

    def _param_type(self, param) -> str:
        """Tipo de um parametro, com sufixo '[]' quando e vetor."""
        return f"{param.param_type}[]" if param.is_array else param.param_type

    def _element_type(self, name: str):
        """Tipo dos elementos de um vetor declarado (sem o sufixo '[]')."""
        base = self.var_types.get(name)
        if base is not None and base.endswith("[]"):
            return base[:-2]
        return base

    def _type_of(self, expr):
        """
        Infere o tipo estatico de uma expressao (sem emitir TAC).

        Espelha a inferencia da analise semantica, mas apenas com o detalhe
        necessario para decidir conversoes numericas. Devolve None quando o
        tipo nao e relevante para conversao (evita coercoes erradas).
        """
        if isinstance(expr, IdentifierNode):
            return self.var_types.get(expr.name)

        if isinstance(expr, ArrayAccessNode):
            return self._element_type(expr.name)

        if isinstance(expr, IntLiteralNode):
            return "inteiro"

        if isinstance(expr, RealLiteralNode):
            return "real"

        if isinstance(expr, StringLiteralNode):
            return "inteiro[]"

        if isinstance(expr, CastExprNode):
            return expr.target_type

        if isinstance(expr, UnaryExprNode):
            return self._type_of(expr.operand)

        if isinstance(expr, BinaryExprNode):
            if expr.operator == "%":
                return "inteiro"
            if expr.operator in {"<", "<=", ">", ">=", "==", "!="}:
                return "inteiro"
            left_type = self._type_of(expr.left)
            right_type = self._type_of(expr.right)
            if left_type == "real" or right_type == "real":
                return "real"
            return "inteiro"

        if isinstance(expr, FunctionCallNode):
            return self.function_returns.get(expr.name)

        return None

    def _convert(self, place: str, from_type, to_type) -> str:
        """
        Emite uma conversao numerica explicita se 'from_type' e 'to_type'
        diferirem entre inteiro e real, devolvendo o novo local. Caso
        contrario devolve o local original inalterado.
        """
        if from_type is None or to_type is None or from_type == to_type:
            return place

        if from_type == "inteiro" and to_type == "real":
            temp = self._new_temp()
            self.program.add(tac_int_to_real(temp, place))
            return temp

        if from_type == "real" and to_type == "inteiro":
            temp = self._new_temp()
            self.program.add(tac_real_to_int(temp, place))
            return temp

        return place

    def _promote_operands(self, expr: BinaryExprNode, left: str, right: str):
        """
        Promove o operando inteiro para real numa operacao mista inteiro/real,
        para que a operacao seja feita em virgula flutuante. O operador '%'
        exige inteiros, pelo que nunca promove.
        """
        if expr.operator == "%":
            return left, right

        left_type = self._type_of(expr.left)
        right_type = self._type_of(expr.right)

        if left_type == "real" and right_type == "inteiro":
            right = self._convert(right, "inteiro", "real")
        elif right_type == "real" and left_type == "inteiro":
            left = self._convert(left, "inteiro", "real")

        return left, right

    # =====================================================
    # Utilitários
    # =====================================================

    def _format_string_literal(self, value: str) -> str:
        escaped = value.replace("\\", "\\\\").replace('"', '\\"')
        return f'"{escaped}"'