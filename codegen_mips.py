"""
codegen_mips.py — Geração de código final MIPS (alvo: simulador MARS) a partir do TAC MOCP.
UC 21018 — Compilação, Universidade Aberta, 2025/2026
Grupo: QUADCORE
Autores: Maria Costa (2304361) | João Rodrigues (2203474) | Nuno Rolo (1900405) | Fábio Oliveira (1800960)

Esta é a etapa de BACK-END do compilador: traduz o código intermédio (TAC),
abstrato e não executável, para código MIPS real, executável no simulador MARS.

Linguagem final escolhida : MIPS (assembly de 32 bits).
Simulador para testar      : MARS  (MIPS Assembler and Runtime Simulator).

------------------------------------------------------------------------------
ESTADO DESTA ITERAÇÃO  (linguagem MOCP completa)
------------------------------------------------------------------------------
Suportado e testado de ponta a ponta (no simulador MARS):
  - funções, convenção de chamadas e recursão  (func/endfunc, getparam, param,
    call, return)  -> bastidor de pilha com $fp;
  - escalares inteiros, aritmética (+ - * / %), simétrico, relacionais;
  - REAIS (vírgula flutuante, precisão simples): aritmética (+ - * /), simétrico,
    comparações relacionais, conversões inteiro<->real (int_to_real/real_to_int),
    cast do utilizador e escrita (escrever de um real -> print_float);
  - controlo de fluxo (label, goto, if, ifFalse);
  - vetores (inteiros e reais): declaração local, inicialização a 0, leitura/
    escrita indexada e PASSAGEM POR REFERÊNCIA como parâmetro;
  - vetores de dimensão determinada em execução (array_decl '?'): a ranhura
    guarda um PONTEIRO para memória dinâmica (sbrk);
  - E/S completa: escrever, escreverc, escrevers, escreverv, ler, lerc, lers.

ESTRATÉGIA PARA OS REAIS
  Um 'real' MOCP é de precisão simples (32 bits) e cada valor já ocupa uma
  palavra. Por isso os reais circulam como PADRÃO DE BITS pela via inteira
  habitual (lw/sw, $v0, pilha): só se usam registos de vírgula flutuante
  ($f*) nos pontos onde há mesmo cálculo real (aritmética, comparação,
  conversão e escrita). Um passe de inferência de tipos sobre o TAC decide,
  em cada instrução, se os operandos são inteiros ou reais (o TAC já traz as
  conversões int_to_real/real_to_int materializadas, o que torna a inferência
  local e fiável).

------------------------------------------------------------------------------
CONVENÇÃO DE E/S DEFINIDA POR NÓS (o enunciado não a fixa)
------------------------------------------------------------------------------
  escrever(n)   -> imprime o inteiro (ou o real) seguido de mudança de linha;
  escreverc(c)  -> imprime um único caráter (código ASCII), sem mudança de linha;
  escrevers(s)  -> imprime a cadeia tal e qual, sem mudança de linha
                   (cadeia literal ou inteiro[] terminado em 0, ex.: lers());
  escreverv(v)  -> imprime cada elemento do vetor seguido de '\\n' (como
                   'escrever' aplicado a cada elemento; dimensão estática);
  lers()        -> lê uma linha e devolve-a como inteiro[] terminado em 0.

------------------------------------------------------------------------------
CONVENÇÃO DE CHAMADAS (bastidor de pilha)
------------------------------------------------------------------------------
A pilha cresce para baixo. Para uma função com FRAME bytes de bastidor:

        endereços altos
        +------------------------+
        |  arg(n-1) ... arg0     |  <- empurrados pelo CHAMADOR; arg0 em 0($fp)
        +------------------------+  <- $fp aponta aqui (fronteira dos argumentos)
        |  $ra guardado          |  -4($fp)
        |  $fp guardado          |  -8($fp)
        |  locais / temporários  |  ... (offsets negativos a partir de $fp)
        +------------------------+  <- $sp aponta aqui (fundo do bastidor)
        endereços baixos

Cada local/temporário ocupa 1 palavra (4 bytes); cada vetor local ocupa N
palavras contíguas. Não há alocação de registos: cada instrução TAC carrega os
operandos para registos, calcula e volta a guardar em memória. É simples e
correto (a recursão funciona porque cada chamada tem o seu próprio bastidor).
"""

import struct
from typing import Dict, List, Optional, Set, Tuple

from tac import (
    TACProgram,
    TACInstruction,
    is_int_literal,
    is_real_literal,
    is_string_literal,
    is_variable_like,
)


class MIPSGenerationError(Exception):
    """Erro interno do gerador MIPS: TAC inesperado/malformado. É uma rede de
    segurança (defesa contra invariantes violadas) — não deve ocorrer para
    programas aceites pelo front-end, cuja linguagem o back-end cobre por completo."""
    pass


# Funções de E/S reservadas da linguagem (não são funções do utilizador).
INPUT_FUNCTIONS = {"ler", "lerc", "lers"}
OUTPUT_FUNCTIONS = {"escrever", "escreverc", "escrevers", "escreverv"}


def _align8(n: int) -> int:
    """Arredonda para cima ao múltiplo de 8 mais próximo."""
    return (n + 7) & ~7


class _Frame:
    """
    Descreve o bastidor de pilha de uma função: que nomes são locais, em que
    offset (relativo a $fp) ficam, quais são vetores e qual o tamanho total.
    """

    def __init__(self) -> None:
        # nome -> (offset_relativo_a_fp, is_array, n_palavras)
        self.slots: Dict[str, Tuple[int, bool, int]] = {}
        self.arrays: Dict[str, int] = {}      # nome do vetor local -> tamanho
        self.locals_declared: set = set()      # nomes com declare/getparam/array_decl
        self.frame_size: int = 8               # mínimo: $ra + $fp guardados

    def fp_offset(self, name: str) -> int:
        return self.slots[name][0]

    def is_local_array(self, name: str) -> bool:
        return name in self.arrays

    def has(self, name: str) -> bool:
        return name in self.slots


class MIPSGenerator:
    """Gera um programa MIPS (texto) a partir de um TACProgram já otimizado."""

    def __init__(self) -> None:
        self.lines: List[str] = []
        self.string_pool: Dict[str, str] = {}   # texto-com-aspas -> rótulo .data
        self.global_scalars: Dict[str, str] = {}  # nome -> valor inicial textual
        self.global_arrays: Dict[str, int] = {}   # nome -> tamanho
        self.global_reals: Set[str] = set()        # globais escalares de tipo real
        # Vetores globais com inicializador literal constante ('{...}'):
        # nome -> {indice: valor}; emitidos como '.word'/'.float' no .data.
        self.global_array_init: Dict[str, Dict[int, str]] = {}
        self.global_array_real: Set[str] = set()   # desses, os de elementos reais
        # Inicialização global NÃO-constante (ex.: g = lers(), g = f(...)):
        # corre num arranque sintético '__init' antes de 'principal'.
        self.global_init_code: List[TACInstruction] = []
        self.func_names: set = set()
        self.frame: Optional[_Frame] = None
        self.pending_params: List[str] = []
        self._helper_label_counter = 0

        # Inferência de tipos (inteiro vs real) sobre o TAC.
        self.func_return_real: Dict[str, bool] = {}        # função -> devolve real?
        self._per_func_real_scalars: Dict[str, Set[str]] = {}
        self._per_func_real_arrays: Dict[str, Set[str]] = {}
        self.real_scalars: Set[str] = set()    # nomes reais na função atual
        self.real_arrays: Set[str] = set()     # vetores de elementos reais (função atual)
        self._lers_helper_needed = False       # gerar a rotina de runtime __lers?

    # =====================================================
    # API principal
    # =====================================================

    def generate(self, program: TACProgram) -> str:
        instructions = list(program.instructions)

        pre_func, functions = self._split_functions(instructions)
        self.func_names = {name for name, _ in functions}

        # Recolher globais (escalares/vetores) e strings.
        self._collect_globals(pre_func)
        self._collect_strings(instructions)

        # Inicialização global não-constante (ex.: 'g = lers()', 'g = f(...)')
        # corre num arranque sintético '__init', tratado como mais uma função.
        if self.global_init_code:
            functions = functions + [("__init", self.global_init_code)]

        # Inferir, por função, que nomes guardam reais (decide inteiro vs $f*).
        self._infer_types(functions)

        # lers() precisa de uma rotina de runtime e de um buffer de leitura: é
        # decidido aqui (antes do .data) para reservar o buffer no segmento certo.
        self._lers_helper_needed = any(instr.op == "reads" for instr in instructions)

        self._emit_data_segment()
        self._emit_text_segment(functions)

        return "\n".join(self.lines) + "\n"

    # =====================================================
    # Separação do programa em funções
    # =====================================================

    def _split_functions(
        self, instructions: List[TACInstruction]
    ) -> Tuple[List[TACInstruction], List[Tuple[str, List[TACInstruction]]]]:
        pre_func: List[TACInstruction] = []
        functions: List[Tuple[str, List[TACInstruction]]] = []

        current_name: Optional[str] = None
        current_body: List[TACInstruction] = []
        in_func = False

        for instr in instructions:
            if instr.op == "func_begin":
                in_func = True
                current_name = instr.label
                current_body = []
            elif instr.op == "func_end":
                functions.append((current_name, current_body))
                in_func = False
                current_name = None
                current_body = []
            elif in_func:
                current_body.append(instr)
            else:
                pre_func.append(instr)

        return pre_func, functions

    # =====================================================
    # Recolha de globais e strings
    # =====================================================

    def _collect_globals(self, pre_func: List[TACInstruction]) -> None:
        # 1ª passagem: declarações reservam armazenamento no .data. Um vetor de
        # dimensão dinâmica ('?') guarda um PONTEIRO, logo trata-se como escalar.
        for instr in pre_func:
            if instr.op == "declare":
                self.global_scalars.setdefault(instr.result, "0")
            elif instr.op == "array_decl":
                if instr.arg1 == "?":
                    self.global_scalars.setdefault(instr.result, "0")
                else:
                    self.global_arrays[instr.result] = int(instr.arg1)

        # 2ª passagem: inicializadores. Os constantes em compilação vão para o
        # .data; os restantes (lers(), chamadas, expressões não dobráveis) são
        # adiados para o arranque sintético '__init' (self.global_init_code).
        for instr in pre_func:
            op = instr.op
            if op in ("declare", "array_decl", "nop", "array_zero_init"):
                continue
            if op == "assign" and instr.result in self.global_scalars \
                    and is_int_literal(instr.arg1):
                self.global_scalars[instr.result] = instr.arg1
            elif op == "assign" and instr.result in self.global_scalars \
                    and is_real_literal(instr.arg1):
                self.global_scalars[instr.result] = instr.arg1
                self.global_reals.add(instr.result)
            elif op == "array_init" and instr.result in self.global_arrays \
                    and is_int_literal(instr.arg1) \
                    and (is_int_literal(instr.arg2) or is_real_literal(instr.arg2)):
                # Elemento constante de um vetor literal global -> vai para o .data.
                self.global_array_init.setdefault(instr.result, {})[
                    int(instr.arg1)
                ] = instr.arg2
                if is_real_literal(instr.arg2):
                    self.global_array_real.add(instr.result)
            else:
                # Inicialização não-constante: executar no arranque ('__init').
                self.global_init_code.append(instr)

    def _collect_strings(self, instructions: List[TACInstruction]) -> None:
        for instr in instructions:
            for operand in (instr.arg1, instr.arg2):
                if is_string_literal(operand) and operand not in self.string_pool:
                    label = f"str_{len(self.string_pool)}"
                    self.string_pool[operand] = label

    # =====================================================
    # Inferência de tipos (inteiro vs real)
    # =====================================================
    #
    # O TAC não anota tipos, mas o gerador de TAC já materializa as conversões
    # numéricas (int_to_real / real_to_int) em todas as fronteiras (atribuição,
    # retorno, argumentos, promoção em expressões mistas). Isso torna cada
    # instrução localmente coerente e permite descobrir, por ponto-fixo, que
    # nomes guardam reais. Só precisamos desta distinção nos sítios onde o
    # cálculo difere mesmo entre inteiro e real (aritmética, comparação,
    # conversão e escrita); cópias, vetores e passagem de argumentos movem 32
    # bits e funcionam igual para ambos.

    def _infer_types(self, functions: List[Tuple[str, List[TACInstruction]]]) -> None:
        self.func_return_real = {name: False for name, _ in functions}

        # Ponto-fixo externo: o tipo de retorno de uma função influencia o tipo
        # do destino de 'call' (e logo a inferência de quem a chama).
        for _ in range(len(functions) + 2):
            changed = False
            for name, body in functions:
                rscal, rarr = self._infer_function_reals(body)
                self._per_func_real_scalars[name] = rscal
                self._per_func_real_arrays[name] = rarr

                ret_real = any(
                    instr.op == "return"
                    and instr.arg1 is not None
                    and self._name_is_real(instr.arg1, rscal)
                    for instr in body
                )
                if ret_real != self.func_return_real.get(name, False):
                    self.func_return_real[name] = ret_real
                    changed = True
            if not changed:
                break

    def _name_is_real(self, name: Optional[str], real_scalars: Set[str]) -> bool:
        if name is None:
            return False
        if is_real_literal(name):
            return True
        if name in self.global_reals:
            return True
        return name in real_scalars

    def _infer_function_reals(
        self, body: List[TACInstruction]
    ) -> Tuple[Set[str], Set[str]]:
        """Devolve (nomes_reais, vetores_de_elementos_reais) para uma função."""
        real: Set[str] = set()
        arr_real: Set[str] = set()

        def is_real(x: Optional[str]) -> bool:
            return self._name_is_real(x, real)

        changed = True
        while changed:
            changed = False

            def mark(n: Optional[str]) -> None:
                nonlocal changed
                if n is not None and is_variable_like(n) and n not in real:
                    real.add(n)
                    changed = True

            def mark_arr(a: Optional[str]) -> None:
                nonlocal changed
                if a is not None and is_variable_like(a) and a not in arr_real:
                    arr_real.add(a)
                    changed = True

            for instr in body:
                op = instr.op
                if op == "int_to_real":
                    mark(instr.result)              # destino é real
                elif op == "real_to_int":
                    mark(instr.arg1)                # origem é real (destino é int)
                elif op == "cast":
                    if instr.arg2 == "real":
                        mark(instr.result)
                elif op == "assign":
                    if is_real(instr.arg1):
                        mark(instr.result)
                    if is_real(instr.result):
                        mark(instr.arg1)
                elif op in ("+", "-", "*", "/"):
                    # O gerador promove operandos mistos: os três têm o mesmo
                    # tipo. ('%' exige inteiros e nunca é real.)
                    if is_real(instr.arg1) or is_real(instr.arg2) or is_real(instr.result):
                        mark(instr.result)
                        mark(instr.arg1)
                        mark(instr.arg2)
                elif op == "uminus":
                    if is_real(instr.arg1):
                        mark(instr.result)
                    if is_real(instr.result):
                        mark(instr.arg1)
                # As relações NÃO propagam: o resultado é inteiro (0/1) e os
                # operandos podem ser de tipos diferentes (o gerador não promove
                # em contexto de condição). Cada operando mantém o seu tipo.
                elif op == "array_load":            # result = arg1[arg2]
                    if instr.arg1 in arr_real:
                        mark(instr.result)
                    if is_real(instr.result):
                        mark_arr(instr.arg1)
                elif op in ("array_store", "array_init"):   # result[arg1] = arg2
                    if is_real(instr.arg2):
                        mark_arr(instr.result)
                    if instr.result in arr_real:
                        mark(instr.arg2)
                elif op == "call":                  # result = call arg1, arg2
                    if instr.result is not None and self.func_return_real.get(instr.arg1):
                        mark(instr.result)

        return real, arr_real

    def _is_real(self, operand: Optional[str]) -> bool:
        """Operando real no contexto da função a ser gerada agora?"""
        return self._name_is_real(operand, self.real_scalars)

    # =====================================================
    # Segmento de dados
    # =====================================================

    def _emit_data_segment(self) -> None:
        self.lines.append("# " + "=" * 60)
        self.lines.append("# Segmento de dados")
        self.lines.append("# " + "=" * 60)
        self.lines.append(".data")

        for name, value in self.global_scalars.items():
            if name in self.global_reals:
                # '.float' guarda o valor em IEEE-754 de precisão simples; lido
                # depois como 32 bits crus (lw) ou como real (lwc1).
                self.lines.append(f"g_{name}: .float {value}")
            else:
                self.lines.append(f"g_{name}: .word {value}")

        for name, size in self.global_arrays.items():
            if name in self.global_array_init:
                # Vetor com inicializador literal constante -> valores no .data.
                values = self.global_array_init[name]
                if name in self.global_array_real:
                    items = [str(values.get(i, "0.0")) for i in range(size)]
                    self.lines.append(f"g_{name}: .float " + ", ".join(items))
                else:
                    items = [str(values.get(i, "0")) for i in range(size)]
                    self.lines.append(f"g_{name}: .word " + ", ".join(items))
            else:
                self.lines.append(f"g_{name}: .space {4 * size}")

        for literal, label in self.string_pool.items():
            # 'literal' já vem com aspas e escapes válidos do TAC.
            self.lines.append(f"{label}: .asciiz {literal}")

        if self._lers_helper_needed:
            # Buffer de bytes onde lers() lê a linha (via read_string) antes de a
            # expandir para inteiro[].
            self.lines.append("__lers_buf: .space 1024")

        # Linha em branco a separar visualmente os dados do código.
        self.lines.append("")

    # =====================================================
    # Segmento de texto
    # =====================================================

    def _emit_text_segment(
        self, functions: List[Tuple[str, List[TACInstruction]]]
    ) -> None:
        self.lines.append("# " + "=" * 60)
        self.lines.append("# Segmento de código")
        self.lines.append("# " + "=" * 60)
        self.lines.append(".text")
        self.lines.append(".globl main")
        self.lines.append("")

        # Arranque: inicializa globais não-constantes (se houver), chama
        # 'principal' e termina o programa (syscall 10).
        self.lines.append("main:")
        if self.global_init_code:
            self.lines.append("    jal f___init")
        self.lines.append("    jal f_principal")
        self.lines.append("    li $v0, 10")
        self.lines.append("    syscall")
        self.lines.append("")

        for name, body in functions:
            self._emit_function(name, body)

        # Rotinas de runtime usadas pelo código gerado (emitidas uma só vez).
        if self._lers_helper_needed:
            self._emit_lers_helper()

    def _emit_function(self, name: str, body: List[TACInstruction]) -> None:
        self.frame = self._analyze_frame(body)
        self.real_scalars = self._per_func_real_scalars.get(name, set())
        self.real_arrays = self._per_func_real_arrays.get(name, set())
        self.pending_params = []

        frame_size = self.frame.frame_size

        self.lines.append(f"# ---- função {name} (bastidor = {frame_size} bytes) ----")
        self.lines.append(f"f_{name}:")
        # Prólogo.
        self._ins(f"addiu $sp, $sp, -{frame_size}")
        self._ins(f"sw $ra, {frame_size - 4}($sp)")
        self._ins(f"sw $fp, {frame_size - 8}($sp)")
        self._ins(f"addiu $fp, $sp, {frame_size}")

        for instr in body:
            self._emit_instruction(instr)

        # Epílogo de segurança (funções 'vazio' que caem no fim sem 'return').
        self.lines.append(f"f_{name}_end:")
        self._emit_epilogue()
        self.lines.append("")

    def _emit_epilogue(self) -> None:
        self._ins("lw $ra, -4($fp)")
        self._ins("lw $t8, -8($fp)")     # $fp anterior (temporário)
        self._ins("move $sp, $fp")        # liberta o bastidor
        self._ins("move $fp, $t8")        # restaura $fp do chamador
        self._ins("jr $ra")

    # =====================================================
    # Análise do bastidor (offsets dos locais)
    # =====================================================

    def _analyze_frame(self, body: List[TACInstruction]) -> _Frame:
        frame = _Frame()

        # 1) Vetores locais e nomes declarados localmente.
        for instr in body:
            if instr.op == "array_decl":
                if instr.arg1 == "?":
                    # Dimensão só conhecida em execução (ex.: 's[] = lers()'): a
                    # ranhura guarda um PONTEIRO (1 palavra) para memória dinâmica,
                    # logo trata-se como um escalar — NÃO entra em frame.arrays.
                    frame.locals_declared.add(instr.result)
                else:
                    frame.arrays[instr.result] = int(instr.arg1)
                    frame.locals_declared.add(instr.result)
            elif instr.op in ("declare", "getparam"):
                frame.locals_declared.add(instr.result)

        # 2) Ordem de aparecimento de todos os nomes locais (inclui temporários).
        order: List[str] = []
        seen = set()

        def consider(name: Optional[str]) -> None:
            if not self._is_local_name(name, frame):
                return
            if name not in seen:
                seen.add(name)
                order.append(name)

        for instr in body:
            # 'result' de uma chamada/escrita pode ser nome de função: filtra-se
            # em _is_local_name através de self.func_names.
            consider(instr.result)
            consider(instr.arg1)
            consider(instr.arg2)

        # 3) Atribuir offsets (a contar do fundo do bastidor, $sp + k).
        offset_from_sp = 0
        layout: List[Tuple[str, int, bool, int]] = []
        for name in order:
            if name in frame.arrays:
                words = frame.arrays[name]
                layout.append((name, offset_from_sp, True, words))
                offset_from_sp += 4 * words
            else:
                layout.append((name, offset_from_sp, False, 1))
                offset_from_sp += 4

        data_bytes = offset_from_sp
        frame.frame_size = _align8(data_bytes + 8)  # +8 = $ra e $fp guardados

        # Converter offsets para relativos a $fp (negativos).
        for name, off_sp, is_arr, words in layout:
            fp_off = off_sp - frame.frame_size
            frame.slots[name] = (fp_off, is_arr, words)

        return frame

    def _is_local_name(self, name: Optional[str], frame: _Frame) -> bool:
        """Decide se um operando é um nome local (com ranhura no bastidor)."""
        if name is None:
            return False
        if is_int_literal(name) or is_string_literal(name):
            return False
        if name in self.func_names or name in INPUT_FUNCTIONS or name in OUTPUT_FUNCTIONS:
            return False
        # Global não-sombreado: pertence ao .data, não ao bastidor.
        if (name in self.global_scalars or name in self.global_arrays) \
                and name not in frame.locals_declared:
            return False
        return True

    # =====================================================
    # Emissão de instruções TAC -> MIPS
    # =====================================================

    def _emit_instruction(self, instr: TACInstruction) -> None:
        op = instr.op
        handler = self._HANDLERS.get(op)
        if handler is None:
            raise MIPSGenerationError(
                f"instrução TAC '{op}' inesperada no gerador MIPS "
                f"(TAC malformado ou operação não prevista por este back-end)"
            )
        handler(self, instr)

    # ---- aritmética / atribuição ----

    def _h_assign(self, instr: TACInstruction) -> None:
        self._load(instr.arg1, "$t0")
        self._store("$t0", instr.result)

    def _h_binary(self, instr: TACInstruction) -> None:
        self._comment(str(instr))
        op = instr.op
        # Aritmética real: '+ - * /' quando algum dos envolvidos é real.
        if op in ("+", "-", "*", "/") and (
            self._is_real(instr.result)
            or self._is_real(instr.arg1)
            or self._is_real(instr.arg2)
        ):
            self._binary_real_arith(instr)
            return
        # Comparação real: relacional com algum operando real.
        if op in ("<", "<=", ">", ">=", "==", "!=") and (
            self._is_real(instr.arg1) or self._is_real(instr.arg2)
        ):
            self._binary_real_rel(instr)
            return

        self._load(instr.arg1, "$t0")
        self._load(instr.arg2, "$t1")
        if op == "+":
            self._ins("addu $t2, $t0, $t1")
        elif op == "-":
            self._ins("subu $t2, $t0, $t1")
        elif op == "*":
            self._ins("mul $t2, $t0, $t1")
        elif op == "/":
            self._ins("div $t0, $t1")
            self._ins("mflo $t2")
        elif op == "%":
            self._ins("div $t0, $t1")
            self._ins("mfhi $t2")
        elif op == "<":
            self._ins("slt $t2, $t0, $t1")
        elif op == "<=":
            self._ins("sle $t2, $t0, $t1")
        elif op == ">":
            self._ins("sgt $t2, $t0, $t1")
        elif op == ">=":
            self._ins("sge $t2, $t0, $t1")
        elif op == "==":
            self._ins("seq $t2, $t0, $t1")
        elif op == "!=":
            self._ins("sne $t2, $t0, $t1")
        else:
            raise MIPSGenerationError(f"operador binário inesperado: {op}")
        self._store("$t2", instr.result)

    def _binary_real_arith(self, instr: TACInstruction) -> None:
        """'+ - * /' em vírgula flutuante de precisão simples."""
        self._load_float(instr.arg1, "$f0", "$t0")
        self._load_float(instr.arg2, "$f2", "$t1")
        fop = {"+": "add.s", "-": "sub.s", "*": "mul.s", "/": "div.s"}[instr.op]
        self._ins(f"{fop} $f4, $f0, $f2")
        self._store_float("$f4", instr.result, "$t0")

    def _binary_real_rel(self, instr: TACInstruction) -> None:
        """Comparação relacional real -> inteiro lógico (0/1)."""
        self._load_float(instr.arg1, "$f0", "$t0")
        self._load_float(instr.arg2, "$f2", "$t1")
        op = instr.op
        # (compare, branch-que-deixa o resultado a 0). Operandos trocados nos
        # casos '>' e '>=' para reutilizar c.lt.s / c.le.s.
        compare, branch = {
            "<":  ("c.lt.s $f0, $f2", "bc1f"),
            "<=": ("c.le.s $f0, $f2", "bc1f"),
            ">":  ("c.lt.s $f2, $f0", "bc1f"),
            ">=": ("c.le.s $f2, $f0", "bc1f"),
            "==": ("c.eq.s $f0, $f2", "bc1f"),
            "!=": ("c.eq.s $f0, $f2", "bc1t"),
        }[op]
        end = self._new_helper_label("frel")
        self._ins("li $t2, 0")
        self._ins(compare)
        self._ins(f"{branch} {end}")
        self._ins("li $t2, 1")
        self.lines.append(f"{end}:")
        self._store("$t2", instr.result)

    def _h_uminus(self, instr: TACInstruction) -> None:
        self._comment(str(instr))
        self._load(instr.arg1, "$t0")
        if self._is_real(instr.result) or self._is_real(instr.arg1):
            # Simétrico real = inverter o bit de sinal (bit 31).
            self._ins("lui $t1, 0x8000")
            self._ins("xor $t2, $t0, $t1")
        else:
            self._ins("subu $t2, $zero, $t0")
        self._store("$t2", instr.result)

    # ---- controlo de fluxo ----

    def _h_label(self, instr: TACInstruction) -> None:
        self.lines.append(f"{instr.label}:")

    def _h_goto(self, instr: TACInstruction) -> None:
        self._ins(f"j {instr.label}")

    def _h_if(self, instr: TACInstruction) -> None:
        self._load(instr.arg1, "$t0")
        self._ins(f"bne $t0, $zero, {instr.label}")

    def _h_iffalse(self, instr: TACInstruction) -> None:
        self._load(instr.arg1, "$t0")
        self._ins(f"beq $t0, $zero, {instr.label}")

    # ---- funções / chamadas ----

    def _h_getparam(self, instr: TACInstruction) -> None:
        index = int(instr.arg1)
        self._ins(f"lw $t2, {4 * index}($fp)")
        self._store("$t2", instr.result)

    def _h_param(self, instr: TACInstruction) -> None:
        self.pending_params.append(instr.arg1)

    def _h_call(self, instr: TACInstruction) -> None:
        target = instr.arg1
        # 'escrever' sem argumentos chega aqui como call; é um no-op de impressão.
        if target in OUTPUT_FUNCTIONS:
            self.pending_params = []
            return

        params = self.pending_params
        self.pending_params = []
        n = len(params)

        self._comment(str(instr))
        if n > 0:
            self._ins(f"addiu $sp, $sp, -{4 * n}")
            for i, p in enumerate(params):
                self._load_argument(p, "$t0")
                self._ins(f"sw $t0, {4 * i}($sp)")

        self._ins(f"jal f_{target}")

        if n > 0:
            self._ins(f"addiu $sp, $sp, {4 * n}")

        if instr.result is not None:
            self._store("$v0", instr.result)

    def _h_return(self, instr: TACInstruction) -> None:
        if instr.arg1 is not None:
            self._load(instr.arg1, "$v0")
        self._emit_epilogue()

    # ---- E/S ----

    def _h_read(self, instr: TACInstruction) -> None:
        self._comment(str(instr))
        self._ins("li $v0, 5")     # read_int
        self._ins("syscall")
        self._store("$v0", instr.result)

    def _h_readc(self, instr: TACInstruction) -> None:
        self._ins("li $v0, 12")    # read_char
        self._ins("syscall")
        self._store("$v0", instr.result)

    def _h_write(self, instr: TACInstruction) -> None:
        func = instr.arg1
        value = instr.arg2
        self._comment(str(instr))
        if func == "escrever":
            if self._is_real(value):
                self._load_float(value, "$f12", "$t0")
                self._ins("li $v0, 2")     # print_float
                self._ins("syscall")
            else:
                self._load(value, "$a0")
                self._ins("li $v0, 1")     # print_int
                self._ins("syscall")
            self._ins("li $a0, 10")    # '\n'
            self._ins("li $v0, 11")    # print_char
            self._ins("syscall")
        elif func == "escreverc":
            self._load(value, "$a0")
            self._ins("li $v0, 11")    # print_char
            self._ins("syscall")
        elif func == "escrevers":
            self._emit_escrevers(value)
        elif func == "escreverv":
            self._emit_escreverv(value)
        else:
            raise MIPSGenerationError(
                f"função de escrita '{func}' não reconhecida pelo gerador MIPS"
            )

    def _emit_escrevers(self, value: str) -> None:
        """escrevers: cadeia literal (.asciiz) ou inteiro[] terminado em 0."""
        if is_string_literal(value):
            label = self.string_pool.get(value)
            if label is None:
                raise MIPSGenerationError(
                    f"'escrevers' requer uma cadeia literal conhecida; "
                    f"recebeu '{value}'"
                )
            self._ins(f"la $a0, {label}")
            self._ins("li $v0, 4")     # print_string
            self._ins("syscall")
            return

        # Cadeia em runtime (ex.: resultado de lers): inteiro[] terminado em 0.
        # Imprime caráter a caráter até encontrar o terminador.
        self._array_base(value, "$t3")
        loop = self._new_helper_label("puts")
        end = self._new_helper_label("putsend")
        self.lines.append(f"{loop}:")
        self._ins("lw $a0, 0($t3)")
        self._ins(f"beq $a0, $zero, {end}")
        self._ins("li $v0, 11")        # print_char
        self._ins("syscall")
        self._ins("addiu $t3, $t3, 4")
        self._ins(f"j {loop}")
        self.lines.append(f"{end}:")

    def _emit_escreverv(self, value: str) -> None:
        """escreverv: imprime cada elemento (dimensão tem de ser estática)."""
        if self.frame is not None and self.frame.is_local_array(value):
            size = self.frame.slots[value][2]
        elif value in self.global_arrays:
            size = self.global_arrays[value]
        else:
            raise MIPSGenerationError(
                f"'escreverv' requer um vetor de dimensão conhecida em compilação; "
                f"'{value}' não a tem (vetor-parâmetro ou de dimensão dinâmica)"
            )

        is_real_elem = value in self.real_arrays
        self._array_base(value, "$t3")
        self._ins(f"li $t5, {size}")       # nº de elementos por imprimir
        loop = self._new_helper_label("pv")
        end = self._new_helper_label("pvend")
        self.lines.append(f"{loop}:")
        self._ins(f"blez $t5, {end}")
        if is_real_elem:
            self._ins("lwc1 $f12, 0($t3)")
            self._ins("li $v0, 2")         # print_float
        else:
            self._ins("lw $a0, 0($t3)")
            self._ins("li $v0, 1")         # print_int
        self._ins("syscall")
        self._ins("li $a0, 10")            # '\n' após cada elemento
        self._ins("li $v0, 11")
        self._ins("syscall")
        self._ins("addiu $t3, $t3, 4")
        self._ins("addiu $t5, $t5, -1")
        self._ins(f"j {loop}")
        self.lines.append(f"{end}:")

    # ---- vetores ----

    def _h_array_zero_init(self, instr: TACInstruction) -> None:
        name = instr.result
        size = int(instr.arg1)
        self._comment(str(instr))
        self._array_base(name, "$t3")
        loop = self._new_helper_label("zinit")
        end = self._new_helper_label("zend")
        self._ins("li $t4, 0")              # i
        self._ins(f"li $t5, {size}")        # N
        self.lines.append(f"{loop}:")
        self._ins(f"bge $t4, $t5, {end}")
        self._ins("sll $t6, $t4, 2")
        self._ins("addu $t7, $t3, $t6")
        self._ins("sw $zero, 0($t7)")
        self._ins("addiu $t4, $t4, 1")
        self._ins(f"j {loop}")
        self.lines.append(f"{end}:")

    def _h_array_store(self, instr: TACInstruction) -> None:
        # result[arg1] = arg2
        self._comment(str(instr))
        self._array_base(instr.result, "$t3")
        self._load(instr.arg1, "$t4")          # índice
        self._ins("sll $t4, $t4, 2")
        self._ins("addu $t3, $t3, $t4")
        self._load(instr.arg2, "$t0")          # valor
        self._ins("sw $t0, 0($t3)")

    def _h_array_init(self, instr: TACInstruction) -> None:
        # Mesma forma que array_store (índice constante vindo do inicializador).
        self._h_array_store(instr)

    def _h_array_load(self, instr: TACInstruction) -> None:
        # result = arg1[arg2]
        self._comment(str(instr))
        self._array_base(instr.arg1, "$t3")
        self._load(instr.arg2, "$t4")          # índice
        self._ins("sll $t4, $t4, 2")
        self._ins("addu $t3, $t3, $t4")
        self._ins("lw $t2, 0($t3)")
        self._store("$t2", instr.result)

    # ---- sem efeito de código ----

    def _h_declare(self, instr: TACInstruction) -> None:
        pass  # ranhura já reservada na análise do bastidor

    def _h_array_decl(self, instr: TACInstruction) -> None:
        pass  # espaço já reservado na análise do bastidor

    def _h_nop(self, instr: TACInstruction) -> None:
        pass

    # ---- conversões numéricas e cast ----

    def _emit_int_to_real(self, src: str, dst: str) -> None:
        self._load(src, "$t0")
        self._ins("mtc1 $t0, $f0")
        self._ins("cvt.s.w $f0, $f0")   # inteiro -> real (precisão simples)
        self._ins("mfc1 $t0, $f0")
        self._store("$t0", dst)

    def _emit_real_to_int(self, src: str, dst: str) -> None:
        self._load(src, "$t0")
        self._ins("mtc1 $t0, $f0")
        self._ins("trunc.w.s $f0, $f0")  # real -> inteiro truncando para zero
        self._ins("mfc1 $t0, $f0")
        self._store("$t0", dst)

    def _h_int_to_real(self, instr: TACInstruction) -> None:
        self._comment(str(instr))
        self._emit_int_to_real(instr.arg1, instr.result)

    def _h_real_to_int(self, instr: TACInstruction) -> None:
        self._comment(str(instr))
        self._emit_real_to_int(instr.arg1, instr.result)

    def _h_cast(self, instr: TACInstruction) -> None:
        # result = (arg2) arg1   ; arg2 in {"inteiro","real"}
        self._comment(str(instr))
        target = instr.arg2
        source_real = self._is_real(instr.arg1)
        if target == "real":
            if source_real:
                self._load(instr.arg1, "$t0")      # já é real: copia os bits
                self._store("$t0", instr.result)
            else:
                self._emit_int_to_real(instr.arg1, instr.result)
        elif target == "inteiro":
            if source_real:
                self._emit_real_to_int(instr.arg1, instr.result)
            else:
                self._load(instr.arg1, "$t0")      # já é inteiro: copia os bits
                self._store("$t0", instr.result)
        else:
            raise MIPSGenerationError(f"cast para tipo não suportado: '{target}'")

    # ---- leitura de cadeia (lers) ----

    def _h_reads(self, instr: TACInstruction) -> None:
        # lers(): lê uma linha e devolve um inteiro[] (terminado em 0) em memória
        # dinâmica. A rotina de runtime __lers faz o trabalho e devolve a base.
        self._comment(str(instr))
        self._lers_helper_needed = True
        self._ins("jal __lers")
        self._store("$v0", instr.result)

    _HANDLERS = {
        "assign": _h_assign,
        "+": _h_binary, "-": _h_binary, "*": _h_binary, "/": _h_binary, "%": _h_binary,
        "<": _h_binary, "<=": _h_binary, ">": _h_binary, ">=": _h_binary,
        "==": _h_binary, "!=": _h_binary,
        "uminus": _h_uminus,
        "label": _h_label, "goto": _h_goto, "if": _h_if, "ifFalse": _h_iffalse,
        "getparam": _h_getparam, "param": _h_param, "call": _h_call, "return": _h_return,
        "read": _h_read, "readc": _h_readc, "write": _h_write,
        "array_zero_init": _h_array_zero_init,
        "array_store": _h_array_store, "array_init": _h_array_init,
        "array_load": _h_array_load,
        "declare": _h_declare, "array_decl": _h_array_decl, "nop": _h_nop,
        # Reais, cast e leitura de cadeia:
        "cast": _h_cast, "int_to_real": _h_int_to_real, "real_to_int": _h_real_to_int,
        "reads": _h_reads,
    }

    # =====================================================
    # Auxiliares de baixo nível
    # =====================================================

    def _real_bits(self, text: str) -> int:
        """Padrão IEEE-754 de precisão simples (32 bits, sem sinal) de um real."""
        return struct.unpack("<I", struct.pack("<f", float(text)))[0]

    def _load(self, operand: str, reg: str) -> None:
        """Carrega o VALOR (32 bits) de um operando escalar para 'reg'."""
        if is_int_literal(operand):
            self._ins(f"li {reg}, {operand}")
            return
        if is_real_literal(operand):
            # Literal real -> carrega o seu padrão de bits (circula como inteiro).
            self._ins(f"li {reg}, 0x{self._real_bits(operand):08X}    # {operand}")
            return
        if self.frame is not None and self.frame.has(operand) and not self.frame.is_local_array(operand):
            off = self.frame.fp_offset(operand)
            self._ins(f"lw {reg}, {off}($fp)")
            return
        if self.frame is not None and self.frame.is_local_array(operand):
            # Valor de um nome de vetor = endereço base.
            off = self.frame.fp_offset(operand)
            self._ins(f"addiu {reg}, $fp, {off}")
            return
        if operand in self.global_scalars:
            self._ins(f"lw {reg}, g_{operand}")
            return
        if operand in self.global_arrays:
            self._ins(f"la {reg}, g_{operand}")
            return
        raise MIPSGenerationError(f"não sei carregar o operando '{operand}'")

    def _load_argument(self, operand: str, reg: str) -> None:
        """
        Carrega um argumento de chamada. Vetores passam-se POR REFERÊNCIA: para
        um vetor local empurra-se o ENDEREÇO base; para tudo o resto, o valor
        (um parâmetro-vetor já guarda o endereço, logo basta o valor).
        """
        if self.frame is not None and self.frame.is_local_array(operand):
            off = self.frame.fp_offset(operand)
            self._ins(f"addiu {reg}, $fp, {off}")
            return
        if operand in self.global_arrays:
            self._ins(f"la {reg}, g_{operand}")
            return
        self._load(operand, reg)

    def _store(self, reg: str, name: str) -> None:
        """Guarda o conteúdo de 'reg' no escalar 'name' (local ou global)."""
        if self.frame is not None and self.frame.has(name) and not self.frame.is_local_array(name):
            off = self.frame.fp_offset(name)
            self._ins(f"sw {reg}, {off}($fp)")
            return
        if name in self.global_scalars:
            self._ins(f"sw {reg}, g_{name}")
            return
        raise MIPSGenerationError(f"não sei guardar em '{name}'")

    def _array_base(self, name: str, reg: str) -> None:
        """Coloca em 'reg' o endereço base do vetor 'name'."""
        if self.frame is not None and self.frame.is_local_array(name):
            off = self.frame.fp_offset(name)
            self._ins(f"addiu {reg}, $fp, {off}")
            return
        if name in self.global_arrays:
            self._ins(f"la {reg}, g_{name}")
            return
        # Caso contrário é um parâmetro-vetor: a ranhura guarda o endereço base.
        if self.frame is not None and self.frame.has(name):
            off = self.frame.fp_offset(name)
            self._ins(f"lw {reg}, {off}($fp)")
            return
        # Vetor global de dimensão dinâmica: a ranhura escalar guarda o ponteiro.
        if name in self.global_scalars:
            self._ins(f"lw {reg}, g_{name}")
            return
        raise MIPSGenerationError(f"não consigo determinar a base do vetor '{name}'")

    def _load_float(self, operand: str, freg: str, gpr: str) -> None:
        """
        Carrega 'operand' no registo de vírgula flutuante 'freg'.
        Reaproveita _load (toda a lógica de endereçamento) para trazer os 32 bits
        a um GPR e depois move-os para o coprocessador 1. Se o operando for
        inteiro (caso de comparação mista real/inteiro), promove-o com cvt.s.w.
        """
        self._load(operand, gpr)
        self._ins(f"mtc1 {gpr}, {freg}")
        if not self._is_real(operand):
            self._ins(f"cvt.s.w {freg}, {freg}")

    def _store_float(self, freg: str, name: str, gpr: str) -> None:
        """Guarda o real em 'freg' (como 32 bits) no escalar 'name'."""
        self._ins(f"mfc1 {gpr}, {freg}")
        self._store(gpr, name)

    def _emit_lers_helper(self) -> None:
        """
        Rotina de runtime para lers(): lê uma linha do stdin e devolve um
        inteiro[] (uma palavra por caráter) terminado em 0, em memória dinâmica.

        Lê a linha inteira com read_string (syscall 8, estilo fgets) para um
        buffer de bytes e depois expande cada byte para uma palavra. (Lê-se a
        linha de uma vez porque o read_char do MARS consome a linha toda
        internamente e nunca devolve o '\\n'.) Base devolvida em $v0. É uma folha:
        só usa $v0/$a0/$t*, que neste back-end nunca guardam valores vivos entre
        instruções TAC.
        """
        self.lines.append("# ---- runtime: lers (lê uma linha como inteiro[] terminado em 0) ----")
        self.lines.append("__lers:")
        # 1) ler a linha para o buffer de bytes.
        self._ins("la $a0, __lers_buf")
        self._ins("li $a1, 1024")
        self._ins("li $v0, 8")               # read_string (estilo fgets)
        self._ins("syscall")
        # 2) alocar o inteiro[] no heap (256 palavras) e preparar cursores.
        self._ins("li $v0, 9")               # sbrk
        self._ins("li $a0, 1024")
        self._ins("syscall")
        self._ins("move $t0, $v0")           # base do inteiro[]
        self._ins("move $t1, $v0")           # cursor de escrita (palavras)
        self._ins("la $t2, __lers_buf")      # cursor de leitura (bytes)
        self.lines.append("__lers_loop:")
        self._ins("lb $t4, 0($t2)")          # próximo byte
        self._ins("beq $t4, $zero, __lers_done")   # fim da cadeia ('\\0')
        self._ins("li $t5, 10")
        self._ins("beq $t4, $t5, __lers_done")     # fim de linha '\\n' (não copiar)
        self._ins("sw $t4, 0($t1)")          # guardar o caráter como palavra
        self._ins("addiu $t1, $t1, 4")
        self._ins("addiu $t2, $t2, 1")
        self._ins("j __lers_loop")
        self.lines.append("__lers_done:")
        self._ins("sw $zero, 0($t1)")        # terminador 0
        self._ins("move $v0, $t0")           # devolve a base
        self._ins("jr $ra")
        self.lines.append("")

    def _new_helper_label(self, prefix: str) -> str:
        self._helper_label_counter += 1
        return f"_{prefix}{self._helper_label_counter}"

    def _ins(self, text: str) -> None:
        self.lines.append(f"    {text}")

    def _comment(self, text: str) -> None:
        self.lines.append(f"    # {text}")


# =========================================================
# API de conveniência
# =========================================================

def generate_mips(program: TACProgram) -> str:
    """Gera código MIPS (texto) a partir de um TACProgram."""
    return MIPSGenerator().generate(program)


# =========================================================
# Execução autónoma:  python codegen_mips.py entrada.mocp [saida.asm]
# Reaproveita o front-end existente (léxico->sintático->AST->semântica->TAC->otimização).
# =========================================================

def _compile_to_optimized_tac(input_path: str) -> TACProgram:
    from antlr4 import FileStream, CommonTokenStream
    from MOCPLexer import MOCPLexer
    from MOCPParser import MOCPParser
    from ast_builder import ASTBuilderVisitor
    from semantic import SemanticAnalyzer
    from tac_generator import TACGenerator
    from optimizer import TACOptimizer

    stream = FileStream(input_path, encoding="utf-8")
    lexer = MOCPLexer(stream)
    tokens = CommonTokenStream(lexer)
    parser = MOCPParser(tokens)
    tree = parser.program()

    ast = ASTBuilderVisitor().visit(tree)
    SemanticAnalyzer().analyze(ast)
    tac = TACGenerator().generate(ast)
    return TACOptimizer().optimize(tac)


def main(argv: List[str]) -> int:
    import sys
    try:
        sys.stdout.reconfigure(encoding="utf-8", errors="replace")
    except Exception:
        pass

    if len(argv) < 2 or len(argv) > 3:
        print("Uso: python codegen_mips.py <entrada.mocp> [saida.asm]")
        return 1

    input_path = argv[1]
    output_path = argv[2] if len(argv) == 3 else None

    try:
        tac = _compile_to_optimized_tac(input_path)
        asm = generate_mips(tac)
    except MIPSGenerationError as e:
        print(f"[MIPS] {e}")
        return 1

    if output_path:
        from pathlib import Path
        Path(output_path).write_text(asm, encoding="utf-8")
        print(f"Código MIPS escrito em: {output_path}")
    else:
        print(asm)

    return 0


if __name__ == "__main__":
    import sys
    sys.exit(main(sys.argv))
