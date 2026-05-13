// Generated from c:/Users/mffcf/MEOCloud/LEI/3 Ano/2Semestre/21018 Compilação/efolio B/efolioB_QUADCORE/MOCP.g4 by ANTLR 4.13.1
import org.antlr.v4.runtime.atn.*;
import org.antlr.v4.runtime.dfa.DFA;
import org.antlr.v4.runtime.*;
import org.antlr.v4.runtime.misc.*;
import org.antlr.v4.runtime.tree.*;
import java.util.List;
import java.util.Iterator;
import java.util.ArrayList;

@SuppressWarnings({"all", "warnings", "unchecked", "unused", "cast", "CheckReturnValue"})
public class MOCPParser extends Parser {
	static { RuntimeMetaData.checkVersion("4.13.1", RuntimeMetaData.VERSION); }

	protected static final DFA[] _decisionToDFA;
	protected static final PredictionContextCache _sharedContextCache =
		new PredictionContextCache();
	public static final int
		INTEIRO=1, REAL=2, VAZIO=3, PRINCIPAL=4, SE=5, SENAO=6, ENQUANTO=7, PARA=8, 
		RETORNAR=9, LER=10, LERC=11, LERS=12, ESCREVER=13, ESCREVERC=14, ESCREVERV=15, 
		ESCREVERS=16, C_INT=17, C_DOUBLE=18, C_VOID=19, C_MAIN=20, C_IF=21, C_ELSE=22, 
		C_WHILE=23, C_FOR=24, C_RETURN=25, C_READ=26, C_READC=27, C_READS=28, 
		C_WRITE=29, C_WRITEC=30, C_WRITEV=31, C_WRITES=32, C_STRUCT=33, C_INCLUDE=34, 
		C_DEFINE=35, AND=36, OR=37, NOT=38, LE=39, GE=40, EQ=41, NE=42, LT=43, 
		GT=44, OP_PLUSPLUS=45, OP_MINUSMINUS=46, OP_PLUSEQ=47, OP_MINUSEQ=48, 
		OP_MULEQ=49, OP_DIVEQ=50, PLUS=51, MINUS=52, MUL=53, DIV=54, MOD=55, ASSIGN=56, 
		LPAREN=57, RPAREN=58, LBRACE=59, RBRACE=60, LBRACK=61, RBRACK=62, COMMA=63, 
		SEMI=64, REAL_LITERAL=65, INT_LITERAL=66, STRING_LITERAL=67, UNCLOSED_STRING=68, 
		ID=69, LINE_COMMENT=70, BLOCK_COMMENT=71, WS=72, ERROR_CHAR=73;
	public static final int
		RULE_program = 0, RULE_prototype = 1, RULE_globalDecl = 2, RULE_functionDef = 3, 
		RULE_functionName = 4, RULE_paramList = 5, RULE_param = 6, RULE_arraySuffix = 7, 
		RULE_block = 8, RULE_varDecl = 9, RULE_varItem = 10, RULE_arrayInit = 11, 
		RULE_stmt = 12, RULE_assignStmt = 13, RULE_ifStmt = 14, RULE_whileStmt = 15, 
		RULE_forStmt = 16, RULE_forInit = 17, RULE_forCond = 18, RULE_forUpdate = 19, 
		RULE_returnStmt = 20, RULE_callStmt = 21, RULE_writeStmt = 22, RULE_condExpr = 23, 
		RULE_logicalOrExpr = 24, RULE_logicalAndExpr = 25, RULE_logicalNotExpr = 26, 
		RULE_relationalExpr = 27, RULE_relOp = 28, RULE_expr = 29, RULE_additiveExpr = 30, 
		RULE_multiplicativeExpr = 31, RULE_unaryExpr = 32, RULE_castExpr = 33, 
		RULE_primaryExpr = 34, RULE_location = 35, RULE_inputCall = 36, RULE_userFunctionCall = 37, 
		RULE_argList = 38, RULE_literal = 39, RULE_returnType = 40, RULE_varType = 41, 
		RULE_castType = 42;
	private static String[] makeRuleNames() {
		return new String[] {
			"program", "prototype", "globalDecl", "functionDef", "functionName", 
			"paramList", "param", "arraySuffix", "block", "varDecl", "varItem", "arrayInit", 
			"stmt", "assignStmt", "ifStmt", "whileStmt", "forStmt", "forInit", "forCond", 
			"forUpdate", "returnStmt", "callStmt", "writeStmt", "condExpr", "logicalOrExpr", 
			"logicalAndExpr", "logicalNotExpr", "relationalExpr", "relOp", "expr", 
			"additiveExpr", "multiplicativeExpr", "unaryExpr", "castExpr", "primaryExpr", 
			"location", "inputCall", "userFunctionCall", "argList", "literal", "returnType", 
			"varType", "castType"
		};
	}
	public static final String[] ruleNames = makeRuleNames();

	private static String[] makeLiteralNames() {
		return new String[] {
			null, "'inteiro'", "'real'", "'vazio'", "'principal'", "'se'", "'senao'", 
			"'enquanto'", "'para'", "'retornar'", "'ler'", "'lerc'", "'lers'", "'escrever'", 
			"'escreverc'", "'escreverv'", "'escrevers'", "'int'", "'double'", "'void'", 
			"'main'", "'if'", "'else'", "'while'", "'for'", "'return'", "'read'", 
			"'readc'", "'reads'", "'write'", "'writec'", "'writev'", "'writes'", 
			"'struct'", "'#include'", "'#define'", "'&&'", "'||'", "'!'", "'<='", 
			"'>='", "'=='", "'!='", "'<'", "'>'", "'++'", "'--'", "'+='", "'-='", 
			"'*='", "'/='", "'+'", "'-'", "'*'", "'/'", "'%'", "'='", "'('", "')'", 
			"'{'", "'}'", "'['", "']'", "','", "';'"
		};
	}
	private static final String[] _LITERAL_NAMES = makeLiteralNames();
	private static String[] makeSymbolicNames() {
		return new String[] {
			null, "INTEIRO", "REAL", "VAZIO", "PRINCIPAL", "SE", "SENAO", "ENQUANTO", 
			"PARA", "RETORNAR", "LER", "LERC", "LERS", "ESCREVER", "ESCREVERC", "ESCREVERV", 
			"ESCREVERS", "C_INT", "C_DOUBLE", "C_VOID", "C_MAIN", "C_IF", "C_ELSE", 
			"C_WHILE", "C_FOR", "C_RETURN", "C_READ", "C_READC", "C_READS", "C_WRITE", 
			"C_WRITEC", "C_WRITEV", "C_WRITES", "C_STRUCT", "C_INCLUDE", "C_DEFINE", 
			"AND", "OR", "NOT", "LE", "GE", "EQ", "NE", "LT", "GT", "OP_PLUSPLUS", 
			"OP_MINUSMINUS", "OP_PLUSEQ", "OP_MINUSEQ", "OP_MULEQ", "OP_DIVEQ", "PLUS", 
			"MINUS", "MUL", "DIV", "MOD", "ASSIGN", "LPAREN", "RPAREN", "LBRACE", 
			"RBRACE", "LBRACK", "RBRACK", "COMMA", "SEMI", "REAL_LITERAL", "INT_LITERAL", 
			"STRING_LITERAL", "UNCLOSED_STRING", "ID", "LINE_COMMENT", "BLOCK_COMMENT", 
			"WS", "ERROR_CHAR"
		};
	}
	private static final String[] _SYMBOLIC_NAMES = makeSymbolicNames();
	public static final Vocabulary VOCABULARY = new VocabularyImpl(_LITERAL_NAMES, _SYMBOLIC_NAMES);

	/**
	 * @deprecated Use {@link #VOCABULARY} instead.
	 */
	@Deprecated
	public static final String[] tokenNames;
	static {
		tokenNames = new String[_SYMBOLIC_NAMES.length];
		for (int i = 0; i < tokenNames.length; i++) {
			tokenNames[i] = VOCABULARY.getLiteralName(i);
			if (tokenNames[i] == null) {
				tokenNames[i] = VOCABULARY.getSymbolicName(i);
			}

			if (tokenNames[i] == null) {
				tokenNames[i] = "<INVALID>";
			}
		}
	}

	@Override
	@Deprecated
	public String[] getTokenNames() {
		return tokenNames;
	}

	@Override

	public Vocabulary getVocabulary() {
		return VOCABULARY;
	}

	@Override
	public String getGrammarFileName() { return "MOCP.g4"; }

	@Override
	public String[] getRuleNames() { return ruleNames; }

	@Override
	public String getSerializedATN() { return _serializedATN; }

	@Override
	public ATN getATN() { return _ATN; }

	public MOCPParser(TokenStream input) {
		super(input);
		_interp = new ParserATNSimulator(this,_ATN,_decisionToDFA,_sharedContextCache);
	}

	@SuppressWarnings("CheckReturnValue")
	public static class ProgramContext extends ParserRuleContext {
		public TerminalNode EOF() { return getToken(MOCPParser.EOF, 0); }
		public List<PrototypeContext> prototype() {
			return getRuleContexts(PrototypeContext.class);
		}
		public PrototypeContext prototype(int i) {
			return getRuleContext(PrototypeContext.class,i);
		}
		public List<GlobalDeclContext> globalDecl() {
			return getRuleContexts(GlobalDeclContext.class);
		}
		public GlobalDeclContext globalDecl(int i) {
			return getRuleContext(GlobalDeclContext.class,i);
		}
		public List<FunctionDefContext> functionDef() {
			return getRuleContexts(FunctionDefContext.class);
		}
		public FunctionDefContext functionDef(int i) {
			return getRuleContext(FunctionDefContext.class,i);
		}
		public ProgramContext(ParserRuleContext parent, int invokingState) {
			super(parent, invokingState);
		}
		@Override public int getRuleIndex() { return RULE_program; }
	}

	public final ProgramContext program() throws RecognitionException {
		ProgramContext _localctx = new ProgramContext(_ctx, getState());
		enterRule(_localctx, 0, RULE_program);
		int _la;
		try {
			int _alt;
			enterOuterAlt(_localctx, 1);
			{
			setState(89);
			_errHandler.sync(this);
			_alt = getInterpreter().adaptivePredict(_input,0,_ctx);
			while ( _alt!=2 && _alt!=org.antlr.v4.runtime.atn.ATN.INVALID_ALT_NUMBER ) {
				if ( _alt==1 ) {
					{
					{
					setState(86);
					prototype();
					}
					} 
				}
				setState(91);
				_errHandler.sync(this);
				_alt = getInterpreter().adaptivePredict(_input,0,_ctx);
			}
			setState(95);
			_errHandler.sync(this);
			_alt = getInterpreter().adaptivePredict(_input,1,_ctx);
			while ( _alt!=2 && _alt!=org.antlr.v4.runtime.atn.ATN.INVALID_ALT_NUMBER ) {
				if ( _alt==1 ) {
					{
					{
					setState(92);
					globalDecl();
					}
					} 
				}
				setState(97);
				_errHandler.sync(this);
				_alt = getInterpreter().adaptivePredict(_input,1,_ctx);
			}
			setState(101);
			_errHandler.sync(this);
			_la = _input.LA(1);
			while ((((_la) & ~0x3f) == 0 && ((1L << _la) & 14L) != 0)) {
				{
				{
				setState(98);
				functionDef();
				}
				}
				setState(103);
				_errHandler.sync(this);
				_la = _input.LA(1);
			}
			setState(104);
			match(EOF);
			}
		}
		catch (RecognitionException re) {
			_localctx.exception = re;
			_errHandler.reportError(this, re);
			_errHandler.recover(this, re);
		}
		finally {
			exitRule();
		}
		return _localctx;
	}

	@SuppressWarnings("CheckReturnValue")
	public static class PrototypeContext extends ParserRuleContext {
		public ReturnTypeContext returnType() {
			return getRuleContext(ReturnTypeContext.class,0);
		}
		public FunctionNameContext functionName() {
			return getRuleContext(FunctionNameContext.class,0);
		}
		public TerminalNode LPAREN() { return getToken(MOCPParser.LPAREN, 0); }
		public ParamListContext paramList() {
			return getRuleContext(ParamListContext.class,0);
		}
		public TerminalNode RPAREN() { return getToken(MOCPParser.RPAREN, 0); }
		public TerminalNode SEMI() { return getToken(MOCPParser.SEMI, 0); }
		public PrototypeContext(ParserRuleContext parent, int invokingState) {
			super(parent, invokingState);
		}
		@Override public int getRuleIndex() { return RULE_prototype; }
	}

	public final PrototypeContext prototype() throws RecognitionException {
		PrototypeContext _localctx = new PrototypeContext(_ctx, getState());
		enterRule(_localctx, 2, RULE_prototype);
		try {
			enterOuterAlt(_localctx, 1);
			{
			setState(106);
			returnType();
			setState(107);
			functionName();
			setState(108);
			match(LPAREN);
			setState(109);
			paramList();
			setState(110);
			match(RPAREN);
			setState(111);
			match(SEMI);
			}
		}
		catch (RecognitionException re) {
			_localctx.exception = re;
			_errHandler.reportError(this, re);
			_errHandler.recover(this, re);
		}
		finally {
			exitRule();
		}
		return _localctx;
	}

	@SuppressWarnings("CheckReturnValue")
	public static class GlobalDeclContext extends ParserRuleContext {
		public VarDeclContext varDecl() {
			return getRuleContext(VarDeclContext.class,0);
		}
		public GlobalDeclContext(ParserRuleContext parent, int invokingState) {
			super(parent, invokingState);
		}
		@Override public int getRuleIndex() { return RULE_globalDecl; }
	}

	public final GlobalDeclContext globalDecl() throws RecognitionException {
		GlobalDeclContext _localctx = new GlobalDeclContext(_ctx, getState());
		enterRule(_localctx, 4, RULE_globalDecl);
		try {
			enterOuterAlt(_localctx, 1);
			{
			setState(113);
			varDecl();
			}
		}
		catch (RecognitionException re) {
			_localctx.exception = re;
			_errHandler.reportError(this, re);
			_errHandler.recover(this, re);
		}
		finally {
			exitRule();
		}
		return _localctx;
	}

	@SuppressWarnings("CheckReturnValue")
	public static class FunctionDefContext extends ParserRuleContext {
		public ReturnTypeContext returnType() {
			return getRuleContext(ReturnTypeContext.class,0);
		}
		public FunctionNameContext functionName() {
			return getRuleContext(FunctionNameContext.class,0);
		}
		public TerminalNode LPAREN() { return getToken(MOCPParser.LPAREN, 0); }
		public ParamListContext paramList() {
			return getRuleContext(ParamListContext.class,0);
		}
		public TerminalNode RPAREN() { return getToken(MOCPParser.RPAREN, 0); }
		public BlockContext block() {
			return getRuleContext(BlockContext.class,0);
		}
		public FunctionDefContext(ParserRuleContext parent, int invokingState) {
			super(parent, invokingState);
		}
		@Override public int getRuleIndex() { return RULE_functionDef; }
	}

	public final FunctionDefContext functionDef() throws RecognitionException {
		FunctionDefContext _localctx = new FunctionDefContext(_ctx, getState());
		enterRule(_localctx, 6, RULE_functionDef);
		try {
			enterOuterAlt(_localctx, 1);
			{
			setState(115);
			returnType();
			setState(116);
			functionName();
			setState(117);
			match(LPAREN);
			setState(118);
			paramList();
			setState(119);
			match(RPAREN);
			setState(120);
			block();
			}
		}
		catch (RecognitionException re) {
			_localctx.exception = re;
			_errHandler.reportError(this, re);
			_errHandler.recover(this, re);
		}
		finally {
			exitRule();
		}
		return _localctx;
	}

	@SuppressWarnings("CheckReturnValue")
	public static class FunctionNameContext extends ParserRuleContext {
		public TerminalNode PRINCIPAL() { return getToken(MOCPParser.PRINCIPAL, 0); }
		public TerminalNode ID() { return getToken(MOCPParser.ID, 0); }
		public FunctionNameContext(ParserRuleContext parent, int invokingState) {
			super(parent, invokingState);
		}
		@Override public int getRuleIndex() { return RULE_functionName; }
	}

	public final FunctionNameContext functionName() throws RecognitionException {
		FunctionNameContext _localctx = new FunctionNameContext(_ctx, getState());
		enterRule(_localctx, 8, RULE_functionName);
		int _la;
		try {
			enterOuterAlt(_localctx, 1);
			{
			setState(122);
			_la = _input.LA(1);
			if ( !(_la==PRINCIPAL || _la==ID) ) {
			_errHandler.recoverInline(this);
			}
			else {
				if ( _input.LA(1)==Token.EOF ) matchedEOF = true;
				_errHandler.reportMatch(this);
				consume();
			}
			}
		}
		catch (RecognitionException re) {
			_localctx.exception = re;
			_errHandler.reportError(this, re);
			_errHandler.recover(this, re);
		}
		finally {
			exitRule();
		}
		return _localctx;
	}

	@SuppressWarnings("CheckReturnValue")
	public static class ParamListContext extends ParserRuleContext {
		public TerminalNode VAZIO() { return getToken(MOCPParser.VAZIO, 0); }
		public List<ParamContext> param() {
			return getRuleContexts(ParamContext.class);
		}
		public ParamContext param(int i) {
			return getRuleContext(ParamContext.class,i);
		}
		public List<TerminalNode> COMMA() { return getTokens(MOCPParser.COMMA); }
		public TerminalNode COMMA(int i) {
			return getToken(MOCPParser.COMMA, i);
		}
		public ParamListContext(ParserRuleContext parent, int invokingState) {
			super(parent, invokingState);
		}
		@Override public int getRuleIndex() { return RULE_paramList; }
	}

	public final ParamListContext paramList() throws RecognitionException {
		ParamListContext _localctx = new ParamListContext(_ctx, getState());
		enterRule(_localctx, 10, RULE_paramList);
		int _la;
		try {
			setState(133);
			_errHandler.sync(this);
			switch (_input.LA(1)) {
			case VAZIO:
				enterOuterAlt(_localctx, 1);
				{
				setState(124);
				match(VAZIO);
				}
				break;
			case INTEIRO:
			case REAL:
				enterOuterAlt(_localctx, 2);
				{
				setState(125);
				param();
				setState(130);
				_errHandler.sync(this);
				_la = _input.LA(1);
				while (_la==COMMA) {
					{
					{
					setState(126);
					match(COMMA);
					setState(127);
					param();
					}
					}
					setState(132);
					_errHandler.sync(this);
					_la = _input.LA(1);
				}
				}
				break;
			default:
				throw new NoViableAltException(this);
			}
		}
		catch (RecognitionException re) {
			_localctx.exception = re;
			_errHandler.reportError(this, re);
			_errHandler.recover(this, re);
		}
		finally {
			exitRule();
		}
		return _localctx;
	}

	@SuppressWarnings("CheckReturnValue")
	public static class ParamContext extends ParserRuleContext {
		public VarTypeContext varType() {
			return getRuleContext(VarTypeContext.class,0);
		}
		public TerminalNode ID() { return getToken(MOCPParser.ID, 0); }
		public ArraySuffixContext arraySuffix() {
			return getRuleContext(ArraySuffixContext.class,0);
		}
		public ParamContext(ParserRuleContext parent, int invokingState) {
			super(parent, invokingState);
		}
		@Override public int getRuleIndex() { return RULE_param; }
	}

	public final ParamContext param() throws RecognitionException {
		ParamContext _localctx = new ParamContext(_ctx, getState());
		enterRule(_localctx, 12, RULE_param);
		int _la;
		try {
			enterOuterAlt(_localctx, 1);
			{
			setState(135);
			varType();
			setState(137);
			_errHandler.sync(this);
			_la = _input.LA(1);
			if (_la==ID) {
				{
				setState(136);
				match(ID);
				}
			}

			setState(140);
			_errHandler.sync(this);
			_la = _input.LA(1);
			if (_la==LBRACK) {
				{
				setState(139);
				arraySuffix();
				}
			}

			}
		}
		catch (RecognitionException re) {
			_localctx.exception = re;
			_errHandler.reportError(this, re);
			_errHandler.recover(this, re);
		}
		finally {
			exitRule();
		}
		return _localctx;
	}

	@SuppressWarnings("CheckReturnValue")
	public static class ArraySuffixContext extends ParserRuleContext {
		public TerminalNode LBRACK() { return getToken(MOCPParser.LBRACK, 0); }
		public TerminalNode RBRACK() { return getToken(MOCPParser.RBRACK, 0); }
		public ArraySuffixContext(ParserRuleContext parent, int invokingState) {
			super(parent, invokingState);
		}
		@Override public int getRuleIndex() { return RULE_arraySuffix; }
	}

	public final ArraySuffixContext arraySuffix() throws RecognitionException {
		ArraySuffixContext _localctx = new ArraySuffixContext(_ctx, getState());
		enterRule(_localctx, 14, RULE_arraySuffix);
		try {
			enterOuterAlt(_localctx, 1);
			{
			setState(142);
			match(LBRACK);
			setState(143);
			match(RBRACK);
			}
		}
		catch (RecognitionException re) {
			_localctx.exception = re;
			_errHandler.reportError(this, re);
			_errHandler.recover(this, re);
		}
		finally {
			exitRule();
		}
		return _localctx;
	}

	@SuppressWarnings("CheckReturnValue")
	public static class BlockContext extends ParserRuleContext {
		public TerminalNode LBRACE() { return getToken(MOCPParser.LBRACE, 0); }
		public TerminalNode RBRACE() { return getToken(MOCPParser.RBRACE, 0); }
		public List<VarDeclContext> varDecl() {
			return getRuleContexts(VarDeclContext.class);
		}
		public VarDeclContext varDecl(int i) {
			return getRuleContext(VarDeclContext.class,i);
		}
		public List<StmtContext> stmt() {
			return getRuleContexts(StmtContext.class);
		}
		public StmtContext stmt(int i) {
			return getRuleContext(StmtContext.class,i);
		}
		public BlockContext(ParserRuleContext parent, int invokingState) {
			super(parent, invokingState);
		}
		@Override public int getRuleIndex() { return RULE_block; }
	}

	public final BlockContext block() throws RecognitionException {
		BlockContext _localctx = new BlockContext(_ctx, getState());
		enterRule(_localctx, 16, RULE_block);
		int _la;
		try {
			enterOuterAlt(_localctx, 1);
			{
			setState(145);
			match(LBRACE);
			setState(149);
			_errHandler.sync(this);
			_la = _input.LA(1);
			while (_la==INTEIRO || _la==REAL) {
				{
				{
				setState(146);
				varDecl();
				}
				}
				setState(151);
				_errHandler.sync(this);
				_la = _input.LA(1);
			}
			setState(155);
			_errHandler.sync(this);
			_la = _input.LA(1);
			while ((((_la) & ~0x3f) == 0 && ((1L << _la) & 576460752303547312L) != 0) || _la==SEMI || _la==ID) {
				{
				{
				setState(152);
				stmt();
				}
				}
				setState(157);
				_errHandler.sync(this);
				_la = _input.LA(1);
			}
			setState(158);
			match(RBRACE);
			}
		}
		catch (RecognitionException re) {
			_localctx.exception = re;
			_errHandler.reportError(this, re);
			_errHandler.recover(this, re);
		}
		finally {
			exitRule();
		}
		return _localctx;
	}

	@SuppressWarnings("CheckReturnValue")
	public static class VarDeclContext extends ParserRuleContext {
		public VarTypeContext varType() {
			return getRuleContext(VarTypeContext.class,0);
		}
		public List<VarItemContext> varItem() {
			return getRuleContexts(VarItemContext.class);
		}
		public VarItemContext varItem(int i) {
			return getRuleContext(VarItemContext.class,i);
		}
		public TerminalNode SEMI() { return getToken(MOCPParser.SEMI, 0); }
		public List<TerminalNode> COMMA() { return getTokens(MOCPParser.COMMA); }
		public TerminalNode COMMA(int i) {
			return getToken(MOCPParser.COMMA, i);
		}
		public VarDeclContext(ParserRuleContext parent, int invokingState) {
			super(parent, invokingState);
		}
		@Override public int getRuleIndex() { return RULE_varDecl; }
	}

	public final VarDeclContext varDecl() throws RecognitionException {
		VarDeclContext _localctx = new VarDeclContext(_ctx, getState());
		enterRule(_localctx, 18, RULE_varDecl);
		int _la;
		try {
			enterOuterAlt(_localctx, 1);
			{
			setState(160);
			varType();
			setState(161);
			varItem();
			setState(166);
			_errHandler.sync(this);
			_la = _input.LA(1);
			while (_la==COMMA) {
				{
				{
				setState(162);
				match(COMMA);
				setState(163);
				varItem();
				}
				}
				setState(168);
				_errHandler.sync(this);
				_la = _input.LA(1);
			}
			setState(169);
			match(SEMI);
			}
		}
		catch (RecognitionException re) {
			_localctx.exception = re;
			_errHandler.reportError(this, re);
			_errHandler.recover(this, re);
		}
		finally {
			exitRule();
		}
		return _localctx;
	}

	@SuppressWarnings("CheckReturnValue")
	public static class VarItemContext extends ParserRuleContext {
		public VarItemContext(ParserRuleContext parent, int invokingState) {
			super(parent, invokingState);
		}
		@Override public int getRuleIndex() { return RULE_varItem; }
	 
		public VarItemContext() { }
		public void copyFrom(VarItemContext ctx) {
			super.copyFrom(ctx);
		}
	}
	@SuppressWarnings("CheckReturnValue")
	public static class VarSimpleDeclContext extends VarItemContext {
		public TerminalNode ID() { return getToken(MOCPParser.ID, 0); }
		public VarSimpleDeclContext(VarItemContext ctx) { copyFrom(ctx); }
	}
	@SuppressWarnings("CheckReturnValue")
	public static class VarArrayInitDeclContext extends VarItemContext {
		public TerminalNode ID() { return getToken(MOCPParser.ID, 0); }
		public TerminalNode LBRACK() { return getToken(MOCPParser.LBRACK, 0); }
		public TerminalNode RBRACK() { return getToken(MOCPParser.RBRACK, 0); }
		public TerminalNode ASSIGN() { return getToken(MOCPParser.ASSIGN, 0); }
		public ArrayInitContext arrayInit() {
			return getRuleContext(ArrayInitContext.class,0);
		}
		public VarArrayInitDeclContext(VarItemContext ctx) { copyFrom(ctx); }
	}
	@SuppressWarnings("CheckReturnValue")
	public static class VarInitDeclContext extends VarItemContext {
		public TerminalNode ID() { return getToken(MOCPParser.ID, 0); }
		public TerminalNode ASSIGN() { return getToken(MOCPParser.ASSIGN, 0); }
		public ExprContext expr() {
			return getRuleContext(ExprContext.class,0);
		}
		public VarInitDeclContext(VarItemContext ctx) { copyFrom(ctx); }
	}
	@SuppressWarnings("CheckReturnValue")
	public static class VarSizedArrayDeclContext extends VarItemContext {
		public TerminalNode ID() { return getToken(MOCPParser.ID, 0); }
		public TerminalNode LBRACK() { return getToken(MOCPParser.LBRACK, 0); }
		public TerminalNode INT_LITERAL() { return getToken(MOCPParser.INT_LITERAL, 0); }
		public TerminalNode RBRACK() { return getToken(MOCPParser.RBRACK, 0); }
		public VarSizedArrayDeclContext(VarItemContext ctx) { copyFrom(ctx); }
	}
	@SuppressWarnings("CheckReturnValue")
	public static class VarArrayExprInitDeclContext extends VarItemContext {
		public TerminalNode ID() { return getToken(MOCPParser.ID, 0); }
		public TerminalNode LBRACK() { return getToken(MOCPParser.LBRACK, 0); }
		public TerminalNode RBRACK() { return getToken(MOCPParser.RBRACK, 0); }
		public TerminalNode ASSIGN() { return getToken(MOCPParser.ASSIGN, 0); }
		public ExprContext expr() {
			return getRuleContext(ExprContext.class,0);
		}
		public VarArrayExprInitDeclContext(VarItemContext ctx) { copyFrom(ctx); }
	}
	@SuppressWarnings("CheckReturnValue")
	public static class VarUnsizedArrayDeclContext extends VarItemContext {
		public TerminalNode ID() { return getToken(MOCPParser.ID, 0); }
		public TerminalNode LBRACK() { return getToken(MOCPParser.LBRACK, 0); }
		public TerminalNode RBRACK() { return getToken(MOCPParser.RBRACK, 0); }
		public VarUnsizedArrayDeclContext(VarItemContext ctx) { copyFrom(ctx); }
	}

	public final VarItemContext varItem() throws RecognitionException {
		VarItemContext _localctx = new VarItemContext(_ctx, getState());
		enterRule(_localctx, 20, RULE_varItem);
		try {
			setState(192);
			_errHandler.sync(this);
			switch ( getInterpreter().adaptivePredict(_input,10,_ctx) ) {
			case 1:
				_localctx = new VarSimpleDeclContext(_localctx);
				enterOuterAlt(_localctx, 1);
				{
				setState(171);
				match(ID);
				}
				break;
			case 2:
				_localctx = new VarInitDeclContext(_localctx);
				enterOuterAlt(_localctx, 2);
				{
				setState(172);
				match(ID);
				setState(173);
				match(ASSIGN);
				setState(174);
				expr();
				}
				break;
			case 3:
				_localctx = new VarSizedArrayDeclContext(_localctx);
				enterOuterAlt(_localctx, 3);
				{
				setState(175);
				match(ID);
				setState(176);
				match(LBRACK);
				setState(177);
				match(INT_LITERAL);
				setState(178);
				match(RBRACK);
				}
				break;
			case 4:
				_localctx = new VarArrayInitDeclContext(_localctx);
				enterOuterAlt(_localctx, 4);
				{
				setState(179);
				match(ID);
				setState(180);
				match(LBRACK);
				setState(181);
				match(RBRACK);
				setState(182);
				match(ASSIGN);
				setState(183);
				arrayInit();
				}
				break;
			case 5:
				_localctx = new VarArrayExprInitDeclContext(_localctx);
				enterOuterAlt(_localctx, 5);
				{
				setState(184);
				match(ID);
				setState(185);
				match(LBRACK);
				setState(186);
				match(RBRACK);
				setState(187);
				match(ASSIGN);
				setState(188);
				expr();
				}
				break;
			case 6:
				_localctx = new VarUnsizedArrayDeclContext(_localctx);
				enterOuterAlt(_localctx, 6);
				{
				setState(189);
				match(ID);
				setState(190);
				match(LBRACK);
				setState(191);
				match(RBRACK);
				}
				break;
			}
		}
		catch (RecognitionException re) {
			_localctx.exception = re;
			_errHandler.reportError(this, re);
			_errHandler.recover(this, re);
		}
		finally {
			exitRule();
		}
		return _localctx;
	}

	@SuppressWarnings("CheckReturnValue")
	public static class ArrayInitContext extends ParserRuleContext {
		public TerminalNode LBRACE() { return getToken(MOCPParser.LBRACE, 0); }
		public List<ExprContext> expr() {
			return getRuleContexts(ExprContext.class);
		}
		public ExprContext expr(int i) {
			return getRuleContext(ExprContext.class,i);
		}
		public TerminalNode RBRACE() { return getToken(MOCPParser.RBRACE, 0); }
		public List<TerminalNode> COMMA() { return getTokens(MOCPParser.COMMA); }
		public TerminalNode COMMA(int i) {
			return getToken(MOCPParser.COMMA, i);
		}
		public ArrayInitContext(ParserRuleContext parent, int invokingState) {
			super(parent, invokingState);
		}
		@Override public int getRuleIndex() { return RULE_arrayInit; }
	}

	public final ArrayInitContext arrayInit() throws RecognitionException {
		ArrayInitContext _localctx = new ArrayInitContext(_ctx, getState());
		enterRule(_localctx, 22, RULE_arrayInit);
		int _la;
		try {
			enterOuterAlt(_localctx, 1);
			{
			setState(194);
			match(LBRACE);
			setState(195);
			expr();
			setState(200);
			_errHandler.sync(this);
			_la = _input.LA(1);
			while (_la==COMMA) {
				{
				{
				setState(196);
				match(COMMA);
				setState(197);
				expr();
				}
				}
				setState(202);
				_errHandler.sync(this);
				_la = _input.LA(1);
			}
			setState(203);
			match(RBRACE);
			}
		}
		catch (RecognitionException re) {
			_localctx.exception = re;
			_errHandler.reportError(this, re);
			_errHandler.recover(this, re);
		}
		finally {
			exitRule();
		}
		return _localctx;
	}

	@SuppressWarnings("CheckReturnValue")
	public static class StmtContext extends ParserRuleContext {
		public AssignStmtContext assignStmt() {
			return getRuleContext(AssignStmtContext.class,0);
		}
		public IfStmtContext ifStmt() {
			return getRuleContext(IfStmtContext.class,0);
		}
		public WhileStmtContext whileStmt() {
			return getRuleContext(WhileStmtContext.class,0);
		}
		public ForStmtContext forStmt() {
			return getRuleContext(ForStmtContext.class,0);
		}
		public ReturnStmtContext returnStmt() {
			return getRuleContext(ReturnStmtContext.class,0);
		}
		public WriteStmtContext writeStmt() {
			return getRuleContext(WriteStmtContext.class,0);
		}
		public CallStmtContext callStmt() {
			return getRuleContext(CallStmtContext.class,0);
		}
		public BlockContext block() {
			return getRuleContext(BlockContext.class,0);
		}
		public TerminalNode SEMI() { return getToken(MOCPParser.SEMI, 0); }
		public StmtContext(ParserRuleContext parent, int invokingState) {
			super(parent, invokingState);
		}
		@Override public int getRuleIndex() { return RULE_stmt; }
	}

	public final StmtContext stmt() throws RecognitionException {
		StmtContext _localctx = new StmtContext(_ctx, getState());
		enterRule(_localctx, 24, RULE_stmt);
		try {
			setState(214);
			_errHandler.sync(this);
			switch ( getInterpreter().adaptivePredict(_input,12,_ctx) ) {
			case 1:
				enterOuterAlt(_localctx, 1);
				{
				setState(205);
				assignStmt();
				}
				break;
			case 2:
				enterOuterAlt(_localctx, 2);
				{
				setState(206);
				ifStmt();
				}
				break;
			case 3:
				enterOuterAlt(_localctx, 3);
				{
				setState(207);
				whileStmt();
				}
				break;
			case 4:
				enterOuterAlt(_localctx, 4);
				{
				setState(208);
				forStmt();
				}
				break;
			case 5:
				enterOuterAlt(_localctx, 5);
				{
				setState(209);
				returnStmt();
				}
				break;
			case 6:
				enterOuterAlt(_localctx, 6);
				{
				setState(210);
				writeStmt();
				}
				break;
			case 7:
				enterOuterAlt(_localctx, 7);
				{
				setState(211);
				callStmt();
				}
				break;
			case 8:
				enterOuterAlt(_localctx, 8);
				{
				setState(212);
				block();
				}
				break;
			case 9:
				enterOuterAlt(_localctx, 9);
				{
				setState(213);
				match(SEMI);
				}
				break;
			}
		}
		catch (RecognitionException re) {
			_localctx.exception = re;
			_errHandler.reportError(this, re);
			_errHandler.recover(this, re);
		}
		finally {
			exitRule();
		}
		return _localctx;
	}

	@SuppressWarnings("CheckReturnValue")
	public static class AssignStmtContext extends ParserRuleContext {
		public LocationContext location() {
			return getRuleContext(LocationContext.class,0);
		}
		public TerminalNode ASSIGN() { return getToken(MOCPParser.ASSIGN, 0); }
		public ExprContext expr() {
			return getRuleContext(ExprContext.class,0);
		}
		public TerminalNode SEMI() { return getToken(MOCPParser.SEMI, 0); }
		public AssignStmtContext(ParserRuleContext parent, int invokingState) {
			super(parent, invokingState);
		}
		@Override public int getRuleIndex() { return RULE_assignStmt; }
	}

	public final AssignStmtContext assignStmt() throws RecognitionException {
		AssignStmtContext _localctx = new AssignStmtContext(_ctx, getState());
		enterRule(_localctx, 26, RULE_assignStmt);
		try {
			enterOuterAlt(_localctx, 1);
			{
			setState(216);
			location();
			setState(217);
			match(ASSIGN);
			setState(218);
			expr();
			setState(219);
			match(SEMI);
			}
		}
		catch (RecognitionException re) {
			_localctx.exception = re;
			_errHandler.reportError(this, re);
			_errHandler.recover(this, re);
		}
		finally {
			exitRule();
		}
		return _localctx;
	}

	@SuppressWarnings("CheckReturnValue")
	public static class IfStmtContext extends ParserRuleContext {
		public TerminalNode SE() { return getToken(MOCPParser.SE, 0); }
		public TerminalNode LPAREN() { return getToken(MOCPParser.LPAREN, 0); }
		public CondExprContext condExpr() {
			return getRuleContext(CondExprContext.class,0);
		}
		public TerminalNode RPAREN() { return getToken(MOCPParser.RPAREN, 0); }
		public List<BlockContext> block() {
			return getRuleContexts(BlockContext.class);
		}
		public BlockContext block(int i) {
			return getRuleContext(BlockContext.class,i);
		}
		public TerminalNode SENAO() { return getToken(MOCPParser.SENAO, 0); }
		public IfStmtContext(ParserRuleContext parent, int invokingState) {
			super(parent, invokingState);
		}
		@Override public int getRuleIndex() { return RULE_ifStmt; }
	}

	public final IfStmtContext ifStmt() throws RecognitionException {
		IfStmtContext _localctx = new IfStmtContext(_ctx, getState());
		enterRule(_localctx, 28, RULE_ifStmt);
		int _la;
		try {
			enterOuterAlt(_localctx, 1);
			{
			setState(221);
			match(SE);
			setState(222);
			match(LPAREN);
			setState(223);
			condExpr();
			setState(224);
			match(RPAREN);
			setState(225);
			block();
			setState(228);
			_errHandler.sync(this);
			_la = _input.LA(1);
			if (_la==SENAO) {
				{
				setState(226);
				match(SENAO);
				setState(227);
				block();
				}
			}

			}
		}
		catch (RecognitionException re) {
			_localctx.exception = re;
			_errHandler.reportError(this, re);
			_errHandler.recover(this, re);
		}
		finally {
			exitRule();
		}
		return _localctx;
	}

	@SuppressWarnings("CheckReturnValue")
	public static class WhileStmtContext extends ParserRuleContext {
		public TerminalNode ENQUANTO() { return getToken(MOCPParser.ENQUANTO, 0); }
		public TerminalNode LPAREN() { return getToken(MOCPParser.LPAREN, 0); }
		public CondExprContext condExpr() {
			return getRuleContext(CondExprContext.class,0);
		}
		public TerminalNode RPAREN() { return getToken(MOCPParser.RPAREN, 0); }
		public BlockContext block() {
			return getRuleContext(BlockContext.class,0);
		}
		public WhileStmtContext(ParserRuleContext parent, int invokingState) {
			super(parent, invokingState);
		}
		@Override public int getRuleIndex() { return RULE_whileStmt; }
	}

	public final WhileStmtContext whileStmt() throws RecognitionException {
		WhileStmtContext _localctx = new WhileStmtContext(_ctx, getState());
		enterRule(_localctx, 30, RULE_whileStmt);
		try {
			enterOuterAlt(_localctx, 1);
			{
			setState(230);
			match(ENQUANTO);
			setState(231);
			match(LPAREN);
			setState(232);
			condExpr();
			setState(233);
			match(RPAREN);
			setState(234);
			block();
			}
		}
		catch (RecognitionException re) {
			_localctx.exception = re;
			_errHandler.reportError(this, re);
			_errHandler.recover(this, re);
		}
		finally {
			exitRule();
		}
		return _localctx;
	}

	@SuppressWarnings("CheckReturnValue")
	public static class ForStmtContext extends ParserRuleContext {
		public TerminalNode PARA() { return getToken(MOCPParser.PARA, 0); }
		public TerminalNode LPAREN() { return getToken(MOCPParser.LPAREN, 0); }
		public List<TerminalNode> SEMI() { return getTokens(MOCPParser.SEMI); }
		public TerminalNode SEMI(int i) {
			return getToken(MOCPParser.SEMI, i);
		}
		public TerminalNode RPAREN() { return getToken(MOCPParser.RPAREN, 0); }
		public BlockContext block() {
			return getRuleContext(BlockContext.class,0);
		}
		public ForInitContext forInit() {
			return getRuleContext(ForInitContext.class,0);
		}
		public ForCondContext forCond() {
			return getRuleContext(ForCondContext.class,0);
		}
		public ForUpdateContext forUpdate() {
			return getRuleContext(ForUpdateContext.class,0);
		}
		public ForStmtContext(ParserRuleContext parent, int invokingState) {
			super(parent, invokingState);
		}
		@Override public int getRuleIndex() { return RULE_forStmt; }
	}

	public final ForStmtContext forStmt() throws RecognitionException {
		ForStmtContext _localctx = new ForStmtContext(_ctx, getState());
		enterRule(_localctx, 32, RULE_forStmt);
		int _la;
		try {
			enterOuterAlt(_localctx, 1);
			{
			setState(236);
			match(PARA);
			setState(237);
			match(LPAREN);
			setState(239);
			_errHandler.sync(this);
			_la = _input.LA(1);
			if (_la==ID) {
				{
				setState(238);
				forInit();
				}
			}

			setState(241);
			match(SEMI);
			setState(243);
			_errHandler.sync(this);
			_la = _input.LA(1);
			if ((((_la) & ~0x3f) == 0 && ((1L << _la) & 148619062581140496L) != 0) || ((((_la - 65)) & ~0x3f) == 0 && ((1L << (_la - 65)) & 23L) != 0)) {
				{
				setState(242);
				forCond();
				}
			}

			setState(245);
			match(SEMI);
			setState(247);
			_errHandler.sync(this);
			_la = _input.LA(1);
			if (_la==ID) {
				{
				setState(246);
				forUpdate();
				}
			}

			setState(249);
			match(RPAREN);
			setState(250);
			block();
			}
		}
		catch (RecognitionException re) {
			_localctx.exception = re;
			_errHandler.reportError(this, re);
			_errHandler.recover(this, re);
		}
		finally {
			exitRule();
		}
		return _localctx;
	}

	@SuppressWarnings("CheckReturnValue")
	public static class ForInitContext extends ParserRuleContext {
		public LocationContext location() {
			return getRuleContext(LocationContext.class,0);
		}
		public TerminalNode ASSIGN() { return getToken(MOCPParser.ASSIGN, 0); }
		public ExprContext expr() {
			return getRuleContext(ExprContext.class,0);
		}
		public ForInitContext(ParserRuleContext parent, int invokingState) {
			super(parent, invokingState);
		}
		@Override public int getRuleIndex() { return RULE_forInit; }
	}

	public final ForInitContext forInit() throws RecognitionException {
		ForInitContext _localctx = new ForInitContext(_ctx, getState());
		enterRule(_localctx, 34, RULE_forInit);
		try {
			enterOuterAlt(_localctx, 1);
			{
			setState(252);
			location();
			setState(253);
			match(ASSIGN);
			setState(254);
			expr();
			}
		}
		catch (RecognitionException re) {
			_localctx.exception = re;
			_errHandler.reportError(this, re);
			_errHandler.recover(this, re);
		}
		finally {
			exitRule();
		}
		return _localctx;
	}

	@SuppressWarnings("CheckReturnValue")
	public static class ForCondContext extends ParserRuleContext {
		public CondExprContext condExpr() {
			return getRuleContext(CondExprContext.class,0);
		}
		public ForCondContext(ParserRuleContext parent, int invokingState) {
			super(parent, invokingState);
		}
		@Override public int getRuleIndex() { return RULE_forCond; }
	}

	public final ForCondContext forCond() throws RecognitionException {
		ForCondContext _localctx = new ForCondContext(_ctx, getState());
		enterRule(_localctx, 36, RULE_forCond);
		try {
			enterOuterAlt(_localctx, 1);
			{
			setState(256);
			condExpr();
			}
		}
		catch (RecognitionException re) {
			_localctx.exception = re;
			_errHandler.reportError(this, re);
			_errHandler.recover(this, re);
		}
		finally {
			exitRule();
		}
		return _localctx;
	}

	@SuppressWarnings("CheckReturnValue")
	public static class ForUpdateContext extends ParserRuleContext {
		public LocationContext location() {
			return getRuleContext(LocationContext.class,0);
		}
		public TerminalNode ASSIGN() { return getToken(MOCPParser.ASSIGN, 0); }
		public ExprContext expr() {
			return getRuleContext(ExprContext.class,0);
		}
		public ForUpdateContext(ParserRuleContext parent, int invokingState) {
			super(parent, invokingState);
		}
		@Override public int getRuleIndex() { return RULE_forUpdate; }
	}

	public final ForUpdateContext forUpdate() throws RecognitionException {
		ForUpdateContext _localctx = new ForUpdateContext(_ctx, getState());
		enterRule(_localctx, 38, RULE_forUpdate);
		try {
			enterOuterAlt(_localctx, 1);
			{
			setState(258);
			location();
			setState(259);
			match(ASSIGN);
			setState(260);
			expr();
			}
		}
		catch (RecognitionException re) {
			_localctx.exception = re;
			_errHandler.reportError(this, re);
			_errHandler.recover(this, re);
		}
		finally {
			exitRule();
		}
		return _localctx;
	}

	@SuppressWarnings("CheckReturnValue")
	public static class ReturnStmtContext extends ParserRuleContext {
		public TerminalNode RETORNAR() { return getToken(MOCPParser.RETORNAR, 0); }
		public TerminalNode SEMI() { return getToken(MOCPParser.SEMI, 0); }
		public ExprContext expr() {
			return getRuleContext(ExprContext.class,0);
		}
		public ReturnStmtContext(ParserRuleContext parent, int invokingState) {
			super(parent, invokingState);
		}
		@Override public int getRuleIndex() { return RULE_returnStmt; }
	}

	public final ReturnStmtContext returnStmt() throws RecognitionException {
		ReturnStmtContext _localctx = new ReturnStmtContext(_ctx, getState());
		enterRule(_localctx, 40, RULE_returnStmt);
		int _la;
		try {
			enterOuterAlt(_localctx, 1);
			{
			setState(262);
			match(RETORNAR);
			setState(264);
			_errHandler.sync(this);
			_la = _input.LA(1);
			if ((((_la) & ~0x3f) == 0 && ((1L << _la) & 148618787703233552L) != 0) || ((((_la - 65)) & ~0x3f) == 0 && ((1L << (_la - 65)) & 23L) != 0)) {
				{
				setState(263);
				expr();
				}
			}

			setState(266);
			match(SEMI);
			}
		}
		catch (RecognitionException re) {
			_localctx.exception = re;
			_errHandler.reportError(this, re);
			_errHandler.recover(this, re);
		}
		finally {
			exitRule();
		}
		return _localctx;
	}

	@SuppressWarnings("CheckReturnValue")
	public static class CallStmtContext extends ParserRuleContext {
		public UserFunctionCallContext userFunctionCall() {
			return getRuleContext(UserFunctionCallContext.class,0);
		}
		public TerminalNode SEMI() { return getToken(MOCPParser.SEMI, 0); }
		public CallStmtContext(ParserRuleContext parent, int invokingState) {
			super(parent, invokingState);
		}
		@Override public int getRuleIndex() { return RULE_callStmt; }
	}

	public final CallStmtContext callStmt() throws RecognitionException {
		CallStmtContext _localctx = new CallStmtContext(_ctx, getState());
		enterRule(_localctx, 42, RULE_callStmt);
		try {
			enterOuterAlt(_localctx, 1);
			{
			setState(268);
			userFunctionCall();
			setState(269);
			match(SEMI);
			}
		}
		catch (RecognitionException re) {
			_localctx.exception = re;
			_errHandler.reportError(this, re);
			_errHandler.recover(this, re);
		}
		finally {
			exitRule();
		}
		return _localctx;
	}

	@SuppressWarnings("CheckReturnValue")
	public static class WriteStmtContext extends ParserRuleContext {
		public TerminalNode ESCREVER() { return getToken(MOCPParser.ESCREVER, 0); }
		public TerminalNode LPAREN() { return getToken(MOCPParser.LPAREN, 0); }
		public ExprContext expr() {
			return getRuleContext(ExprContext.class,0);
		}
		public TerminalNode RPAREN() { return getToken(MOCPParser.RPAREN, 0); }
		public TerminalNode SEMI() { return getToken(MOCPParser.SEMI, 0); }
		public TerminalNode ESCREVERC() { return getToken(MOCPParser.ESCREVERC, 0); }
		public TerminalNode ESCREVERS() { return getToken(MOCPParser.ESCREVERS, 0); }
		public TerminalNode ESCREVERV() { return getToken(MOCPParser.ESCREVERV, 0); }
		public TerminalNode ID() { return getToken(MOCPParser.ID, 0); }
		public WriteStmtContext(ParserRuleContext parent, int invokingState) {
			super(parent, invokingState);
		}
		@Override public int getRuleIndex() { return RULE_writeStmt; }
	}

	public final WriteStmtContext writeStmt() throws RecognitionException {
		WriteStmtContext _localctx = new WriteStmtContext(_ctx, getState());
		enterRule(_localctx, 44, RULE_writeStmt);
		try {
			setState(294);
			_errHandler.sync(this);
			switch (_input.LA(1)) {
			case ESCREVER:
				enterOuterAlt(_localctx, 1);
				{
				setState(271);
				match(ESCREVER);
				setState(272);
				match(LPAREN);
				setState(273);
				expr();
				setState(274);
				match(RPAREN);
				setState(275);
				match(SEMI);
				}
				break;
			case ESCREVERC:
				enterOuterAlt(_localctx, 2);
				{
				setState(277);
				match(ESCREVERC);
				setState(278);
				match(LPAREN);
				setState(279);
				expr();
				setState(280);
				match(RPAREN);
				setState(281);
				match(SEMI);
				}
				break;
			case ESCREVERS:
				enterOuterAlt(_localctx, 3);
				{
				setState(283);
				match(ESCREVERS);
				setState(284);
				match(LPAREN);
				setState(285);
				expr();
				setState(286);
				match(RPAREN);
				setState(287);
				match(SEMI);
				}
				break;
			case ESCREVERV:
				enterOuterAlt(_localctx, 4);
				{
				setState(289);
				match(ESCREVERV);
				setState(290);
				match(LPAREN);
				setState(291);
				match(ID);
				setState(292);
				match(RPAREN);
				setState(293);
				match(SEMI);
				}
				break;
			default:
				throw new NoViableAltException(this);
			}
		}
		catch (RecognitionException re) {
			_localctx.exception = re;
			_errHandler.reportError(this, re);
			_errHandler.recover(this, re);
		}
		finally {
			exitRule();
		}
		return _localctx;
	}

	@SuppressWarnings("CheckReturnValue")
	public static class CondExprContext extends ParserRuleContext {
		public LogicalOrExprContext logicalOrExpr() {
			return getRuleContext(LogicalOrExprContext.class,0);
		}
		public CondExprContext(ParserRuleContext parent, int invokingState) {
			super(parent, invokingState);
		}
		@Override public int getRuleIndex() { return RULE_condExpr; }
	}

	public final CondExprContext condExpr() throws RecognitionException {
		CondExprContext _localctx = new CondExprContext(_ctx, getState());
		enterRule(_localctx, 46, RULE_condExpr);
		try {
			enterOuterAlt(_localctx, 1);
			{
			setState(296);
			logicalOrExpr();
			}
		}
		catch (RecognitionException re) {
			_localctx.exception = re;
			_errHandler.reportError(this, re);
			_errHandler.recover(this, re);
		}
		finally {
			exitRule();
		}
		return _localctx;
	}

	@SuppressWarnings("CheckReturnValue")
	public static class LogicalOrExprContext extends ParserRuleContext {
		public List<LogicalAndExprContext> logicalAndExpr() {
			return getRuleContexts(LogicalAndExprContext.class);
		}
		public LogicalAndExprContext logicalAndExpr(int i) {
			return getRuleContext(LogicalAndExprContext.class,i);
		}
		public List<TerminalNode> OR() { return getTokens(MOCPParser.OR); }
		public TerminalNode OR(int i) {
			return getToken(MOCPParser.OR, i);
		}
		public LogicalOrExprContext(ParserRuleContext parent, int invokingState) {
			super(parent, invokingState);
		}
		@Override public int getRuleIndex() { return RULE_logicalOrExpr; }
	}

	public final LogicalOrExprContext logicalOrExpr() throws RecognitionException {
		LogicalOrExprContext _localctx = new LogicalOrExprContext(_ctx, getState());
		enterRule(_localctx, 48, RULE_logicalOrExpr);
		int _la;
		try {
			enterOuterAlt(_localctx, 1);
			{
			setState(298);
			logicalAndExpr();
			setState(303);
			_errHandler.sync(this);
			_la = _input.LA(1);
			while (_la==OR) {
				{
				{
				setState(299);
				match(OR);
				setState(300);
				logicalAndExpr();
				}
				}
				setState(305);
				_errHandler.sync(this);
				_la = _input.LA(1);
			}
			}
		}
		catch (RecognitionException re) {
			_localctx.exception = re;
			_errHandler.reportError(this, re);
			_errHandler.recover(this, re);
		}
		finally {
			exitRule();
		}
		return _localctx;
	}

	@SuppressWarnings("CheckReturnValue")
	public static class LogicalAndExprContext extends ParserRuleContext {
		public List<LogicalNotExprContext> logicalNotExpr() {
			return getRuleContexts(LogicalNotExprContext.class);
		}
		public LogicalNotExprContext logicalNotExpr(int i) {
			return getRuleContext(LogicalNotExprContext.class,i);
		}
		public List<TerminalNode> AND() { return getTokens(MOCPParser.AND); }
		public TerminalNode AND(int i) {
			return getToken(MOCPParser.AND, i);
		}
		public LogicalAndExprContext(ParserRuleContext parent, int invokingState) {
			super(parent, invokingState);
		}
		@Override public int getRuleIndex() { return RULE_logicalAndExpr; }
	}

	public final LogicalAndExprContext logicalAndExpr() throws RecognitionException {
		LogicalAndExprContext _localctx = new LogicalAndExprContext(_ctx, getState());
		enterRule(_localctx, 50, RULE_logicalAndExpr);
		int _la;
		try {
			enterOuterAlt(_localctx, 1);
			{
			setState(306);
			logicalNotExpr();
			setState(311);
			_errHandler.sync(this);
			_la = _input.LA(1);
			while (_la==AND) {
				{
				{
				setState(307);
				match(AND);
				setState(308);
				logicalNotExpr();
				}
				}
				setState(313);
				_errHandler.sync(this);
				_la = _input.LA(1);
			}
			}
		}
		catch (RecognitionException re) {
			_localctx.exception = re;
			_errHandler.reportError(this, re);
			_errHandler.recover(this, re);
		}
		finally {
			exitRule();
		}
		return _localctx;
	}

	@SuppressWarnings("CheckReturnValue")
	public static class LogicalNotExprContext extends ParserRuleContext {
		public TerminalNode NOT() { return getToken(MOCPParser.NOT, 0); }
		public LogicalNotExprContext logicalNotExpr() {
			return getRuleContext(LogicalNotExprContext.class,0);
		}
		public RelationalExprContext relationalExpr() {
			return getRuleContext(RelationalExprContext.class,0);
		}
		public LogicalNotExprContext(ParserRuleContext parent, int invokingState) {
			super(parent, invokingState);
		}
		@Override public int getRuleIndex() { return RULE_logicalNotExpr; }
	}

	public final LogicalNotExprContext logicalNotExpr() throws RecognitionException {
		LogicalNotExprContext _localctx = new LogicalNotExprContext(_ctx, getState());
		enterRule(_localctx, 52, RULE_logicalNotExpr);
		try {
			setState(317);
			_errHandler.sync(this);
			switch (_input.LA(1)) {
			case NOT:
				enterOuterAlt(_localctx, 1);
				{
				setState(314);
				match(NOT);
				setState(315);
				logicalNotExpr();
				}
				break;
			case PRINCIPAL:
			case LER:
			case LERC:
			case LERS:
			case MINUS:
			case LPAREN:
			case REAL_LITERAL:
			case INT_LITERAL:
			case STRING_LITERAL:
			case ID:
				enterOuterAlt(_localctx, 2);
				{
				setState(316);
				relationalExpr();
				}
				break;
			default:
				throw new NoViableAltException(this);
			}
		}
		catch (RecognitionException re) {
			_localctx.exception = re;
			_errHandler.reportError(this, re);
			_errHandler.recover(this, re);
		}
		finally {
			exitRule();
		}
		return _localctx;
	}

	@SuppressWarnings("CheckReturnValue")
	public static class RelationalExprContext extends ParserRuleContext {
		public List<ExprContext> expr() {
			return getRuleContexts(ExprContext.class);
		}
		public ExprContext expr(int i) {
			return getRuleContext(ExprContext.class,i);
		}
		public RelOpContext relOp() {
			return getRuleContext(RelOpContext.class,0);
		}
		public TerminalNode LPAREN() { return getToken(MOCPParser.LPAREN, 0); }
		public CondExprContext condExpr() {
			return getRuleContext(CondExprContext.class,0);
		}
		public TerminalNode RPAREN() { return getToken(MOCPParser.RPAREN, 0); }
		public RelationalExprContext(ParserRuleContext parent, int invokingState) {
			super(parent, invokingState);
		}
		@Override public int getRuleIndex() { return RULE_relationalExpr; }
	}

	public final RelationalExprContext relationalExpr() throws RecognitionException {
		RelationalExprContext _localctx = new RelationalExprContext(_ctx, getState());
		enterRule(_localctx, 54, RULE_relationalExpr);
		int _la;
		try {
			setState(329);
			_errHandler.sync(this);
			switch ( getInterpreter().adaptivePredict(_input,23,_ctx) ) {
			case 1:
				enterOuterAlt(_localctx, 1);
				{
				setState(319);
				expr();
				setState(323);
				_errHandler.sync(this);
				_la = _input.LA(1);
				if ((((_la) & ~0x3f) == 0 && ((1L << _la) & 34634616274944L) != 0)) {
					{
					setState(320);
					relOp();
					setState(321);
					expr();
					}
				}

				}
				break;
			case 2:
				enterOuterAlt(_localctx, 2);
				{
				setState(325);
				match(LPAREN);
				setState(326);
				condExpr();
				setState(327);
				match(RPAREN);
				}
				break;
			}
		}
		catch (RecognitionException re) {
			_localctx.exception = re;
			_errHandler.reportError(this, re);
			_errHandler.recover(this, re);
		}
		finally {
			exitRule();
		}
		return _localctx;
	}

	@SuppressWarnings("CheckReturnValue")
	public static class RelOpContext extends ParserRuleContext {
		public TerminalNode LT() { return getToken(MOCPParser.LT, 0); }
		public TerminalNode LE() { return getToken(MOCPParser.LE, 0); }
		public TerminalNode GT() { return getToken(MOCPParser.GT, 0); }
		public TerminalNode GE() { return getToken(MOCPParser.GE, 0); }
		public TerminalNode EQ() { return getToken(MOCPParser.EQ, 0); }
		public TerminalNode NE() { return getToken(MOCPParser.NE, 0); }
		public RelOpContext(ParserRuleContext parent, int invokingState) {
			super(parent, invokingState);
		}
		@Override public int getRuleIndex() { return RULE_relOp; }
	}

	public final RelOpContext relOp() throws RecognitionException {
		RelOpContext _localctx = new RelOpContext(_ctx, getState());
		enterRule(_localctx, 56, RULE_relOp);
		int _la;
		try {
			enterOuterAlt(_localctx, 1);
			{
			setState(331);
			_la = _input.LA(1);
			if ( !((((_la) & ~0x3f) == 0 && ((1L << _la) & 34634616274944L) != 0)) ) {
			_errHandler.recoverInline(this);
			}
			else {
				if ( _input.LA(1)==Token.EOF ) matchedEOF = true;
				_errHandler.reportMatch(this);
				consume();
			}
			}
		}
		catch (RecognitionException re) {
			_localctx.exception = re;
			_errHandler.reportError(this, re);
			_errHandler.recover(this, re);
		}
		finally {
			exitRule();
		}
		return _localctx;
	}

	@SuppressWarnings("CheckReturnValue")
	public static class ExprContext extends ParserRuleContext {
		public AdditiveExprContext additiveExpr() {
			return getRuleContext(AdditiveExprContext.class,0);
		}
		public ExprContext(ParserRuleContext parent, int invokingState) {
			super(parent, invokingState);
		}
		@Override public int getRuleIndex() { return RULE_expr; }
	}

	public final ExprContext expr() throws RecognitionException {
		ExprContext _localctx = new ExprContext(_ctx, getState());
		enterRule(_localctx, 58, RULE_expr);
		try {
			enterOuterAlt(_localctx, 1);
			{
			setState(333);
			additiveExpr();
			}
		}
		catch (RecognitionException re) {
			_localctx.exception = re;
			_errHandler.reportError(this, re);
			_errHandler.recover(this, re);
		}
		finally {
			exitRule();
		}
		return _localctx;
	}

	@SuppressWarnings("CheckReturnValue")
	public static class AdditiveExprContext extends ParserRuleContext {
		public List<MultiplicativeExprContext> multiplicativeExpr() {
			return getRuleContexts(MultiplicativeExprContext.class);
		}
		public MultiplicativeExprContext multiplicativeExpr(int i) {
			return getRuleContext(MultiplicativeExprContext.class,i);
		}
		public List<TerminalNode> PLUS() { return getTokens(MOCPParser.PLUS); }
		public TerminalNode PLUS(int i) {
			return getToken(MOCPParser.PLUS, i);
		}
		public List<TerminalNode> MINUS() { return getTokens(MOCPParser.MINUS); }
		public TerminalNode MINUS(int i) {
			return getToken(MOCPParser.MINUS, i);
		}
		public AdditiveExprContext(ParserRuleContext parent, int invokingState) {
			super(parent, invokingState);
		}
		@Override public int getRuleIndex() { return RULE_additiveExpr; }
	}

	public final AdditiveExprContext additiveExpr() throws RecognitionException {
		AdditiveExprContext _localctx = new AdditiveExprContext(_ctx, getState());
		enterRule(_localctx, 60, RULE_additiveExpr);
		int _la;
		try {
			enterOuterAlt(_localctx, 1);
			{
			setState(335);
			multiplicativeExpr();
			setState(340);
			_errHandler.sync(this);
			_la = _input.LA(1);
			while (_la==PLUS || _la==MINUS) {
				{
				{
				setState(336);
				_la = _input.LA(1);
				if ( !(_la==PLUS || _la==MINUS) ) {
				_errHandler.recoverInline(this);
				}
				else {
					if ( _input.LA(1)==Token.EOF ) matchedEOF = true;
					_errHandler.reportMatch(this);
					consume();
				}
				setState(337);
				multiplicativeExpr();
				}
				}
				setState(342);
				_errHandler.sync(this);
				_la = _input.LA(1);
			}
			}
		}
		catch (RecognitionException re) {
			_localctx.exception = re;
			_errHandler.reportError(this, re);
			_errHandler.recover(this, re);
		}
		finally {
			exitRule();
		}
		return _localctx;
	}

	@SuppressWarnings("CheckReturnValue")
	public static class MultiplicativeExprContext extends ParserRuleContext {
		public List<UnaryExprContext> unaryExpr() {
			return getRuleContexts(UnaryExprContext.class);
		}
		public UnaryExprContext unaryExpr(int i) {
			return getRuleContext(UnaryExprContext.class,i);
		}
		public List<TerminalNode> MUL() { return getTokens(MOCPParser.MUL); }
		public TerminalNode MUL(int i) {
			return getToken(MOCPParser.MUL, i);
		}
		public List<TerminalNode> DIV() { return getTokens(MOCPParser.DIV); }
		public TerminalNode DIV(int i) {
			return getToken(MOCPParser.DIV, i);
		}
		public List<TerminalNode> MOD() { return getTokens(MOCPParser.MOD); }
		public TerminalNode MOD(int i) {
			return getToken(MOCPParser.MOD, i);
		}
		public MultiplicativeExprContext(ParserRuleContext parent, int invokingState) {
			super(parent, invokingState);
		}
		@Override public int getRuleIndex() { return RULE_multiplicativeExpr; }
	}

	public final MultiplicativeExprContext multiplicativeExpr() throws RecognitionException {
		MultiplicativeExprContext _localctx = new MultiplicativeExprContext(_ctx, getState());
		enterRule(_localctx, 62, RULE_multiplicativeExpr);
		int _la;
		try {
			enterOuterAlt(_localctx, 1);
			{
			setState(343);
			unaryExpr();
			setState(348);
			_errHandler.sync(this);
			_la = _input.LA(1);
			while ((((_la) & ~0x3f) == 0 && ((1L << _la) & 63050394783186944L) != 0)) {
				{
				{
				setState(344);
				_la = _input.LA(1);
				if ( !((((_la) & ~0x3f) == 0 && ((1L << _la) & 63050394783186944L) != 0)) ) {
				_errHandler.recoverInline(this);
				}
				else {
					if ( _input.LA(1)==Token.EOF ) matchedEOF = true;
					_errHandler.reportMatch(this);
					consume();
				}
				setState(345);
				unaryExpr();
				}
				}
				setState(350);
				_errHandler.sync(this);
				_la = _input.LA(1);
			}
			}
		}
		catch (RecognitionException re) {
			_localctx.exception = re;
			_errHandler.reportError(this, re);
			_errHandler.recover(this, re);
		}
		finally {
			exitRule();
		}
		return _localctx;
	}

	@SuppressWarnings("CheckReturnValue")
	public static class UnaryExprContext extends ParserRuleContext {
		public TerminalNode MINUS() { return getToken(MOCPParser.MINUS, 0); }
		public UnaryExprContext unaryExpr() {
			return getRuleContext(UnaryExprContext.class,0);
		}
		public CastExprContext castExpr() {
			return getRuleContext(CastExprContext.class,0);
		}
		public UnaryExprContext(ParserRuleContext parent, int invokingState) {
			super(parent, invokingState);
		}
		@Override public int getRuleIndex() { return RULE_unaryExpr; }
	}

	public final UnaryExprContext unaryExpr() throws RecognitionException {
		UnaryExprContext _localctx = new UnaryExprContext(_ctx, getState());
		enterRule(_localctx, 64, RULE_unaryExpr);
		try {
			setState(354);
			_errHandler.sync(this);
			switch (_input.LA(1)) {
			case MINUS:
				enterOuterAlt(_localctx, 1);
				{
				setState(351);
				match(MINUS);
				setState(352);
				unaryExpr();
				}
				break;
			case PRINCIPAL:
			case LER:
			case LERC:
			case LERS:
			case LPAREN:
			case REAL_LITERAL:
			case INT_LITERAL:
			case STRING_LITERAL:
			case ID:
				enterOuterAlt(_localctx, 2);
				{
				setState(353);
				castExpr();
				}
				break;
			default:
				throw new NoViableAltException(this);
			}
		}
		catch (RecognitionException re) {
			_localctx.exception = re;
			_errHandler.reportError(this, re);
			_errHandler.recover(this, re);
		}
		finally {
			exitRule();
		}
		return _localctx;
	}

	@SuppressWarnings("CheckReturnValue")
	public static class CastExprContext extends ParserRuleContext {
		public TerminalNode LPAREN() { return getToken(MOCPParser.LPAREN, 0); }
		public CastTypeContext castType() {
			return getRuleContext(CastTypeContext.class,0);
		}
		public TerminalNode RPAREN() { return getToken(MOCPParser.RPAREN, 0); }
		public UnaryExprContext unaryExpr() {
			return getRuleContext(UnaryExprContext.class,0);
		}
		public PrimaryExprContext primaryExpr() {
			return getRuleContext(PrimaryExprContext.class,0);
		}
		public CastExprContext(ParserRuleContext parent, int invokingState) {
			super(parent, invokingState);
		}
		@Override public int getRuleIndex() { return RULE_castExpr; }
	}

	public final CastExprContext castExpr() throws RecognitionException {
		CastExprContext _localctx = new CastExprContext(_ctx, getState());
		enterRule(_localctx, 66, RULE_castExpr);
		try {
			setState(362);
			_errHandler.sync(this);
			switch ( getInterpreter().adaptivePredict(_input,27,_ctx) ) {
			case 1:
				enterOuterAlt(_localctx, 1);
				{
				setState(356);
				match(LPAREN);
				setState(357);
				castType();
				setState(358);
				match(RPAREN);
				setState(359);
				unaryExpr();
				}
				break;
			case 2:
				enterOuterAlt(_localctx, 2);
				{
				setState(361);
				primaryExpr();
				}
				break;
			}
		}
		catch (RecognitionException re) {
			_localctx.exception = re;
			_errHandler.reportError(this, re);
			_errHandler.recover(this, re);
		}
		finally {
			exitRule();
		}
		return _localctx;
	}

	@SuppressWarnings("CheckReturnValue")
	public static class PrimaryExprContext extends ParserRuleContext {
		public LocationContext location() {
			return getRuleContext(LocationContext.class,0);
		}
		public InputCallContext inputCall() {
			return getRuleContext(InputCallContext.class,0);
		}
		public UserFunctionCallContext userFunctionCall() {
			return getRuleContext(UserFunctionCallContext.class,0);
		}
		public LiteralContext literal() {
			return getRuleContext(LiteralContext.class,0);
		}
		public TerminalNode LPAREN() { return getToken(MOCPParser.LPAREN, 0); }
		public ExprContext expr() {
			return getRuleContext(ExprContext.class,0);
		}
		public TerminalNode RPAREN() { return getToken(MOCPParser.RPAREN, 0); }
		public PrimaryExprContext(ParserRuleContext parent, int invokingState) {
			super(parent, invokingState);
		}
		@Override public int getRuleIndex() { return RULE_primaryExpr; }
	}

	public final PrimaryExprContext primaryExpr() throws RecognitionException {
		PrimaryExprContext _localctx = new PrimaryExprContext(_ctx, getState());
		enterRule(_localctx, 68, RULE_primaryExpr);
		try {
			setState(372);
			_errHandler.sync(this);
			switch ( getInterpreter().adaptivePredict(_input,28,_ctx) ) {
			case 1:
				enterOuterAlt(_localctx, 1);
				{
				setState(364);
				location();
				}
				break;
			case 2:
				enterOuterAlt(_localctx, 2);
				{
				setState(365);
				inputCall();
				}
				break;
			case 3:
				enterOuterAlt(_localctx, 3);
				{
				setState(366);
				userFunctionCall();
				}
				break;
			case 4:
				enterOuterAlt(_localctx, 4);
				{
				setState(367);
				literal();
				}
				break;
			case 5:
				enterOuterAlt(_localctx, 5);
				{
				setState(368);
				match(LPAREN);
				setState(369);
				expr();
				setState(370);
				match(RPAREN);
				}
				break;
			}
		}
		catch (RecognitionException re) {
			_localctx.exception = re;
			_errHandler.reportError(this, re);
			_errHandler.recover(this, re);
		}
		finally {
			exitRule();
		}
		return _localctx;
	}

	@SuppressWarnings("CheckReturnValue")
	public static class LocationContext extends ParserRuleContext {
		public TerminalNode ID() { return getToken(MOCPParser.ID, 0); }
		public TerminalNode LBRACK() { return getToken(MOCPParser.LBRACK, 0); }
		public ExprContext expr() {
			return getRuleContext(ExprContext.class,0);
		}
		public TerminalNode RBRACK() { return getToken(MOCPParser.RBRACK, 0); }
		public LocationContext(ParserRuleContext parent, int invokingState) {
			super(parent, invokingState);
		}
		@Override public int getRuleIndex() { return RULE_location; }
	}

	public final LocationContext location() throws RecognitionException {
		LocationContext _localctx = new LocationContext(_ctx, getState());
		enterRule(_localctx, 70, RULE_location);
		try {
			setState(380);
			_errHandler.sync(this);
			switch ( getInterpreter().adaptivePredict(_input,29,_ctx) ) {
			case 1:
				enterOuterAlt(_localctx, 1);
				{
				setState(374);
				match(ID);
				}
				break;
			case 2:
				enterOuterAlt(_localctx, 2);
				{
				setState(375);
				match(ID);
				setState(376);
				match(LBRACK);
				setState(377);
				expr();
				setState(378);
				match(RBRACK);
				}
				break;
			}
		}
		catch (RecognitionException re) {
			_localctx.exception = re;
			_errHandler.reportError(this, re);
			_errHandler.recover(this, re);
		}
		finally {
			exitRule();
		}
		return _localctx;
	}

	@SuppressWarnings("CheckReturnValue")
	public static class InputCallContext extends ParserRuleContext {
		public TerminalNode LER() { return getToken(MOCPParser.LER, 0); }
		public TerminalNode LPAREN() { return getToken(MOCPParser.LPAREN, 0); }
		public TerminalNode RPAREN() { return getToken(MOCPParser.RPAREN, 0); }
		public TerminalNode LERC() { return getToken(MOCPParser.LERC, 0); }
		public TerminalNode LERS() { return getToken(MOCPParser.LERS, 0); }
		public InputCallContext(ParserRuleContext parent, int invokingState) {
			super(parent, invokingState);
		}
		@Override public int getRuleIndex() { return RULE_inputCall; }
	}

	public final InputCallContext inputCall() throws RecognitionException {
		InputCallContext _localctx = new InputCallContext(_ctx, getState());
		enterRule(_localctx, 72, RULE_inputCall);
		try {
			setState(391);
			_errHandler.sync(this);
			switch (_input.LA(1)) {
			case LER:
				enterOuterAlt(_localctx, 1);
				{
				setState(382);
				match(LER);
				setState(383);
				match(LPAREN);
				setState(384);
				match(RPAREN);
				}
				break;
			case LERC:
				enterOuterAlt(_localctx, 2);
				{
				setState(385);
				match(LERC);
				setState(386);
				match(LPAREN);
				setState(387);
				match(RPAREN);
				}
				break;
			case LERS:
				enterOuterAlt(_localctx, 3);
				{
				setState(388);
				match(LERS);
				setState(389);
				match(LPAREN);
				setState(390);
				match(RPAREN);
				}
				break;
			default:
				throw new NoViableAltException(this);
			}
		}
		catch (RecognitionException re) {
			_localctx.exception = re;
			_errHandler.reportError(this, re);
			_errHandler.recover(this, re);
		}
		finally {
			exitRule();
		}
		return _localctx;
	}

	@SuppressWarnings("CheckReturnValue")
	public static class UserFunctionCallContext extends ParserRuleContext {
		public FunctionNameContext functionName() {
			return getRuleContext(FunctionNameContext.class,0);
		}
		public TerminalNode LPAREN() { return getToken(MOCPParser.LPAREN, 0); }
		public TerminalNode RPAREN() { return getToken(MOCPParser.RPAREN, 0); }
		public ArgListContext argList() {
			return getRuleContext(ArgListContext.class,0);
		}
		public UserFunctionCallContext(ParserRuleContext parent, int invokingState) {
			super(parent, invokingState);
		}
		@Override public int getRuleIndex() { return RULE_userFunctionCall; }
	}

	public final UserFunctionCallContext userFunctionCall() throws RecognitionException {
		UserFunctionCallContext _localctx = new UserFunctionCallContext(_ctx, getState());
		enterRule(_localctx, 74, RULE_userFunctionCall);
		int _la;
		try {
			enterOuterAlt(_localctx, 1);
			{
			setState(393);
			functionName();
			setState(394);
			match(LPAREN);
			setState(396);
			_errHandler.sync(this);
			_la = _input.LA(1);
			if ((((_la) & ~0x3f) == 0 && ((1L << _la) & 148618787703233552L) != 0) || ((((_la - 65)) & ~0x3f) == 0 && ((1L << (_la - 65)) & 23L) != 0)) {
				{
				setState(395);
				argList();
				}
			}

			setState(398);
			match(RPAREN);
			}
		}
		catch (RecognitionException re) {
			_localctx.exception = re;
			_errHandler.reportError(this, re);
			_errHandler.recover(this, re);
		}
		finally {
			exitRule();
		}
		return _localctx;
	}

	@SuppressWarnings("CheckReturnValue")
	public static class ArgListContext extends ParserRuleContext {
		public List<ExprContext> expr() {
			return getRuleContexts(ExprContext.class);
		}
		public ExprContext expr(int i) {
			return getRuleContext(ExprContext.class,i);
		}
		public List<TerminalNode> COMMA() { return getTokens(MOCPParser.COMMA); }
		public TerminalNode COMMA(int i) {
			return getToken(MOCPParser.COMMA, i);
		}
		public ArgListContext(ParserRuleContext parent, int invokingState) {
			super(parent, invokingState);
		}
		@Override public int getRuleIndex() { return RULE_argList; }
	}

	public final ArgListContext argList() throws RecognitionException {
		ArgListContext _localctx = new ArgListContext(_ctx, getState());
		enterRule(_localctx, 76, RULE_argList);
		int _la;
		try {
			enterOuterAlt(_localctx, 1);
			{
			setState(400);
			expr();
			setState(405);
			_errHandler.sync(this);
			_la = _input.LA(1);
			while (_la==COMMA) {
				{
				{
				setState(401);
				match(COMMA);
				setState(402);
				expr();
				}
				}
				setState(407);
				_errHandler.sync(this);
				_la = _input.LA(1);
			}
			}
		}
		catch (RecognitionException re) {
			_localctx.exception = re;
			_errHandler.reportError(this, re);
			_errHandler.recover(this, re);
		}
		finally {
			exitRule();
		}
		return _localctx;
	}

	@SuppressWarnings("CheckReturnValue")
	public static class LiteralContext extends ParserRuleContext {
		public TerminalNode INT_LITERAL() { return getToken(MOCPParser.INT_LITERAL, 0); }
		public TerminalNode REAL_LITERAL() { return getToken(MOCPParser.REAL_LITERAL, 0); }
		public TerminalNode STRING_LITERAL() { return getToken(MOCPParser.STRING_LITERAL, 0); }
		public LiteralContext(ParserRuleContext parent, int invokingState) {
			super(parent, invokingState);
		}
		@Override public int getRuleIndex() { return RULE_literal; }
	}

	public final LiteralContext literal() throws RecognitionException {
		LiteralContext _localctx = new LiteralContext(_ctx, getState());
		enterRule(_localctx, 78, RULE_literal);
		int _la;
		try {
			enterOuterAlt(_localctx, 1);
			{
			setState(408);
			_la = _input.LA(1);
			if ( !(((((_la - 65)) & ~0x3f) == 0 && ((1L << (_la - 65)) & 7L) != 0)) ) {
			_errHandler.recoverInline(this);
			}
			else {
				if ( _input.LA(1)==Token.EOF ) matchedEOF = true;
				_errHandler.reportMatch(this);
				consume();
			}
			}
		}
		catch (RecognitionException re) {
			_localctx.exception = re;
			_errHandler.reportError(this, re);
			_errHandler.recover(this, re);
		}
		finally {
			exitRule();
		}
		return _localctx;
	}

	@SuppressWarnings("CheckReturnValue")
	public static class ReturnTypeContext extends ParserRuleContext {
		public TerminalNode INTEIRO() { return getToken(MOCPParser.INTEIRO, 0); }
		public TerminalNode REAL() { return getToken(MOCPParser.REAL, 0); }
		public TerminalNode VAZIO() { return getToken(MOCPParser.VAZIO, 0); }
		public ReturnTypeContext(ParserRuleContext parent, int invokingState) {
			super(parent, invokingState);
		}
		@Override public int getRuleIndex() { return RULE_returnType; }
	}

	public final ReturnTypeContext returnType() throws RecognitionException {
		ReturnTypeContext _localctx = new ReturnTypeContext(_ctx, getState());
		enterRule(_localctx, 80, RULE_returnType);
		int _la;
		try {
			enterOuterAlt(_localctx, 1);
			{
			setState(410);
			_la = _input.LA(1);
			if ( !((((_la) & ~0x3f) == 0 && ((1L << _la) & 14L) != 0)) ) {
			_errHandler.recoverInline(this);
			}
			else {
				if ( _input.LA(1)==Token.EOF ) matchedEOF = true;
				_errHandler.reportMatch(this);
				consume();
			}
			}
		}
		catch (RecognitionException re) {
			_localctx.exception = re;
			_errHandler.reportError(this, re);
			_errHandler.recover(this, re);
		}
		finally {
			exitRule();
		}
		return _localctx;
	}

	@SuppressWarnings("CheckReturnValue")
	public static class VarTypeContext extends ParserRuleContext {
		public TerminalNode INTEIRO() { return getToken(MOCPParser.INTEIRO, 0); }
		public TerminalNode REAL() { return getToken(MOCPParser.REAL, 0); }
		public VarTypeContext(ParserRuleContext parent, int invokingState) {
			super(parent, invokingState);
		}
		@Override public int getRuleIndex() { return RULE_varType; }
	}

	public final VarTypeContext varType() throws RecognitionException {
		VarTypeContext _localctx = new VarTypeContext(_ctx, getState());
		enterRule(_localctx, 82, RULE_varType);
		int _la;
		try {
			enterOuterAlt(_localctx, 1);
			{
			setState(412);
			_la = _input.LA(1);
			if ( !(_la==INTEIRO || _la==REAL) ) {
			_errHandler.recoverInline(this);
			}
			else {
				if ( _input.LA(1)==Token.EOF ) matchedEOF = true;
				_errHandler.reportMatch(this);
				consume();
			}
			}
		}
		catch (RecognitionException re) {
			_localctx.exception = re;
			_errHandler.reportError(this, re);
			_errHandler.recover(this, re);
		}
		finally {
			exitRule();
		}
		return _localctx;
	}

	@SuppressWarnings("CheckReturnValue")
	public static class CastTypeContext extends ParserRuleContext {
		public TerminalNode INTEIRO() { return getToken(MOCPParser.INTEIRO, 0); }
		public TerminalNode REAL() { return getToken(MOCPParser.REAL, 0); }
		public CastTypeContext(ParserRuleContext parent, int invokingState) {
			super(parent, invokingState);
		}
		@Override public int getRuleIndex() { return RULE_castType; }
	}

	public final CastTypeContext castType() throws RecognitionException {
		CastTypeContext _localctx = new CastTypeContext(_ctx, getState());
		enterRule(_localctx, 84, RULE_castType);
		int _la;
		try {
			enterOuterAlt(_localctx, 1);
			{
			setState(414);
			_la = _input.LA(1);
			if ( !(_la==INTEIRO || _la==REAL) ) {
			_errHandler.recoverInline(this);
			}
			else {
				if ( _input.LA(1)==Token.EOF ) matchedEOF = true;
				_errHandler.reportMatch(this);
				consume();
			}
			}
		}
		catch (RecognitionException re) {
			_localctx.exception = re;
			_errHandler.reportError(this, re);
			_errHandler.recover(this, re);
		}
		finally {
			exitRule();
		}
		return _localctx;
	}

	public static final String _serializedATN =
		"\u0004\u0001I\u01a1\u0002\u0000\u0007\u0000\u0002\u0001\u0007\u0001\u0002"+
		"\u0002\u0007\u0002\u0002\u0003\u0007\u0003\u0002\u0004\u0007\u0004\u0002"+
		"\u0005\u0007\u0005\u0002\u0006\u0007\u0006\u0002\u0007\u0007\u0007\u0002"+
		"\b\u0007\b\u0002\t\u0007\t\u0002\n\u0007\n\u0002\u000b\u0007\u000b\u0002"+
		"\f\u0007\f\u0002\r\u0007\r\u0002\u000e\u0007\u000e\u0002\u000f\u0007\u000f"+
		"\u0002\u0010\u0007\u0010\u0002\u0011\u0007\u0011\u0002\u0012\u0007\u0012"+
		"\u0002\u0013\u0007\u0013\u0002\u0014\u0007\u0014\u0002\u0015\u0007\u0015"+
		"\u0002\u0016\u0007\u0016\u0002\u0017\u0007\u0017\u0002\u0018\u0007\u0018"+
		"\u0002\u0019\u0007\u0019\u0002\u001a\u0007\u001a\u0002\u001b\u0007\u001b"+
		"\u0002\u001c\u0007\u001c\u0002\u001d\u0007\u001d\u0002\u001e\u0007\u001e"+
		"\u0002\u001f\u0007\u001f\u0002 \u0007 \u0002!\u0007!\u0002\"\u0007\"\u0002"+
		"#\u0007#\u0002$\u0007$\u0002%\u0007%\u0002&\u0007&\u0002\'\u0007\'\u0002"+
		"(\u0007(\u0002)\u0007)\u0002*\u0007*\u0001\u0000\u0005\u0000X\b\u0000"+
		"\n\u0000\f\u0000[\t\u0000\u0001\u0000\u0005\u0000^\b\u0000\n\u0000\f\u0000"+
		"a\t\u0000\u0001\u0000\u0005\u0000d\b\u0000\n\u0000\f\u0000g\t\u0000\u0001"+
		"\u0000\u0001\u0000\u0001\u0001\u0001\u0001\u0001\u0001\u0001\u0001\u0001"+
		"\u0001\u0001\u0001\u0001\u0001\u0001\u0002\u0001\u0002\u0001\u0003\u0001"+
		"\u0003\u0001\u0003\u0001\u0003\u0001\u0003\u0001\u0003\u0001\u0003\u0001"+
		"\u0004\u0001\u0004\u0001\u0005\u0001\u0005\u0001\u0005\u0001\u0005\u0005"+
		"\u0005\u0081\b\u0005\n\u0005\f\u0005\u0084\t\u0005\u0003\u0005\u0086\b"+
		"\u0005\u0001\u0006\u0001\u0006\u0003\u0006\u008a\b\u0006\u0001\u0006\u0003"+
		"\u0006\u008d\b\u0006\u0001\u0007\u0001\u0007\u0001\u0007\u0001\b\u0001"+
		"\b\u0005\b\u0094\b\b\n\b\f\b\u0097\t\b\u0001\b\u0005\b\u009a\b\b\n\b\f"+
		"\b\u009d\t\b\u0001\b\u0001\b\u0001\t\u0001\t\u0001\t\u0001\t\u0005\t\u00a5"+
		"\b\t\n\t\f\t\u00a8\t\t\u0001\t\u0001\t\u0001\n\u0001\n\u0001\n\u0001\n"+
		"\u0001\n\u0001\n\u0001\n\u0001\n\u0001\n\u0001\n\u0001\n\u0001\n\u0001"+
		"\n\u0001\n\u0001\n\u0001\n\u0001\n\u0001\n\u0001\n\u0001\n\u0001\n\u0003"+
		"\n\u00c1\b\n\u0001\u000b\u0001\u000b\u0001\u000b\u0001\u000b\u0005\u000b"+
		"\u00c7\b\u000b\n\u000b\f\u000b\u00ca\t\u000b\u0001\u000b\u0001\u000b\u0001"+
		"\f\u0001\f\u0001\f\u0001\f\u0001\f\u0001\f\u0001\f\u0001\f\u0001\f\u0003"+
		"\f\u00d7\b\f\u0001\r\u0001\r\u0001\r\u0001\r\u0001\r\u0001\u000e\u0001"+
		"\u000e\u0001\u000e\u0001\u000e\u0001\u000e\u0001\u000e\u0001\u000e\u0003"+
		"\u000e\u00e5\b\u000e\u0001\u000f\u0001\u000f\u0001\u000f\u0001\u000f\u0001"+
		"\u000f\u0001\u000f\u0001\u0010\u0001\u0010\u0001\u0010\u0003\u0010\u00f0"+
		"\b\u0010\u0001\u0010\u0001\u0010\u0003\u0010\u00f4\b\u0010\u0001\u0010"+
		"\u0001\u0010\u0003\u0010\u00f8\b\u0010\u0001\u0010\u0001\u0010\u0001\u0010"+
		"\u0001\u0011\u0001\u0011\u0001\u0011\u0001\u0011\u0001\u0012\u0001\u0012"+
		"\u0001\u0013\u0001\u0013\u0001\u0013\u0001\u0013\u0001\u0014\u0001\u0014"+
		"\u0003\u0014\u0109\b\u0014\u0001\u0014\u0001\u0014\u0001\u0015\u0001\u0015"+
		"\u0001\u0015\u0001\u0016\u0001\u0016\u0001\u0016\u0001\u0016\u0001\u0016"+
		"\u0001\u0016\u0001\u0016\u0001\u0016\u0001\u0016\u0001\u0016\u0001\u0016"+
		"\u0001\u0016\u0001\u0016\u0001\u0016\u0001\u0016\u0001\u0016\u0001\u0016"+
		"\u0001\u0016\u0001\u0016\u0001\u0016\u0001\u0016\u0001\u0016\u0001\u0016"+
		"\u0003\u0016\u0127\b\u0016\u0001\u0017\u0001\u0017\u0001\u0018\u0001\u0018"+
		"\u0001\u0018\u0005\u0018\u012e\b\u0018\n\u0018\f\u0018\u0131\t\u0018\u0001"+
		"\u0019\u0001\u0019\u0001\u0019\u0005\u0019\u0136\b\u0019\n\u0019\f\u0019"+
		"\u0139\t\u0019\u0001\u001a\u0001\u001a\u0001\u001a\u0003\u001a\u013e\b"+
		"\u001a\u0001\u001b\u0001\u001b\u0001\u001b\u0001\u001b\u0003\u001b\u0144"+
		"\b\u001b\u0001\u001b\u0001\u001b\u0001\u001b\u0001\u001b\u0003\u001b\u014a"+
		"\b\u001b\u0001\u001c\u0001\u001c\u0001\u001d\u0001\u001d\u0001\u001e\u0001"+
		"\u001e\u0001\u001e\u0005\u001e\u0153\b\u001e\n\u001e\f\u001e\u0156\t\u001e"+
		"\u0001\u001f\u0001\u001f\u0001\u001f\u0005\u001f\u015b\b\u001f\n\u001f"+
		"\f\u001f\u015e\t\u001f\u0001 \u0001 \u0001 \u0003 \u0163\b \u0001!\u0001"+
		"!\u0001!\u0001!\u0001!\u0001!\u0003!\u016b\b!\u0001\"\u0001\"\u0001\""+
		"\u0001\"\u0001\"\u0001\"\u0001\"\u0001\"\u0003\"\u0175\b\"\u0001#\u0001"+
		"#\u0001#\u0001#\u0001#\u0001#\u0003#\u017d\b#\u0001$\u0001$\u0001$\u0001"+
		"$\u0001$\u0001$\u0001$\u0001$\u0001$\u0003$\u0188\b$\u0001%\u0001%\u0001"+
		"%\u0003%\u018d\b%\u0001%\u0001%\u0001&\u0001&\u0001&\u0005&\u0194\b&\n"+
		"&\f&\u0197\t&\u0001\'\u0001\'\u0001(\u0001(\u0001)\u0001)\u0001*\u0001"+
		"*\u0001*\u0000\u0000+\u0000\u0002\u0004\u0006\b\n\f\u000e\u0010\u0012"+
		"\u0014\u0016\u0018\u001a\u001c\u001e \"$&(*,.02468:<>@BDFHJLNPRT\u0000"+
		"\u0007\u0002\u0000\u0004\u0004EE\u0001\u0000\',\u0001\u000034\u0001\u0000"+
		"57\u0001\u0000AC\u0001\u0000\u0001\u0003\u0001\u0000\u0001\u0002\u01a7"+
		"\u0000Y\u0001\u0000\u0000\u0000\u0002j\u0001\u0000\u0000\u0000\u0004q"+
		"\u0001\u0000\u0000\u0000\u0006s\u0001\u0000\u0000\u0000\bz\u0001\u0000"+
		"\u0000\u0000\n\u0085\u0001\u0000\u0000\u0000\f\u0087\u0001\u0000\u0000"+
		"\u0000\u000e\u008e\u0001\u0000\u0000\u0000\u0010\u0091\u0001\u0000\u0000"+
		"\u0000\u0012\u00a0\u0001\u0000\u0000\u0000\u0014\u00c0\u0001\u0000\u0000"+
		"\u0000\u0016\u00c2\u0001\u0000\u0000\u0000\u0018\u00d6\u0001\u0000\u0000"+
		"\u0000\u001a\u00d8\u0001\u0000\u0000\u0000\u001c\u00dd\u0001\u0000\u0000"+
		"\u0000\u001e\u00e6\u0001\u0000\u0000\u0000 \u00ec\u0001\u0000\u0000\u0000"+
		"\"\u00fc\u0001\u0000\u0000\u0000$\u0100\u0001\u0000\u0000\u0000&\u0102"+
		"\u0001\u0000\u0000\u0000(\u0106\u0001\u0000\u0000\u0000*\u010c\u0001\u0000"+
		"\u0000\u0000,\u0126\u0001\u0000\u0000\u0000.\u0128\u0001\u0000\u0000\u0000"+
		"0\u012a\u0001\u0000\u0000\u00002\u0132\u0001\u0000\u0000\u00004\u013d"+
		"\u0001\u0000\u0000\u00006\u0149\u0001\u0000\u0000\u00008\u014b\u0001\u0000"+
		"\u0000\u0000:\u014d\u0001\u0000\u0000\u0000<\u014f\u0001\u0000\u0000\u0000"+
		">\u0157\u0001\u0000\u0000\u0000@\u0162\u0001\u0000\u0000\u0000B\u016a"+
		"\u0001\u0000\u0000\u0000D\u0174\u0001\u0000\u0000\u0000F\u017c\u0001\u0000"+
		"\u0000\u0000H\u0187\u0001\u0000\u0000\u0000J\u0189\u0001\u0000\u0000\u0000"+
		"L\u0190\u0001\u0000\u0000\u0000N\u0198\u0001\u0000\u0000\u0000P\u019a"+
		"\u0001\u0000\u0000\u0000R\u019c\u0001\u0000\u0000\u0000T\u019e\u0001\u0000"+
		"\u0000\u0000VX\u0003\u0002\u0001\u0000WV\u0001\u0000\u0000\u0000X[\u0001"+
		"\u0000\u0000\u0000YW\u0001\u0000\u0000\u0000YZ\u0001\u0000\u0000\u0000"+
		"Z_\u0001\u0000\u0000\u0000[Y\u0001\u0000\u0000\u0000\\^\u0003\u0004\u0002"+
		"\u0000]\\\u0001\u0000\u0000\u0000^a\u0001\u0000\u0000\u0000_]\u0001\u0000"+
		"\u0000\u0000_`\u0001\u0000\u0000\u0000`e\u0001\u0000\u0000\u0000a_\u0001"+
		"\u0000\u0000\u0000bd\u0003\u0006\u0003\u0000cb\u0001\u0000\u0000\u0000"+
		"dg\u0001\u0000\u0000\u0000ec\u0001\u0000\u0000\u0000ef\u0001\u0000\u0000"+
		"\u0000fh\u0001\u0000\u0000\u0000ge\u0001\u0000\u0000\u0000hi\u0005\u0000"+
		"\u0000\u0001i\u0001\u0001\u0000\u0000\u0000jk\u0003P(\u0000kl\u0003\b"+
		"\u0004\u0000lm\u00059\u0000\u0000mn\u0003\n\u0005\u0000no\u0005:\u0000"+
		"\u0000op\u0005@\u0000\u0000p\u0003\u0001\u0000\u0000\u0000qr\u0003\u0012"+
		"\t\u0000r\u0005\u0001\u0000\u0000\u0000st\u0003P(\u0000tu\u0003\b\u0004"+
		"\u0000uv\u00059\u0000\u0000vw\u0003\n\u0005\u0000wx\u0005:\u0000\u0000"+
		"xy\u0003\u0010\b\u0000y\u0007\u0001\u0000\u0000\u0000z{\u0007\u0000\u0000"+
		"\u0000{\t\u0001\u0000\u0000\u0000|\u0086\u0005\u0003\u0000\u0000}\u0082"+
		"\u0003\f\u0006\u0000~\u007f\u0005?\u0000\u0000\u007f\u0081\u0003\f\u0006"+
		"\u0000\u0080~\u0001\u0000\u0000\u0000\u0081\u0084\u0001\u0000\u0000\u0000"+
		"\u0082\u0080\u0001\u0000\u0000\u0000\u0082\u0083\u0001\u0000\u0000\u0000"+
		"\u0083\u0086\u0001\u0000\u0000\u0000\u0084\u0082\u0001\u0000\u0000\u0000"+
		"\u0085|\u0001\u0000\u0000\u0000\u0085}\u0001\u0000\u0000\u0000\u0086\u000b"+
		"\u0001\u0000\u0000\u0000\u0087\u0089\u0003R)\u0000\u0088\u008a\u0005E"+
		"\u0000\u0000\u0089\u0088\u0001\u0000\u0000\u0000\u0089\u008a\u0001\u0000"+
		"\u0000\u0000\u008a\u008c\u0001\u0000\u0000\u0000\u008b\u008d\u0003\u000e"+
		"\u0007\u0000\u008c\u008b\u0001\u0000\u0000\u0000\u008c\u008d\u0001\u0000"+
		"\u0000\u0000\u008d\r\u0001\u0000\u0000\u0000\u008e\u008f\u0005=\u0000"+
		"\u0000\u008f\u0090\u0005>\u0000\u0000\u0090\u000f\u0001\u0000\u0000\u0000"+
		"\u0091\u0095\u0005;\u0000\u0000\u0092\u0094\u0003\u0012\t\u0000\u0093"+
		"\u0092\u0001\u0000\u0000\u0000\u0094\u0097\u0001\u0000\u0000\u0000\u0095"+
		"\u0093\u0001\u0000\u0000\u0000\u0095\u0096\u0001\u0000\u0000\u0000\u0096"+
		"\u009b\u0001\u0000\u0000\u0000\u0097\u0095\u0001\u0000\u0000\u0000\u0098"+
		"\u009a\u0003\u0018\f\u0000\u0099\u0098\u0001\u0000\u0000\u0000\u009a\u009d"+
		"\u0001\u0000\u0000\u0000\u009b\u0099\u0001\u0000\u0000\u0000\u009b\u009c"+
		"\u0001\u0000\u0000\u0000\u009c\u009e\u0001\u0000\u0000\u0000\u009d\u009b"+
		"\u0001\u0000\u0000\u0000\u009e\u009f\u0005<\u0000\u0000\u009f\u0011\u0001"+
		"\u0000\u0000\u0000\u00a0\u00a1\u0003R)\u0000\u00a1\u00a6\u0003\u0014\n"+
		"\u0000\u00a2\u00a3\u0005?\u0000\u0000\u00a3\u00a5\u0003\u0014\n\u0000"+
		"\u00a4\u00a2\u0001\u0000\u0000\u0000\u00a5\u00a8\u0001\u0000\u0000\u0000"+
		"\u00a6\u00a4\u0001\u0000\u0000\u0000\u00a6\u00a7\u0001\u0000\u0000\u0000"+
		"\u00a7\u00a9\u0001\u0000\u0000\u0000\u00a8\u00a6\u0001\u0000\u0000\u0000"+
		"\u00a9\u00aa\u0005@\u0000\u0000\u00aa\u0013\u0001\u0000\u0000\u0000\u00ab"+
		"\u00c1\u0005E\u0000\u0000\u00ac\u00ad\u0005E\u0000\u0000\u00ad\u00ae\u0005"+
		"8\u0000\u0000\u00ae\u00c1\u0003:\u001d\u0000\u00af\u00b0\u0005E\u0000"+
		"\u0000\u00b0\u00b1\u0005=\u0000\u0000\u00b1\u00b2\u0005B\u0000\u0000\u00b2"+
		"\u00c1\u0005>\u0000\u0000\u00b3\u00b4\u0005E\u0000\u0000\u00b4\u00b5\u0005"+
		"=\u0000\u0000\u00b5\u00b6\u0005>\u0000\u0000\u00b6\u00b7\u00058\u0000"+
		"\u0000\u00b7\u00c1\u0003\u0016\u000b\u0000\u00b8\u00b9\u0005E\u0000\u0000"+
		"\u00b9\u00ba\u0005=\u0000\u0000\u00ba\u00bb\u0005>\u0000\u0000\u00bb\u00bc"+
		"\u00058\u0000\u0000\u00bc\u00c1\u0003:\u001d\u0000\u00bd\u00be\u0005E"+
		"\u0000\u0000\u00be\u00bf\u0005=\u0000\u0000\u00bf\u00c1\u0005>\u0000\u0000"+
		"\u00c0\u00ab\u0001\u0000\u0000\u0000\u00c0\u00ac\u0001\u0000\u0000\u0000"+
		"\u00c0\u00af\u0001\u0000\u0000\u0000\u00c0\u00b3\u0001\u0000\u0000\u0000"+
		"\u00c0\u00b8\u0001\u0000\u0000\u0000\u00c0\u00bd\u0001\u0000\u0000\u0000"+
		"\u00c1\u0015\u0001\u0000\u0000\u0000\u00c2\u00c3\u0005;\u0000\u0000\u00c3"+
		"\u00c8\u0003:\u001d\u0000\u00c4\u00c5\u0005?\u0000\u0000\u00c5\u00c7\u0003"+
		":\u001d\u0000\u00c6\u00c4\u0001\u0000\u0000\u0000\u00c7\u00ca\u0001\u0000"+
		"\u0000\u0000\u00c8\u00c6\u0001\u0000\u0000\u0000\u00c8\u00c9\u0001\u0000"+
		"\u0000\u0000\u00c9\u00cb\u0001\u0000\u0000\u0000\u00ca\u00c8\u0001\u0000"+
		"\u0000\u0000\u00cb\u00cc\u0005<\u0000\u0000\u00cc\u0017\u0001\u0000\u0000"+
		"\u0000\u00cd\u00d7\u0003\u001a\r\u0000\u00ce\u00d7\u0003\u001c\u000e\u0000"+
		"\u00cf\u00d7\u0003\u001e\u000f\u0000\u00d0\u00d7\u0003 \u0010\u0000\u00d1"+
		"\u00d7\u0003(\u0014\u0000\u00d2\u00d7\u0003,\u0016\u0000\u00d3\u00d7\u0003"+
		"*\u0015\u0000\u00d4\u00d7\u0003\u0010\b\u0000\u00d5\u00d7\u0005@\u0000"+
		"\u0000\u00d6\u00cd\u0001\u0000\u0000\u0000\u00d6\u00ce\u0001\u0000\u0000"+
		"\u0000\u00d6\u00cf\u0001\u0000\u0000\u0000\u00d6\u00d0\u0001\u0000\u0000"+
		"\u0000\u00d6\u00d1\u0001\u0000\u0000\u0000\u00d6\u00d2\u0001\u0000\u0000"+
		"\u0000\u00d6\u00d3\u0001\u0000\u0000\u0000\u00d6\u00d4\u0001\u0000\u0000"+
		"\u0000\u00d6\u00d5\u0001\u0000\u0000\u0000\u00d7\u0019\u0001\u0000\u0000"+
		"\u0000\u00d8\u00d9\u0003F#\u0000\u00d9\u00da\u00058\u0000\u0000\u00da"+
		"\u00db\u0003:\u001d\u0000\u00db\u00dc\u0005@\u0000\u0000\u00dc\u001b\u0001"+
		"\u0000\u0000\u0000\u00dd\u00de\u0005\u0005\u0000\u0000\u00de\u00df\u0005"+
		"9\u0000\u0000\u00df\u00e0\u0003.\u0017\u0000\u00e0\u00e1\u0005:\u0000"+
		"\u0000\u00e1\u00e4\u0003\u0010\b\u0000\u00e2\u00e3\u0005\u0006\u0000\u0000"+
		"\u00e3\u00e5\u0003\u0010\b\u0000\u00e4\u00e2\u0001\u0000\u0000\u0000\u00e4"+
		"\u00e5\u0001\u0000\u0000\u0000\u00e5\u001d\u0001\u0000\u0000\u0000\u00e6"+
		"\u00e7\u0005\u0007\u0000\u0000\u00e7\u00e8\u00059\u0000\u0000\u00e8\u00e9"+
		"\u0003.\u0017\u0000\u00e9\u00ea\u0005:\u0000\u0000\u00ea\u00eb\u0003\u0010"+
		"\b\u0000\u00eb\u001f\u0001\u0000\u0000\u0000\u00ec\u00ed\u0005\b\u0000"+
		"\u0000\u00ed\u00ef\u00059\u0000\u0000\u00ee\u00f0\u0003\"\u0011\u0000"+
		"\u00ef\u00ee\u0001\u0000\u0000\u0000\u00ef\u00f0\u0001\u0000\u0000\u0000"+
		"\u00f0\u00f1\u0001\u0000\u0000\u0000\u00f1\u00f3\u0005@\u0000\u0000\u00f2"+
		"\u00f4\u0003$\u0012\u0000\u00f3\u00f2\u0001\u0000\u0000\u0000\u00f3\u00f4"+
		"\u0001\u0000\u0000\u0000\u00f4\u00f5\u0001\u0000\u0000\u0000\u00f5\u00f7"+
		"\u0005@\u0000\u0000\u00f6\u00f8\u0003&\u0013\u0000\u00f7\u00f6\u0001\u0000"+
		"\u0000\u0000\u00f7\u00f8\u0001\u0000\u0000\u0000\u00f8\u00f9\u0001\u0000"+
		"\u0000\u0000\u00f9\u00fa\u0005:\u0000\u0000\u00fa\u00fb\u0003\u0010\b"+
		"\u0000\u00fb!\u0001\u0000\u0000\u0000\u00fc\u00fd\u0003F#\u0000\u00fd"+
		"\u00fe\u00058\u0000\u0000\u00fe\u00ff\u0003:\u001d\u0000\u00ff#\u0001"+
		"\u0000\u0000\u0000\u0100\u0101\u0003.\u0017\u0000\u0101%\u0001\u0000\u0000"+
		"\u0000\u0102\u0103\u0003F#\u0000\u0103\u0104\u00058\u0000\u0000\u0104"+
		"\u0105\u0003:\u001d\u0000\u0105\'\u0001\u0000\u0000\u0000\u0106\u0108"+
		"\u0005\t\u0000\u0000\u0107\u0109\u0003:\u001d\u0000\u0108\u0107\u0001"+
		"\u0000\u0000\u0000\u0108\u0109\u0001\u0000\u0000\u0000\u0109\u010a\u0001"+
		"\u0000\u0000\u0000\u010a\u010b\u0005@\u0000\u0000\u010b)\u0001\u0000\u0000"+
		"\u0000\u010c\u010d\u0003J%\u0000\u010d\u010e\u0005@\u0000\u0000\u010e"+
		"+\u0001\u0000\u0000\u0000\u010f\u0110\u0005\r\u0000\u0000\u0110\u0111"+
		"\u00059\u0000\u0000\u0111\u0112\u0003:\u001d\u0000\u0112\u0113\u0005:"+
		"\u0000\u0000\u0113\u0114\u0005@\u0000\u0000\u0114\u0127\u0001\u0000\u0000"+
		"\u0000\u0115\u0116\u0005\u000e\u0000\u0000\u0116\u0117\u00059\u0000\u0000"+
		"\u0117\u0118\u0003:\u001d\u0000\u0118\u0119\u0005:\u0000\u0000\u0119\u011a"+
		"\u0005@\u0000\u0000\u011a\u0127\u0001\u0000\u0000\u0000\u011b\u011c\u0005"+
		"\u0010\u0000\u0000\u011c\u011d\u00059\u0000\u0000\u011d\u011e\u0003:\u001d"+
		"\u0000\u011e\u011f\u0005:\u0000\u0000\u011f\u0120\u0005@\u0000\u0000\u0120"+
		"\u0127\u0001\u0000\u0000\u0000\u0121\u0122\u0005\u000f\u0000\u0000\u0122"+
		"\u0123\u00059\u0000\u0000\u0123\u0124\u0005E\u0000\u0000\u0124\u0125\u0005"+
		":\u0000\u0000\u0125\u0127\u0005@\u0000\u0000\u0126\u010f\u0001\u0000\u0000"+
		"\u0000\u0126\u0115\u0001\u0000\u0000\u0000\u0126\u011b\u0001\u0000\u0000"+
		"\u0000\u0126\u0121\u0001\u0000\u0000\u0000\u0127-\u0001\u0000\u0000\u0000"+
		"\u0128\u0129\u00030\u0018\u0000\u0129/\u0001\u0000\u0000\u0000\u012a\u012f"+
		"\u00032\u0019\u0000\u012b\u012c\u0005%\u0000\u0000\u012c\u012e\u00032"+
		"\u0019\u0000\u012d\u012b\u0001\u0000\u0000\u0000\u012e\u0131\u0001\u0000"+
		"\u0000\u0000\u012f\u012d\u0001\u0000\u0000\u0000\u012f\u0130\u0001\u0000"+
		"\u0000\u0000\u01301\u0001\u0000\u0000\u0000\u0131\u012f\u0001\u0000\u0000"+
		"\u0000\u0132\u0137\u00034\u001a\u0000\u0133\u0134\u0005$\u0000\u0000\u0134"+
		"\u0136\u00034\u001a\u0000\u0135\u0133\u0001\u0000\u0000\u0000\u0136\u0139"+
		"\u0001\u0000\u0000\u0000\u0137\u0135\u0001\u0000\u0000\u0000\u0137\u0138"+
		"\u0001\u0000\u0000\u0000\u01383\u0001\u0000\u0000\u0000\u0139\u0137\u0001"+
		"\u0000\u0000\u0000\u013a\u013b\u0005&\u0000\u0000\u013b\u013e\u00034\u001a"+
		"\u0000\u013c\u013e\u00036\u001b\u0000\u013d\u013a\u0001\u0000\u0000\u0000"+
		"\u013d\u013c\u0001\u0000\u0000\u0000\u013e5\u0001\u0000\u0000\u0000\u013f"+
		"\u0143\u0003:\u001d\u0000\u0140\u0141\u00038\u001c\u0000\u0141\u0142\u0003"+
		":\u001d\u0000\u0142\u0144\u0001\u0000\u0000\u0000\u0143\u0140\u0001\u0000"+
		"\u0000\u0000\u0143\u0144\u0001\u0000\u0000\u0000\u0144\u014a\u0001\u0000"+
		"\u0000\u0000\u0145\u0146\u00059\u0000\u0000\u0146\u0147\u0003.\u0017\u0000"+
		"\u0147\u0148\u0005:\u0000\u0000\u0148\u014a\u0001\u0000\u0000\u0000\u0149"+
		"\u013f\u0001\u0000\u0000\u0000\u0149\u0145\u0001\u0000\u0000\u0000\u014a"+
		"7\u0001\u0000\u0000\u0000\u014b\u014c\u0007\u0001\u0000\u0000\u014c9\u0001"+
		"\u0000\u0000\u0000\u014d\u014e\u0003<\u001e\u0000\u014e;\u0001\u0000\u0000"+
		"\u0000\u014f\u0154\u0003>\u001f\u0000\u0150\u0151\u0007\u0002\u0000\u0000"+
		"\u0151\u0153\u0003>\u001f\u0000\u0152\u0150\u0001\u0000\u0000\u0000\u0153"+
		"\u0156\u0001\u0000\u0000\u0000\u0154\u0152\u0001\u0000\u0000\u0000\u0154"+
		"\u0155\u0001\u0000\u0000\u0000\u0155=\u0001\u0000\u0000\u0000\u0156\u0154"+
		"\u0001\u0000\u0000\u0000\u0157\u015c\u0003@ \u0000\u0158\u0159\u0007\u0003"+
		"\u0000\u0000\u0159\u015b\u0003@ \u0000\u015a\u0158\u0001\u0000\u0000\u0000"+
		"\u015b\u015e\u0001\u0000\u0000\u0000\u015c\u015a\u0001\u0000\u0000\u0000"+
		"\u015c\u015d\u0001\u0000\u0000\u0000\u015d?\u0001\u0000\u0000\u0000\u015e"+
		"\u015c\u0001\u0000\u0000\u0000\u015f\u0160\u00054\u0000\u0000\u0160\u0163"+
		"\u0003@ \u0000\u0161\u0163\u0003B!\u0000\u0162\u015f\u0001\u0000\u0000"+
		"\u0000\u0162\u0161\u0001\u0000\u0000\u0000\u0163A\u0001\u0000\u0000\u0000"+
		"\u0164\u0165\u00059\u0000\u0000\u0165\u0166\u0003T*\u0000\u0166\u0167"+
		"\u0005:\u0000\u0000\u0167\u0168\u0003@ \u0000\u0168\u016b\u0001\u0000"+
		"\u0000\u0000\u0169\u016b\u0003D\"\u0000\u016a\u0164\u0001\u0000\u0000"+
		"\u0000\u016a\u0169\u0001\u0000\u0000\u0000\u016bC\u0001\u0000\u0000\u0000"+
		"\u016c\u0175\u0003F#\u0000\u016d\u0175\u0003H$\u0000\u016e\u0175\u0003"+
		"J%\u0000\u016f\u0175\u0003N\'\u0000\u0170\u0171\u00059\u0000\u0000\u0171"+
		"\u0172\u0003:\u001d\u0000\u0172\u0173\u0005:\u0000\u0000\u0173\u0175\u0001"+
		"\u0000\u0000\u0000\u0174\u016c\u0001\u0000\u0000\u0000\u0174\u016d\u0001"+
		"\u0000\u0000\u0000\u0174\u016e\u0001\u0000\u0000\u0000\u0174\u016f\u0001"+
		"\u0000\u0000\u0000\u0174\u0170\u0001\u0000\u0000\u0000\u0175E\u0001\u0000"+
		"\u0000\u0000\u0176\u017d\u0005E\u0000\u0000\u0177\u0178\u0005E\u0000\u0000"+
		"\u0178\u0179\u0005=\u0000\u0000\u0179\u017a\u0003:\u001d\u0000\u017a\u017b"+
		"\u0005>\u0000\u0000\u017b\u017d\u0001\u0000\u0000\u0000\u017c\u0176\u0001"+
		"\u0000\u0000\u0000\u017c\u0177\u0001\u0000\u0000\u0000\u017dG\u0001\u0000"+
		"\u0000\u0000\u017e\u017f\u0005\n\u0000\u0000\u017f\u0180\u00059\u0000"+
		"\u0000\u0180\u0188\u0005:\u0000\u0000\u0181\u0182\u0005\u000b\u0000\u0000"+
		"\u0182\u0183\u00059\u0000\u0000\u0183\u0188\u0005:\u0000\u0000\u0184\u0185"+
		"\u0005\f\u0000\u0000\u0185\u0186\u00059\u0000\u0000\u0186\u0188\u0005"+
		":\u0000\u0000\u0187\u017e\u0001\u0000\u0000\u0000\u0187\u0181\u0001\u0000"+
		"\u0000\u0000\u0187\u0184\u0001\u0000\u0000\u0000\u0188I\u0001\u0000\u0000"+
		"\u0000\u0189\u018a\u0003\b\u0004\u0000\u018a\u018c\u00059\u0000\u0000"+
		"\u018b\u018d\u0003L&\u0000\u018c\u018b\u0001\u0000\u0000\u0000\u018c\u018d"+
		"\u0001\u0000\u0000\u0000\u018d\u018e\u0001\u0000\u0000\u0000\u018e\u018f"+
		"\u0005:\u0000\u0000\u018fK\u0001\u0000\u0000\u0000\u0190\u0195\u0003:"+
		"\u001d\u0000\u0191\u0192\u0005?\u0000\u0000\u0192\u0194\u0003:\u001d\u0000"+
		"\u0193\u0191\u0001\u0000\u0000\u0000\u0194\u0197\u0001\u0000\u0000\u0000"+
		"\u0195\u0193\u0001\u0000\u0000\u0000\u0195\u0196\u0001\u0000\u0000\u0000"+
		"\u0196M\u0001\u0000\u0000\u0000\u0197\u0195\u0001\u0000\u0000\u0000\u0198"+
		"\u0199\u0007\u0004\u0000\u0000\u0199O\u0001\u0000\u0000\u0000\u019a\u019b"+
		"\u0007\u0005\u0000\u0000\u019bQ\u0001\u0000\u0000\u0000\u019c\u019d\u0007"+
		"\u0006\u0000\u0000\u019dS\u0001\u0000\u0000\u0000\u019e\u019f\u0007\u0006"+
		"\u0000\u0000\u019fU\u0001\u0000\u0000\u0000!Y_e\u0082\u0085\u0089\u008c"+
		"\u0095\u009b\u00a6\u00c0\u00c8\u00d6\u00e4\u00ef\u00f3\u00f7\u0108\u0126"+
		"\u012f\u0137\u013d\u0143\u0149\u0154\u015c\u0162\u016a\u0174\u017c\u0187"+
		"\u018c\u0195";
	public static final ATN _ATN =
		new ATNDeserializer().deserialize(_serializedATN.toCharArray());
	static {
		_decisionToDFA = new DFA[_ATN.getNumberOfDecisions()];
		for (int i = 0; i < _ATN.getNumberOfDecisions(); i++) {
			_decisionToDFA[i] = new DFA(_ATN.getDecisionState(i), i);
		}
	}
}