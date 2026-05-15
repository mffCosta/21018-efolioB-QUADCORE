========================================================================
E-FOLIO B - COMPILACAO (UC 21018)
Licenciatura em Engenharia Informatica
Universidade Aberta - 2025/2026
========================================================================

Grupo QUADCORE (4 membros):
  - Maria Costa (2304361)
  - Joao Rodrigues (2203474)
  - Nuno Rolo (1900405)
  - Flávio Oliveira (1900860)

------------------------------------------------------------------------
1. OBJETIVO
------------------------------------------------------------------------
Processador para a linguagem MOCP (My Own C in Portugues), desenvolvido
em Python com ANTLR4. O programa le um ficheiro fonte MOCP e executa o
pipeline completo de compilacao:
  - analise lexica;
  - analise sintatica;
  - construcao da Arvore de Sintaxe Abstrata (AST);
  - analise semantica;
  - geracao de codigo intermedio TAC (Three Address Code);
  - OTIMIZACAO do codigo intermedio TAC.
Os erros detetados em qualquer fase sao mostrados no ecra.

------------------------------------------------------------------------
2. CONTEUDO DO PROJETO
------------------------------------------------------------------------
Gramatica e codigo fonte:
  MOCP.g4            - gramatica ANTLR4 da linguagem MOCP
  main.py            - programa principal (orquestra o pipeline)
  ast_nodes.py       - definicao dos nos da AST
  ast_builder.py     - construcao da AST a partir da parse tree
  semantic.py        - analise semantica (inclui a tabela de simbolos)
  tac.py             - representacao do codigo intermedio TAC
  tac_generator.py   - geracao de TAC a partir da AST
  optimizer.py       - otimizacao do codigo intermedio TAC
  error_handler.py   - tratamento de erros lexicos e sintaticos
  run_tests.py       - execucao automatica da bateria de testes

Ficheiros gerados pelo ANTLR (a partir de MOCP.g4):
  MOCPLexer.py, MOCPParser.py, MOCPVisitor.py, MOCPListener.py
  MOCP.tokens, MOCPLexer.tokens, MOCP.interp, MOCPLexer.interp

Programas de teste (.mocp):
  exemplo_correto.mocp        - programa valido (prototipos, recursao,
                                vetores, ciclos, I/O, casting)
  exemplo_erros.mocp          - programa com erros variados
  melhorias_efolioA.mocp      - casos das melhorias ao E-folio A
  teste_global.mocp           - teste integrado da linguagem
  teste_ciclos_vetores.mocp   - ciclos, vetores e funcoes multiplas
  teste_erros_lexicos.mocp    - erros lexicos
  teste_erros_semanticos.mocp - erros semanticos
  teste_erros_variados.mocp   - varios tipos de erro em simultaneo
  spec_fatorial.mocp          - exemplo canonico: Fatorial Recursivo
  spec_media.mocp             - exemplo canonico: Media de um vetor
  teste_cobertura.mocp        - cobre construcoes nao cobertas pelos restantes

------------------------------------------------------------------------
3. REQUISITOS
------------------------------------------------------------------------
  - Python 3.10 ou superior
  - Runtime ANTLR para Python:
        pip install antlr4-python3-runtime==4.13.2
  - Java 11 ou superior - APENAS se quiser regenerar o parser a partir
    da gramatica (nao e necessario para executar o projeto).

------------------------------------------------------------------------
4. REGENERAR O PARSER ANTLR (opcional)
------------------------------------------------------------------------
Os ficheiros gerados ja estao incluidos. Para os regenerar:

  java -jar antlr-4.13.2-complete.jar -Dlanguage=Python3 -visitor MOCP.g4

------------------------------------------------------------------------
5. EXECUCAO
------------------------------------------------------------------------
  python main.py <ficheiro.mocp> [saida_ast.txt] [saida_tac.txt]

O primeiro argumento (ficheiro fonte) e obrigatorio. Os dois argumentos
seguintes sao opcionais e indicam ficheiros onde guardar a AST e o TAC.

Exemplos:
  python main.py spec_fatorial.mocp
  python main.py spec_media.mocp ast.txt tac.txt
  python main.py teste_erros_semanticos.mocp

------------------------------------------------------------------------
6. FUNCIONAMENTO (7 fases do pipeline)
------------------------------------------------------------------------
  1. Leitura do ficheiro fonte.
  2. Analise lexica - tokenizacao com ANTLR e detecao de tokens C
     proibidos (palavras-chave C, operadores nao suportados, caracteres
     invalidos, strings nao terminadas).
  3. Analise sintatica - verificacao da estrutura segundo a gramatica.
  4. Construcao da AST.
  5. Analise semantica - tabela de simbolos, declaracao de variaveis e
     funcoes, verificacao de tipos, numero de argumentos, existencia de
     'principal', funcoes com 'retornar'.
  6. Geracao de codigo intermedio TAC.
  7. Otimizacao do codigo intermedio TAC.

------------------------------------------------------------------------
7. SAIDA ESPERADA
------------------------------------------------------------------------
Programa valido:
  - mensagem "Analise concluida com sucesso";
  - impressao da AST;
  - seccao "Codigo intermedio TAC original";
  - seccao "Codigo intermedio TAC otimizado".

Programa com erros:
  - mensagem "Foram encontrados erros:" seguida das linhas de erro,
    cada uma classificada como [LEXICO], [SINTATICO] ou [SEMANTICO].

------------------------------------------------------------------------
8. TESTES AUTOMATICOS
------------------------------------------------------------------------
  python run_tests.py

Executa toda a bateria de programas .mocp e mostra o resultado de cada um.

------------------------------------------------------------------------
9. OBSERVACOES SOBRE A LINGUAGEM MOCP
------------------------------------------------------------------------
  - As palavras-chave sao em portugues (inteiro, real, vazio, se, senao,
    enquanto, para, retornar, etc.).
  - As palavras-chave da linguagem C (int, if, return, ...) sao tratadas
    como ERRO.
  - As funcoes sem parametros usam '(vazio)'.
  - Os blocos sao sempre delimitados por chavetas { }.
  - Os prototipos das funcoes devem aparecer antes das definicoes de
    funcoes e das variaveis globais.
========================================================================
