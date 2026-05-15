"""
ast_nodes.py — Definição de nós da Árvore de Sintaxe Abstrata (AST) para MOCP.
UC 21018 — Compilação, Universidade Aberta, 2025/2026
Autores: Maria Costa (2304361) | João Rodrigues (2203474) | Nuno Rolo ([Nº A PREENCHER]) | Fábio Oliveira ([Nº A PREENCHER])
Grupo: QUADCORE
"""

from dataclasses import dataclass, field
from typing import List, Optional, Any


class ASTNode:
    def pretty(self, indent: int = 0) -> str:
        return self._pretty(indent)

    def _pretty(self, indent: int = 0) -> str:
        pad = "  " * indent
        lines = [f"{pad}{self.__class__.__name__}"]

        for name, value in vars(self).items():
            lines.extend(self._pretty_field(name, value, indent + 1))

        return "\n".join(lines)

    def _pretty_field(self, name: str, value: Any, indent: int) -> List[str]:
        pad = "  " * indent
        lines: List[str] = []

        if isinstance(value, ASTNode):
            lines.append(f"{pad}{name}:")
            lines.append(value._pretty(indent + 1))

        elif isinstance(value, list):
            if not value:
                lines.append(f"{pad}{name}: []")
            else:
                lines.append(f"{pad}{name}: [")
                for item in value:
                    if isinstance(item, ASTNode):
                        lines.append(item._pretty(indent + 1))
                    else:
                        lines.append(f"{pad}  {repr(item)}")
                lines.append(f"{pad}]")

        else:
            lines.append(f"{pad}{name}: {repr(value)}")

        return lines

    def __str__(self) -> str:
        return self.pretty()


# =========================================================
# Programa e topo
# =========================================================

@dataclass
class ProgramNode(ASTNode):
    prototypes: List["PrototypeNode"] = field(default_factory=list)
    global_decls: List["VarDeclNode"] = field(default_factory=list)
    functions: List["FunctionDefNode"] = field(default_factory=list)


@dataclass
class PrototypeNode(ASTNode):
    return_type: str
    name: str
    params: List["ParamNode"] = field(default_factory=list)


@dataclass
class FunctionDefNode(ASTNode):
    return_type: str
    name: str
    params: List["ParamNode"] = field(default_factory=list)
    body: Optional["BlockNode"] = None


@dataclass
class ParamNode(ASTNode):
    param_type: str
    name: str
    is_array: bool = False


# =========================================================
# Blocos e declarações
# =========================================================

@dataclass
class BlockNode(ASTNode):
    declarations: List["VarDeclNode"] = field(default_factory=list)
    statements: List["StmtNode"] = field(default_factory=list)


class StmtNode(ASTNode):
    pass


@dataclass
class VarDeclNode(ASTNode):
    var_type: str
    items: List["VarItemNode"] = field(default_factory=list)


class VarItemNode(ASTNode):
    pass


@dataclass
class VarSimpleDeclNode(VarItemNode):
    name: str


@dataclass
class VarInitDeclNode(VarItemNode):
    name: str
    value: "ExprNode"


@dataclass
class VarSizedArrayDeclNode(VarItemNode):
    name: str
    size: int


@dataclass
class VarUnsizedArrayDeclNode(VarItemNode):
    name: str


@dataclass
class VarArrayInitDeclNode(VarItemNode):
    name: str
    values: List["ExprNode"] = field(default_factory=list)


@dataclass
class VarArrayExprInitDeclNode(VarItemNode):
    name: str
    value: "ExprNode"


# =========================================================
# Instruções
# =========================================================

@dataclass
class AssignStmtNode(StmtNode):
    target: "LocationNode"
    value: "ExprNode"


@dataclass
class IfStmtNode(StmtNode):
    condition: "CondNode"
    then_block: BlockNode
    else_block: Optional[BlockNode] = None


@dataclass
class WhileStmtNode(StmtNode):
    condition: "CondNode"
    body: BlockNode


@dataclass
class ForStmtNode(StmtNode):
    init: Optional["AssignExprNode"] = None
    condition: Optional["CondNode"] = None
    update: Optional["AssignExprNode"] = None
    body: Optional[BlockNode] = None


@dataclass
class ReturnStmtNode(StmtNode):
    value: Optional["ExprNode"] = None


@dataclass
class ExprStmtNode(StmtNode):
    expr: "ExprNode"


@dataclass
class EmptyStmtNode(StmtNode):
    pass


@dataclass
class AssignExprNode(ASTNode):
    target: "LocationNode"
    value: "ExprNode"


# =========================================================
# Condições
# =========================================================

class CondNode(ASTNode):
    pass


@dataclass
class RelationalCondNode(CondNode):
    left: "ExprNode"
    operator: str
    right: "ExprNode"


@dataclass
class NotCondNode(CondNode):
    operand: CondNode


@dataclass
class BinaryLogicalCondNode(CondNode):
    left: CondNode
    operator: str
    right: CondNode


@dataclass
class ExprAsCondNode(CondNode):
    expr: "ExprNode"


# =========================================================
# Expressões
# =========================================================

class ExprNode(ASTNode):
    pass


@dataclass
class BinaryExprNode(ExprNode):
    left: ExprNode
    operator: str
    right: ExprNode


@dataclass
class UnaryExprNode(ExprNode):
    operator: str
    operand: ExprNode


@dataclass
class CastExprNode(ExprNode):
    target_type: str
    expr: ExprNode


# =========================================================
# Localizações
# =========================================================

class LocationNode(ExprNode):
    pass


@dataclass
class IdentifierNode(LocationNode):
    name: str


@dataclass
class ArrayAccessNode(LocationNode):
    name: str
    index: ExprNode


# =========================================================
# Chamadas de função
# =========================================================

@dataclass
class FunctionCallNode(ExprNode):
    name: str
    args: List[ExprNode] = field(default_factory=list)
    is_reserved_io: bool = False


# =========================================================
# Literais
# =========================================================

@dataclass
class IntLiteralNode(ExprNode):
    value: int


@dataclass
class RealLiteralNode(ExprNode):
    value: float


@dataclass
class StringLiteralNode(ExprNode):
    value: str
