"""
tac.py — Representação de Código Intermédio TAC para MOCP.
UC 21018 — Compilação, Universidade Aberta, 2025/2026
Grupo: QUADCORE
Autores: Maria Costa (2304361) | João Rodrigues (2203474) | Nuno Rolo ([Nº A PREENCHER]) | Fábio Oliveira ([Nº A PREENCHER])

Este módulo define uma representação estruturada de Three Address Code (TAC),
preparada para:
  - geração de código intermédio;
  - impressão legível;
  - otimização posterior;
  - análise de usos/definições.
"""

from dataclasses import dataclass, field
from typing import List, Optional, Set


# =========================================================
# Instrução TAC
# =========================================================

@dataclass
class TACInstruction:
    """
    Representa uma instrução de código intermédio do tipo Three Address Code.

    Campos principais:
      op      — operação TAC
      result  — destino da operação
      arg1    — primeiro operando
      arg2    — segundo operando
      label   — label associada, quando aplicável
      comment — comentário opcional para facilitar leitura/relatório

    Exemplos:
      t1 = a + b              -> op='+', result='t1', arg1='a', arg2='b'
      x = t1                  -> op='assign', result='x', arg1='t1'
      ifFalse t1 goto L1      -> op='ifFalse', arg1='t1', label='L1'
      goto L2                 -> op='goto', label='L2'
      L1:                     -> op='label', label='L1'
      call escrever, x        -> op='call', result='escrever', arg1='x'
      return x                -> op='return', arg1='x'
    """

    op: str
    result: Optional[str] = None
    arg1: Optional[str] = None
    arg2: Optional[str] = None
    label: Optional[str] = None
    comment: Optional[str] = None

    # -----------------------------------------------------
    # Representação textual
    # -----------------------------------------------------

    def __str__(self) -> str:
        text = self.to_string()

        if self.comment:
            return f"{text:<40} # {self.comment}"

        return text

    def to_string(self) -> str:
        if self.op == "label":
            return f"{self.label}:"

        if self.op == "goto":
            return f"goto {self.label}"

        if self.op == "if":
            return f"if {self.arg1} goto {self.label}"

        if self.op == "ifFalse":
            return f"ifFalse {self.arg1} goto {self.label}"

        if self.op == "assign":
            return f"{self.result} = {self.arg1}"

        if self.op in {"+", "-", "*", "/", "%", "<", "<=", ">", ">=", "==", "!="}:
            return f"{self.result} = {self.arg1} {self.op} {self.arg2}"

        if self.op == "uminus":
            return f"{self.result} = -{self.arg1}"

        if self.op == "cast":
            return f"{self.result} = ({self.arg2}) {self.arg1}"

        if self.op == "array_load":
            return f"{self.result} = {self.arg1}[{self.arg2}]"

        if self.op == "array_store":
            return f"{self.result}[{self.arg1}] = {self.arg2}"

        if self.op == "array_decl":
            return f"declare {self.result}[{self.arg1}]"

        if self.op == "array_init":
            return f"{self.result}[{self.arg1}] = {self.arg2}"

        if self.op == "param":
            return f"param {self.arg1}"

        if self.op == "call":
            if self.result:
                return f"{self.result} = call {self.arg1}, {self.arg2}"
            return f"call {self.arg1}, {self.arg2}"

        if self.op == "return":
            if self.arg1 is None:
                return "return"
            return f"return {self.arg1}"

        if self.op == "func_begin":
            return f"func {self.label}:"

        if self.op == "func_end":
            return f"endfunc {self.label}"

        if self.op == "declare":
            return f"declare {self.result}"

        if self.op == "read":
            return f"{self.result} = call ler, 0"

        if self.op == "readc":
            return f"{self.result} = call lerc, 0"

        if self.op == "reads":
            return f"{self.result} = call lers, 0"

        if self.op == "write":
            return f"call {self.arg1}, {self.arg2}"

        if self.op == "nop":
            return "nop"

        return self._fallback_string()

    def _fallback_string(self) -> str:
        parts = [self.op]

        if self.result is not None:
            parts.append(f"result={self.result}")
        if self.arg1 is not None:
            parts.append(f"arg1={self.arg1}")
        if self.arg2 is not None:
            parts.append(f"arg2={self.arg2}")
        if self.label is not None:
            parts.append(f"label={self.label}")

        return " ".join(parts)

    # -----------------------------------------------------
    # Apoio à otimização
    # -----------------------------------------------------

    def defines(self) -> Optional[str]:
        """
        Devolve a variável/temporário definido pela instrução, se existir.
        Usado em otimizações como dead code elimination.
        """
        if self.op in {
            "assign",
            "+", "-", "*", "/", "%",
            "<", "<=", ">", ">=", "==", "!=",
            "uminus",
            "cast",
            "array_load",
            "call",
            "read",
            "readc",
            "reads",
        }:
            return self.result

        return None

    def uses(self) -> Set[str]:
        """
        Devolve o conjunto de variáveis/temporários usados pela instrução.
        Literais numéricos e strings não são considerados usos.
        """
        uses: Set[str] = set()

        def add_if_var(value: Optional[str]) -> None:
            if value is not None and is_variable_like(value):
                uses.add(value)

        if self.op in {"+", "-", "*", "/", "%", "<", "<=", ">", ">=", "==", "!="}:
            add_if_var(self.arg1)
            add_if_var(self.arg2)

        elif self.op in {"assign", "uminus", "cast", "if", "ifFalse", "return", "param"}:
            add_if_var(self.arg1)

        elif self.op == "array_load":
            add_if_var(self.arg1)
            add_if_var(self.arg2)

        elif self.op == "array_store":
            add_if_var(self.result)
            add_if_var(self.arg1)
            add_if_var(self.arg2)

        elif self.op == "array_init":
            add_if_var(self.result)
            add_if_var(self.arg1)
            add_if_var(self.arg2)

        elif self.op == "call":
            add_if_var(self.arg2)

        elif self.op == "write":
            add_if_var(self.arg2)

        return uses

    def has_side_effect(self) -> bool:
        """
        Indica se a instrução tem efeitos laterais e não deve ser removida
        por otimizações conservadoras.
        """
        return self.op in {
            "goto",
            "if",
            "ifFalse",
            "label",
            "func_begin",
            "func_end",
            "return",
            "param",
            "call",
            "write",
            "array_store",
            "array_init",
            "declare",
            "array_decl",
            "read",
            "readc",
            "reads",
        }


# =========================================================
# Programa TAC
# =========================================================

@dataclass
class TACProgram:
    """
    Representa o conjunto completo de instruções TAC de um programa.

    O campo 'temporaries' guarda o conjunto de nomes de temporários
    efetivamente gerados pelo compilador. É usado pela otimização
    (dead code elimination) para distinguir, sem ambiguidade, um
    temporário de uma variável do utilizador que, por acaso, tenha um
    nome com o mesmo padrão (por exemplo, uma variável chamada 't1').
    """

    instructions: List[TACInstruction] = field(default_factory=list)
    temporaries: Set[str] = field(default_factory=set)

    def add(self, instruction: TACInstruction) -> None:
        self.instructions.append(instruction)

    def extend(self, instructions: List[TACInstruction]) -> None:
        self.instructions.extend(instructions)

    def __iter__(self):
        return iter(self.instructions)

    def __len__(self) -> int:
        return len(self.instructions)

    def __getitem__(self, index: int) -> TACInstruction:
        return self.instructions[index]

    def to_string(self, numbered: bool = False) -> str:
        lines = []

        for i, instr in enumerate(self.instructions):
            if numbered:
                lines.append(f"{i:04d}: {instr}")
            else:
                lines.append(str(instr))

        return "\n".join(lines)

    def pretty(self) -> str:
        return self.to_string(numbered=True)

    def copy(self) -> "TACProgram":
        return TACProgram(
            instructions=[
                TACInstruction(
                    op=instr.op,
                    result=instr.result,
                    arg1=instr.arg1,
                    arg2=instr.arg2,
                    label=instr.label,
                    comment=instr.comment,
                )
                for instr in self.instructions
            ],
            temporaries=set(self.temporaries),
        )


# =========================================================
# Gerador de temporários e labels
# =========================================================

class TACNameGenerator:
    """
    Gera nomes únicos para temporários e labels.

    Temporários:
      t1, t2, t3, ...

    Labels:
      L1, L2, L3, ...
    """

    def __init__(self):
        self.temp_counter = 0
        self.label_counter = 0

    def new_temp(self) -> str:
        self.temp_counter += 1
        return f"t{self.temp_counter}"

    def new_label(self, prefix: str = "L") -> str:
        self.label_counter += 1
        return f"{prefix}{self.label_counter}"


# =========================================================
# Funções auxiliares
# =========================================================

def is_int_literal(value: Optional[str]) -> bool:
    if value is None:
        return False

    try:
        int(value)
        return True
    except ValueError:
        return False


def is_real_literal(value: Optional[str]) -> bool:
    if value is None:
        return False

    try:
        float(value)
        return "." in value
    except ValueError:
        return False


def is_numeric_literal(value: Optional[str]) -> bool:
    return is_int_literal(value) or is_real_literal(value)


def is_string_literal(value: Optional[str]) -> bool:
    if value is None:
        return False

    return len(value) >= 2 and value[0] == '"' and value[-1] == '"'


def is_variable_like(value: Optional[str]) -> bool:
    """
    Determina se um valor parece ser variável/temporário.

    Exclui:
      - None
      - literais inteiros
      - literais reais
      - strings literais
    """
    if value is None:
        return False

    if is_numeric_literal(value):
        return False

    if is_string_literal(value):
        return False

    return True


def is_temporary(value: Optional[str]) -> bool:
    if value is None:
        return False

    if not value.startswith("t"):
        return False

    suffix = value[1:]
    return suffix.isdigit()


def is_binary_operator(op: str) -> bool:
    return op in {"+", "-", "*", "/", "%", "<", "<=", ">", ">=", "==", "!="}


def is_jump(op: str) -> bool:
    return op in {"goto", "if", "ifFalse"}


def is_label(op: str) -> bool:
    return op == "label"


def is_arithmetic_operator(op: str) -> bool:
    return op in {"+", "-", "*", "/", "%"}


def is_relational_operator(op: str) -> bool:
    return op in {"<", "<=", ">", ">=", "==", "!="}


# =========================================================
# Construtores auxiliares de instruções
# =========================================================

def tac_label(label: str) -> TACInstruction:
    return TACInstruction(op="label", label=label)


def tac_goto(label: str) -> TACInstruction:
    return TACInstruction(op="goto", label=label)


def tac_if(condition: str, label: str) -> TACInstruction:
    return TACInstruction(op="if", arg1=condition, label=label)


def tac_if_false(condition: str, label: str) -> TACInstruction:
    return TACInstruction(op="ifFalse", arg1=condition, label=label)


def tac_assign(target: str, value: str) -> TACInstruction:
    return TACInstruction(op="assign", result=target, arg1=value)


def tac_binary(target: str, left: str, op: str, right: str) -> TACInstruction:
    return TACInstruction(op=op, result=target, arg1=left, arg2=right)


def tac_unary_minus(target: str, value: str) -> TACInstruction:
    return TACInstruction(op="uminus", result=target, arg1=value)


def tac_cast(target: str, value: str, target_type: str) -> TACInstruction:
    return TACInstruction(op="cast", result=target, arg1=value, arg2=target_type)


def tac_array_load(target: str, array_name: str, index: str) -> TACInstruction:
    return TACInstruction(op="array_load", result=target, arg1=array_name, arg2=index)


def tac_array_store(array_name: str, index: str, value: str) -> TACInstruction:
    return TACInstruction(op="array_store", result=array_name, arg1=index, arg2=value)


def tac_array_decl(array_name: str, size: str) -> TACInstruction:
    return TACInstruction(op="array_decl", result=array_name, arg1=size)


def tac_array_init(array_name: str, index: str, value: str) -> TACInstruction:
    return TACInstruction(op="array_init", result=array_name, arg1=index, arg2=value)


def tac_param(value: str) -> TACInstruction:
    return TACInstruction(op="param", arg1=value)


def tac_call(function_name: str, arg_count: int, target: Optional[str] = None) -> TACInstruction:
    return TACInstruction(
        op="call",
        result=target,
        arg1=function_name,
        arg2=str(arg_count),
    )


def tac_return(value: Optional[str] = None) -> TACInstruction:
    return TACInstruction(op="return", arg1=value)


def tac_func_begin(name: str) -> TACInstruction:
    return TACInstruction(op="func_begin", label=name)


def tac_func_end(name: str) -> TACInstruction:
    return TACInstruction(op="func_end", label=name)


def tac_declare(name: str) -> TACInstruction:
    return TACInstruction(op="declare", result=name)


def tac_read(target: str) -> TACInstruction:
    return TACInstruction(op="read", result=target)


def tac_readc(target: str) -> TACInstruction:
    return TACInstruction(op="readc", result=target)


def tac_reads(target: str) -> TACInstruction:
    return TACInstruction(op="reads", result=target)


def tac_write(function_name: str, value: str) -> TACInstruction:
    return TACInstruction(op="write", arg1=function_name, arg2=value)


def tac_nop() -> TACInstruction:
    return TACInstruction(op="nop")