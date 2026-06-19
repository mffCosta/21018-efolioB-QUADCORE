"""
run_codegen_tests.py — Testes ponta-a-ponta da GERAÇÃO DE CÓDIGO FINAL (MIPS).
UC 21018 — Compilação, Universidade Aberta, 2025/2026
Grupo: QUADCORE
Autores: Maria Costa (2304361) | João Rodrigues (2203474) | Nuno Rolo (1900405) | Fábio Oliveira (1800960)

------------------------------------------------------------------------------
OBJETIVO
------------------------------------------------------------------------------
Verificar que o código MIPS gerado por `codegen_mips.py` está CORRETO, ou seja,
que ao ser realmente executado produz o resultado esperado.

Diferença para `run_tests.py`:
  - `run_tests.py`  compara a *estrutura textual* do .asm com um .asm de
    referência (deteta regressões no gerador, mas não prova que o código corre);
  - `run_codegen_tests.py` (este)  GERA o assembly a partir do .mocp, EXECUTA-o
    no simulador MARS (Mars4_5.jar) com uma entrada definida e compara a SAÍDA
    do programa com a saída esperada — a prova de execução exigida pelo
    enunciado do E-fólio Global.

Para cada programa válido o ciclo é:
    .mocp  --(codegen_mips.py)-->  .asm  --(MARS)-->  saída  ==?  esperado

------------------------------------------------------------------------------
EXECUÇÃO
------------------------------------------------------------------------------
    python run_codegen_tests.py

Requisitos: Java (para o MARS) e o ficheiro Mars4_5.jar na raiz do projeto.
Se o Java/MARS não estiverem disponíveis, os testes são ignorados com aviso
(o script termina com código 0 para não quebrar ambientes sem Java).
"""

import shutil
import subprocess
import sys
import tempfile
from dataclasses import dataclass, field
from pathlib import Path
from typing import List

ROOT = Path(__file__).resolve().parent
TESTS_DIR = ROOT / "Testes"
MARS_JAR = ROOT / "Mars4_5.jar"


@dataclass
class Caso:
    """Um caso de teste de execução: programa, entrada e saída esperada."""
    stem: str                       # nome do .mocp (sem extensão) em Testes/
    entrada: str                    # texto enviado para o stdin do programa
    esperado: str                   # saída lógica esperada do programa
    descricao: str = ""             # o que este caso demonstra
    nota: str = ""                  # justificação do valor esperado


# ──────────────────────────────────────────────────────────────────────────
# Casos de teste — saídas esperadas calculadas à mão a partir da semântica
# de cada programa MOCP (ver 'nota'). A entrada usa um inteiro por linha,
# porque o read_int do MARS (syscall 5) consome uma linha de cada vez.
# ──────────────────────────────────────────────────────────────────────────
CASOS: List[Caso] = [
    Caso(
        stem="spec_fatorial",
        entrada="5\n",
        esperado="Introduza inteiro: 120\n",
        descricao="recursão, se/senao, ler/escrever/escrevers",
        nota="fact(5) = 5*4*3*2*1 = 120; a cadeia é o prompt escrito antes da leitura.",
    ),
    Caso(
        stem="spec_media",
        entrada="4\n10\n20\n30\n40\n",
        esperado="Introduza tamanho e valores: 25.0\n",
        descricao="vetor real por referência, ciclo para, divisão real, retorno real",
        nota="média de [10,20,30,40] = 100/4 = 25.0 (impresso como real).",
    ),
    Caso(
        stem="exemplo_correto",
        entrada="5\n",
        esperado="10\n120\n120.0\n0\n2\n4\n6\n8\n10\n12\n14\n16\n18\n",
        descricao="escrever literal, recursão, cast inteiro->real, vetor + bubble sort",
        nota="escrever(10); fatorial(5)=120; (real)120=120.0; vetor i*2 já ordenado: 0..18.",
    ),
    Caso(
        stem="teste_ciclos_vetores",
        entrada="",
        esperado="20\n30\n40\n50\n80\n220\n220\n",
        descricao="ordenação por seleção, função com vetor por referência, ciclo para",
        nota="[50,30,80,20,40] ordenado = 20 30 40 50 80; soma=220; maximo(220,100)=220.",
    ),
    Caso(
        stem="teste_global",
        entrada="",
        esperado="120\n30\n120\n120.0\n50\n30\n80\n20\n40\n220\n220\n14\n14\n14\n0\n",
        descricao="várias funções, real, vetor, &&, e expressões para otimização TAC",
        nota=(
            "fatorial(5)=120; soma(10,20)=30; maximo(120,30)=120; (real)120=120.0; "
            "vetor 50 30 80 20 40; total=220; (220>100 && 120>10)->220; "
            "2+3*4=14; +0=14; *1=14; *0=0."
        ),
    ),
    Caso(
        stem="teste_cobertura",
        entrada="hello\nA\n",
        esperado="1\n2\n3\nA10\n20\n30\nhello",
        descricao="globais com init, lers/lerc, /, %, !, ||, &&, escreverc/v/s, retornar vazio",
        nota=(
            "m=1,n=2,soma=3 -> escrever 1,2,3; lerc()='A'(65) -> escreverc imprime 'A' "
            "(sem mudança de linha, por isso a linha fica 'A10'); escreverv({10,20,30}); "
            "lers()='hello' -> escrevers imprime 'hello'; retornar antecipado em g>0 "
            "(7>0) impede escrever(dobro(g))."
        ),
    ),
    Caso(
        stem="teste_globais",
        entrada="abc\n",
        esperado="10\n3\n6\n9\n42\nabc",
        descricao="init de globais: escalar/vetor literal (.data) e chamada/lers (__init)",
        nota=(
            "base=10; tabela={3,6,9} -> escreverv 3,6,9; dobrado=dobro(21)=42; "
            "linha=lers()='abc' -> escrevers 'abc'. Os dois ultimos sao inicializados "
            "no arranque sintetico __init, antes de principal."
        ),
    ),
]


def _normalizar(texto: str) -> str:
    """Saída lógica do programa: finais de linha uniformes e sem mudanças de
    linha finais. O MARS, no fim da execução, acrescenta sempre um '\\n' extra
    à saída — esse artefacto do simulador é removido aqui; as mudanças de linha
    internas (que separam os valores impressos) são preservadas e comparadas."""
    if texto is None:
        return ""
    return texto.replace("\r\n", "\n").rstrip("\n")


def _gerar_asm(mocp_path: Path, asm_path: Path) -> subprocess.CompletedProcess:
    """Gera o assembly MIPS a partir do .mocp (back-end sob teste)."""
    return subprocess.run(
        [sys.executable, "codegen_mips.py", str(mocp_path), str(asm_path)],
        cwd=ROOT,
        capture_output=True,
        text=True,
        encoding="utf-8",
        errors="replace",
    )


def _correr_mars(asm_path: Path, entrada: str) -> subprocess.CompletedProcess:
    """Executa o assembly no MARS (nc = sem cabeçalho; sm = arranca em 'main')."""
    return subprocess.run(
        ["java", "-jar", str(MARS_JAR), "nc", "sm", str(asm_path)],
        cwd=ROOT,
        input=entrada,
        capture_output=True,
        text=True,
        encoding="utf-8",
        errors="replace",
        timeout=60,
    )


def _mostrar_primeira_diferenca(esperado: str, obtido: str) -> None:
    esp = esperado.split("\n")
    obt = obtido.split("\n")
    for i in range(max(len(esp), len(obt))):
        e = esp[i] if i < len(esp) else "<sem linha>"
        o = obt[i] if i < len(obt) else "<sem linha>"
        if e != o:
            print(f"    primeira diferença na linha {i + 1}:")
            print(f"      esperado : {e!r}")
            print(f"      obtido   : {o!r}")
            return


def _correr_caso(caso: Caso, tmp_dir: Path) -> bool:
    mocp_path = TESTS_DIR / f"{caso.stem}.mocp"
    asm_path = tmp_dir / f"{caso.stem}.asm"

    print("-" * 70)
    print(f"CODEGEN+MARS: {caso.stem}.mocp")
    if caso.descricao:
        print(f"  ({caso.descricao})")

    if not mocp_path.exists():
        print(f"  FALHOU — ficheiro fonte não encontrado: {mocp_path}")
        return False

    # 1) gerar o assembly
    ger = _gerar_asm(mocp_path, asm_path)
    if ger.returncode != 0 or not asm_path.exists():
        print(f"  FALHOU — codegen_mips.py terminou com erro (código {ger.returncode})")
        if ger.stdout.strip():
            print("  STDOUT:", ger.stdout.strip())
        if ger.stderr.strip():
            print("  STDERR:", ger.stderr.strip())
        return False

    # 2) executar no MARS
    try:
        exe = _correr_mars(asm_path, caso.entrada)
    except subprocess.TimeoutExpired:
        print("  FALHOU — execução no MARS excedeu o tempo limite (possível ciclo infinito)")
        return False

    if exe.returncode != 0:
        print(f"  FALHOU — MARS terminou com erro (código {exe.returncode})")
        if exe.stderr.strip():
            print("  STDERR:", exe.stderr.strip())
        return False

    # 3) comparar a saída
    obtido = _normalizar(exe.stdout)
    esperado = _normalizar(caso.esperado)

    entrada_repr = caso.entrada.replace("\n", "\\n") or "<vazia>"
    if obtido == esperado:
        print(f"  OK — entrada {entrada_repr!r} -> saída correta")
        return True

    print(f"  FALHOU — saída diferente do esperado (entrada {entrada_repr!r})")
    print(f"    esperado : {esperado!r}")
    print(f"    obtido   : {obtido!r}")
    _mostrar_primeira_diferenca(esperado, obtido)
    return False


def main() -> int:
    print("=" * 70)
    print("Testes de execução do código MIPS gerado (codegen_mips.py + MARS)")
    print("=" * 70)
    print()

    if not TESTS_DIR.exists():
        print(f"ERRO: pasta de testes não encontrada: {TESTS_DIR}")
        return 1

    # Pré-requisitos: Java e o MARS. Sem eles, ignoramos (sem falhar o build).
    if shutil.which("java") is None:
        print("AVISO: 'java' não encontrado no PATH; testes de execução IGNORADOS.")
        print("       (Instale o Java para correr o MARS e validar a execução.)")
        return 0
    if not MARS_JAR.exists():
        print(f"AVISO: simulador não encontrado ({MARS_JAR.name}); testes IGNORADOS.")
        return 0

    passou = 0
    falhou = 0
    with tempfile.TemporaryDirectory(prefix="mocp_asm_") as tmp:
        tmp_dir = Path(tmp)
        for caso in CASOS:
            if _correr_caso(caso, tmp_dir):
                passou += 1
            else:
                falhou += 1
            print()

    print("=" * 70)
    print(f"RESULTADO: {passou} passou(ram) | {falhou} falhou(aram) "
          f"| {len(CASOS)} no total")
    print("=" * 70)
    return 0 if falhou == 0 else 1


if __name__ == "__main__":
    sys.exit(main())
