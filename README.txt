===============================================================
E-FÓLIO B — COMPILAÇÃO (UC 21018)
Licenciatura em Engenharia Informática — Universidade Aberta
Ano letivo 2025/2026
Grupo QUADCORE
Estudantes:
- Maria Costa (2304361)
- João Rodrigues (2203474)
- Nuno Rolo (1900405)
- Flávio Oliveira (1900860)
===============================================================

1. OBJETIVO
---------------------------------------------------------------
Este trabalho implementa, com recurso ao ANTLR4 e Python, um
processador completo para a linguagem MOCP (My Own C in Português).

A solução realiza:
- análise léxica;
- análise sintática;
- construção de uma árvore sintática abstrata (AST);
- validação semântica;
- geração de código intermédio de três endereços (TAC);
- otimização do código intermédio;
- apresentação de erros no ecrã.

2. CONTEÚDO DO PROJETO
---------------------------------------------------------------
Ficheiros principais:
- MOCP.g4                  Gramática ANTLR da linguagem MOCP
- main.py                  Programa principal e pipeline de compilação
- ast_nodes.py             Definição dos nós da AST
- ast_builder.py           Visitor para construir a AST
- error_handler.py         Deteção de palavras-chave C proibidas
- semantic.py              Validação semântica
- tac_generator.py         Geração de código TAC (Three Address Code)
- optimizer.py             Otimização do código intermédio TAC

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

Exemplos básicos:

    python main.py exemplo_correto.mocp
    python main.py exemplo_erros.mocp
    python main.py teste_ciclos_vetores.mocp
    python main.py teste_erros_variados.mocp
    python main.py teste_global.mocp

Guardar AST e TAC em ficheiros:

    python main.py exemplo_correto.mocp ast.txt
    python main.py exemplo_correto.mocp ast.txt codigo.tac

O primeiro argumento é obrigatório (ficheiro MOCP).
O segundo argumento (opcional) define onde guardar a AST.
O terceiro argumento (opcional) define onde guardar o TAC (original e otimizado).

6. FUNCIONAMENTO
---------------------------------------------------------------
O programa segue um pipeline de compilação com 10 etapas:

1) Leitura do ficheiro
   - o ficheiro MOCP é lido com encoding UTF-8.

2) Análise léxica
   - o lexer converte o texto de entrada em tokens;
   - comentários e espaços são ignorados;
   - símbolos inválidos são assinalados.

3) Deteção de tokens C proibidos
   - são identificadas palavras-chave da linguagem C original
     (por exemplo int, double, if, while, return, main);
   - são identificados operadores não suportados em MOCP
     (por exemplo ++, --, +=, -=, *=, /=).

4) Análise sintática
   - o parser verifica se a estrutura do programa respeita a
     gramática MOCP.

5) Construção da AST
   - a parse tree do ANTLR é convertida numa AST mais simples e
     abstrata.

6) Validação semântica
   - deteção de variáveis não declaradas;
   - validação de chamadas de função;
   - verificação de vetores, retornos e tipos.

7) Geração de TAC (Three Address Code)
   - a AST é convertida num código intermédio de três endereços;
   - cada instrução tem no máximo 3 operandos;
   - permite análise e otimização independente da linguagem alvo.

8) Otimização de TAC
   - redução de código redundante;
   - eliminação de operações desnecessárias;
   - simplificação e melhoria da eficiência do código intermédio.

9) Impressão da AST
   - a AST é apresentada num formato legível no terminal.

10) Impressão do TAC
    - tanto o TAC original como o TAC otimizado são apresentados
      no terminal e opcionalmente guardados em ficheiro.

7. SAÍDA ESPERADA
---------------------------------------------------------------
Se o ficheiro estiver correto, a saída inclui:

    Análise concluída com sucesso.
    
    AST gerada:
    ----------------------------------------
    ProgramNode
      ...
    
    Código intermédio TAC original:
    ----------------------------------------
    ...
    
    Código intermédio TAC otimizado:
    ----------------------------------------
    ...
    
    AST guardada em: ast.txt
    TAC original e otimizado guardados em: codigo.tac

Se o ficheiro contiver erros, a compilação é interrompida e mensagens
erro são apresentadas:

    Foram encontrados erros:
    [LÉXICO] linha X, coluna Y: ...
    [SINTÁTICO] linha X, coluna Y: ...
    [SEMÂNTICO] ...
    [TAC] ...

8. OBSERVAÇÕES
---------------------------------------------------------------
- A linguagem MOCP usa palavras-chave em português.
- O uso direto de palavras-chave da linguagem C é tratado como erro.
- As funções sem parâmetros devem ser escritas com (vazio).
- Todos os blocos de controlo usam chavetas.

===============================================================
FIM
===============================================================