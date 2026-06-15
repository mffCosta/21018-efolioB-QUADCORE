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
ESTADO DESTA ITERAÇÃO  (subconjunto INTEIRO completo)
------------------------------------------------------------------------------
Suportado e testado de ponta a ponta:
  - funções, convenção de chamadas e recursão  (func/endfunc, getparam, param,
    call, return)  -> bastidor de pilha com $fp;
  - escalares inteiros, aritmética (+ - * / %), simétrico, relacionais;
  - controlo de fluxo (label, goto, if, ifFalse);
  - vetores de inteiros: declaração local, inicialização a 0, leitura/escrita
    indexada e PASSAGEM POR REFERÊNCIA como parâmetro;
  - E/S inteira: escrever, escreverc, escrevers, ler, lerc.

Deixado explicitamente para as próximas iterações (levanta erro claro):
  - reais / vírgula flutuante (int_to_real, real_to_int, operações e E/S reais);
  - cast do utilizador;
  - escreverv (escrever vetor) e lers (ler string);
  - vetores de dimensão determinada em execução (array_decl com tamanho '?').

------------------------------------------------------------------------------
CONVENÇÃO DE E/S DEFINIDA POR NÓS (o enunciado não a fixa)
------------------------------------------------------------------------------
  escrever(n)   -> imprime o inteiro seguido de mudança de linha '\\n';
  escreverc(c)  -> imprime um único caráter (código ASCII), sem mudança de linha;
  escrevers(s)  -> imprime a cadeia tal e qual, sem mudança de linha.

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

from typing import Dict, List, Optional, Tuple

from tac import (
    TACProgram,
    TACInstruction,
    is_int_literal,
    is_string_literal,
)


class MIPSGenerationError(Exception):
    """Erro durante a geração de código MIPS (ex.: construção ainda não suportada)."""
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
        self.func_names: set = set()
        self.frame: Optional[_Frame] = None
        self.pending_params: List[str] = []
        self._helper_label_counter = 0

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
        for instr in pre_func:
            if instr.op == "declare":
                self.global_scalars.setdefault(instr.result, "0")
            elif instr.op == "assign" and instr.result in self.global_scalars:
                if is_int_literal(instr.arg1):
                    self.global_scalars[instr.result] = instr.arg1
            elif instr.op == "array_decl":
                if instr.arg1 == "?":
                    raise MIPSGenerationError(
                        "vetor global de dimensão determinada em execução ('?') "
                        "ainda não suportado no gerador MIPS"
                    )
                self.global_arrays[instr.result] = int(instr.arg1)

    def _collect_strings(self, instructions: List[TACInstruction]) -> None:
        for instr in instructions:
            for operand in (instr.arg1, instr.arg2):
                if is_string_literal(operand) and operand not in self.string_pool:
                    label = f"str_{len(self.string_pool)}"
                    self.string_pool[operand] = label

    # =====================================================
    # Segmento de dados
    # =====================================================

    def _emit_data_segment(self) -> None:
        self.lines.append("# " + "=" * 60)
        self.lines.append("# Segmento de dados")
        self.lines.append("# " + "=" * 60)
        self.lines.append(".data")

        for name, value in self.global_scalars.items():
            self.lines.append(f"g_{name}: .word {value}")

        for name, size in self.global_arrays.items():
            self.lines.append(f"g_{name}: .space {4 * size}")

        for literal, label in self.string_pool.items():
            # 'literal' já vem com aspas e escapes válidos do TAC.
            self.lines.append(f"{label}: .asciiz {literal}")

        # Cadeia auxiliar para a mudança de linha do 'escrever'.
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

        # Arranque: chama 'principal' e termina o programa (syscall 10).
        self.lines.append("main:")
        self.lines.append("    jal f_principal")
        self.lines.append("    li $v0, 10")
        self.lines.append("    syscall")
        self.lines.append("")

        for name, body in functions:
            self._emit_function(name, body)

    def _emit_function(self, name: str, body: List[TACInstruction]) -> None:
        self.frame = self._analyze_frame(body)
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
                    raise MIPSGenerationError(
                        f"vetor '{instr.result}' de dimensão determinada em execução "
                        "('?') ainda não suportado no gerador MIPS"
                    )
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
                f"instrução TAC '{op}' ainda não suportada pelo gerador MIPS "
                f"(esta iteração cobre o subconjunto inteiro)"
            )
        handler(self, instr)

    # ---- aritmética / atribuição ----

    def _h_assign(self, instr: TACInstruction) -> None:
        self._load(instr.arg1, "$t0")
        self._store("$t0", instr.result)

    def _h_binary(self, instr: TACInstruction) -> None:
        self._comment(str(instr))
        self._load(instr.arg1, "$t0")
        self._load(instr.arg2, "$t1")
        op = instr.op
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

    def _h_uminus(self, instr: TACInstruction) -> None:
        self._load(instr.arg1, "$t0")
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
            label = self.string_pool[value]
            self._ins(f"la $a0, {label}")
            self._ins("li $v0, 4")     # print_string
            self._ins("syscall")
        else:
            raise MIPSGenerationError(
                f"'{func}' ainda não suportado no gerador MIPS "
                "(escreverv fica para a próxima iteração)"
            )

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

    # ---- ainda não suportado (próxima iteração) ----

    def _h_not_yet(self, instr: TACInstruction) -> None:
        raise MIPSGenerationError(
            f"instrução TAC '{instr.op}' (suporte a reais/cast) fica para a "
            "próxima iteração do gerador MIPS"
        )

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
        # Reservado para a próxima iteração:
        "cast": _h_not_yet, "int_to_real": _h_not_yet, "real_to_int": _h_not_yet,
        "reads": _h_not_yet,
    }

    # =====================================================
    # Auxiliares de baixo nível
    # =====================================================

    def _load(self, operand: str, reg: str) -> None:
        """Carrega o VALOR de um operando escalar para 'reg'."""
        if is_int_literal(operand):
            self._ins(f"li {reg}, {operand}")
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
        raise MIPSGenerationError(f"não consigo determinar a base do vetor '{name}'")

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
