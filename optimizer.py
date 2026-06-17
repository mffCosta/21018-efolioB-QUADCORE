"""
optimizer.py — Otimização de código intermédio TAC para MOCP.
UC 21018 — Compilação, Universidade Aberta, 2025/2026
Grupo: QUADCORE
Autores: Maria Costa (2304361) | João Rodrigues (2203474) | Nuno Rolo (1900405) | Fábio Oliveira (1800960)

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
        """
        Elimina definições mortas de temporários, com análise de vivacidade
        SENSÍVEL AO FLUXO DE CONTROLO.

        Uma versão anterior fazia um único passe linear para trás, o que estava
        ERRADO na presença de saltos: no losango de curto-circuito de '&&'/'||'
        (t=1; goto FIM; L: t=0; FIM: ...) o ramo 't=0' apagava 't' do conjunto
        de vivos e o 'goto' não repunha a vivacidade vinda da etiqueta de junção,
        pelo que a atribuição 't=1' era apagada e a expressão lógica ficava
        miscompilada. Aqui calcula-se a vivacidade por ponto-fixo sobre o grafo
        de fluxo (cada salto/etiqueta liga os pontos certos), o que torna a
        eliminação correta para qualquer estrutura de controlo.
        """
        instrs = program.instructions
        n = len(instrs)
        temporaries = program.temporaries

        if n == 0:
            return TACProgram([], temporaries=set(temporaries))

        # Índice de cada etiqueta (são únicas em todo o programa).
        label_index: Dict[str, int] = {
            instr.label: i for i, instr in enumerate(instrs) if instr.op == "label"
        }

        def successors(i: int) -> List[int]:
            instr = instrs[i]
            op = instr.op
            if op == "goto":
                tgt = label_index.get(instr.label)
                return [tgt] if tgt is not None else []
            if op in ("if", "ifFalse"):
                succ: List[int] = []
                if i + 1 < n:
                    succ.append(i + 1)
                tgt = label_index.get(instr.label)
                if tgt is not None:
                    succ.append(tgt)
                return succ
            # 'return' e 'func_end' não têm continuação; uma função nunca cai na
            # seguinte (não há aresta de fluxo entre funções).
            if op in ("return", "func_end"):
                return []
            return [i + 1] if i + 1 < n else []

        defs = [instr.defines() for instr in instrs]
        uses = [instr.uses() for instr in instrs]
        live_in: List[Set[str]] = [set() for _ in range(n)]
        live_out: List[Set[str]] = [set() for _ in range(n)]

        # Ponto-fixo de vivacidade (para trás).
        changed = True
        while changed:
            changed = False
            for i in range(n - 1, -1, -1):
                out: Set[str] = set()
                for s in successors(i):
                    out |= live_in[s]
                new_in = uses[i] | (out - ({defs[i]} if defs[i] else set()))
                if out != live_out[i] or new_in != live_in[i]:
                    live_out[i] = out
                    live_in[i] = new_in
                    changed = True

        # Remove definições mortas: só temporários do compilador, sem efeitos
        # laterais e não vivos à saída da instrução. Variáveis do utilizador
        # preservam-se sempre.
        kept: List[TACInstruction] = []
        for i, instr in enumerate(instrs):
            defined = defs[i]
            if (
                not instr.has_side_effect()
                and defined is not None
                and defined in temporaries
                and defined not in live_out[i]
            ):
                self.changed = True
                continue
            kept.append(instr)

        return TACProgram(kept, temporaries=set(temporaries))

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
        # Esta função só formata RESULTADOS REAIS (dobragem de '+ - * /' reais,
        # simétrico real e cast para real). Tem de preservar a marca de real —
        # o ponto decimal — mesmo quando o valor é inteiro (ex.: 3.0 - 2.0 = 1.0).
        # Caso contrário, "1.0" colapsaria para "1" e o back-end imprimi-lo-ia
        # como inteiro (print_int) em vez de real (print_float).
        if value.is_integer():
            return f"{int(value)}.0"
        return repr(value)