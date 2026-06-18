"""
run_tests.py — Execução automática dos testes MOCP.
UC 21018 — Compilação, Universidade Aberta, 2025/2026
Grupo: QUADCORE
Autores: Maria Costa (2304361) | João Rodrigues (2203474) | Nuno Rolo (1900405) | Fábio Oliveira (1800960)
"""

import os
import subprocess
import sys
from pathlib import Path
from typing import Optional


TESTS_DIR = Path("Testes")
EXPECTED_DIR = TESTS_DIR / "expected"


def normalize_output(text: str) -> str:
    """Normaliza texto para comparação:
    - normaliza finais de linha;
    - substitui temporários `t<number>` por `t#` e labels `L<number>` por `L#`;
    - colapsa espaços finais e linhas vazias à direita.
    """
    import re
    import unicodedata

    if text is None:
        return ""

    s = text.replace("\r\n", "\n")

    # remover diacríticos e normalizar unicode (faz comparações estáveis)
    s = unicodedata.normalize("NFKD", s)
    s = s.encode("ascii", "ignore").decode("ascii")
    s = s.lower()

    # substituir temporários e labels por tokens genéricos
    s = re.sub(r"\bt\d+\b", "t#", s)
    s = re.sub(r"\bL\d+\b", "L#", s)

    # normalizar espaços e remover espaços finais em cada linha
    s = "\n".join(line.rstrip() for line in s.split("\n"))

    # remover espaços em excesso (opcional) and strip overall
    s = re.sub(r"[ \t]+", " ", s).strip()

    return s


def read_expected_file(path: Path) -> Optional[str]:
    if not path.exists():
        return None
    # Tenta varias codificações para tolerância a BOMs e encodings do Windows
    for enc in ("utf-8", "utf-8-sig", "cp1252", "latin-1"):
        try:
            return path.read_text(encoding=enc, errors="replace")
        except Exception:
            continue
    return path.read_text(encoding="utf-8", errors="replace")


def run_test(path: Path) -> None:
    test_file = path.name
    stem = path.stem
    expected_stdout_path = EXPECTED_DIR / f"{stem}.stdout.txt"
    expected_exitcode_path = EXPECTED_DIR / f"{stem}.exitcode.txt"

    print("=" * 70)
    print(f"TESTE: {test_file}")
    print("=" * 70)

    if not path.exists():
        print(f"ERRO: ficheiro '{test_file}' não encontrado.")
        print()
        return

    result = subprocess.run(
        [sys.executable, "main.py", str(path)],
        capture_output=True,
        text=True,
        encoding="utf-8",
        errors="replace",
        env={**os.environ, "PYTHONIOENCODING": "utf-8"},
    )

    print(result.stdout)

    if result.stderr:
        print("STDERR:")
        print(result.stderr)

    print(f"Código de saída: {result.returncode}")

    expected_stdout = read_expected_file(expected_stdout_path)
    expected_exitcode = read_expected_file(expected_exitcode_path)

    if expected_stdout is None and expected_exitcode is None:
        print("Sem saída esperada associada; teste executado apenas como referência.")
        print()
        return

    stdout_ok = True
    exitcode_ok = True

    if expected_stdout is not None:
        stdout_ok = normalize_output(result.stdout) == normalize_output(expected_stdout)

    if expected_exitcode is not None:
        try:
            exitcode_ok = result.returncode == int(expected_exitcode.strip())
        except ValueError:
            exitcode_ok = False

    if stdout_ok and exitcode_ok:
        print("Comparação com saída esperada: OK")
    else:
        print("Comparação com saída esperada: FALHOU")
        if expected_stdout is not None and not stdout_ok:
            print(f"- stdout difere de {expected_stdout_path}")
        if expected_exitcode is not None and not exitcode_ok:
            print(f"- código de saída difere de {expected_exitcode_path}")
    print()


def normalize_asm(text: str) -> str:
    """Normaliza assembly MIPS para comparação estrutural:
    - normaliza finais de linha e espaços;
    - substitui labels geradas (L0, L1, ...) por L#;
    - substitui temporários de registos ($t0..$t9) por $t#;
    - remove comentários de linha (# ...).
    """
    import re

    if text is None:
        return ""

    s = text.replace("\r\n", "\n")
    # remover comentários inline
    s = re.sub(r"#[^\n]*", "", s)
    # normalizar labels geradas (L seguido de dígitos)
    s = re.sub(r"\bL\d+\b", "L#", s)
    # normalizar registos temporários $t0..$t9
    s = re.sub(r"\$t\d\b", "$t#", s)
    # normalizar espaços finais e linhas vazias
    lines = [line.rstrip() for line in s.split("\n") if line.strip()]
    return "\n".join(lines).strip()


def run_mips_test(mocp_path: Path) -> bool:
    """Corre codegen_mips.py sobre 'mocp_path' e compara com o .asm de referência
    (se existir). Devolve True se passou, False se falhou."""
    stem = mocp_path.stem
    ref_asm_path = TESTS_DIR / f"{stem}.asm"

    print("-" * 70)
    print(f"MIPS: {mocp_path.name}")

    result = subprocess.run(
        [sys.executable, "codegen_mips.py", str(mocp_path)],
        capture_output=True,
        text=True,
        encoding="utf-8",
        errors="replace",
        env={**os.environ, "PYTHONIOENCODING": "utf-8"},
    )

    if result.returncode != 0:
        print(f"  FALHOU — codegen_mips.py terminou com erro (código {result.returncode})")
        if result.stderr:
            print("  STDERR:", result.stderr.strip())
        return False

    if not ref_asm_path.exists():
        print("  OK (sem .asm de referência; apenas verificado que não produz erros)")
        return True

    ref_text = ref_asm_path.read_text(encoding="utf-8", errors="replace")
    got_norm = normalize_asm(result.stdout)
    ref_norm = normalize_asm(ref_text)

    if got_norm == ref_norm:
        print("  OK — assembly coincide com referência")
        return True
    else:
        print("  DIFERENTE — assembly gerado difere de referência (estrutura)")
        # mostrar primeiras linhas divergentes para diagnóstico
        got_lines = got_norm.splitlines()
        ref_lines = ref_norm.splitlines()
        for i, (g, r) in enumerate(zip(got_lines, ref_lines)):
            if g != r:
                print(f"    primeira diferença na linha {i + 1}:")
                print(f"    esperado : {r}")
                print(f"    obtido   : {g}")
                break
        return False


def main() -> None:
    print("Execução automática dos testes MOCP")
    print()

    if not TESTS_DIR.exists():
        print(f"ERRO: pasta '{TESTS_DIR}' não encontrada.")
        return

    EXPECTED_DIR.mkdir(parents=True, exist_ok=True)

    test_files = sorted(TESTS_DIR.glob("*.mocp"))

    if not test_files:
        print(f"ERRO: não foram encontrados ficheiros .mocp em '{TESTS_DIR}'.")
        return

    # ── Fase 1: testes do pipeline principal (main.py) ──────────────────────
    for test_file in test_files:
        run_test(test_file)

    # ── Fase 2: testes de geração MIPS (codegen_mips.py) ────────────────────
    print()
    print("=" * 70)
    print("Testes de geração de código MIPS32")
    print("=" * 70)
    print()

    mips_passed = 0
    mips_failed = 0
    mips_skipped = 0

    for test_file in test_files:
        # Apenas programas sem erros devem gerar assembly com sucesso.
        # Salta ficheiros cujo exit code esperado seja != 0 (programas com erros).
        ec_path = EXPECTED_DIR / f"{test_file.stem}.exitcode.txt"
        if ec_path.exists():
            try:
                expected_ec = int(ec_path.read_text(encoding="utf-8").strip())
            except ValueError:
                expected_ec = 0
            if expected_ec != 0:
                mips_skipped += 1
                continue
        ok = run_mips_test(test_file)
        if ok:
            mips_passed += 1
        else:
            mips_failed += 1

    print()
    print(f"MIPS: {mips_passed} passou(ram) | {mips_failed} falhou(aram) | {mips_skipped} ignorado(s) (testes de erros)")
    print()
    print("=" * 70)
    print("Execução dos testes concluída.")
    print("=" * 70)


if __name__ == "__main__":
    main()