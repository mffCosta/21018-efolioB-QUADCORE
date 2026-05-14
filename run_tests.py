"""
run_tests.py — Execução automática dos testes MOCP.
UC 21018 — Compilação, Universidade Aberta, 2025/2026
Grupo: QUADCORE
"""

import subprocess
from pathlib import Path


TEST_FILES = [
    "teste_global.mocp",
    "teste_erros_lexicos.mocp",
    "teste_erros_semanticos.mocp",
]


def run_test(test_file: str) -> None:
    path = Path(test_file)

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
        encoding="utf-8"
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

    for test_file in TEST_FILES:
        run_test(test_file)

    print("=" * 70)
    print("Execução dos testes concluída.")
    print("=" * 70)


if __name__ == "__main__":
    main()