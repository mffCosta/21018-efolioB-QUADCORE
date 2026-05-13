===============================================================
E-FÓLIO A — COMPILAÇÃO (UC 21018)
Licenciatura em Engenharia Informática — Universidade Aberta
Ano letivo 2025/2026
Grupo DUALCORE
Estudantes:
- Maria Costa (2304361)
- João Rodrigues (2203474)
===============================================================

1. OBJETIVO
---------------------------------------------------------------
Este trabalho implementa, com recurso ao ANTLR4 e Python, um
processador para a linguagem MOCP (My Own C in Português).

A solução realiza:
- análise léxica;
- análise sintática;
- construção de uma árvore sintática abstrata (AST);
- apresentação de erros no ecrã;
- validação semântica básica adicional.

Nota:
A análise semântica incluída é uma extensão simples à solução base.
O foco principal do trabalho é a análise léxica e sintática da
linguagem MOCP e a construção da AST.

2. CONTEÚDO DO PROJETO
---------------------------------------------------------------
Ficheiros principais:
- MOCP.g4                  Gramática ANTLR da linguagem MOCP
- main.py                  Programa principal
- ast_nodes.py             Definição dos nós da AST
- ast_builder.py           Visitor para construir a AST
- error_handler.py         Deteção de palavras-chave C proibidas
- semantic.py              Validação semântica básica adicional

Ficheiros de teste:
- exemplo_correto.mocp
- exemplo_erros.mocp
- teste_ciclos_vetores.mocp
- teste_erros_variados.mocp

Ficheiros gerados pelo ANTLR (incluídos no projeto):
- MOCPLexer.py
- MOCPParser.py
- MOCPVisitor.py
- MOCPListener.py
- ficheiros auxiliares *.tokens e *.interp

3. REQUISITOS
---------------------------------------------------------------
Software necessário:
- Python 3.10 ou superior
- Java 11 ou superior
- ANTLR 4.13.2 (ou versão compatível)

Biblioteca Python necessária:
- antlr4-python3-runtime==4.13.2

Instalação do runtime:
    pip install antlr4-python3-runtime==4.13.2

4. GERAÇÃO DOS FICHEIROS DO ANTLR
---------------------------------------------------------------
Se os ficheiros MOCPLexer.py, MOCPParser.py, MOCPVisitor.py e
MOCPListener.py já estiverem incluídos, este passo não é obrigatório.

Para regenerar a partir da gramática, executar na pasta do projeto:

    java -jar antlr-4.13.2-complete.jar -Dlanguage=Python3 -visitor MOCP.g4

5. EXECUÇÃO
---------------------------------------------------------------
Para executar o compilador sobre um ficheiro MOCP:

    python main.py <ficheiro_entrada.mocp>

Exemplos:

    python main.py exemplo_correto.mocp
    python main.py exemplo_erros.mocp
    python main.py teste_ciclos_vetores.mocp
    python main.py teste_erros_variados.mocp

Também é possível guardar a AST num ficheiro:

    python main.py exemplo_correto.mocp ast_saida.txt

6. FUNCIONAMENTO
---------------------------------------------------------------
O programa segue as etapas seguintes:

1) Análise léxica
   - o lexer converte o texto de entrada em tokens;
   - comentários e espaços são ignorados;
   - símbolos inválidos são assinalados.

2) Deteção de tokens C proibidos
   - são identificadas palavras-chave da linguagem C original
     (por exemplo int, double, if, while, return, main);
   - são identificados operadores não suportados em MOCP
     (por exemplo ++, --, +=, -=, *=, /=).

3) Análise sintática
   - o parser verifica se a estrutura do programa respeita a
     gramática MOCP.

4) Construção da AST
   - a parse tree do ANTLR é convertida numa AST mais simples e
     abstrata.

5) Validação semântica básica adicional
   - deteção de variáveis não declaradas;
   - validação básica de chamadas de função;
   - verificação simples de vetores, retornos e tipos.

7. SAÍDA ESPERADA
---------------------------------------------------------------
Se o ficheiro estiver correto, a saída é do tipo:

    Análise concluída com sucesso.
    AST gerada:
    ProgramNode
      ...

Se o ficheiro contiver erros, a saída apresenta mensagens como:

    Foram encontrados erros:
    [LÉXICO] linha X, coluna Y: ...
    [SINTÁTICO] linha X, coluna Y: ...
    [LÉXICO/SINTÁTICO] linha X, coluna Y: ...

8. OBSERVAÇÕES
---------------------------------------------------------------
- A linguagem MOCP usa palavras-chave em português.
- O uso direto de palavras-chave da linguagem C é tratado como erro.
- As funções sem parâmetros devem ser escritas com (vazio).
- Todos os blocos de controlo usam chavetas.

===============================================================
FIM
===============================================================