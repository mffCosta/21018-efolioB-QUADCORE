"""
main.py — Programa principal do compilador MOCP.
UC 21018 — Compilação, Universidade Aberta, 2025/2026
Autores: João Rodrigues (2203474) | Maria Costa (2304361)
Grupo: DUALCORE

Pipeline de compilação:
  1. Leitura do ficheiro
  2. Análise léxica (com deteção de tokens C proibidos e erros léxicos controlados)
  3. Análise sintática
  4. Construção da AST
  5. Análise semântica
"""

import sys
import re
from pathlib import Path
from typing import List

from antlr4 import FileStream, CommonTokenStream
from antlr4.error.ErrorListener import ErrorListener

from MOCPLexer import MOCPLexer
from MOCPParser import MOCPParser

from ast_builder import ASTBuilderVisitor
from semantic import SemanticAnalyzer, SemanticError
from error_handler import verificar_tokens_proibidos


# =========================================================
# Estrutura de erro
# =========================================================

class CompilationError:
    """
    Representa um erro detetado durante a compilação.
    phase: LÉXICO | SINTÁTICO | SEMÂNTICO
    """

    def __init__(self, phase: str, line: int, column: int, message: str):
        self.phase = phase
        self.line = line
        self.column = column
        self.message = message

    def __str__(self) -> str:
        return f"[{self.phase}] linha {self.line}, coluna {self.column}: {self.message}"


# =========================================================
# Listener de erros
# =========================================================

class CollectingErrorListener(ErrorListener):
    """
    Recolhe erros do lexer/parser em vez de os deixar ir diretamente para stderr.
    """

    def __init__(self, phase: str, errors: List[CompilationError]):
        super().__init__()
        self.phase = phase
        self.errors = errors

    def syntaxError(self, recognizer, offendingSymbol, line, column, msg, e):
        self.errors.append(CompilationError(self.phase, line, column, msg))


# =========================================================
# Utilitários
# =========================================================

def print_usage() -> None:
    print("Uso:")
    print("  python main.py <ficheiro_entrada.mocp> [ficheiro_saida_ast.txt]")


def print_errors(errors: List[CompilationError]) -> None:
    print("Foram encontrados erros:")
    for err in errors:
        print(err)


def save_text_file(path: Path, text: str) -> None:
    path.write_text(text, encoding="utf-8")


# =========================================================
# Programa principal
# =========================================================

def main() -> int:
    # -----------------------------------------------------
    # 1. Validar argumentos
    # -----------------------------------------------------
    if len(sys.argv) < 2 or len(sys.argv) > 3:
        print_usage()
        return 1

    input_path = Path(sys.argv[1])

    if not input_path.exists():
        print(f"Erro: o ficheiro '{input_path}' não existe.")
        return 1

    if not input_path.is_file():
        print(f"Erro: '{input_path}' não é um ficheiro válido.")
        return 1

    output_ast_path = Path(sys.argv[2]) if len(sys.argv) == 3 else None

    # -----------------------------------------------------
    # 2. Ler ficheiro
    # -----------------------------------------------------
    try:
        input_stream = FileStream(str(input_path), encoding="utf-8")
    except Exception as e:
        print(f"Erro ao abrir o ficheiro '{input_path}': {e}")
        return 1

    # -----------------------------------------------------
    # 3. Preparar recolha de erros
    # -----------------------------------------------------
    errors: List[CompilationError] = []

    # -----------------------------------------------------
    # 4. Lexer
    # -----------------------------------------------------
    lexer = MOCPLexer(input_stream)
    lexer.removeErrorListeners()
    lexer.addErrorListener(CollectingErrorListener("LÉXICO", errors))

    token_stream = CommonTokenStream(lexer)

    # Detetar tokens C proibidos, operadores proibidos e erros léxicos controlados
    proibidos_errors = verificar_tokens_proibidos(token_stream)

    for err_msg in proibidos_errors:
        # Converter formato "erro" em CompilationError.
        # Formato esperado: "[FASE] linha X, coluna Y: mensagem"
        try:
            match = re.search(
                r'\[([^\]]+)\]\s+linha\s+(\d+),\s+coluna\s+(\d+):\s*(.*)',
                err_msg
            )
            if match:
                phase = match.group(1)
                line = int(match.group(2))
                column = int(match.group(3))
                message = match.group(4)
                errors.append(CompilationError(phase, line, column, message))
            else:
                errors.append(CompilationError(
                    "LÉXICO/SINTÁTICO",
                    0,
                    0,
                    err_msg
                ))
        except Exception:
            errors.append(CompilationError(
                "LÉXICO/SINTÁTICO",
                0,
                0,
                err_msg
            ))
            
    # If forbidden tokens found, report immediately
    if proibidos_errors:
        print_errors(errors)
        return 1

    # -----------------------------------------------------
    # 5. Parser
    # -----------------------------------------------------
    parser = MOCPParser(token_stream)
    parser.removeErrorListeners()
    parser.addErrorListener(CollectingErrorListener("SINTÁTICO", errors))

    # -----------------------------------------------------
    # 6. Parsing
    # -----------------------------------------------------
    try:
        tree = parser.program()
    except Exception as e:
        print(f"Erro interno durante a análise sintática: {e}")
        return 1

    # -----------------------------------------------------
    # 7. Se houver erros léxicos/sintáticos, reportar
    # -----------------------------------------------------
    if errors:
        print_errors(errors)
        return 1

    # -----------------------------------------------------
    # 8. Construção da AST
    # -----------------------------------------------------
    try:
        builder = ASTBuilderVisitor()
        ast = builder.visit(tree)
    except Exception as e:
        print(f"Erro ao construir a AST: {e}")
        return 1

    # -----------------------------------------------------
    # 9. Análise semântica
    # -----------------------------------------------------
    try:
        analyzer = SemanticAnalyzer()
        analyzer.analyze(ast)
    except SemanticError as e:
        print(f"[SEMÂNTICO] {e}")
        return 1
    except Exception as e:
        print(f"Erro interno durante a análise semântica: {e}")
        return 1

    # -----------------------------------------------------
    # 10. Imprimir AST
    # -----------------------------------------------------
    print("Análise concluída com sucesso.")
    print("AST gerada:")

    ast_text = ast.pretty() if hasattr(ast, "pretty") else str(ast)
    print(ast_text)

    # -----------------------------------------------------
    # 11. Guardar AST em ficheiro, se pedido
    # -----------------------------------------------------
    if output_ast_path is not None:
        try:
            save_text_file(output_ast_path, ast_text)
            print(f"AST guardada em: {output_ast_path}")
        except Exception as e:
            print(f"Erro ao guardar AST em ficheiro: {e}")
            return 1

    return 0


if __name__ == "__main__":
    sys.exit(main())
