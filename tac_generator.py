"""
tac_generator.py — Geração de código intermédio TAC para MOCP.
UC 21018 — Compilação, Universidade Aberta, 2025/2026
Grupo: QUADCORE
Autores: Maria Costa (2304361) | João Rodrigues (2203474) | Nuno Rolo (1900405) | Flávio Oliveira (1900860)

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
    tac_if_false,
    tac_assign,
    tac_binary,
    tac_unary_minus,
    tac_cast,
    tac_array_load,
    tac_array_store,
    tac_array_decl,
    tac_array_init,
    tac_param,
    tac_call,
    tac_return,
    tac_func_begin,
    tac_func_end,
    tac_declare,
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
        self.program = TACProgram()
        self.names = TACNameGenerator()
        self.current_function = None

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
        
        self.visit_program(ast)

        return self.program

    # =====================================================
    # Programa / funções
    # =====================================================

    def visit_program(self, node: ProgramNode) -> None:
        for decl in node.global_decls:
            self.visit_var_decl(decl)

        for func in node.functions:
            self.visit_function(func)

    def visit_function(self, node: FunctionDefNode) -> None:
        self.current_function = node.name

        self.program.add(tac_func_begin(node.name))

        for param in node.params:
            if param.name:
                self.program.add(tac_declare(param.name))

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
        for item in node.items:
            if isinstance(item, VarSimpleDeclNode):
                self.program.add(tac_declare(item.name))

            elif isinstance(item, VarInitDeclNode):
                self.program.add(tac_declare(item.name))
                value = self.visit_expr(item.value)
                self.program.add(tac_assign(item.name, value))

            elif isinstance(item, VarSizedArrayDeclNode):
                self.program.add(tac_array_decl(item.name, str(item.size)))

            elif isinstance(item, VarUnsizedArrayDeclNode):
                self.program.add(tac_array_decl(item.name, "?"))

            elif isinstance(item, VarArrayInitDeclNode):
                self.program.add(tac_array_decl(item.name, str(len(item.values))))

                for index, expr in enumerate(item.values):
                    value = self.visit_expr(expr)
                    self.program.add(tac_array_init(item.name, str(index), value))

            elif isinstance(item, VarArrayExprInitDeclNode):
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

        if isinstance(target, IdentifierNode):
            self.program.add(tac_assign(target.name, value))

        elif isinstance(target, ArrayAccessNode):
            index = self.visit_expr(target.index)
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
            left = self.visit_cond_expr(cond.left)
            right = self.visit_cond_expr(cond.right)

            # Normaliza ambos os operandos para 0/1 antes de os combinar.
            # Sem esta normalizacao, o '||' implementado como soma podia
            # anular-se (ex.: 1 || -1 -> 1 + (-1) = 0, falsamente falso) e o
            # '&&' como produto podia exceder 1. Com os operandos em {0,1}:
            #   &&  ->  produto em {0,1}
            #   ||  ->  soma em {0,1,2} (tratada como verdadeira se != 0)
            left_bool = self._new_temp()
            self.program.add(tac_binary(left_bool, left, "!=", "0"))

            right_bool = self._new_temp()
            self.program.add(tac_binary(right_bool, right, "!=", "0"))

            temp = self._new_temp()

            if cond.operator == "&&":
                self.program.add(tac_binary(temp, left_bool, "*", right_bool))
                return temp

            if cond.operator == "||":
                self.program.add(tac_binary(temp, left_bool, "+", right_bool))
                return temp

            raise TACGenerationError(
                f"Operador lógico desconhecido: {cond.operator}"
            )

        raise TACGenerationError(
            f"Condição sem tratamento TAC: {type(cond).__name__}"
        )

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

        args = [self.visit_expr(arg) for arg in call.args]

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
    # Utilitários
    # =====================================================

    def _format_string_literal(self, value: str) -> str:
        escaped = value.replace("\\", "\\\\").replace('"', '\\"')
        return f'"{escaped}"'