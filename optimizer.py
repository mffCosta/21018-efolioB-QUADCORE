"""
optimizer.py — Otimização de código intermédio TAC para MOCP.
UC 21018 — Compilação, Universidade Aberta, 2025/2026
Grupo: QUADCORE
Autores: Maria Costa (2304361) | João Rodrigues (2203474) | Nuno Rolo ([Nº A PREENCHER]) | Fábio Oliveira ([Nº A PREENCHER])

Otimizações implementadas:
  1. Constant folding
  2. Simplificação algébrica
  3. Constant propagation
  4. Copy propagation
  5. Dead code elimination conservadora

A otimização é conservadora: não remove instruções com efeitos laterais,
saltos, labels, chamadas, retornos, acessos de escrita a vetores ou I/O.
"""

from typing import Dict, Optional, Set, List
from copy import deepcopy

from tac import (
    TACProgram,
    TACInstruction,
    is_numeric_literal,
    is_real_literal,
    is_variable_like,
    is_binary_operator,
)


class TACOptimizer:
    """
    Otimizador simples e conservador para TAC.

    A abordagem é iterativa: aplica passes sucessivos enquanto houver alterações.
    """

    def __init__(self, max_iterations: int = 8):
        self.max_iterations = max_iterations
        self.changed = False

    # =====================================================
    # API principal
    # =====================================================

    def optimize(self, program: TACProgram) -> TACProgram:
        optimized = program.copy()

        for _ in range(self.max_iterations):
            self.changed = False

            optimized = self.constant_folding_and_algebraic_simplification(optimized)
            optimized = self.constant_and_copy_propagation(optimized)
            optimized = self.dead_code_elimination(optimized)
            optimized = self.remove_nops(optimized)

            if not self.changed:
                break

        return optimized

    # =====================================================
    # 1. Constant folding + simplificação algébrica
    # =====================================================

    def constant_folding_and_algebraic_simplification(
        self,
        program: TACProgram
    ) -> TACProgram:
        new_program = TACProgram(temporaries=set(program.temporaries))

        for instr in program.instructions:
            instr = deepcopy(instr)

            if is_binary_operator(instr.op):
                folded = self._try_constant_fold(instr)
                if folded is not None:
                    new_program.add(folded)
                    self.changed = True
                    continue

                simplified = self._try_algebraic_simplification(instr)
                if simplified is not None:
                    new_program.add(simplified)
                    self.changed = True
                    continue

            if instr.op == "uminus" and is_numeric_literal(instr.arg1):
                value = self._eval_unary_minus(instr.arg1)
                new_program.add(TACInstruction(
                    op="assign",
                    result=instr.result,
                    arg1=value,
                    comment="constant folding"
                ))
                self.changed = True
                continue

            if instr.op == "cast" and is_numeric_literal(instr.arg1):
                value = self._eval_cast(instr.arg1, instr.arg2)
                if value is not None:
                    new_program.add(TACInstruction(
                        op="assign",
                        result=instr.result,
                        arg1=value,
                        comment="constant folding cast"
                    ))
                    self.changed = True
                    continue

            new_program.add(instr)

        return new_program

    def _try_constant_fold(self, instr: TACInstruction) -> Optional[TACInstruction]:
        if instr.arg1 is None or instr.arg2 is None:
            return None

        if not is_numeric_literal(instr.arg1) or not is_numeric_literal(instr.arg2):
            return None

        result = self._eval_binary(instr.arg1, instr.op, instr.arg2)

        if result is None:
            return None

        return TACInstruction(
            op="assign",
            result=instr.result,
            arg1=result,
            comment="constant folding"
        )

    def _try_algebraic_simplification(
        self,
        instr: TACInstruction
    ) -> Optional[TACInstruction]:
        op = instr.op
        left = instr.arg1
        right = instr.arg2
        target = instr.result

        if op == "+":
            if right == "0":
                return TACInstruction("assign", result=target, arg1=left,
                                      comment="x + 0")
            if left == "0":
                return TACInstruction("assign", result=target, arg1=right,
                                      comment="0 + x")

        if op == "-":
            if right == "0":
                return TACInstruction("assign", result=target, arg1=left,
                                      comment="x - 0")

        if op == "*":
            if right == "1":
                return TACInstruction("assign", result=target, arg1=left,
                                      comment="x * 1")
            if left == "1":
                return TACInstruction("assign", result=target, arg1=right,
                                      comment="1 * x")
            if right == "0" or left == "0":
                return TACInstruction("assign", result=target, arg1="0",
                                      comment="x * 0")

        if op == "/":
            if right == "1":
                return TACInstruction("assign", result=target, arg1=left,
                                      comment="x / 1")

        if op == "%":
            if right == "1":
                return TACInstruction("assign", result=target, arg1="0",
                                      comment="x % 1")

        return None

    # =====================================================
    # 2. Constant propagation + copy propagation
    # =====================================================

    def constant_and_copy_propagation(self, program: TACProgram) -> TACProgram:
        new_program = TACProgram(temporaries=set(program.temporaries))

        constants: Dict[str, str] = {}
        copies: Dict[str, str] = {}

        for instr in program.instructions:
            instr = deepcopy(instr)

            # Barreiras de fluxo: evita propagar informação de forma insegura
            if instr.op in {"label", "goto", "if", "ifFalse", "func_begin", "func_end"}:
                constants.clear()
                copies.clear()
                new_program.add(instr)
                continue

            # Substituir usos conhecidos.
            # Em escritas de vetor evitamos propagação para não alterar a semântica
            # em presença de aliases ou dependências de memória.
            before = deepcopy(instr)
            if instr.op not in {"array_store", "array_init", "write"}:
                self._replace_uses(instr, constants, copies)

            if instr != before:
                self.changed = True

            # Se a instrução tem efeitos laterais, invalida informação conservadoramente
            if instr.op in {"call", "write", "read", "readc", "reads", "array_store", "array_init"}:
                if instr.op in {"array_store", "array_init"}:
                    constants.clear()
                    copies.clear()

                defined = instr.defines()
                if defined:
                    self._kill(defined, constants, copies)

                new_program.add(instr)
                continue

            defined = instr.defines()

            if defined:
                self._kill(defined, constants, copies)

                if instr.op == "assign":
                    if is_numeric_literal(instr.arg1):
                        constants[defined] = instr.arg1
                    elif is_variable_like(instr.arg1):
                        root = self._resolve_copy(instr.arg1, copies)
                        copies[defined] = root

            new_program.add(instr)

        return new_program

    def _replace_uses(
        self,
        instr: TACInstruction,
        constants: Dict[str, str],
        copies: Dict[str, str]
    ) -> None:
        instr.arg1 = self._replace_value(instr.arg1, constants, copies)
        instr.arg2 = self._replace_value(instr.arg2, constants, copies)

        # Para array_store, o campo result é o nome do vetor e não deve ser substituído.
        # Para instruções normais, result é destino e também não deve ser substituído.

    def _replace_value(
        self,
        value: Optional[str],
        constants: Dict[str, str],
        copies: Dict[str, str]
    ) -> Optional[str]:
        if value is None:
            return None

        if not is_variable_like(value):
            return value

        value = self._resolve_copy(value, copies)

        if value in constants:
            return constants[value]

        return value

    def _resolve_copy(self, value: str, copies: Dict[str, str]) -> str:
        seen = set()

        while value in copies and value not in seen:
            seen.add(value)
            value = copies[value]

        return value

    def _kill(
        self,
        name: str,
        constants: Dict[str, str],
        copies: Dict[str, str]
    ) -> None:
        constants.pop(name, None)
        copies.pop(name, None)

        # remover cópias que dependiam deste nome
        for key in list(copies.keys()):
            if copies[key] == name:
                copies.pop(key, None)

    # =====================================================
    # 3. Dead code elimination conservadora
    # =====================================================

    def dead_code_elimination(self, program: TACProgram) -> TACProgram:
        live: Set[str] = set()
        kept_reversed: List[TACInstruction] = []
        temporaries = program.temporaries

        for instr in reversed(program.instructions):
            defined = instr.defines()
            used = instr.uses()

            if instr.has_side_effect():
                kept_reversed.append(instr)
                live.update(used)

                if defined:
                    live.discard(defined)

                continue

            if defined is None:
                kept_reversed.append(instr)
                live.update(used)
                continue

            # Só se eliminam temporários gerados pelo compilador (registados
            # em program.temporaries) que não voltam a ser usados. Variáveis
            # do utilizador são sempre preservadas, ainda que tenham um nome
            # com o padrão de um temporário.
            if defined in live or defined not in temporaries:
                kept_reversed.append(instr)
                live.discard(defined)
                live.update(used)
            else:
                self.changed = True

        kept_reversed.reverse()
        return TACProgram(kept_reversed, temporaries=set(temporaries))

    # =====================================================
    # 4. Remoção de NOPs
    # =====================================================

    def remove_nops(self, program: TACProgram) -> TACProgram:
        new_program = TACProgram(temporaries=set(program.temporaries))

        for instr in program.instructions:
            if instr.op == "nop":
                self.changed = True
                continue
            new_program.add(instr)

        return new_program

    # =====================================================
    # Avaliação de expressões constantes
    # =====================================================

    def _eval_binary(self, left: str, op: str, right: str) -> Optional[str]:
        try:
            if is_real_literal(left) or is_real_literal(right):
                a = float(left)
                b = float(right)

                if op == "+":
                    return self._format_number(a + b)
                if op == "-":
                    return self._format_number(a - b)
                if op == "*":
                    return self._format_number(a * b)
                if op == "/":
                    if b == 0:
                        return None
                    return self._format_number(a / b)

                # Relações devolvem inteiro lógico: 1 verdadeiro, 0 falso
                if op == "<":
                    return "1" if a < b else "0"
                if op == "<=":
                    return "1" if a <= b else "0"
                if op == ">":
                    return "1" if a > b else "0"
                if op == ">=":
                    return "1" if a >= b else "0"
                if op == "==":
                    return "1" if a == b else "0"
                if op == "!=":
                    return "1" if a != b else "0"

                return None

            a = int(left)
            b = int(right)

            if op == "+":
                return str(a + b)
            if op == "-":
                return str(a - b)
            if op == "*":
                return str(a * b)
            if op == "/":
                if b == 0:
                    return None
                # Divisao inteira com truncamento para zero (regras do C),
                # em vez do floor que o operador // do Python aplica.
                return str(self._c_int_div(a, b))
            if op == "%":
                if b == 0:
                    return None
                # Resto coerente com a divisao truncada do C:
                #   a % b == a - (a / b) * b
                return str(a - self._c_int_div(a, b) * b)

            if op == "<":
                return "1" if a < b else "0"
            if op == "<=":
                return "1" if a <= b else "0"
            if op == ">":
                return "1" if a > b else "0"
            if op == ">=":
                return "1" if a >= b else "0"
            if op == "==":
                return "1" if a == b else "0"
            if op == "!=":
                return "1" if a != b else "0"

            return None

        except Exception:
            return None

    def _c_int_div(self, a: int, b: int) -> int:
        """
        Divisao inteira com truncamento para zero, como em C.
        Difere do operador // do Python, que arredonda para baixo
        (ex.: -7 / 2 == -3 em C, mas -7 // 2 == -4 em Python).
        """
        quociente = abs(a) // abs(b)
        if (a < 0) != (b < 0):
            quociente = -quociente
        return quociente

    def _eval_unary_minus(self, value: str) -> str:
        if is_real_literal(value):
            return self._format_number(-float(value))

        return str(-int(value))

    def _eval_cast(self, value: str, target_type: Optional[str]) -> Optional[str]:
        try:
            if target_type == "inteiro":
                return str(int(float(value)))

            if target_type == "real":
                return self._format_number(float(value))

            return None
        except Exception:
            return None

    def _format_number(self, value: float) -> str:
        if value.is_integer():
            return str(int(value))
        return str(value)