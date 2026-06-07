"""
run_tests.py — Execução automática dos testes MOCP.
UC 21018 — Compilação, Universidade Aberta, 2025/2026
Grupo: QUADCORE
Autores: Maria Costa (2304361) | João Rodrigues (2203474) | Nuno Rolo (1900405) | Fábio Oliveira (1800960)
"""

import os
import subprocess
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
        ["python", "main.py", str(path)],
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

    for test_file in test_files:
        run_test(test_file)

    print("=" * 70)
    print("Execução dos testes concluída.")
    print("=" * 70)


if __name__ == "__main__":
    main()