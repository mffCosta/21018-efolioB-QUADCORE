"""
error_handler.py — Tratamento de erros léxicos e sintáticos para MOCP.
UC 21018 — Compilação, Universidade Aberta, 2025/2026
Autores: Maria Costa (2304361) | João Rodrigues (2203474) | Nuno Rolo ([Nº A PREENCHER]) | Fábio Oliveira ([Nº A PREENCHER])
Grupo: QUADCORE

Implementa verificação de palavras-chave C proibidas e operadores não suportados.
Produz mensagens de erro claras em português.
"""

from MOCPLexer import MOCPLexer

# Tokens de palavras-chave C proibidas
C_KEYWORDS_TOKENS = {
    MOCPLexer.C_INT, MOCPLexer.C_DOUBLE, MOCPLexer.C_VOID,
    MOCPLexer.C_MAIN, MOCPLexer.C_IF, MOCPLexer.C_ELSE,
    MOCPLexer.C_WHILE, MOCPLexer.C_FOR, MOCPLexer.C_RETURN,
    MOCPLexer.C_READ, MOCPLexer.C_READC, MOCPLexer.C_READS,
    MOCPLexer.C_WRITE, MOCPLexer.C_WRITEC, MOCPLexer.C_WRITEV,
    MOCPLexer.C_WRITES, MOCPLexer.C_STRUCT, MOCPLexer.C_INCLUDE,
    MOCPLexer.C_DEFINE,
}

C_KEYWORDS_MAP = {
    'int': 'inteiro',
    'double': 'real',
    'void': 'vazio',
    'main': 'principal',
    'if': 'se',
    'else': 'senao',
    'while': 'enquanto',
    'for': 'para',
    'return': 'retornar',
    'read': 'ler',
    'readc': 'lerc',
    'reads': 'lers',
    'write': 'escrever',
    'writec': 'escreverc',
    'writev': 'escreverv',
    'writes': 'escrevers',
    'struct': '(não existe em MOCP)',
    '#include': '(não existe em MOCP)',
    '#define': '(não existe em MOCP)',
}

FORBIDDEN_OPS = {
    MOCPLexer.OP_PLUSPLUS, MOCPLexer.OP_MINUSMINUS,
    MOCPLexer.OP_PLUSEQ, MOCPLexer.OP_MINUSEQ,
    MOCPLexer.OP_MULEQ, MOCPLexer.OP_DIVEQ,
}

FORBIDDEN_OPS_MAP = {
    '++': 'Use i = i + 1',
    '--': 'Use i = i - 1',
    '+=': 'Use x = x + valor',
    '-=': 'Use x = x - valor',
    '*=': 'Use x = x * valor',
    '/=': 'Use x = x / valor',
}


def verificar_tokens_proibidos(token_stream):
    """
    Verifica se existem tokens de palavras-chave C ou operadores proibidos.
    Retorna uma lista de strings de erro (formato compatível com CompilationError).
    """
    erros = []
    token_stream.fill()
    
    for token in token_stream.tokens:
        if token.type in C_KEYWORDS_TOKENS:
            text = token.text
            sugestao = C_KEYWORDS_MAP.get(text, '?')
            erros.append(
                f"[LÉXICO/SINTÁTICO] linha {token.line}, coluna {token.column}: "
                f"Palavra-chave C '{text}' detetada. Em MOCP use '{sugestao}'."
            )
        elif token.type in FORBIDDEN_OPS:
            sugestao = FORBIDDEN_OPS_MAP.get(token.text, 'Use expressões explícitas')
            erros.append(
                f"[LÉXICO/SINTÁTICO] linha {token.line}, coluna {token.column}: "
                f"Operador '{token.text}' não é suportado em MOCP. {sugestao}."
            )
        elif token.type == MOCPLexer.UNCLOSED_STRING:
            erros.append(
                f"[LÉXICO] linha {token.line}, coluna {token.column}: "
                "string não terminada."
            )

        elif token.type == MOCPLexer.ERROR_CHAR:
            erros.append(
                f"[LÉXICO] linha {token.line}, coluna {token.column}: "
                f"carácter inesperado '{token.text}'."
            )
    return erros
