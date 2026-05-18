"""
run_tests.py — Execução automática dos testes MOCP.
UC 21018 — Compilação, Universidade Aberta, 2025/2026
Grupo: QUADCORE
Autores: Maria Costa (2304361) | João Rodrigues (2203474) | Nuno Rolo (1900405) | Fábio Oliveira (1800960)
"""

import os
import subprocess
from pathlib import Path


TESTS_DIR = Path("Testes")


def run_test(path: Path) -> None:
    test_file = path.name

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
    print()


def main() -> None:
    print("Execução automática dos testes MOCP")
    print()

    if not TESTS_DIR.exists():
        print(f"ERRO: pasta '{TESTS_DIR}' não encontrada.")
        return

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