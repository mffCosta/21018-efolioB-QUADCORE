"""
semantic.py — Análise semântica para MOCP.
UC 21018 — Compilação, Universidade Aberta, 2025/2026
Autores: Maria Costa (2304361) | João Rodrigues (2203474) | Nuno Rolo ([Nº A PREENCHER]) | Fábio Oliveira ([Nº A PREENCHER])
Grupo: QUADCORE

Responsabilidades:
  - gestão de tabela de símbolos;
  - validação de variáveis e funções;
  - validação de tipos;
  - validação de vetores;
  - validação de retornos;
  - preparação semântica para geração de código intermédio.
"""

from dataclasses import dataclass
from typing import Dict, List, Optional

from ast_nodes import (
    ProgramNode,
    PrototypeNode,
    FunctionDefNode,
    ParamNode,
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


# =========================================================
# Exceção semântica
# =========================================================

class SemanticError(Exception):
    pass


# =========================================================
# Símbolos
# =========================================================

@dataclass
class VariableSymbol:
    name: str
    var_type: str
    is_array: bool = False


@dataclass
class FunctionSymbol:
    name: str
    return_type: str
    params: List[ParamNode]
    has_definition: bool = False


# =========================================================
# Tabela de símbolos multinível
# =========================================================

class SymbolTable:
    def __init__(self):
        self.scopes: List[Dict[str, VariableSymbol]] = [{}]

    def enter_scope(self) -> None:
        self.scopes.append({})

    def exit_scope(self) -> None:
        if len(self.scopes) == 1:
            raise RuntimeError("Não é possível remover o scope global.")
        self.scopes.pop()

    def declare(self, symbol: VariableSymbol) -> None:
        current_scope = self.scopes[-1]
        if symbol.name in current_scope:
            raise SemanticError(
                f"Identificador '{symbol.name}' já declarado neste bloco."
            )
        current_scope[symbol.name] = symbol

    def lookup(self, name: str) -> Optional[VariableSymbol]:
        for scope in reversed(self.scopes):
            if name in scope:
                return scope[name]
        return None


# =========================================================
# Analisador semântico
# =========================================================

class SemanticAnalyzer:
    def __init__(self):
        self.symbols = SymbolTable()
        self.functions: Dict[str, FunctionSymbol] = {}
        self.current_function: Optional[FunctionSymbol] = None

        self.reserved_io = {
            "ler",
            "lerc",
            "lers",
            "escrever",
            "escreverc",
            "escrevers",
            "escreverv",
        }

    # -----------------------------------------------------
    # API principal
    # -----------------------------------------------------

    def analyze(self, program: ProgramNode) -> None:
        self._register_builtins()
        self._register_prototypes(program.prototypes)
        self._register_function_headers(program.functions)

        self._check_main_exists()
        self._check_main_signature()

        for decl in program.global_decls:
            self.visit_var_decl(decl)

        for func in program.functions:
            self.visit_function(func)

        self._check_prototypes_defined()

    # -----------------------------------------------------
    # Registo inicial
    # -----------------------------------------------------

    def _register_builtins(self) -> None:
        self.functions["ler"] = FunctionSymbol("ler", "inteiro", [], True)
        self.functions["lerc"] = FunctionSymbol("lerc", "inteiro", [], True)
        self.functions["lers"] = FunctionSymbol("lers", "inteiro[]", [], True)

        self.functions["escrever"] = FunctionSymbol(
            "escrever", "vazio", [ParamNode("inteiro", "x", False)], True
        )
        self.functions["escreverc"] = FunctionSymbol(
            "escreverc", "vazio", [ParamNode("inteiro", "x", False)], True
        )
        self.functions["escrevers"] = FunctionSymbol(
            "escrevers", "vazio", [ParamNode("inteiro", "s", True)], True
        )
        self.functions["escreverv"] = FunctionSymbol(
            "escreverv", "vazio", [ParamNode("inteiro", "v", True)], True
        )

    def _register_prototypes(self, prototypes: List[PrototypeNode]) -> None:
        for proto in prototypes:
            if proto.name in self.reserved_io:
                raise SemanticError(
                    f"Não é permitido declarar protótipo com nome reservado '{proto.name}'."
                )

            existing = self.functions.get(proto.name)
            if existing is not None and existing.name not in self.reserved_io:
                self._check_function_signature_compatibility(
                    proto.name,
                    existing.return_type,
                    existing.params,
                    proto.return_type,
                    proto.params,
                )
            else:
                self.functions[proto.name] = FunctionSymbol(
                    name=proto.name,
                    return_type=proto.return_type,
                    params=proto.params,
                    has_definition=False,
                )

    def _register_function_headers(self, functions: List[FunctionDefNode]) -> None:
        for func in functions:
            if func.name in self.reserved_io:
                raise SemanticError(
                    f"Não é permitido definir função com nome reservado '{func.name}'."
                )

            existing = self.functions.get(func.name)
            if existing is not None and existing.name not in self.reserved_io:
                self._check_function_signature_compatibility(
                    func.name,
                    existing.return_type,
                    existing.params,
                    func.return_type,
                    func.params,
                )

                if existing.has_definition:
                    raise SemanticError(
                        f"Função '{func.name}' definida mais do que uma vez."
                    )

                existing.has_definition = True
            else:
                self.functions[func.name] = FunctionSymbol(
                    name=func.name,
                    return_type=func.return_type,
                    params=func.params,
                    has_definition=True,
                )

    def _check_main_exists(self) -> None:
        if "principal" not in self.functions:
            raise SemanticError("A função 'principal' não foi definida.")

    def _check_main_signature(self) -> None:
        principal = self.functions.get("principal")

        if principal is None:
            return

        if principal.return_type != "vazio":
            raise SemanticError(
                "A função 'principal' deve ter tipo de retorno 'vazio'."
            )

        if len(principal.params) != 0:
            raise SemanticError(
                "A função 'principal' não deve receber parâmetros. Use principal(vazio)."
            )

        if not principal.has_definition:
            raise SemanticError(
                "A função 'principal' foi declarada, mas não foi definida."
            )

    def _check_prototypes_defined(self) -> None:
        for name, fn in self.functions.items():
            if name in self.reserved_io:
                continue
            if not fn.has_definition:
                raise SemanticError(
                    f"A função '{name}' foi declarada em protótipo mas não foi definida."
                )

    def _check_function_signature_compatibility(
        self,
        name: str,
        ret1: str,
        params1: List[ParamNode],
        ret2: str,
        params2: List[ParamNode],
    ) -> None:
        if ret1 != ret2:
            raise SemanticError(
                f"Assinatura incompatível para a função '{name}': tipos de retorno diferentes."
            )

        if len(params1) != len(params2):
            raise SemanticError(
                f"Assinatura incompatível para a função '{name}': número de parâmetros diferente."
            )

        for i, (p1, p2) in enumerate(zip(params1, params2), start=1):
            if p1.param_type != p2.param_type or p1.is_array != p2.is_array:
                raise SemanticError(
                    f"Assinatura incompatível para a função '{name}' no parâmetro {i}."
                )

    # -----------------------------------------------------
    # Funções / blocos
    # -----------------------------------------------------

    def visit_function(self, func: FunctionDefNode) -> None:
        self.current_function = self.functions[func.name]
        self.symbols.enter_scope()

        for param in func.params:
            if param.name:
                self.symbols.declare(
                    VariableSymbol(
                        name=param.name,
                        var_type=param.param_type,
                        is_array=param.is_array,
                    )
                )

        self.visit_block(func.body, create_scope=False)

        if func.return_type != "vazio" and not self._block_has_return(func.body):
            raise SemanticError(
                f"A função '{func.name}' deve conter pelo menos uma instrução 'retornar'."
            )

        self.symbols.exit_scope()
        self.current_function = None

    def visit_block(self, block: BlockNode, create_scope: bool = True) -> None:
        if create_scope:
            self.symbols.enter_scope()

        for decl in block.declarations:
            self.visit_var_decl(decl)

        for stmt in block.statements:
            self.visit_stmt(stmt)

        if create_scope:
            self.symbols.exit_scope()

    def _block_has_return(self, block: BlockNode) -> bool:
        for stmt in block.statements:
            if isinstance(stmt, ReturnStmtNode):
                return True

            if isinstance(stmt, BlockNode) and self._block_has_return(stmt):
                return True

            if isinstance(stmt, IfStmtNode):
                then_has = self._block_has_return(stmt.then_block)
                else_has = (
                    self._block_has_return(stmt.else_block)
                    if stmt.else_block is not None
                    else False
                )
                if then_has and else_has:
                    return True

            # Um 'retornar' dentro do corpo de um ciclo conta como retorno
            # existente. O ciclo pode nao executar, mas esta verificacao
            # destina-se apenas a confirmar que a funcao tem pelo menos um
            # 'retornar', evitando falsos positivos.
            if isinstance(stmt, WhileStmtNode) and self._block_has_return(stmt.body):
                return True

            if isinstance(stmt, ForStmtNode) and stmt.body is not None \
                    and self._block_has_return(stmt.body):
                return True

        return False

    # -----------------------------------------------------
    # Declarações
    # -----------------------------------------------------

    def visit_var_decl(self, decl: VarDeclNode) -> None:
        for item in decl.items:
            if isinstance(item, VarSimpleDeclNode):
                self.symbols.declare(
                    VariableSymbol(item.name, decl.var_type, False)
                )

            elif isinstance(item, VarInitDeclNode):
                value_type = self.visit_expr(item.value)
                self._check_assignment_compatible(decl.var_type, value_type)
                self.symbols.declare(
                    VariableSymbol(item.name, decl.var_type, False)
                )

            elif isinstance(item, VarSizedArrayDeclNode):
                if item.size <= 0:
                    raise SemanticError(
                        f"O vetor '{item.name}' deve ter tamanho positivo."
                    )
                self.symbols.declare(
                    VariableSymbol(item.name, decl.var_type, True)
                )

            elif isinstance(item, VarUnsizedArrayDeclNode):
                self.symbols.declare(
                    VariableSymbol(item.name, decl.var_type, True)
                )

            elif isinstance(item, VarArrayInitDeclNode):
                for expr in item.values:
                    expr_type = self.visit_expr(expr)
                    self._check_assignment_compatible(decl.var_type, expr_type)

                self.symbols.declare(
                    VariableSymbol(item.name, decl.var_type, True)
                )

            elif isinstance(item, VarArrayExprInitDeclNode):
                value_type = self.visit_expr(item.value)
                expected = f"{decl.var_type}[]"

                if value_type != expected:
                    raise SemanticError(
                        f"Inicialização incompatível do vetor '{item.name}': "
                        f"recebido '{value_type}', esperado '{expected}'."
                    )

                self.symbols.declare(
                    VariableSymbol(item.name, decl.var_type, True)
                )

    # -----------------------------------------------------
    # Instruções
    # -----------------------------------------------------

    def visit_stmt(self, stmt) -> None:
        if isinstance(stmt, AssignStmtNode):
            target_type = self.visit_location(stmt.target)
            value_type = self.visit_expr(stmt.value)
            self._check_assignment_compatible(target_type, value_type)

        elif isinstance(stmt, IfStmtNode):
            self.visit_cond(stmt.condition)
            self.visit_block(stmt.then_block)
            if stmt.else_block is not None:
                self.visit_block(stmt.else_block)

        elif isinstance(stmt, WhileStmtNode):
            self.visit_cond(stmt.condition)
            self.visit_block(stmt.body)

        elif isinstance(stmt, ForStmtNode):
            if stmt.init is not None:
                self.visit_assign_expr(stmt.init)
            if stmt.condition is not None:
                self.visit_cond(stmt.condition)
            if stmt.update is not None:
                self.visit_assign_expr(stmt.update)

            self.visit_block(stmt.body)

        elif isinstance(stmt, ReturnStmtNode):
            self.visit_return_stmt(stmt)

        elif isinstance(stmt, ExprStmtNode):
            self.visit_expr(stmt.expr)

        elif isinstance(stmt, EmptyStmtNode):
            pass

        elif isinstance(stmt, BlockNode):
            self.visit_block(stmt)

        else:
            raise SemanticError(
                f"Instrução sem tratamento semântico: {type(stmt).__name__}"
            )

    def visit_assign_expr(self, expr: AssignExprNode) -> None:
        target_type = self.visit_location(expr.target)
        value_type = self.visit_expr(expr.value)
        self._check_assignment_compatible(target_type, value_type)

    def visit_return_stmt(self, stmt: ReturnStmtNode) -> None:
        if self.current_function is None:
            raise SemanticError("Instrução 'retornar' fora de função.")

        expected = self.current_function.return_type

        if expected == "vazio":
            if stmt.value is not None:
                raise SemanticError(
                    f"A função '{self.current_function.name}' é do tipo 'vazio' "
                    "e não deve retornar valor."
                )
        else:
            if stmt.value is None:
                raise SemanticError(
                    f"A função '{self.current_function.name}' deve retornar um valor."
                )

            received = self.visit_expr(stmt.value)
            self._check_assignment_compatible(expected, received)

    # -----------------------------------------------------
    # Condições
    # -----------------------------------------------------

    def visit_cond(self, cond) -> None:
        if isinstance(cond, ExprAsCondNode):
            expr_type = self.visit_expr(cond.expr)
            self._check_condition_type(expr_type)

        elif isinstance(cond, RelationalCondNode):
            left_type = self.visit_expr(cond.left)
            right_type = self.visit_expr(cond.right)

            self._check_condition_type(left_type)
            self._check_condition_type(right_type)

            if left_type.endswith("[]") or right_type.endswith("[]"):
                raise SemanticError(
                    "Condições relacionais não podem ser aplicadas a vetores."
                )

        elif isinstance(cond, NotCondNode):
            self.visit_cond(cond.operand)

        elif isinstance(cond, BinaryLogicalCondNode):
            self.visit_cond(cond.left)
            self.visit_cond(cond.right)

        else:
            raise SemanticError(
                f"Condição sem tratamento semântico: {type(cond).__name__}"
            )

    # -----------------------------------------------------
    # Expressões
    # -----------------------------------------------------

    def visit_expr(self, expr) -> str:
        if isinstance(expr, IdentifierNode):
            return self.visit_identifier(expr)

        if isinstance(expr, ArrayAccessNode):
            return self.visit_array_access(expr)

        if isinstance(expr, FunctionCallNode):
            return self.visit_function_call(expr)

        if isinstance(expr, BinaryExprNode):
            left_type = self.visit_expr(expr.left)
            right_type = self.visit_expr(expr.right)
            return self._infer_binary_expr_type(left_type, right_type, expr.operator)

        if isinstance(expr, UnaryExprNode):
            operand_type = self.visit_expr(expr.operand)
            if operand_type.endswith("[]"):
                raise SemanticError(
                    f"Operador unário '{expr.operator}' não permitido com vetor."
                )
            return operand_type

        if isinstance(expr, CastExprNode):
            inner_type = self.visit_expr(expr.expr)
            if inner_type.endswith("[]"):
                raise SemanticError("Não é permitido fazer cast de vetores.")
            return expr.target_type

        if isinstance(expr, IntLiteralNode):
            return "inteiro"

        if isinstance(expr, RealLiteralNode):
            return "real"

        if isinstance(expr, StringLiteralNode):
            # Em MOCP, strings são representadas como vetores de inteiros
            # terminados em 0.
            return "inteiro[]"

        raise SemanticError(
            f"Expressão sem tratamento semântico: {type(expr).__name__}"
        )

    def visit_identifier(self, ident: IdentifierNode) -> str:
        symbol = self.symbols.lookup(ident.name)
        if symbol is None:
            raise SemanticError(
                f"Variável '{ident.name}' usada sem declaração prévia."
            )
        return f"{symbol.var_type}[]" if symbol.is_array else symbol.var_type

    def visit_array_access(self, access: ArrayAccessNode) -> str:
        symbol = self.symbols.lookup(access.name)
        if symbol is None:
            raise SemanticError(
                f"Variável '{access.name}' usada sem declaração prévia."
            )

        if not symbol.is_array:
            raise SemanticError(
                f"O identificador '{access.name}' não é um vetor."
            )

        index_type = self.visit_expr(access.index)
        if index_type != "inteiro":
            raise SemanticError(
                f"O índice do vetor '{access.name}' deve ser do tipo 'inteiro'."
            )

        return symbol.var_type

    def visit_location(self, loc) -> str:
        if isinstance(loc, IdentifierNode):
            return self.visit_identifier(loc)

        if isinstance(loc, ArrayAccessNode):
            return self.visit_array_access(loc)

        raise SemanticError(f"Localização inválida: {type(loc).__name__}")

    def visit_function_call(self, call: FunctionCallNode) -> str:
        fn = self.functions.get(call.name)
        if fn is None:
            raise SemanticError(
                f"Função '{call.name}' chamada mas não declarada/definida."
            )

        arg_types = [self.visit_expr(arg) for arg in call.args]

        expected = len(fn.params)
        received = len(call.args)

        if expected != received:
            raise SemanticError(
                f"Chamada à função '{call.name}' com {received} argumento(s), "
                f"mas eram esperados {expected}."
            )

        if call.name == "escrever":
            for i, arg_type in enumerate(arg_types, start=1):
                if arg_type.endswith("[]"):
                    raise SemanticError(
                        f"Tipo incompatível no argumento {i} da função 'escrever': "
                        f"recebido '{arg_type}', esperado valor simples."
                    )
            return fn.return_type

        if call.name == "escreverc":
            for i, arg_type in enumerate(arg_types, start=1):
                if arg_type != "inteiro":
                    raise SemanticError(
                        f"Tipo incompatível no argumento {i} da função 'escreverc': "
                        f"recebido '{arg_type}', esperado 'inteiro'."
                    )
            return fn.return_type

        if call.name == "escrevers":
            for i, arg_type in enumerate(arg_types, start=1):
                if arg_type != "inteiro[]":
                    raise SemanticError(
                        f"Tipo incompatível no argumento {i} da função 'escrevers': "
                        f"recebido '{arg_type}', esperado 'inteiro[]'."
                    )
            return fn.return_type

        if call.name == "escreverv":
            for i, arg_type in enumerate(arg_types, start=1):
                if not arg_type.endswith("[]"):
                    raise SemanticError(
                        f"Tipo incompatível no argumento {i} da função 'escreverv': "
                        f"recebido '{arg_type}', esperado vetor."
                    )
            return fn.return_type

        for i, (arg_type, param) in enumerate(zip(arg_types, fn.params), start=1):
            expected_type = param.param_type
            if param.is_array and not expected_type.endswith("[]"):
                expected_type += "[]"

            if not self._types_compatible(expected_type, arg_type):
                raise SemanticError(
                    f"Tipo incompatível no argumento {i} da função '{call.name}': "
                    f"recebido '{arg_type}', esperado '{expected_type}'."
                )

        return fn.return_type

    # -----------------------------------------------------
    # Inferência e validações de tipos
    # -----------------------------------------------------

    def _infer_binary_expr_type(self, left_type: str, right_type: str, operator: str) -> str:
        if left_type.endswith("[]") or right_type.endswith("[]"):
            raise SemanticError(
                f"Operação '{operator}' não permitida com vetores."
            )

        if operator == "%":
            if left_type != "inteiro" or right_type != "inteiro":
                raise SemanticError(
                    "O operador '%' exige operandos inteiros."
                )
            return "inteiro"

        if operator in {"<", "<=", ">", ">=", "==", "!="}:
            self._check_condition_type(left_type)
            self._check_condition_type(right_type)
            return "inteiro"

        if left_type == "real" or right_type == "real":
            return "real"

        return "inteiro"

    def _check_assignment_compatible(self, target_type: str, value_type: str) -> None:
        if not self._types_compatible(target_type, value_type):
            raise SemanticError(
                f"Atribuição incompatível: destino '{target_type}', valor '{value_type}'."
            )

    def _types_compatible(self, target_type: str, value_type: str) -> bool:
        if target_type == value_type:
            return True

        # Conversões numéricas básicas, coerentes com a especificação da MOCP
        # e com as conversões simples entre inteiro e real.
        if target_type in {"inteiro", "real"} and value_type in {"inteiro", "real"}:
            return True

        return False

    def _check_condition_type(self, typ: str) -> None:
        if typ.endswith("[]"):
            raise SemanticError(
                f"Tipo '{typ}' não pode ser usado diretamente como condição."
            )