========================================================================
E-FOLIO GLOBAL - COMPILACAO (UC 21018)
Licenciatura em Engenharia Informatica
Universidade Aberta - 2025/2026
========================================================================

Grupo QUADCORE (4 membros):
  - Maria Costa (2304361)
  - Joao Rodrigues (2203474)
  - Nuno Rolo (1900405)
  - Fábio Oliveira (1800960)

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
  - OTIMIZACAO do codigo intermedio TAC;
  - GERACAO DE CODIGO FINAL MIPS32.
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
  codegen_mips.py    - geracao de codigo final MIPS32 a partir de TAC otimizado
  run_codegen_tests.py - testes de execucao do MIPS gerado no simulador MARS

Ficheiros gerados pelo ANTLR (a partir de MOCP.g4):
  MOCPLexer.py, MOCPParser.py, MOCPVisitor.py, MOCPListener.py
  MOCP.tokens, MOCPLexer.tokens, MOCP.interp, MOCPLexer.interp

Simulador e artefactos de teste:
  Mars4_5.jar        - simulador MARS (binario de terceiros)
  Testes/*.asm       - assembly MIPS de referencia (um por programa valido)
  Testes/expected/   - saidas esperadas do pipeline (usadas por run_tests.py)

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
  teste_erros_escreverv.mocp  - erro semantico: escreverv exige vetor de dim. fixa
  spec_fatorial.mocp          - exemplo canonico: Fatorial Recursivo
  spec_media.mocp             - exemplo canonico: Media de um vetor
  teste_cobertura.mocp        - cobre construcoes nao cobertas pelos restantes
  teste_globais.mocp          - inicializacao de variaveis globais (escalar,
                                vetor literal, vetor dinamico e por chamada)

------------------------------------------------------------------------
3. REQUISITOS
------------------------------------------------------------------------
  - Python 3.10 ou superior
  - Runtime ANTLR para Python:
        pip install antlr4-python3-runtime==4.13.2
  - Java 11 ou superior - necessario para EXECUTAR o codigo MIPS gerado no
    simulador MARS e para os testes de execucao (run_codegen_tests.py).
    Tambem permite regenerar o parser ANTLR (seccao 4). O pipeline ate a
    geracao do .asm corre apenas com Python.
  - Simulador MARS (Mars4_5.jar) colocado na raiz do projeto - binario de
    terceiros. Necessario apenas para executar/testar o codigo MIPS gerado.

------------------------------------------------------------------------
4. REGENERAR O PARSER ANTLR (opcional)
------------------------------------------------------------------------
Os ficheiros gerados ja estao incluidos. Para os regenerar:

  java -jar antlr-4.13.2-complete.jar -Dlanguage=Python3 -visitor MOCP.g4

------------------------------------------------------------------------
5. EXECUCAO
------------------------------------------------------------------------
  python main.py <ficheiro.mocp> [saida_ast.txt] [saida_tac.txt]
Nota:
A geracao de codigo MIPS32 e efetuada atraves do modulo
codegen_mips.py descrito na secao seguinte.

O primeiro argumento (ficheiro fonte) e obrigatorio. Os dois argumentos
seguintes sao opcionais e indicam ficheiros onde guardar a AST e o TAC.

Exemplos:
 python main.py Testes/spec_fatorial.mocp
 python main.py Testes/spec_media.mocp ast.txt tac.txt
 python main.py Testes/teste_erros_semanticos.mocp

------------------------------------------------------------------------
6. GERACAO DE CODIGO FINAL MIPS32
------------------------------------------------------------------------

O projeto inclui um backend capaz de traduzir TAC otimizado para
assembly MIPS32.

Gerar ficheiro assembly:

  python codegen_mips.py <entrada.mocp> <saida.asm>

Exemplos:

  python codegen_mips.py Testes/spec_fatorial.mocp Testes/spec_fatorial.asm

  python codegen_mips.py Testes/spec_media.mocp Testes/spec_media.asm


------------------------------------------------------------------------
7. EXECUCAO DO CODIGO MIPS
------------------------------------------------------------------------

Os ficheiros .asm gerados foram desenvolvidos para o simulador MARS.

No ambiente grafico do MARS:
  1. Abrir o simulador MARS.
  2. Abrir o ficheiro .asm gerado.
  3. Selecionar Assemble.
  4. Selecionar Run.
  (Os programas que leem dados - ex.: spec_fatorial, spec_media - esperam a
   entrada na janela de I/O do Run, um inteiro por linha.)

Em linha de comando (sem interface grafica):
  java -jar Mars4_5.jar nc sm <ficheiro.asm>
  (nc = sem cabecalho; sm = arranca no rotulo 'main'; a entrada vem do stdin,
   ex.: printf '5\n' | java -jar Mars4_5.jar nc sm Testes/spec_fatorial.asm)

A correcao dos exemplos foi validada automaticamente (ver seccao 10.1).

------------------------------------------------------------------------
8. FUNCIONAMENTO (8 fases do pipeline)
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
  8. Geracao de codigo final MIPS32.

------------------------------------------------------------------------
9. SAIDA ESPERADA
------------------------------------------------------------------------
Programa valido (codigo de saida 0) - main.py mostra:
  - "Análise concluída com sucesso.";
  - a AST ("AST gerada:");
  - "Código intermédio TAC original:";
  - "Código intermédio TAC otimizado:".
  (A geracao do assembly MIPS32 e feita a parte, por codegen_mips.py - seccao 6.)

Programa com erros (codigo de saida 1) - o formato depende da fase:
  - Erros lexicos/sintaticos: a linha "Foram encontrados erros:" seguida de
    uma linha por erro, p. ex.:
        [LÉXICO] linha 10, coluna 8: carácter inesperado '@'.
        [LÉXICO/SINTÁTICO] linha 16, coluna 0: Palavra-chave C 'int'
        detetada. Em MOCP use 'inteiro'.
  - Erro semantico: e mostrado diretamente (sem cabecalho) e a analise para
    no primeiro erro, p. ex.:
        [SEMÂNTICO] Variável 'y' usada sem declaração prévia.

------------------------------------------------------------------------
10. TESTES AUTOMATICOS
------------------------------------------------------------------------
  python run_tests.py

O script `run_tests.py` descobre automaticamente todos os ficheiros
.mocp na pasta `Testes` (ordenados por nome) e executa cada um chamando
`python main.py <ficheiro.mocp>`. Não é necessário editar uma lista
de ficheiros no script — basta colocar os testes na pasta `Testes`.

Exemplos:
  - Executar a bateria completa de testes:
      python run_tests.py
  - Executar um único ficheiro de teste diretamente:
      python main.py Testes/spec_fatorial.mocp

Se a pasta `Testes` não existir ou não contiver ficheiros `.mocp`, o
script avisará e terminará sem executar testes.

O `run_tests.py` cobre duas fases: (1) o pipeline principal (main.py) e
(2) a geração MIPS, comparando a ESTRUTURA do .asm gerado com um .asm de
referência (deteta regressões no gerador).

------------------------------------------------------------------------
10.1 TESTES DE EXECUCAO DO CODIGO MIPS GERADO
------------------------------------------------------------------------
  python run_codegen_tests.py

Enquanto o run_tests.py confirma a estrutura do assembly, o script
run_codegen_tests.py valida que o codigo gerado esta correto ao ser
efetivamente executado. Para cada programa valido:

  .mocp --(codegen_mips.py)--> .asm --(MARS)--> saida ==? esperado

ou seja, gera o assembly, corre-o no simulador MARS (Mars4_5.jar) com uma
entrada definida e compara a saida do programa com a saida esperada
(calculada a mao a partir da semantica de cada programa). E a prova de
execucao exigida pelo enunciado do E-folio Global.

Requisitos: Java (para o MARS) e o ficheiro Mars4_5.jar na raiz do
projeto. Se o Java/MARS nao estiverem disponiveis, os testes de execucao
sao ignorados com aviso (sem falhar ambientes sem Java).

------------------------------------------------------------------------
11. OBSERVACOES SOBRE A LINGUAGEM MOCP
------------------------------------------------------------------------
  - As palavras-chave sao em portugues (inteiro, real, vazio, se, senao,
    enquanto, para, retornar, etc.).
  - As palavras-chave da linguagem C (int, if, return, ...) sao tratadas
    como ERRO.
  - As funcoes sem parametros usam '(vazio)'.
  - Os blocos sao sempre delimitados por chavetas { }.
  - Os prototipos das funcoes devem aparecer antes das definicoes de
    funcoes e das variaveis globais.

------------------------------------------------------------------------
12. NOTA SOBRE O E-FOLIO GLOBAL
------------------------------------------------------------------------

Esta versao corresponde ao E-Folio Global e integra todas as
funcionalidades desenvolvidas nos E-Folios A e B, bem como as melhorias
introduzidas posteriormente, incluindo novas validacoes semanticas,
otimizacoes adicionais e geracao de codigo final MIPS32.
========================================================================
