/**
 * MOCP.g4 — Gramática ANTLR4 para a linguagem MOCP (My Own C in Português)
 * UC 21018 — Compilação, Universidade Aberta, 2025/2026
 * Autores: João Rodrigues (2203474) | Maria Costa (2304361)
 * Grupo: DUALCORE
 */

grammar MOCP;

// ======================================================
// PARSER RULES
// ======================================================

program
    : prototype* globalDecl* functionDef* EOF
    ;

// ------------------------------------------------------
// Protótipos e funções
// ------------------------------------------------------

prototype
    : returnType functionName LPAREN paramList RPAREN SEMI
    ;

globalDecl
    : varDecl
    ;

functionDef
    : returnType functionName LPAREN paramList RPAREN block
    ;

functionName
    : PRINCIPAL
    | ID
    ;

// ------------------------------------------------------
// Parâmetros
// Aceita:
//   vazio
//   inteiro x
//   real v[]
//   inteiro x, real y[]
//   real[]
// ------------------------------------------------------

paramList
    : VAZIO
    | param (COMMA param)*
    ;

param
    : varType ID? arraySuffix?
    ;

arraySuffix
    : LBRACK RBRACK
    ;

// ------------------------------------------------------
// Blocos e declarações
// ------------------------------------------------------

block
    : LBRACE varDecl* stmt* RBRACE
    ;

varDecl
    : varType varItem (COMMA varItem)* SEMI
    ;

varItem
    : ID                                              # VarSimpleDecl
    | ID ASSIGN expr                                  # VarInitDecl
    | ID LBRACK INT_LITERAL RBRACK                    # VarSizedArrayDecl
    | ID LBRACK RBRACK ASSIGN arrayInit               # VarArrayInitDecl
    | ID LBRACK RBRACK ASSIGN expr                    # VarArrayExprInitDecl
    | ID LBRACK RBRACK                                # VarUnsizedArrayDecl
    ;

arrayInit
    : LBRACE expr (COMMA expr)* RBRACE
    ;

// ------------------------------------------------------
// Instruções
// ------------------------------------------------------

stmt
    : assignStmt
    | ifStmt
    | whileStmt
    | forStmt
    | returnStmt
    | writeStmt
    | callStmt
    | block
    | SEMI
    ;

assignStmt
    : location ASSIGN expr SEMI
    ;

ifStmt
    : SE LPAREN condExpr RPAREN block (SENAO block)?
    ;

whileStmt
    : ENQUANTO LPAREN condExpr RPAREN block
    ;

forStmt
    : PARA LPAREN forInit? SEMI forCond? SEMI forUpdate? RPAREN block
    ;

forInit
    : location ASSIGN expr
    ;

forCond
    : condExpr
    ;

forUpdate
    : location ASSIGN expr
    ;

returnStmt
    : RETORNAR expr? SEMI
    ;

// chamada a função normal como instrução
callStmt
    : userFunctionCall SEMI
    ;

// escrita como instrução, não como expressão
writeStmt
    : ESCREVER  LPAREN expr RPAREN SEMI
    | ESCREVERC LPAREN expr RPAREN SEMI
    | ESCREVERS LPAREN expr RPAREN SEMI
    | ESCREVERV LPAREN ID RPAREN SEMI
    ;

// ======================================================
// CONDIÇÕES
// Conforme o enunciado: Expr ou Expr OpCond Expr,
// além de &&, || e !
// ======================================================

condExpr
    : logicalOrExpr
    ;

logicalOrExpr
    : logicalAndExpr (OR logicalAndExpr)*
    ;

logicalAndExpr
    : logicalNotExpr (AND logicalNotExpr)*
    ;

logicalNotExpr
    : NOT logicalNotExpr
    | relationalExpr
    ;

relationalExpr
    : expr (relOp expr)?
    | LPAREN condExpr RPAREN
    ;

relOp
    : LT
    | LE
    | GT
    | GE
    | EQ
    | NE
    ;

// ======================================================
// EXPRESSÕES
// ======================================================

expr
    : additiveExpr
    ;

additiveExpr
    : multiplicativeExpr ((PLUS | MINUS) multiplicativeExpr)*
    ;

multiplicativeExpr
    : unaryExpr ((MUL | DIV | MOD) unaryExpr)*
    ;

unaryExpr
    : MINUS unaryExpr
    | castExpr
    ;

castExpr
    : LPAREN castType RPAREN unaryExpr
    | primaryExpr
    ;

primaryExpr
    : location
    | inputCall
    | userFunctionCall
    | literal
    | LPAREN expr RPAREN
    ;

// ------------------------------------------------------
// Localizações
// ------------------------------------------------------

location
    : ID
    | ID LBRACK expr RBRACK
    ;

// ------------------------------------------------------
// Chamadas
// Ler/lerc/lers podem aparecer em expressões.
// Escrever* fica restrito a writeStmt.
// ------------------------------------------------------

inputCall
    : LER LPAREN RPAREN
    | LERC LPAREN RPAREN
    | LERS LPAREN RPAREN
    ;

userFunctionCall
    : functionName LPAREN argList? RPAREN
    ;

argList
    : expr (COMMA expr)*
    ;

// ------------------------------------------------------
// Literais
// ------------------------------------------------------

literal
    : INT_LITERAL
    | REAL_LITERAL
    | STRING_LITERAL
    ;

// ------------------------------------------------------
// Tipos
// returnType admite vazio
// varType e castType não admitem vazio
// ------------------------------------------------------

returnType
    : INTEIRO
    | REAL
    | VAZIO
    ;

varType
    : INTEIRO
    | REAL
    ;

castType
    : INTEIRO
    | REAL
    ;

// ======================================================
// LEXER RULES
// ======================================================

// --- Palavras-chave MOCP ---
INTEIRO   : 'inteiro';
REAL      : 'real';
VAZIO     : 'vazio';
PRINCIPAL : 'principal';

SE        : 'se';
SENAO     : 'senao';
ENQUANTO  : 'enquanto';
PARA      : 'para';
RETORNAR  : 'retornar';

LER       : 'ler';
LERC      : 'lerc';
LERS      : 'lers';

ESCREVER  : 'escrever';
ESCREVERC : 'escreverc';
ESCREVERV : 'escreverv';
ESCREVERS : 'escrevers';

// --- Palavras-chave C PROIBIDAS (deteção de erros) ---
C_INT        : 'int'      ;
C_DOUBLE     : 'double'   ;
C_VOID       : 'void'     ;
C_MAIN       : 'main'     ;
C_IF         : 'if'       ;
C_ELSE       : 'else'     ;
C_WHILE      : 'while'    ;
C_FOR        : 'for'      ;
C_RETURN     : 'return'   ;
C_READ       : 'read'     ;
C_READC      : 'readc'    ;
C_READS      : 'reads'    ;
C_WRITE      : 'write'    ;
C_WRITEC     : 'writec'   ;
C_WRITEV     : 'writev'   ;
C_WRITES     : 'writes'   ;
C_STRUCT     : 'struct'   ;
C_INCLUDE    : '#include' ;
C_DEFINE     : '#define'  ;

// --- Operadores lógicos ---
AND       : '&&';
OR        : '||';
NOT       : '!';

// --- Operadores relacionais ---
LE        : '<=';
GE        : '>=';
EQ        : '==';
NE        : '!=';
LT        : '<';
GT        : '>';

// --- Operadores aritméticos / atribuição (multi-char ANTES de single-char) ---
OP_PLUSPLUS   : '++' ;
OP_MINUSMINUS : '--' ;
OP_PLUSEQ     : '+=' ;
OP_MINUSEQ    : '-=' ;
OP_MULEQ      : '*=' ;
OP_DIVEQ      : '/=' ;

PLUS      : '+';
MINUS     : '-';
MUL       : '*';
DIV       : '/';
MOD       : '%';
ASSIGN    : '=';

// --- Delimitadores ---
LPAREN    : '(';
RPAREN    : ')';
LBRACE    : '{';
RBRACE    : '}';
LBRACK    : '[';
RBRACK    : ']';
COMMA     : ',';
SEMI      : ';';

// --- Literais ---
fragment DIGITS
    : [0-9]+
    ;

REAL_LITERAL
    : DIGITS '.' DIGITS?
    | '.' DIGITS
    ;

INT_LITERAL
    : DIGITS
    ;

STRING_LITERAL
    : '"' (ESC_SEQ | ~["\\\r\n])* '"'
    ;

UNCLOSED_STRING
    : '"' (ESC_SEQ | ~["\\\r\n])*
    ;

fragment ESC_SEQ
    : '\\' [btnr"\\]
    ;

// --- Identificadores ---
ID
    : [a-zA-Z_][a-zA-Z_0-9]*
    ;

// --- Comentários e espaços ---
LINE_COMMENT
    : '//' ~[\r\n]* -> skip
    ;

BLOCK_COMMENT
    : '/*' .*? '*/' -> skip
    ;

WS
    : [ \t\r\n]+ -> skip
    ;

ERROR_CHAR
    : .
    ;
