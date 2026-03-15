// Generated from c:/Users/Monica/Desktop/Braket-Proglang/BraKet.g4 by ANTLR 4.13.1
import org.antlr.v4.runtime.atn.*;
import org.antlr.v4.runtime.dfa.DFA;
import org.antlr.v4.runtime.*;
import org.antlr.v4.runtime.misc.*;
import org.antlr.v4.runtime.tree.*;
import java.util.List;
import java.util.Iterator;
import java.util.ArrayList;

@SuppressWarnings({"all", "warnings", "unchecked", "unused", "cast", "CheckReturnValue"})
public class BraKetParser extends Parser {
	static { RuntimeMetaData.checkVersion("4.13.1", RuntimeMetaData.VERSION); }

	protected static final DFA[] _decisionToDFA;
	protected static final PredictionContextCache _sharedContextCache =
		new PredictionContextCache();
	public static final int
		COMMA=1, WS=2, FROM=3, IMPORT=4, CONST=5, KET_IDENTIFIER=6, BRA_IDENTIFIER=7, 
		INT=8, FLOAT=9, CHAR=10, STRING=11, COMPLEX=12, RETURN=13, IF=14, ELIF=15, 
		ELSE=16, FOR=17, WHILE=18, DO=19, BOOL_TRUE=20, BOOL_FALSE=21, MAIN=22, 
		FUNC=23, ADD=24, SUB=25, MUL=26, DIV=27, EXP=28, MOD=29, ASSIGN=30, GT=31, 
		LT=32, GTE=33, LTE=34, EQ=35, NEQ=36, LOGICAL_OR=37, LOGICAL_AND=38, NEG=39, 
		LPAREN=40, RPAREN=41, LSQUARE=42, RSQUARE=43, LCURLY=44, RCURLY=45, TENSOR=46, 
		SEMICOLON=47, DOT=48, IDENTIFIER=49;
	public static final int
		RULE_program = 0, RULE_import_list = 1, RULE_import_statement = 2, RULE_func_list = 3, 
		RULE_const_decl_list = 4, RULE_const_decl = 5, RULE_var_decl_list = 6, 
		RULE_var_decl = 7, RULE_value = 8, RULE_braket_vector = 9, RULE_braket_value = 10, 
		RULE_braket_expression = 11, RULE_braket_term = 12, RULE_braket_factor = 13, 
		RULE_array = 14, RULE_struct = 15, RULE_struct_value = 16, RULE_op = 17, 
		RULE_statement_list = 18, RULE_statement = 19, RULE_assign_statement = 20, 
		RULE_func_call_statement = 21, RULE_arg_list = 22, RULE_arg = 23, RULE_return_statement = 24, 
		RULE_if_statement = 25, RULE_elif = 26, RULE_else = 27, RULE_for_statement = 28, 
		RULE_while_statement = 29, RULE_do_statement = 30, RULE_expression = 31, 
		RULE_string_expression = 32, RULE_num_expression = 33, RULE_num_term = 34, 
		RULE_num_factor = 35, RULE_array_access = 36, RULE_struct_access = 37, 
		RULE_dirac_expression = 38, RULE_num_comp = 39, RULE_eq_comp = 40, RULE_bool_expression = 41, 
		RULE_bool_or = 42, RULE_bool_and = 43, RULE_bool_cmp = 44, RULE_bool_unary = 45, 
		RULE_bool_primary = 46, RULE_func_decl_list = 47, RULE_func_decl = 48, 
		RULE_param_list = 49, RULE_identifier_list = 50, RULE_default_list = 51, 
		RULE_main_function = 52;
	private static String[] makeRuleNames() {
		return new String[] {
			"program", "import_list", "import_statement", "func_list", "const_decl_list", 
			"const_decl", "var_decl_list", "var_decl", "value", "braket_vector", 
			"braket_value", "braket_expression", "braket_term", "braket_factor", 
			"array", "struct", "struct_value", "op", "statement_list", "statement", 
			"assign_statement", "func_call_statement", "arg_list", "arg", "return_statement", 
			"if_statement", "elif", "else", "for_statement", "while_statement", "do_statement", 
			"expression", "string_expression", "num_expression", "num_term", "num_factor", 
			"array_access", "struct_access", "dirac_expression", "num_comp", "eq_comp", 
			"bool_expression", "bool_or", "bool_and", "bool_cmp", "bool_unary", "bool_primary", 
			"func_decl_list", "func_decl", "param_list", "identifier_list", "default_list", 
			"main_function"
		};
	}
	public static final String[] ruleNames = makeRuleNames();

	private static String[] makeLiteralNames() {
		return new String[] {
			null, "','", null, "'from'", "'import'", "'const'", null, null, null, 
			null, null, null, null, "'return'", "'if'", "'elif'", "'else'", "'for'", 
			"'while'", "'do'", "'true'", "'false'", "'main'", "'func'", "'+'", "'-'", 
			"'*'", "'/'", "'**'", "'%'", "'='", "'>'", "'<'", "'>='", "'<='", "'=='", 
			"'!='", "'||'", "'&&'", "'!'", "'('", "')'", "'['", "']'", "'{'", "'}'", 
			"'@'", "';'", "'.'"
		};
	}
	private static final String[] _LITERAL_NAMES = makeLiteralNames();
	private static String[] makeSymbolicNames() {
		return new String[] {
			null, "COMMA", "WS", "FROM", "IMPORT", "CONST", "KET_IDENTIFIER", "BRA_IDENTIFIER", 
			"INT", "FLOAT", "CHAR", "STRING", "COMPLEX", "RETURN", "IF", "ELIF", 
			"ELSE", "FOR", "WHILE", "DO", "BOOL_TRUE", "BOOL_FALSE", "MAIN", "FUNC", 
			"ADD", "SUB", "MUL", "DIV", "EXP", "MOD", "ASSIGN", "GT", "LT", "GTE", 
			"LTE", "EQ", "NEQ", "LOGICAL_OR", "LOGICAL_AND", "NEG", "LPAREN", "RPAREN", 
			"LSQUARE", "RSQUARE", "LCURLY", "RCURLY", "TENSOR", "SEMICOLON", "DOT", 
			"IDENTIFIER"
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
	public String getGrammarFileName() { return "BraKet.g4"; }

	@Override
	public String[] getRuleNames() { return ruleNames; }

	@Override
	public String getSerializedATN() { return _serializedATN; }

	@Override
	public ATN getATN() { return _ATN; }

	public BraKetParser(TokenStream input) {
		super(input);
		_interp = new ParserATNSimulator(this,_ATN,_decisionToDFA,_sharedContextCache);
	}

	@SuppressWarnings("CheckReturnValue")
	public static class ProgramContext extends ParserRuleContext {
		public Import_listContext import_list() {
			return getRuleContext(Import_listContext.class,0);
		}
		public Const_decl_listContext const_decl_list() {
			return getRuleContext(Const_decl_listContext.class,0);
		}
		public Func_decl_listContext func_decl_list() {
			return getRuleContext(Func_decl_listContext.class,0);
		}
		public Main_functionContext main_function() {
			return getRuleContext(Main_functionContext.class,0);
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
			enterOuterAlt(_localctx, 1);
			{
			setState(107);
			_errHandler.sync(this);
			_la = _input.LA(1);
			if (_la==FROM || _la==IMPORT) {
				{
				setState(106);
				import_list();
				}
			}

			setState(110);
			_errHandler.sync(this);
			_la = _input.LA(1);
			if (_la==CONST) {
				{
				setState(109);
				const_decl_list();
				}
			}

			setState(113);
			_errHandler.sync(this);
			_la = _input.LA(1);
			if (_la==FUNC) {
				{
				setState(112);
				func_decl_list();
				}
			}

			setState(116);
			_errHandler.sync(this);
			_la = _input.LA(1);
			if (_la==MAIN) {
				{
				setState(115);
				main_function();
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
	public static class Import_listContext extends ParserRuleContext {
		public List<Import_statementContext> import_statement() {
			return getRuleContexts(Import_statementContext.class);
		}
		public Import_statementContext import_statement(int i) {
			return getRuleContext(Import_statementContext.class,i);
		}
		public Import_listContext(ParserRuleContext parent, int invokingState) {
			super(parent, invokingState);
		}
		@Override public int getRuleIndex() { return RULE_import_list; }
	}

	public final Import_listContext import_list() throws RecognitionException {
		Import_listContext _localctx = new Import_listContext(_ctx, getState());
		enterRule(_localctx, 2, RULE_import_list);
		int _la;
		try {
			enterOuterAlt(_localctx, 1);
			{
			setState(118);
			import_statement();
			setState(122);
			_errHandler.sync(this);
			_la = _input.LA(1);
			while (_la==FROM || _la==IMPORT) {
				{
				{
				setState(119);
				import_statement();
				}
				}
				setState(124);
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
	public static class Import_statementContext extends ParserRuleContext {
		public TerminalNode FROM() { return getToken(BraKetParser.FROM, 0); }
		public TerminalNode IDENTIFIER() { return getToken(BraKetParser.IDENTIFIER, 0); }
		public TerminalNode IMPORT() { return getToken(BraKetParser.IMPORT, 0); }
		public Func_listContext func_list() {
			return getRuleContext(Func_listContext.class,0);
		}
		public Import_statementContext(ParserRuleContext parent, int invokingState) {
			super(parent, invokingState);
		}
		@Override public int getRuleIndex() { return RULE_import_statement; }
	}

	public final Import_statementContext import_statement() throws RecognitionException {
		Import_statementContext _localctx = new Import_statementContext(_ctx, getState());
		enterRule(_localctx, 4, RULE_import_statement);
		try {
			setState(131);
			_errHandler.sync(this);
			switch (_input.LA(1)) {
			case FROM:
				enterOuterAlt(_localctx, 1);
				{
				setState(125);
				match(FROM);
				setState(126);
				match(IDENTIFIER);
				setState(127);
				match(IMPORT);
				setState(128);
				func_list();
				}
				break;
			case IMPORT:
				enterOuterAlt(_localctx, 2);
				{
				setState(129);
				match(IMPORT);
				setState(130);
				match(IDENTIFIER);
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
	public static class Func_listContext extends ParserRuleContext {
		public List<TerminalNode> IDENTIFIER() { return getTokens(BraKetParser.IDENTIFIER); }
		public TerminalNode IDENTIFIER(int i) {
			return getToken(BraKetParser.IDENTIFIER, i);
		}
		public List<TerminalNode> COMMA() { return getTokens(BraKetParser.COMMA); }
		public TerminalNode COMMA(int i) {
			return getToken(BraKetParser.COMMA, i);
		}
		public Func_listContext(ParserRuleContext parent, int invokingState) {
			super(parent, invokingState);
		}
		@Override public int getRuleIndex() { return RULE_func_list; }
	}

	public final Func_listContext func_list() throws RecognitionException {
		Func_listContext _localctx = new Func_listContext(_ctx, getState());
		enterRule(_localctx, 6, RULE_func_list);
		int _la;
		try {
			enterOuterAlt(_localctx, 1);
			{
			setState(133);
			match(IDENTIFIER);
			setState(138);
			_errHandler.sync(this);
			_la = _input.LA(1);
			while (_la==COMMA) {
				{
				{
				setState(134);
				match(COMMA);
				setState(135);
				match(IDENTIFIER);
				}
				}
				setState(140);
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
	public static class Const_decl_listContext extends ParserRuleContext {
		public List<Const_declContext> const_decl() {
			return getRuleContexts(Const_declContext.class);
		}
		public Const_declContext const_decl(int i) {
			return getRuleContext(Const_declContext.class,i);
		}
		public Const_decl_listContext(ParserRuleContext parent, int invokingState) {
			super(parent, invokingState);
		}
		@Override public int getRuleIndex() { return RULE_const_decl_list; }
	}

	public final Const_decl_listContext const_decl_list() throws RecognitionException {
		Const_decl_listContext _localctx = new Const_decl_listContext(_ctx, getState());
		enterRule(_localctx, 8, RULE_const_decl_list);
		int _la;
		try {
			enterOuterAlt(_localctx, 1);
			{
			setState(142); 
			_errHandler.sync(this);
			_la = _input.LA(1);
			do {
				{
				{
				setState(141);
				const_decl();
				}
				}
				setState(144); 
				_errHandler.sync(this);
				_la = _input.LA(1);
			} while ( _la==CONST );
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
	public static class Const_declContext extends ParserRuleContext {
		public TerminalNode CONST() { return getToken(BraKetParser.CONST, 0); }
		public Var_declContext var_decl() {
			return getRuleContext(Var_declContext.class,0);
		}
		public Const_declContext(ParserRuleContext parent, int invokingState) {
			super(parent, invokingState);
		}
		@Override public int getRuleIndex() { return RULE_const_decl; }
	}

	public final Const_declContext const_decl() throws RecognitionException {
		Const_declContext _localctx = new Const_declContext(_ctx, getState());
		enterRule(_localctx, 10, RULE_const_decl);
		try {
			enterOuterAlt(_localctx, 1);
			{
			setState(146);
			match(CONST);
			setState(147);
			var_decl();
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
	public static class Var_decl_listContext extends ParserRuleContext {
		public List<Var_declContext> var_decl() {
			return getRuleContexts(Var_declContext.class);
		}
		public Var_declContext var_decl(int i) {
			return getRuleContext(Var_declContext.class,i);
		}
		public Var_decl_listContext(ParserRuleContext parent, int invokingState) {
			super(parent, invokingState);
		}
		@Override public int getRuleIndex() { return RULE_var_decl_list; }
	}

	public final Var_decl_listContext var_decl_list() throws RecognitionException {
		Var_decl_listContext _localctx = new Var_decl_listContext(_ctx, getState());
		enterRule(_localctx, 12, RULE_var_decl_list);
		int _la;
		try {
			enterOuterAlt(_localctx, 1);
			{
			setState(150); 
			_errHandler.sync(this);
			_la = _input.LA(1);
			do {
				{
				{
				setState(149);
				var_decl();
				}
				}
				setState(152); 
				_errHandler.sync(this);
				_la = _input.LA(1);
			} while ( (((_la) & ~0x3f) == 0 && ((1L << _la) & 562949953421504L) != 0) );
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
	public static class Var_declContext extends ParserRuleContext {
		public TerminalNode IDENTIFIER() { return getToken(BraKetParser.IDENTIFIER, 0); }
		public TerminalNode ASSIGN() { return getToken(BraKetParser.ASSIGN, 0); }
		public ExpressionContext expression() {
			return getRuleContext(ExpressionContext.class,0);
		}
		public TerminalNode KET_IDENTIFIER() { return getToken(BraKetParser.KET_IDENTIFIER, 0); }
		public Num_expressionContext num_expression() {
			return getRuleContext(Num_expressionContext.class,0);
		}
		public TerminalNode BRA_IDENTIFIER() { return getToken(BraKetParser.BRA_IDENTIFIER, 0); }
		public Var_declContext(ParserRuleContext parent, int invokingState) {
			super(parent, invokingState);
		}
		@Override public int getRuleIndex() { return RULE_var_decl; }
	}

	public final Var_declContext var_decl() throws RecognitionException {
		Var_declContext _localctx = new Var_declContext(_ctx, getState());
		enterRule(_localctx, 14, RULE_var_decl);
		try {
			setState(163);
			_errHandler.sync(this);
			switch (_input.LA(1)) {
			case IDENTIFIER:
				enterOuterAlt(_localctx, 1);
				{
				setState(154);
				match(IDENTIFIER);
				setState(155);
				match(ASSIGN);
				setState(156);
				expression();
				}
				break;
			case KET_IDENTIFIER:
				enterOuterAlt(_localctx, 2);
				{
				setState(157);
				match(KET_IDENTIFIER);
				setState(158);
				match(ASSIGN);
				setState(159);
				num_expression();
				}
				break;
			case BRA_IDENTIFIER:
				enterOuterAlt(_localctx, 3);
				{
				setState(160);
				match(BRA_IDENTIFIER);
				setState(161);
				match(ASSIGN);
				setState(162);
				num_expression();
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
	public static class ValueContext extends ParserRuleContext {
		public TerminalNode INT() { return getToken(BraKetParser.INT, 0); }
		public TerminalNode FLOAT() { return getToken(BraKetParser.FLOAT, 0); }
		public TerminalNode CHAR() { return getToken(BraKetParser.CHAR, 0); }
		public TerminalNode STRING() { return getToken(BraKetParser.STRING, 0); }
		public ArrayContext array() {
			return getRuleContext(ArrayContext.class,0);
		}
		public StructContext struct() {
			return getRuleContext(StructContext.class,0);
		}
		public TerminalNode COMPLEX() { return getToken(BraKetParser.COMPLEX, 0); }
		public OpContext op() {
			return getRuleContext(OpContext.class,0);
		}
		public TerminalNode BOOL_FALSE() { return getToken(BraKetParser.BOOL_FALSE, 0); }
		public TerminalNode BOOL_TRUE() { return getToken(BraKetParser.BOOL_TRUE, 0); }
		public ValueContext(ParserRuleContext parent, int invokingState) {
			super(parent, invokingState);
		}
		@Override public int getRuleIndex() { return RULE_value; }
	}

	public final ValueContext value() throws RecognitionException {
		ValueContext _localctx = new ValueContext(_ctx, getState());
		enterRule(_localctx, 16, RULE_value);
		try {
			setState(175);
			_errHandler.sync(this);
			switch (_input.LA(1)) {
			case INT:
				enterOuterAlt(_localctx, 1);
				{
				setState(165);
				match(INT);
				}
				break;
			case FLOAT:
				enterOuterAlt(_localctx, 2);
				{
				setState(166);
				match(FLOAT);
				}
				break;
			case CHAR:
				enterOuterAlt(_localctx, 3);
				{
				setState(167);
				match(CHAR);
				}
				break;
			case STRING:
				enterOuterAlt(_localctx, 4);
				{
				setState(168);
				match(STRING);
				}
				break;
			case LSQUARE:
				enterOuterAlt(_localctx, 5);
				{
				setState(169);
				array();
				}
				break;
			case LCURLY:
				enterOuterAlt(_localctx, 6);
				{
				setState(170);
				struct();
				}
				break;
			case COMPLEX:
				enterOuterAlt(_localctx, 7);
				{
				setState(171);
				match(COMPLEX);
				}
				break;
			case LPAREN:
				enterOuterAlt(_localctx, 8);
				{
				setState(172);
				op();
				}
				break;
			case BOOL_FALSE:
				enterOuterAlt(_localctx, 9);
				{
				setState(173);
				match(BOOL_FALSE);
				}
				break;
			case BOOL_TRUE:
				enterOuterAlt(_localctx, 10);
				{
				setState(174);
				match(BOOL_TRUE);
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
	public static class Braket_vectorContext extends ParserRuleContext {
		public TerminalNode LPAREN() { return getToken(BraKetParser.LPAREN, 0); }
		public TerminalNode RPAREN() { return getToken(BraKetParser.RPAREN, 0); }
		public List<Braket_valueContext> braket_value() {
			return getRuleContexts(Braket_valueContext.class);
		}
		public Braket_valueContext braket_value(int i) {
			return getRuleContext(Braket_valueContext.class,i);
		}
		public List<TerminalNode> COMMA() { return getTokens(BraKetParser.COMMA); }
		public TerminalNode COMMA(int i) {
			return getToken(BraKetParser.COMMA, i);
		}
		public Braket_vectorContext(ParserRuleContext parent, int invokingState) {
			super(parent, invokingState);
		}
		@Override public int getRuleIndex() { return RULE_braket_vector; }
	}

	public final Braket_vectorContext braket_vector() throws RecognitionException {
		Braket_vectorContext _localctx = new Braket_vectorContext(_ctx, getState());
		enterRule(_localctx, 18, RULE_braket_vector);
		int _la;
		try {
			enterOuterAlt(_localctx, 1);
			{
			setState(177);
			match(LPAREN);
			{
			setState(178);
			braket_value();
			setState(183);
			_errHandler.sync(this);
			_la = _input.LA(1);
			while (_la==COMMA) {
				{
				{
				setState(179);
				match(COMMA);
				setState(180);
				braket_value();
				}
				}
				setState(185);
				_errHandler.sync(this);
				_la = _input.LA(1);
			}
			}
			setState(186);
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
	public static class Braket_valueContext extends ParserRuleContext {
		public TerminalNode ADD() { return getToken(BraKetParser.ADD, 0); }
		public TerminalNode INT() { return getToken(BraKetParser.INT, 0); }
		public TerminalNode SUB() { return getToken(BraKetParser.SUB, 0); }
		public TerminalNode FLOAT() { return getToken(BraKetParser.FLOAT, 0); }
		public TerminalNode COMPLEX() { return getToken(BraKetParser.COMPLEX, 0); }
		public Braket_valueContext(ParserRuleContext parent, int invokingState) {
			super(parent, invokingState);
		}
		@Override public int getRuleIndex() { return RULE_braket_value; }
	}

	public final Braket_valueContext braket_value() throws RecognitionException {
		Braket_valueContext _localctx = new Braket_valueContext(_ctx, getState());
		enterRule(_localctx, 20, RULE_braket_value);
		try {
			setState(199);
			_errHandler.sync(this);
			switch ( getInterpreter().adaptivePredict(_input,12,_ctx) ) {
			case 1:
				enterOuterAlt(_localctx, 1);
				{
				setState(188);
				match(ADD);
				setState(189);
				match(INT);
				}
				break;
			case 2:
				enterOuterAlt(_localctx, 2);
				{
				setState(190);
				match(SUB);
				setState(191);
				match(INT);
				}
				break;
			case 3:
				enterOuterAlt(_localctx, 3);
				{
				setState(192);
				match(INT);
				}
				break;
			case 4:
				enterOuterAlt(_localctx, 4);
				{
				setState(193);
				match(ADD);
				setState(194);
				match(FLOAT);
				}
				break;
			case 5:
				enterOuterAlt(_localctx, 5);
				{
				setState(195);
				match(SUB);
				setState(196);
				match(FLOAT);
				}
				break;
			case 6:
				enterOuterAlt(_localctx, 6);
				{
				setState(197);
				match(FLOAT);
				}
				break;
			case 7:
				enterOuterAlt(_localctx, 7);
				{
				setState(198);
				match(COMPLEX);
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
	public static class Braket_expressionContext extends ParserRuleContext {
		public Braket_termContext braket_term() {
			return getRuleContext(Braket_termContext.class,0);
		}
		public TerminalNode ADD() { return getToken(BraKetParser.ADD, 0); }
		public Braket_expressionContext braket_expression() {
			return getRuleContext(Braket_expressionContext.class,0);
		}
		public TerminalNode SUB() { return getToken(BraKetParser.SUB, 0); }
		public Braket_expressionContext(ParserRuleContext parent, int invokingState) {
			super(parent, invokingState);
		}
		@Override public int getRuleIndex() { return RULE_braket_expression; }
	}

	public final Braket_expressionContext braket_expression() throws RecognitionException {
		Braket_expressionContext _localctx = new Braket_expressionContext(_ctx, getState());
		enterRule(_localctx, 22, RULE_braket_expression);
		try {
			setState(210);
			_errHandler.sync(this);
			switch ( getInterpreter().adaptivePredict(_input,13,_ctx) ) {
			case 1:
				enterOuterAlt(_localctx, 1);
				{
				setState(201);
				braket_term();
				setState(202);
				match(ADD);
				setState(203);
				braket_expression();
				}
				break;
			case 2:
				enterOuterAlt(_localctx, 2);
				{
				setState(205);
				braket_term();
				setState(206);
				match(SUB);
				setState(207);
				braket_expression();
				}
				break;
			case 3:
				enterOuterAlt(_localctx, 3);
				{
				setState(209);
				braket_term();
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
	public static class Braket_termContext extends ParserRuleContext {
		public Braket_factorContext braket_factor() {
			return getRuleContext(Braket_factorContext.class,0);
		}
		public TerminalNode MUL() { return getToken(BraKetParser.MUL, 0); }
		public Braket_termContext braket_term() {
			return getRuleContext(Braket_termContext.class,0);
		}
		public TerminalNode DIV() { return getToken(BraKetParser.DIV, 0); }
		public TerminalNode MOD() { return getToken(BraKetParser.MOD, 0); }
		public TerminalNode EXP() { return getToken(BraKetParser.EXP, 0); }
		public Braket_termContext(ParserRuleContext parent, int invokingState) {
			super(parent, invokingState);
		}
		@Override public int getRuleIndex() { return RULE_braket_term; }
	}

	public final Braket_termContext braket_term() throws RecognitionException {
		Braket_termContext _localctx = new Braket_termContext(_ctx, getState());
		enterRule(_localctx, 24, RULE_braket_term);
		try {
			setState(229);
			_errHandler.sync(this);
			switch ( getInterpreter().adaptivePredict(_input,14,_ctx) ) {
			case 1:
				enterOuterAlt(_localctx, 1);
				{
				setState(212);
				braket_factor();
				setState(213);
				match(MUL);
				setState(214);
				braket_term();
				}
				break;
			case 2:
				enterOuterAlt(_localctx, 2);
				{
				setState(216);
				braket_factor();
				setState(217);
				match(DIV);
				setState(218);
				braket_term();
				}
				break;
			case 3:
				enterOuterAlt(_localctx, 3);
				{
				setState(220);
				braket_factor();
				setState(221);
				match(MOD);
				setState(222);
				braket_term();
				}
				break;
			case 4:
				enterOuterAlt(_localctx, 4);
				{
				setState(224);
				braket_factor();
				setState(225);
				match(EXP);
				setState(226);
				braket_term();
				}
				break;
			case 5:
				enterOuterAlt(_localctx, 5);
				{
				setState(228);
				braket_factor();
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
	public static class Braket_factorContext extends ParserRuleContext {
		public TerminalNode LPAREN() { return getToken(BraKetParser.LPAREN, 0); }
		public Braket_expressionContext braket_expression() {
			return getRuleContext(Braket_expressionContext.class,0);
		}
		public TerminalNode RPAREN() { return getToken(BraKetParser.RPAREN, 0); }
		public TerminalNode COMPLEX() { return getToken(BraKetParser.COMPLEX, 0); }
		public TerminalNode ADD() { return getToken(BraKetParser.ADD, 0); }
		public Braket_factorContext braket_factor() {
			return getRuleContext(Braket_factorContext.class,0);
		}
		public TerminalNode SUB() { return getToken(BraKetParser.SUB, 0); }
		public TerminalNode INT() { return getToken(BraKetParser.INT, 0); }
		public TerminalNode FLOAT() { return getToken(BraKetParser.FLOAT, 0); }
		public TerminalNode IDENTIFIER() { return getToken(BraKetParser.IDENTIFIER, 0); }
		public Braket_factorContext(ParserRuleContext parent, int invokingState) {
			super(parent, invokingState);
		}
		@Override public int getRuleIndex() { return RULE_braket_factor; }
	}

	public final Braket_factorContext braket_factor() throws RecognitionException {
		Braket_factorContext _localctx = new Braket_factorContext(_ctx, getState());
		enterRule(_localctx, 26, RULE_braket_factor);
		try {
			setState(243);
			_errHandler.sync(this);
			switch (_input.LA(1)) {
			case LPAREN:
				enterOuterAlt(_localctx, 1);
				{
				setState(231);
				match(LPAREN);
				setState(232);
				braket_expression();
				setState(233);
				match(RPAREN);
				}
				break;
			case COMPLEX:
				enterOuterAlt(_localctx, 2);
				{
				setState(235);
				match(COMPLEX);
				}
				break;
			case ADD:
				enterOuterAlt(_localctx, 3);
				{
				setState(236);
				match(ADD);
				setState(237);
				braket_factor();
				}
				break;
			case SUB:
				enterOuterAlt(_localctx, 4);
				{
				setState(238);
				match(SUB);
				setState(239);
				braket_factor();
				}
				break;
			case INT:
				enterOuterAlt(_localctx, 5);
				{
				setState(240);
				match(INT);
				}
				break;
			case FLOAT:
				enterOuterAlt(_localctx, 6);
				{
				setState(241);
				match(FLOAT);
				}
				break;
			case IDENTIFIER:
				enterOuterAlt(_localctx, 7);
				{
				setState(242);
				match(IDENTIFIER);
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
	public static class ArrayContext extends ParserRuleContext {
		public TerminalNode LSQUARE() { return getToken(BraKetParser.LSQUARE, 0); }
		public TerminalNode RSQUARE() { return getToken(BraKetParser.RSQUARE, 0); }
		public List<ExpressionContext> expression() {
			return getRuleContexts(ExpressionContext.class);
		}
		public ExpressionContext expression(int i) {
			return getRuleContext(ExpressionContext.class,i);
		}
		public List<TerminalNode> COMMA() { return getTokens(BraKetParser.COMMA); }
		public TerminalNode COMMA(int i) {
			return getToken(BraKetParser.COMMA, i);
		}
		public ArrayContext(ParserRuleContext parent, int invokingState) {
			super(parent, invokingState);
		}
		@Override public int getRuleIndex() { return RULE_array; }
	}

	public final ArrayContext array() throws RecognitionException {
		ArrayContext _localctx = new ArrayContext(_ctx, getState());
		enterRule(_localctx, 28, RULE_array);
		int _la;
		try {
			enterOuterAlt(_localctx, 1);
			{
			setState(245);
			match(LSQUARE);
			setState(254);
			_errHandler.sync(this);
			_la = _input.LA(1);
			if ((((_la) & ~0x3f) == 0 && ((1L << _la) & 586589506904000L) != 0)) {
				{
				setState(246);
				expression();
				setState(251);
				_errHandler.sync(this);
				_la = _input.LA(1);
				while (_la==COMMA) {
					{
					{
					setState(247);
					match(COMMA);
					setState(248);
					expression();
					}
					}
					setState(253);
					_errHandler.sync(this);
					_la = _input.LA(1);
				}
				}
			}

			setState(256);
			match(RSQUARE);
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
	public static class StructContext extends ParserRuleContext {
		public TerminalNode LCURLY() { return getToken(BraKetParser.LCURLY, 0); }
		public TerminalNode RCURLY() { return getToken(BraKetParser.RCURLY, 0); }
		public Struct_valueContext struct_value() {
			return getRuleContext(Struct_valueContext.class,0);
		}
		public StructContext(ParserRuleContext parent, int invokingState) {
			super(parent, invokingState);
		}
		@Override public int getRuleIndex() { return RULE_struct; }
	}

	public final StructContext struct() throws RecognitionException {
		StructContext _localctx = new StructContext(_ctx, getState());
		enterRule(_localctx, 30, RULE_struct);
		int _la;
		try {
			enterOuterAlt(_localctx, 1);
			{
			setState(258);
			match(LCURLY);
			setState(260);
			_errHandler.sync(this);
			_la = _input.LA(1);
			if ((((_la) & ~0x3f) == 0 && ((1L << _la) & 562949961810112L) != 0)) {
				{
				setState(259);
				struct_value();
				}
			}

			setState(262);
			match(RCURLY);
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
	public static class Struct_valueContext extends ParserRuleContext {
		public Var_declContext var_decl() {
			return getRuleContext(Var_declContext.class,0);
		}
		public TerminalNode COMMA() { return getToken(BraKetParser.COMMA, 0); }
		public Struct_valueContext struct_value() {
			return getRuleContext(Struct_valueContext.class,0);
		}
		public Func_declContext func_decl() {
			return getRuleContext(Func_declContext.class,0);
		}
		public Struct_valueContext(ParserRuleContext parent, int invokingState) {
			super(parent, invokingState);
		}
		@Override public int getRuleIndex() { return RULE_struct_value; }
	}

	public final Struct_valueContext struct_value() throws RecognitionException {
		Struct_valueContext _localctx = new Struct_valueContext(_ctx, getState());
		enterRule(_localctx, 32, RULE_struct_value);
		try {
			setState(274);
			_errHandler.sync(this);
			switch ( getInterpreter().adaptivePredict(_input,19,_ctx) ) {
			case 1:
				enterOuterAlt(_localctx, 1);
				{
				setState(264);
				var_decl();
				setState(265);
				match(COMMA);
				setState(266);
				struct_value();
				}
				break;
			case 2:
				enterOuterAlt(_localctx, 2);
				{
				setState(268);
				func_decl();
				setState(269);
				match(COMMA);
				setState(270);
				struct_value();
				}
				break;
			case 3:
				enterOuterAlt(_localctx, 3);
				{
				setState(272);
				var_decl();
				}
				break;
			case 4:
				enterOuterAlt(_localctx, 4);
				{
				setState(273);
				func_decl();
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
	public static class OpContext extends ParserRuleContext {
		public TerminalNode LPAREN() { return getToken(BraKetParser.LPAREN, 0); }
		public List<Braket_vectorContext> braket_vector() {
			return getRuleContexts(Braket_vectorContext.class);
		}
		public Braket_vectorContext braket_vector(int i) {
			return getRuleContext(Braket_vectorContext.class,i);
		}
		public TerminalNode RPAREN() { return getToken(BraKetParser.RPAREN, 0); }
		public List<TerminalNode> COMMA() { return getTokens(BraKetParser.COMMA); }
		public TerminalNode COMMA(int i) {
			return getToken(BraKetParser.COMMA, i);
		}
		public OpContext(ParserRuleContext parent, int invokingState) {
			super(parent, invokingState);
		}
		@Override public int getRuleIndex() { return RULE_op; }
	}

	public final OpContext op() throws RecognitionException {
		OpContext _localctx = new OpContext(_ctx, getState());
		enterRule(_localctx, 34, RULE_op);
		int _la;
		try {
			enterOuterAlt(_localctx, 1);
			{
			setState(276);
			match(LPAREN);
			setState(277);
			braket_vector();
			setState(282);
			_errHandler.sync(this);
			_la = _input.LA(1);
			while (_la==COMMA) {
				{
				{
				setState(278);
				match(COMMA);
				setState(279);
				braket_vector();
				}
				}
				setState(284);
				_errHandler.sync(this);
				_la = _input.LA(1);
			}
			setState(285);
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
	public static class Statement_listContext extends ParserRuleContext {
		public List<StatementContext> statement() {
			return getRuleContexts(StatementContext.class);
		}
		public StatementContext statement(int i) {
			return getRuleContext(StatementContext.class,i);
		}
		public Statement_listContext(ParserRuleContext parent, int invokingState) {
			super(parent, invokingState);
		}
		@Override public int getRuleIndex() { return RULE_statement_list; }
	}

	public final Statement_listContext statement_list() throws RecognitionException {
		Statement_listContext _localctx = new Statement_listContext(_ctx, getState());
		enterRule(_localctx, 36, RULE_statement_list);
		int _la;
		try {
			enterOuterAlt(_localctx, 1);
			{
			setState(288); 
			_errHandler.sync(this);
			_la = _input.LA(1);
			do {
				{
				{
				setState(287);
				statement();
				}
				}
				setState(290); 
				_errHandler.sync(this);
				_la = _input.LA(1);
			} while ( (((_la) & ~0x3f) == 0 && ((1L << _la) & 562949954363584L) != 0) );
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
	public static class StatementContext extends ParserRuleContext {
		public Assign_statementContext assign_statement() {
			return getRuleContext(Assign_statementContext.class,0);
		}
		public Func_call_statementContext func_call_statement() {
			return getRuleContext(Func_call_statementContext.class,0);
		}
		public Return_statementContext return_statement() {
			return getRuleContext(Return_statementContext.class,0);
		}
		public If_statementContext if_statement() {
			return getRuleContext(If_statementContext.class,0);
		}
		public For_statementContext for_statement() {
			return getRuleContext(For_statementContext.class,0);
		}
		public While_statementContext while_statement() {
			return getRuleContext(While_statementContext.class,0);
		}
		public Do_statementContext do_statement() {
			return getRuleContext(Do_statementContext.class,0);
		}
		public StatementContext(ParserRuleContext parent, int invokingState) {
			super(parent, invokingState);
		}
		@Override public int getRuleIndex() { return RULE_statement; }
	}

	public final StatementContext statement() throws RecognitionException {
		StatementContext _localctx = new StatementContext(_ctx, getState());
		enterRule(_localctx, 38, RULE_statement);
		try {
			setState(299);
			_errHandler.sync(this);
			switch ( getInterpreter().adaptivePredict(_input,22,_ctx) ) {
			case 1:
				enterOuterAlt(_localctx, 1);
				{
				setState(292);
				assign_statement();
				}
				break;
			case 2:
				enterOuterAlt(_localctx, 2);
				{
				setState(293);
				func_call_statement();
				}
				break;
			case 3:
				enterOuterAlt(_localctx, 3);
				{
				setState(294);
				return_statement();
				}
				break;
			case 4:
				enterOuterAlt(_localctx, 4);
				{
				setState(295);
				if_statement();
				}
				break;
			case 5:
				enterOuterAlt(_localctx, 5);
				{
				setState(296);
				for_statement();
				}
				break;
			case 6:
				enterOuterAlt(_localctx, 6);
				{
				setState(297);
				while_statement();
				}
				break;
			case 7:
				enterOuterAlt(_localctx, 7);
				{
				setState(298);
				do_statement();
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
	public static class Assign_statementContext extends ParserRuleContext {
		public Var_declContext var_decl() {
			return getRuleContext(Var_declContext.class,0);
		}
		public Array_accessContext array_access() {
			return getRuleContext(Array_accessContext.class,0);
		}
		public TerminalNode ASSIGN() { return getToken(BraKetParser.ASSIGN, 0); }
		public ExpressionContext expression() {
			return getRuleContext(ExpressionContext.class,0);
		}
		public Struct_accessContext struct_access() {
			return getRuleContext(Struct_accessContext.class,0);
		}
		public Assign_statementContext(ParserRuleContext parent, int invokingState) {
			super(parent, invokingState);
		}
		@Override public int getRuleIndex() { return RULE_assign_statement; }
	}

	public final Assign_statementContext assign_statement() throws RecognitionException {
		Assign_statementContext _localctx = new Assign_statementContext(_ctx, getState());
		enterRule(_localctx, 40, RULE_assign_statement);
		try {
			setState(310);
			_errHandler.sync(this);
			switch ( getInterpreter().adaptivePredict(_input,23,_ctx) ) {
			case 1:
				enterOuterAlt(_localctx, 1);
				{
				setState(301);
				var_decl();
				}
				break;
			case 2:
				enterOuterAlt(_localctx, 2);
				{
				setState(302);
				array_access();
				setState(303);
				match(ASSIGN);
				setState(304);
				expression();
				}
				break;
			case 3:
				enterOuterAlt(_localctx, 3);
				{
				setState(306);
				struct_access();
				setState(307);
				match(ASSIGN);
				setState(308);
				expression();
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
	public static class Func_call_statementContext extends ParserRuleContext {
		public TerminalNode IDENTIFIER() { return getToken(BraKetParser.IDENTIFIER, 0); }
		public TerminalNode LPAREN() { return getToken(BraKetParser.LPAREN, 0); }
		public TerminalNode RPAREN() { return getToken(BraKetParser.RPAREN, 0); }
		public Arg_listContext arg_list() {
			return getRuleContext(Arg_listContext.class,0);
		}
		public Func_call_statementContext(ParserRuleContext parent, int invokingState) {
			super(parent, invokingState);
		}
		@Override public int getRuleIndex() { return RULE_func_call_statement; }
	}

	public final Func_call_statementContext func_call_statement() throws RecognitionException {
		Func_call_statementContext _localctx = new Func_call_statementContext(_ctx, getState());
		enterRule(_localctx, 42, RULE_func_call_statement);
		int _la;
		try {
			enterOuterAlt(_localctx, 1);
			{
			setState(312);
			match(IDENTIFIER);
			setState(313);
			match(LPAREN);
			setState(315);
			_errHandler.sync(this);
			_la = _input.LA(1);
			if ((((_la) & ~0x3f) == 0 && ((1L << _la) & 586039700758464L) != 0)) {
				{
				setState(314);
				arg_list();
				}
			}

			setState(317);
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
	public static class Arg_listContext extends ParserRuleContext {
		public ArgContext arg() {
			return getRuleContext(ArgContext.class,0);
		}
		public List<TerminalNode> COMMA() { return getTokens(BraKetParser.COMMA); }
		public TerminalNode COMMA(int i) {
			return getToken(BraKetParser.COMMA, i);
		}
		public List<Arg_listContext> arg_list() {
			return getRuleContexts(Arg_listContext.class);
		}
		public Arg_listContext arg_list(int i) {
			return getRuleContext(Arg_listContext.class,i);
		}
		public Arg_listContext(ParserRuleContext parent, int invokingState) {
			super(parent, invokingState);
		}
		@Override public int getRuleIndex() { return RULE_arg_list; }
	}

	public final Arg_listContext arg_list() throws RecognitionException {
		Arg_listContext _localctx = new Arg_listContext(_ctx, getState());
		enterRule(_localctx, 44, RULE_arg_list);
		try {
			int _alt;
			enterOuterAlt(_localctx, 1);
			{
			setState(319);
			arg();
			setState(324);
			_errHandler.sync(this);
			_alt = getInterpreter().adaptivePredict(_input,25,_ctx);
			while ( _alt!=2 && _alt!=org.antlr.v4.runtime.atn.ATN.INVALID_ALT_NUMBER ) {
				if ( _alt==1 ) {
					{
					{
					setState(320);
					match(COMMA);
					setState(321);
					arg_list();
					}
					} 
				}
				setState(326);
				_errHandler.sync(this);
				_alt = getInterpreter().adaptivePredict(_input,25,_ctx);
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
	public static class ArgContext extends ParserRuleContext {
		public Assign_statementContext assign_statement() {
			return getRuleContext(Assign_statementContext.class,0);
		}
		public TerminalNode IDENTIFIER() { return getToken(BraKetParser.IDENTIFIER, 0); }
		public ValueContext value() {
			return getRuleContext(ValueContext.class,0);
		}
		public Array_accessContext array_access() {
			return getRuleContext(Array_accessContext.class,0);
		}
		public Struct_accessContext struct_access() {
			return getRuleContext(Struct_accessContext.class,0);
		}
		public ArgContext(ParserRuleContext parent, int invokingState) {
			super(parent, invokingState);
		}
		@Override public int getRuleIndex() { return RULE_arg; }
	}

	public final ArgContext arg() throws RecognitionException {
		ArgContext _localctx = new ArgContext(_ctx, getState());
		enterRule(_localctx, 46, RULE_arg);
		try {
			setState(332);
			_errHandler.sync(this);
			switch ( getInterpreter().adaptivePredict(_input,26,_ctx) ) {
			case 1:
				enterOuterAlt(_localctx, 1);
				{
				setState(327);
				assign_statement();
				}
				break;
			case 2:
				enterOuterAlt(_localctx, 2);
				{
				setState(328);
				match(IDENTIFIER);
				}
				break;
			case 3:
				enterOuterAlt(_localctx, 3);
				{
				setState(329);
				value();
				}
				break;
			case 4:
				enterOuterAlt(_localctx, 4);
				{
				setState(330);
				array_access();
				}
				break;
			case 5:
				enterOuterAlt(_localctx, 5);
				{
				setState(331);
				struct_access();
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
	public static class Return_statementContext extends ParserRuleContext {
		public TerminalNode RETURN() { return getToken(BraKetParser.RETURN, 0); }
		public ExpressionContext expression() {
			return getRuleContext(ExpressionContext.class,0);
		}
		public Return_statementContext(ParserRuleContext parent, int invokingState) {
			super(parent, invokingState);
		}
		@Override public int getRuleIndex() { return RULE_return_statement; }
	}

	public final Return_statementContext return_statement() throws RecognitionException {
		Return_statementContext _localctx = new Return_statementContext(_ctx, getState());
		enterRule(_localctx, 48, RULE_return_statement);
		try {
			enterOuterAlt(_localctx, 1);
			{
			setState(334);
			match(RETURN);
			setState(335);
			expression();
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
	public static class If_statementContext extends ParserRuleContext {
		public TerminalNode IF() { return getToken(BraKetParser.IF, 0); }
		public TerminalNode LPAREN() { return getToken(BraKetParser.LPAREN, 0); }
		public Bool_expressionContext bool_expression() {
			return getRuleContext(Bool_expressionContext.class,0);
		}
		public TerminalNode RPAREN() { return getToken(BraKetParser.RPAREN, 0); }
		public TerminalNode LCURLY() { return getToken(BraKetParser.LCURLY, 0); }
		public Statement_listContext statement_list() {
			return getRuleContext(Statement_listContext.class,0);
		}
		public TerminalNode RCURLY() { return getToken(BraKetParser.RCURLY, 0); }
		public List<ElifContext> elif() {
			return getRuleContexts(ElifContext.class);
		}
		public ElifContext elif(int i) {
			return getRuleContext(ElifContext.class,i);
		}
		public ElseContext else_() {
			return getRuleContext(ElseContext.class,0);
		}
		public If_statementContext(ParserRuleContext parent, int invokingState) {
			super(parent, invokingState);
		}
		@Override public int getRuleIndex() { return RULE_if_statement; }
	}

	public final If_statementContext if_statement() throws RecognitionException {
		If_statementContext _localctx = new If_statementContext(_ctx, getState());
		enterRule(_localctx, 50, RULE_if_statement);
		int _la;
		try {
			enterOuterAlt(_localctx, 1);
			{
			setState(337);
			match(IF);
			setState(338);
			match(LPAREN);
			setState(339);
			bool_expression();
			setState(340);
			match(RPAREN);
			setState(341);
			match(LCURLY);
			setState(342);
			statement_list();
			setState(343);
			match(RCURLY);
			setState(347);
			_errHandler.sync(this);
			_la = _input.LA(1);
			while (_la==ELIF) {
				{
				{
				setState(344);
				elif();
				}
				}
				setState(349);
				_errHandler.sync(this);
				_la = _input.LA(1);
			}
			setState(351);
			_errHandler.sync(this);
			_la = _input.LA(1);
			if (_la==ELSE) {
				{
				setState(350);
				else_();
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
	public static class ElifContext extends ParserRuleContext {
		public TerminalNode ELIF() { return getToken(BraKetParser.ELIF, 0); }
		public TerminalNode LPAREN() { return getToken(BraKetParser.LPAREN, 0); }
		public Bool_expressionContext bool_expression() {
			return getRuleContext(Bool_expressionContext.class,0);
		}
		public TerminalNode RPAREN() { return getToken(BraKetParser.RPAREN, 0); }
		public TerminalNode LCURLY() { return getToken(BraKetParser.LCURLY, 0); }
		public Statement_listContext statement_list() {
			return getRuleContext(Statement_listContext.class,0);
		}
		public TerminalNode RCURLY() { return getToken(BraKetParser.RCURLY, 0); }
		public ElifContext(ParserRuleContext parent, int invokingState) {
			super(parent, invokingState);
		}
		@Override public int getRuleIndex() { return RULE_elif; }
	}

	public final ElifContext elif() throws RecognitionException {
		ElifContext _localctx = new ElifContext(_ctx, getState());
		enterRule(_localctx, 52, RULE_elif);
		try {
			enterOuterAlt(_localctx, 1);
			{
			setState(353);
			match(ELIF);
			setState(354);
			match(LPAREN);
			setState(355);
			bool_expression();
			setState(356);
			match(RPAREN);
			setState(357);
			match(LCURLY);
			setState(358);
			statement_list();
			setState(359);
			match(RCURLY);
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
	public static class ElseContext extends ParserRuleContext {
		public TerminalNode ELSE() { return getToken(BraKetParser.ELSE, 0); }
		public TerminalNode LCURLY() { return getToken(BraKetParser.LCURLY, 0); }
		public Statement_listContext statement_list() {
			return getRuleContext(Statement_listContext.class,0);
		}
		public TerminalNode RCURLY() { return getToken(BraKetParser.RCURLY, 0); }
		public ElseContext(ParserRuleContext parent, int invokingState) {
			super(parent, invokingState);
		}
		@Override public int getRuleIndex() { return RULE_else; }
	}

	public final ElseContext else_() throws RecognitionException {
		ElseContext _localctx = new ElseContext(_ctx, getState());
		enterRule(_localctx, 54, RULE_else);
		try {
			enterOuterAlt(_localctx, 1);
			{
			setState(361);
			match(ELSE);
			setState(362);
			match(LCURLY);
			setState(363);
			statement_list();
			setState(364);
			match(RCURLY);
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
	public static class For_statementContext extends ParserRuleContext {
		public TerminalNode FOR() { return getToken(BraKetParser.FOR, 0); }
		public TerminalNode LPAREN() { return getToken(BraKetParser.LPAREN, 0); }
		public List<Assign_statementContext> assign_statement() {
			return getRuleContexts(Assign_statementContext.class);
		}
		public Assign_statementContext assign_statement(int i) {
			return getRuleContext(Assign_statementContext.class,i);
		}
		public List<TerminalNode> SEMICOLON() { return getTokens(BraKetParser.SEMICOLON); }
		public TerminalNode SEMICOLON(int i) {
			return getToken(BraKetParser.SEMICOLON, i);
		}
		public Bool_expressionContext bool_expression() {
			return getRuleContext(Bool_expressionContext.class,0);
		}
		public TerminalNode RPAREN() { return getToken(BraKetParser.RPAREN, 0); }
		public TerminalNode LCURLY() { return getToken(BraKetParser.LCURLY, 0); }
		public Statement_listContext statement_list() {
			return getRuleContext(Statement_listContext.class,0);
		}
		public TerminalNode RCURLY() { return getToken(BraKetParser.RCURLY, 0); }
		public For_statementContext(ParserRuleContext parent, int invokingState) {
			super(parent, invokingState);
		}
		@Override public int getRuleIndex() { return RULE_for_statement; }
	}

	public final For_statementContext for_statement() throws RecognitionException {
		For_statementContext _localctx = new For_statementContext(_ctx, getState());
		enterRule(_localctx, 56, RULE_for_statement);
		try {
			enterOuterAlt(_localctx, 1);
			{
			setState(366);
			match(FOR);
			setState(367);
			match(LPAREN);
			setState(368);
			assign_statement();
			setState(369);
			match(SEMICOLON);
			setState(370);
			bool_expression();
			setState(371);
			match(SEMICOLON);
			setState(372);
			assign_statement();
			setState(373);
			match(RPAREN);
			setState(374);
			match(LCURLY);
			setState(375);
			statement_list();
			setState(376);
			match(RCURLY);
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
	public static class While_statementContext extends ParserRuleContext {
		public TerminalNode WHILE() { return getToken(BraKetParser.WHILE, 0); }
		public TerminalNode LPAREN() { return getToken(BraKetParser.LPAREN, 0); }
		public Bool_expressionContext bool_expression() {
			return getRuleContext(Bool_expressionContext.class,0);
		}
		public TerminalNode RPAREN() { return getToken(BraKetParser.RPAREN, 0); }
		public TerminalNode LCURLY() { return getToken(BraKetParser.LCURLY, 0); }
		public Statement_listContext statement_list() {
			return getRuleContext(Statement_listContext.class,0);
		}
		public TerminalNode RCURLY() { return getToken(BraKetParser.RCURLY, 0); }
		public While_statementContext(ParserRuleContext parent, int invokingState) {
			super(parent, invokingState);
		}
		@Override public int getRuleIndex() { return RULE_while_statement; }
	}

	public final While_statementContext while_statement() throws RecognitionException {
		While_statementContext _localctx = new While_statementContext(_ctx, getState());
		enterRule(_localctx, 58, RULE_while_statement);
		try {
			enterOuterAlt(_localctx, 1);
			{
			setState(378);
			match(WHILE);
			setState(379);
			match(LPAREN);
			setState(380);
			bool_expression();
			setState(381);
			match(RPAREN);
			setState(382);
			match(LCURLY);
			setState(383);
			statement_list();
			setState(384);
			match(RCURLY);
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
	public static class Do_statementContext extends ParserRuleContext {
		public TerminalNode DO() { return getToken(BraKetParser.DO, 0); }
		public TerminalNode LCURLY() { return getToken(BraKetParser.LCURLY, 0); }
		public Statement_listContext statement_list() {
			return getRuleContext(Statement_listContext.class,0);
		}
		public TerminalNode RCURLY() { return getToken(BraKetParser.RCURLY, 0); }
		public TerminalNode WHILE() { return getToken(BraKetParser.WHILE, 0); }
		public TerminalNode LPAREN() { return getToken(BraKetParser.LPAREN, 0); }
		public Bool_expressionContext bool_expression() {
			return getRuleContext(Bool_expressionContext.class,0);
		}
		public TerminalNode RPAREN() { return getToken(BraKetParser.RPAREN, 0); }
		public Do_statementContext(ParserRuleContext parent, int invokingState) {
			super(parent, invokingState);
		}
		@Override public int getRuleIndex() { return RULE_do_statement; }
	}

	public final Do_statementContext do_statement() throws RecognitionException {
		Do_statementContext _localctx = new Do_statementContext(_ctx, getState());
		enterRule(_localctx, 60, RULE_do_statement);
		try {
			enterOuterAlt(_localctx, 1);
			{
			setState(386);
			match(DO);
			setState(387);
			match(LCURLY);
			setState(388);
			statement_list();
			setState(389);
			match(RCURLY);
			setState(390);
			match(WHILE);
			setState(391);
			match(LPAREN);
			setState(392);
			bool_expression();
			setState(393);
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
	public static class ExpressionContext extends ParserRuleContext {
		public TerminalNode IDENTIFIER() { return getToken(BraKetParser.IDENTIFIER, 0); }
		public Num_expressionContext num_expression() {
			return getRuleContext(Num_expressionContext.class,0);
		}
		public ArrayContext array() {
			return getRuleContext(ArrayContext.class,0);
		}
		public StructContext struct() {
			return getRuleContext(StructContext.class,0);
		}
		public Array_accessContext array_access() {
			return getRuleContext(Array_accessContext.class,0);
		}
		public Struct_accessContext struct_access() {
			return getRuleContext(Struct_accessContext.class,0);
		}
		public Dirac_expressionContext dirac_expression() {
			return getRuleContext(Dirac_expressionContext.class,0);
		}
		public Bool_expressionContext bool_expression() {
			return getRuleContext(Bool_expressionContext.class,0);
		}
		public Func_call_statementContext func_call_statement() {
			return getRuleContext(Func_call_statementContext.class,0);
		}
		public String_expressionContext string_expression() {
			return getRuleContext(String_expressionContext.class,0);
		}
		public ExpressionContext(ParserRuleContext parent, int invokingState) {
			super(parent, invokingState);
		}
		@Override public int getRuleIndex() { return RULE_expression; }
	}

	public final ExpressionContext expression() throws RecognitionException {
		ExpressionContext _localctx = new ExpressionContext(_ctx, getState());
		enterRule(_localctx, 62, RULE_expression);
		try {
			setState(405);
			_errHandler.sync(this);
			switch ( getInterpreter().adaptivePredict(_input,29,_ctx) ) {
			case 1:
				enterOuterAlt(_localctx, 1);
				{
				setState(395);
				match(IDENTIFIER);
				}
				break;
			case 2:
				enterOuterAlt(_localctx, 2);
				{
				setState(396);
				num_expression();
				}
				break;
			case 3:
				enterOuterAlt(_localctx, 3);
				{
				setState(397);
				array();
				}
				break;
			case 4:
				enterOuterAlt(_localctx, 4);
				{
				setState(398);
				struct();
				}
				break;
			case 5:
				enterOuterAlt(_localctx, 5);
				{
				setState(399);
				array_access();
				}
				break;
			case 6:
				enterOuterAlt(_localctx, 6);
				{
				setState(400);
				struct_access();
				}
				break;
			case 7:
				enterOuterAlt(_localctx, 7);
				{
				setState(401);
				dirac_expression(0);
				}
				break;
			case 8:
				enterOuterAlt(_localctx, 8);
				{
				setState(402);
				bool_expression();
				}
				break;
			case 9:
				enterOuterAlt(_localctx, 9);
				{
				setState(403);
				func_call_statement();
				}
				break;
			case 10:
				enterOuterAlt(_localctx, 10);
				{
				setState(404);
				string_expression(0);
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
	public static class String_expressionContext extends ParserRuleContext {
		public TerminalNode STRING() { return getToken(BraKetParser.STRING, 0); }
		public TerminalNode IDENTIFIER() { return getToken(BraKetParser.IDENTIFIER, 0); }
		public List<String_expressionContext> string_expression() {
			return getRuleContexts(String_expressionContext.class);
		}
		public String_expressionContext string_expression(int i) {
			return getRuleContext(String_expressionContext.class,i);
		}
		public TerminalNode ADD() { return getToken(BraKetParser.ADD, 0); }
		public String_expressionContext(ParserRuleContext parent, int invokingState) {
			super(parent, invokingState);
		}
		@Override public int getRuleIndex() { return RULE_string_expression; }
	}

	public final String_expressionContext string_expression() throws RecognitionException {
		return string_expression(0);
	}

	private String_expressionContext string_expression(int _p) throws RecognitionException {
		ParserRuleContext _parentctx = _ctx;
		int _parentState = getState();
		String_expressionContext _localctx = new String_expressionContext(_ctx, _parentState);
		String_expressionContext _prevctx = _localctx;
		int _startState = 64;
		enterRecursionRule(_localctx, 64, RULE_string_expression, _p);
		try {
			int _alt;
			enterOuterAlt(_localctx, 1);
			{
			setState(410);
			_errHandler.sync(this);
			switch (_input.LA(1)) {
			case STRING:
				{
				setState(408);
				match(STRING);
				}
				break;
			case IDENTIFIER:
				{
				setState(409);
				match(IDENTIFIER);
				}
				break;
			default:
				throw new NoViableAltException(this);
			}
			_ctx.stop = _input.LT(-1);
			setState(417);
			_errHandler.sync(this);
			_alt = getInterpreter().adaptivePredict(_input,31,_ctx);
			while ( _alt!=2 && _alt!=org.antlr.v4.runtime.atn.ATN.INVALID_ALT_NUMBER ) {
				if ( _alt==1 ) {
					if ( _parseListeners!=null ) triggerExitRuleEvent();
					_prevctx = _localctx;
					{
					{
					_localctx = new String_expressionContext(_parentctx, _parentState);
					pushNewRecursionContext(_localctx, _startState, RULE_string_expression);
					setState(412);
					if (!(precpred(_ctx, 3))) throw new FailedPredicateException(this, "precpred(_ctx, 3)");
					setState(413);
					match(ADD);
					setState(414);
					string_expression(4);
					}
					} 
				}
				setState(419);
				_errHandler.sync(this);
				_alt = getInterpreter().adaptivePredict(_input,31,_ctx);
			}
			}
		}
		catch (RecognitionException re) {
			_localctx.exception = re;
			_errHandler.reportError(this, re);
			_errHandler.recover(this, re);
		}
		finally {
			unrollRecursionContexts(_parentctx);
		}
		return _localctx;
	}

	@SuppressWarnings("CheckReturnValue")
	public static class Num_expressionContext extends ParserRuleContext {
		public Num_termContext num_term() {
			return getRuleContext(Num_termContext.class,0);
		}
		public TerminalNode ADD() { return getToken(BraKetParser.ADD, 0); }
		public Num_expressionContext num_expression() {
			return getRuleContext(Num_expressionContext.class,0);
		}
		public TerminalNode SUB() { return getToken(BraKetParser.SUB, 0); }
		public Num_expressionContext(ParserRuleContext parent, int invokingState) {
			super(parent, invokingState);
		}
		@Override public int getRuleIndex() { return RULE_num_expression; }
	}

	public final Num_expressionContext num_expression() throws RecognitionException {
		Num_expressionContext _localctx = new Num_expressionContext(_ctx, getState());
		enterRule(_localctx, 66, RULE_num_expression);
		try {
			setState(429);
			_errHandler.sync(this);
			switch ( getInterpreter().adaptivePredict(_input,32,_ctx) ) {
			case 1:
				enterOuterAlt(_localctx, 1);
				{
				setState(420);
				num_term();
				setState(421);
				match(ADD);
				setState(422);
				num_expression();
				}
				break;
			case 2:
				enterOuterAlt(_localctx, 2);
				{
				setState(424);
				num_term();
				setState(425);
				match(SUB);
				setState(426);
				num_expression();
				}
				break;
			case 3:
				enterOuterAlt(_localctx, 3);
				{
				setState(428);
				num_term();
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
	public static class Num_termContext extends ParserRuleContext {
		public Num_factorContext num_factor() {
			return getRuleContext(Num_factorContext.class,0);
		}
		public TerminalNode MUL() { return getToken(BraKetParser.MUL, 0); }
		public Num_termContext num_term() {
			return getRuleContext(Num_termContext.class,0);
		}
		public TerminalNode DIV() { return getToken(BraKetParser.DIV, 0); }
		public TerminalNode MOD() { return getToken(BraKetParser.MOD, 0); }
		public TerminalNode EXP() { return getToken(BraKetParser.EXP, 0); }
		public Num_termContext(ParserRuleContext parent, int invokingState) {
			super(parent, invokingState);
		}
		@Override public int getRuleIndex() { return RULE_num_term; }
	}

	public final Num_termContext num_term() throws RecognitionException {
		Num_termContext _localctx = new Num_termContext(_ctx, getState());
		enterRule(_localctx, 68, RULE_num_term);
		try {
			setState(448);
			_errHandler.sync(this);
			switch ( getInterpreter().adaptivePredict(_input,33,_ctx) ) {
			case 1:
				enterOuterAlt(_localctx, 1);
				{
				setState(431);
				num_factor();
				setState(432);
				match(MUL);
				setState(433);
				num_term();
				}
				break;
			case 2:
				enterOuterAlt(_localctx, 2);
				{
				setState(435);
				num_factor();
				setState(436);
				match(DIV);
				setState(437);
				num_term();
				}
				break;
			case 3:
				enterOuterAlt(_localctx, 3);
				{
				setState(439);
				num_factor();
				setState(440);
				match(MOD);
				setState(441);
				num_term();
				}
				break;
			case 4:
				enterOuterAlt(_localctx, 4);
				{
				setState(443);
				num_factor();
				setState(444);
				match(EXP);
				setState(445);
				num_term();
				}
				break;
			case 5:
				enterOuterAlt(_localctx, 5);
				{
				setState(447);
				num_factor();
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
	public static class Num_factorContext extends ParserRuleContext {
		public TerminalNode LPAREN() { return getToken(BraKetParser.LPAREN, 0); }
		public Num_expressionContext num_expression() {
			return getRuleContext(Num_expressionContext.class,0);
		}
		public TerminalNode RPAREN() { return getToken(BraKetParser.RPAREN, 0); }
		public TerminalNode COMPLEX() { return getToken(BraKetParser.COMPLEX, 0); }
		public TerminalNode ADD() { return getToken(BraKetParser.ADD, 0); }
		public Num_factorContext num_factor() {
			return getRuleContext(Num_factorContext.class,0);
		}
		public TerminalNode SUB() { return getToken(BraKetParser.SUB, 0); }
		public TerminalNode INT() { return getToken(BraKetParser.INT, 0); }
		public TerminalNode FLOAT() { return getToken(BraKetParser.FLOAT, 0); }
		public TerminalNode CHAR() { return getToken(BraKetParser.CHAR, 0); }
		public Dirac_expressionContext dirac_expression() {
			return getRuleContext(Dirac_expressionContext.class,0);
		}
		public TerminalNode IDENTIFIER() { return getToken(BraKetParser.IDENTIFIER, 0); }
		public Num_factorContext(ParserRuleContext parent, int invokingState) {
			super(parent, invokingState);
		}
		@Override public int getRuleIndex() { return RULE_num_factor; }
	}

	public final Num_factorContext num_factor() throws RecognitionException {
		Num_factorContext _localctx = new Num_factorContext(_ctx, getState());
		enterRule(_localctx, 70, RULE_num_factor);
		try {
			setState(464);
			_errHandler.sync(this);
			switch ( getInterpreter().adaptivePredict(_input,34,_ctx) ) {
			case 1:
				enterOuterAlt(_localctx, 1);
				{
				setState(450);
				match(LPAREN);
				setState(451);
				num_expression();
				setState(452);
				match(RPAREN);
				}
				break;
			case 2:
				enterOuterAlt(_localctx, 2);
				{
				setState(454);
				match(COMPLEX);
				}
				break;
			case 3:
				enterOuterAlt(_localctx, 3);
				{
				setState(455);
				match(ADD);
				setState(456);
				num_factor();
				}
				break;
			case 4:
				enterOuterAlt(_localctx, 4);
				{
				setState(457);
				match(SUB);
				setState(458);
				num_factor();
				}
				break;
			case 5:
				enterOuterAlt(_localctx, 5);
				{
				setState(459);
				match(INT);
				}
				break;
			case 6:
				enterOuterAlt(_localctx, 6);
				{
				setState(460);
				match(FLOAT);
				}
				break;
			case 7:
				enterOuterAlt(_localctx, 7);
				{
				setState(461);
				match(CHAR);
				}
				break;
			case 8:
				enterOuterAlt(_localctx, 8);
				{
				setState(462);
				dirac_expression(0);
				}
				break;
			case 9:
				enterOuterAlt(_localctx, 9);
				{
				setState(463);
				match(IDENTIFIER);
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
	public static class Array_accessContext extends ParserRuleContext {
		public TerminalNode IDENTIFIER() { return getToken(BraKetParser.IDENTIFIER, 0); }
		public List<TerminalNode> LSQUARE() { return getTokens(BraKetParser.LSQUARE); }
		public TerminalNode LSQUARE(int i) {
			return getToken(BraKetParser.LSQUARE, i);
		}
		public List<Num_expressionContext> num_expression() {
			return getRuleContexts(Num_expressionContext.class);
		}
		public Num_expressionContext num_expression(int i) {
			return getRuleContext(Num_expressionContext.class,i);
		}
		public List<TerminalNode> RSQUARE() { return getTokens(BraKetParser.RSQUARE); }
		public TerminalNode RSQUARE(int i) {
			return getToken(BraKetParser.RSQUARE, i);
		}
		public Array_accessContext(ParserRuleContext parent, int invokingState) {
			super(parent, invokingState);
		}
		@Override public int getRuleIndex() { return RULE_array_access; }
	}

	public final Array_accessContext array_access() throws RecognitionException {
		Array_accessContext _localctx = new Array_accessContext(_ctx, getState());
		enterRule(_localctx, 72, RULE_array_access);
		int _la;
		try {
			enterOuterAlt(_localctx, 1);
			{
			setState(466);
			match(IDENTIFIER);
			setState(471); 
			_errHandler.sync(this);
			_la = _input.LA(1);
			do {
				{
				{
				setState(467);
				match(LSQUARE);
				setState(468);
				num_expression();
				setState(469);
				match(RSQUARE);
				}
				}
				setState(473); 
				_errHandler.sync(this);
				_la = _input.LA(1);
			} while ( _la==LSQUARE );
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
	public static class Struct_accessContext extends ParserRuleContext {
		public List<TerminalNode> IDENTIFIER() { return getTokens(BraKetParser.IDENTIFIER); }
		public TerminalNode IDENTIFIER(int i) {
			return getToken(BraKetParser.IDENTIFIER, i);
		}
		public List<TerminalNode> DOT() { return getTokens(BraKetParser.DOT); }
		public TerminalNode DOT(int i) {
			return getToken(BraKetParser.DOT, i);
		}
		public Struct_accessContext(ParserRuleContext parent, int invokingState) {
			super(parent, invokingState);
		}
		@Override public int getRuleIndex() { return RULE_struct_access; }
	}

	public final Struct_accessContext struct_access() throws RecognitionException {
		Struct_accessContext _localctx = new Struct_accessContext(_ctx, getState());
		enterRule(_localctx, 74, RULE_struct_access);
		int _la;
		try {
			enterOuterAlt(_localctx, 1);
			{
			setState(475);
			match(IDENTIFIER);
			setState(478); 
			_errHandler.sync(this);
			_la = _input.LA(1);
			do {
				{
				{
				setState(476);
				match(DOT);
				setState(477);
				match(IDENTIFIER);
				}
				}
				setState(480); 
				_errHandler.sync(this);
				_la = _input.LA(1);
			} while ( _la==DOT );
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
	public static class Dirac_expressionContext extends ParserRuleContext {
		public TerminalNode KET_IDENTIFIER() { return getToken(BraKetParser.KET_IDENTIFIER, 0); }
		public TerminalNode BRA_IDENTIFIER() { return getToken(BraKetParser.BRA_IDENTIFIER, 0); }
		public TerminalNode IDENTIFIER() { return getToken(BraKetParser.IDENTIFIER, 0); }
		public Braket_vectorContext braket_vector() {
			return getRuleContext(Braket_vectorContext.class,0);
		}
		public OpContext op() {
			return getRuleContext(OpContext.class,0);
		}
		public List<Dirac_expressionContext> dirac_expression() {
			return getRuleContexts(Dirac_expressionContext.class);
		}
		public Dirac_expressionContext dirac_expression(int i) {
			return getRuleContext(Dirac_expressionContext.class,i);
		}
		public TerminalNode MUL() { return getToken(BraKetParser.MUL, 0); }
		public TerminalNode TENSOR() { return getToken(BraKetParser.TENSOR, 0); }
		public Dirac_expressionContext(ParserRuleContext parent, int invokingState) {
			super(parent, invokingState);
		}
		@Override public int getRuleIndex() { return RULE_dirac_expression; }
	}

	public final Dirac_expressionContext dirac_expression() throws RecognitionException {
		return dirac_expression(0);
	}

	private Dirac_expressionContext dirac_expression(int _p) throws RecognitionException {
		ParserRuleContext _parentctx = _ctx;
		int _parentState = getState();
		Dirac_expressionContext _localctx = new Dirac_expressionContext(_ctx, _parentState);
		Dirac_expressionContext _prevctx = _localctx;
		int _startState = 76;
		enterRecursionRule(_localctx, 76, RULE_dirac_expression, _p);
		try {
			int _alt;
			enterOuterAlt(_localctx, 1);
			{
			setState(488);
			_errHandler.sync(this);
			switch ( getInterpreter().adaptivePredict(_input,37,_ctx) ) {
			case 1:
				{
				setState(483);
				match(KET_IDENTIFIER);
				}
				break;
			case 2:
				{
				setState(484);
				match(BRA_IDENTIFIER);
				}
				break;
			case 3:
				{
				setState(485);
				match(IDENTIFIER);
				}
				break;
			case 4:
				{
				setState(486);
				braket_vector();
				}
				break;
			case 5:
				{
				setState(487);
				op();
				}
				break;
			}
			_ctx.stop = _input.LT(-1);
			setState(498);
			_errHandler.sync(this);
			_alt = getInterpreter().adaptivePredict(_input,39,_ctx);
			while ( _alt!=2 && _alt!=org.antlr.v4.runtime.atn.ATN.INVALID_ALT_NUMBER ) {
				if ( _alt==1 ) {
					if ( _parseListeners!=null ) triggerExitRuleEvent();
					_prevctx = _localctx;
					{
					setState(496);
					_errHandler.sync(this);
					switch ( getInterpreter().adaptivePredict(_input,38,_ctx) ) {
					case 1:
						{
						_localctx = new Dirac_expressionContext(_parentctx, _parentState);
						pushNewRecursionContext(_localctx, _startState, RULE_dirac_expression);
						setState(490);
						if (!(precpred(_ctx, 7))) throw new FailedPredicateException(this, "precpred(_ctx, 7)");
						setState(491);
						match(MUL);
						setState(492);
						dirac_expression(8);
						}
						break;
					case 2:
						{
						_localctx = new Dirac_expressionContext(_parentctx, _parentState);
						pushNewRecursionContext(_localctx, _startState, RULE_dirac_expression);
						setState(493);
						if (!(precpred(_ctx, 6))) throw new FailedPredicateException(this, "precpred(_ctx, 6)");
						setState(494);
						match(TENSOR);
						setState(495);
						dirac_expression(7);
						}
						break;
					}
					} 
				}
				setState(500);
				_errHandler.sync(this);
				_alt = getInterpreter().adaptivePredict(_input,39,_ctx);
			}
			}
		}
		catch (RecognitionException re) {
			_localctx.exception = re;
			_errHandler.reportError(this, re);
			_errHandler.recover(this, re);
		}
		finally {
			unrollRecursionContexts(_parentctx);
		}
		return _localctx;
	}

	@SuppressWarnings("CheckReturnValue")
	public static class Num_compContext extends ParserRuleContext {
		public Eq_compContext eq_comp() {
			return getRuleContext(Eq_compContext.class,0);
		}
		public TerminalNode GT() { return getToken(BraKetParser.GT, 0); }
		public TerminalNode LT() { return getToken(BraKetParser.LT, 0); }
		public TerminalNode GTE() { return getToken(BraKetParser.GTE, 0); }
		public TerminalNode LTE() { return getToken(BraKetParser.LTE, 0); }
		public Num_compContext(ParserRuleContext parent, int invokingState) {
			super(parent, invokingState);
		}
		@Override public int getRuleIndex() { return RULE_num_comp; }
	}

	public final Num_compContext num_comp() throws RecognitionException {
		Num_compContext _localctx = new Num_compContext(_ctx, getState());
		enterRule(_localctx, 78, RULE_num_comp);
		try {
			setState(506);
			_errHandler.sync(this);
			switch (_input.LA(1)) {
			case EQ:
			case NEQ:
				enterOuterAlt(_localctx, 1);
				{
				setState(501);
				eq_comp();
				}
				break;
			case GT:
				enterOuterAlt(_localctx, 2);
				{
				setState(502);
				match(GT);
				}
				break;
			case LT:
				enterOuterAlt(_localctx, 3);
				{
				setState(503);
				match(LT);
				}
				break;
			case GTE:
				enterOuterAlt(_localctx, 4);
				{
				setState(504);
				match(GTE);
				}
				break;
			case LTE:
				enterOuterAlt(_localctx, 5);
				{
				setState(505);
				match(LTE);
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
	public static class Eq_compContext extends ParserRuleContext {
		public TerminalNode EQ() { return getToken(BraKetParser.EQ, 0); }
		public TerminalNode NEQ() { return getToken(BraKetParser.NEQ, 0); }
		public Eq_compContext(ParserRuleContext parent, int invokingState) {
			super(parent, invokingState);
		}
		@Override public int getRuleIndex() { return RULE_eq_comp; }
	}

	public final Eq_compContext eq_comp() throws RecognitionException {
		Eq_compContext _localctx = new Eq_compContext(_ctx, getState());
		enterRule(_localctx, 80, RULE_eq_comp);
		int _la;
		try {
			enterOuterAlt(_localctx, 1);
			{
			setState(508);
			_la = _input.LA(1);
			if ( !(_la==EQ || _la==NEQ) ) {
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
	public static class Bool_expressionContext extends ParserRuleContext {
		public Bool_orContext bool_or() {
			return getRuleContext(Bool_orContext.class,0);
		}
		public Bool_expressionContext(ParserRuleContext parent, int invokingState) {
			super(parent, invokingState);
		}
		@Override public int getRuleIndex() { return RULE_bool_expression; }
	}

	public final Bool_expressionContext bool_expression() throws RecognitionException {
		Bool_expressionContext _localctx = new Bool_expressionContext(_ctx, getState());
		enterRule(_localctx, 82, RULE_bool_expression);
		try {
			enterOuterAlt(_localctx, 1);
			{
			setState(510);
			bool_or(0);
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
	public static class Bool_orContext extends ParserRuleContext {
		public Bool_andContext bool_and() {
			return getRuleContext(Bool_andContext.class,0);
		}
		public List<Bool_orContext> bool_or() {
			return getRuleContexts(Bool_orContext.class);
		}
		public Bool_orContext bool_or(int i) {
			return getRuleContext(Bool_orContext.class,i);
		}
		public TerminalNode LOGICAL_OR() { return getToken(BraKetParser.LOGICAL_OR, 0); }
		public Bool_orContext(ParserRuleContext parent, int invokingState) {
			super(parent, invokingState);
		}
		@Override public int getRuleIndex() { return RULE_bool_or; }
	}

	public final Bool_orContext bool_or() throws RecognitionException {
		return bool_or(0);
	}

	private Bool_orContext bool_or(int _p) throws RecognitionException {
		ParserRuleContext _parentctx = _ctx;
		int _parentState = getState();
		Bool_orContext _localctx = new Bool_orContext(_ctx, _parentState);
		Bool_orContext _prevctx = _localctx;
		int _startState = 84;
		enterRecursionRule(_localctx, 84, RULE_bool_or, _p);
		try {
			int _alt;
			enterOuterAlt(_localctx, 1);
			{
			{
			setState(513);
			bool_and(0);
			}
			_ctx.stop = _input.LT(-1);
			setState(520);
			_errHandler.sync(this);
			_alt = getInterpreter().adaptivePredict(_input,41,_ctx);
			while ( _alt!=2 && _alt!=org.antlr.v4.runtime.atn.ATN.INVALID_ALT_NUMBER ) {
				if ( _alt==1 ) {
					if ( _parseListeners!=null ) triggerExitRuleEvent();
					_prevctx = _localctx;
					{
					{
					_localctx = new Bool_orContext(_parentctx, _parentState);
					pushNewRecursionContext(_localctx, _startState, RULE_bool_or);
					setState(515);
					if (!(precpred(_ctx, 2))) throw new FailedPredicateException(this, "precpred(_ctx, 2)");
					setState(516);
					match(LOGICAL_OR);
					setState(517);
					bool_or(3);
					}
					} 
				}
				setState(522);
				_errHandler.sync(this);
				_alt = getInterpreter().adaptivePredict(_input,41,_ctx);
			}
			}
		}
		catch (RecognitionException re) {
			_localctx.exception = re;
			_errHandler.reportError(this, re);
			_errHandler.recover(this, re);
		}
		finally {
			unrollRecursionContexts(_parentctx);
		}
		return _localctx;
	}

	@SuppressWarnings("CheckReturnValue")
	public static class Bool_andContext extends ParserRuleContext {
		public Bool_cmpContext bool_cmp() {
			return getRuleContext(Bool_cmpContext.class,0);
		}
		public List<Bool_andContext> bool_and() {
			return getRuleContexts(Bool_andContext.class);
		}
		public Bool_andContext bool_and(int i) {
			return getRuleContext(Bool_andContext.class,i);
		}
		public TerminalNode LOGICAL_AND() { return getToken(BraKetParser.LOGICAL_AND, 0); }
		public Bool_andContext(ParserRuleContext parent, int invokingState) {
			super(parent, invokingState);
		}
		@Override public int getRuleIndex() { return RULE_bool_and; }
	}

	public final Bool_andContext bool_and() throws RecognitionException {
		return bool_and(0);
	}

	private Bool_andContext bool_and(int _p) throws RecognitionException {
		ParserRuleContext _parentctx = _ctx;
		int _parentState = getState();
		Bool_andContext _localctx = new Bool_andContext(_ctx, _parentState);
		Bool_andContext _prevctx = _localctx;
		int _startState = 86;
		enterRecursionRule(_localctx, 86, RULE_bool_and, _p);
		try {
			int _alt;
			enterOuterAlt(_localctx, 1);
			{
			{
			setState(524);
			bool_cmp();
			}
			_ctx.stop = _input.LT(-1);
			setState(531);
			_errHandler.sync(this);
			_alt = getInterpreter().adaptivePredict(_input,42,_ctx);
			while ( _alt!=2 && _alt!=org.antlr.v4.runtime.atn.ATN.INVALID_ALT_NUMBER ) {
				if ( _alt==1 ) {
					if ( _parseListeners!=null ) triggerExitRuleEvent();
					_prevctx = _localctx;
					{
					{
					_localctx = new Bool_andContext(_parentctx, _parentState);
					pushNewRecursionContext(_localctx, _startState, RULE_bool_and);
					setState(526);
					if (!(precpred(_ctx, 2))) throw new FailedPredicateException(this, "precpred(_ctx, 2)");
					setState(527);
					match(LOGICAL_AND);
					setState(528);
					bool_and(3);
					}
					} 
				}
				setState(533);
				_errHandler.sync(this);
				_alt = getInterpreter().adaptivePredict(_input,42,_ctx);
			}
			}
		}
		catch (RecognitionException re) {
			_localctx.exception = re;
			_errHandler.reportError(this, re);
			_errHandler.recover(this, re);
		}
		finally {
			unrollRecursionContexts(_parentctx);
		}
		return _localctx;
	}

	@SuppressWarnings("CheckReturnValue")
	public static class Bool_cmpContext extends ParserRuleContext {
		public List<Num_expressionContext> num_expression() {
			return getRuleContexts(Num_expressionContext.class);
		}
		public Num_expressionContext num_expression(int i) {
			return getRuleContext(Num_expressionContext.class,i);
		}
		public Num_compContext num_comp() {
			return getRuleContext(Num_compContext.class,0);
		}
		public List<String_expressionContext> string_expression() {
			return getRuleContexts(String_expressionContext.class);
		}
		public String_expressionContext string_expression(int i) {
			return getRuleContext(String_expressionContext.class,i);
		}
		public Eq_compContext eq_comp() {
			return getRuleContext(Eq_compContext.class,0);
		}
		public List<Bool_unaryContext> bool_unary() {
			return getRuleContexts(Bool_unaryContext.class);
		}
		public Bool_unaryContext bool_unary(int i) {
			return getRuleContext(Bool_unaryContext.class,i);
		}
		public Bool_cmpContext(ParserRuleContext parent, int invokingState) {
			super(parent, invokingState);
		}
		@Override public int getRuleIndex() { return RULE_bool_cmp; }
	}

	public final Bool_cmpContext bool_cmp() throws RecognitionException {
		Bool_cmpContext _localctx = new Bool_cmpContext(_ctx, getState());
		enterRule(_localctx, 88, RULE_bool_cmp);
		try {
			setState(547);
			_errHandler.sync(this);
			switch ( getInterpreter().adaptivePredict(_input,43,_ctx) ) {
			case 1:
				enterOuterAlt(_localctx, 1);
				{
				setState(534);
				num_expression();
				setState(535);
				num_comp();
				setState(536);
				num_expression();
				}
				break;
			case 2:
				enterOuterAlt(_localctx, 2);
				{
				setState(538);
				string_expression(0);
				setState(539);
				eq_comp();
				setState(540);
				string_expression(0);
				}
				break;
			case 3:
				enterOuterAlt(_localctx, 3);
				{
				setState(542);
				bool_unary();
				setState(543);
				eq_comp();
				setState(544);
				bool_unary();
				}
				break;
			case 4:
				enterOuterAlt(_localctx, 4);
				{
				setState(546);
				bool_unary();
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
	public static class Bool_unaryContext extends ParserRuleContext {
		public TerminalNode NEG() { return getToken(BraKetParser.NEG, 0); }
		public Bool_unaryContext bool_unary() {
			return getRuleContext(Bool_unaryContext.class,0);
		}
		public Bool_primaryContext bool_primary() {
			return getRuleContext(Bool_primaryContext.class,0);
		}
		public Bool_unaryContext(ParserRuleContext parent, int invokingState) {
			super(parent, invokingState);
		}
		@Override public int getRuleIndex() { return RULE_bool_unary; }
	}

	public final Bool_unaryContext bool_unary() throws RecognitionException {
		Bool_unaryContext _localctx = new Bool_unaryContext(_ctx, getState());
		enterRule(_localctx, 90, RULE_bool_unary);
		try {
			setState(552);
			_errHandler.sync(this);
			switch (_input.LA(1)) {
			case NEG:
				enterOuterAlt(_localctx, 1);
				{
				setState(549);
				match(NEG);
				setState(550);
				bool_unary();
				}
				break;
			case INT:
			case BOOL_TRUE:
			case BOOL_FALSE:
			case LPAREN:
			case IDENTIFIER:
				enterOuterAlt(_localctx, 2);
				{
				setState(551);
				bool_primary();
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
	public static class Bool_primaryContext extends ParserRuleContext {
		public TerminalNode LPAREN() { return getToken(BraKetParser.LPAREN, 0); }
		public Bool_expressionContext bool_expression() {
			return getRuleContext(Bool_expressionContext.class,0);
		}
		public TerminalNode RPAREN() { return getToken(BraKetParser.RPAREN, 0); }
		public TerminalNode BOOL_TRUE() { return getToken(BraKetParser.BOOL_TRUE, 0); }
		public TerminalNode BOOL_FALSE() { return getToken(BraKetParser.BOOL_FALSE, 0); }
		public TerminalNode INT() { return getToken(BraKetParser.INT, 0); }
		public TerminalNode IDENTIFIER() { return getToken(BraKetParser.IDENTIFIER, 0); }
		public Bool_primaryContext(ParserRuleContext parent, int invokingState) {
			super(parent, invokingState);
		}
		@Override public int getRuleIndex() { return RULE_bool_primary; }
	}

	public final Bool_primaryContext bool_primary() throws RecognitionException {
		Bool_primaryContext _localctx = new Bool_primaryContext(_ctx, getState());
		enterRule(_localctx, 92, RULE_bool_primary);
		try {
			setState(562);
			_errHandler.sync(this);
			switch (_input.LA(1)) {
			case LPAREN:
				enterOuterAlt(_localctx, 1);
				{
				setState(554);
				match(LPAREN);
				setState(555);
				bool_expression();
				setState(556);
				match(RPAREN);
				}
				break;
			case BOOL_TRUE:
				enterOuterAlt(_localctx, 2);
				{
				setState(558);
				match(BOOL_TRUE);
				}
				break;
			case BOOL_FALSE:
				enterOuterAlt(_localctx, 3);
				{
				setState(559);
				match(BOOL_FALSE);
				}
				break;
			case INT:
				enterOuterAlt(_localctx, 4);
				{
				setState(560);
				match(INT);
				}
				break;
			case IDENTIFIER:
				enterOuterAlt(_localctx, 5);
				{
				setState(561);
				match(IDENTIFIER);
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
	public static class Func_decl_listContext extends ParserRuleContext {
		public List<Func_declContext> func_decl() {
			return getRuleContexts(Func_declContext.class);
		}
		public Func_declContext func_decl(int i) {
			return getRuleContext(Func_declContext.class,i);
		}
		public Func_decl_listContext(ParserRuleContext parent, int invokingState) {
			super(parent, invokingState);
		}
		@Override public int getRuleIndex() { return RULE_func_decl_list; }
	}

	public final Func_decl_listContext func_decl_list() throws RecognitionException {
		Func_decl_listContext _localctx = new Func_decl_listContext(_ctx, getState());
		enterRule(_localctx, 94, RULE_func_decl_list);
		int _la;
		try {
			enterOuterAlt(_localctx, 1);
			{
			setState(565); 
			_errHandler.sync(this);
			_la = _input.LA(1);
			do {
				{
				{
				setState(564);
				func_decl();
				}
				}
				setState(567); 
				_errHandler.sync(this);
				_la = _input.LA(1);
			} while ( _la==FUNC );
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
	public static class Func_declContext extends ParserRuleContext {
		public TerminalNode FUNC() { return getToken(BraKetParser.FUNC, 0); }
		public TerminalNode IDENTIFIER() { return getToken(BraKetParser.IDENTIFIER, 0); }
		public TerminalNode LPAREN() { return getToken(BraKetParser.LPAREN, 0); }
		public TerminalNode RPAREN() { return getToken(BraKetParser.RPAREN, 0); }
		public TerminalNode LCURLY() { return getToken(BraKetParser.LCURLY, 0); }
		public TerminalNode RCURLY() { return getToken(BraKetParser.RCURLY, 0); }
		public Param_listContext param_list() {
			return getRuleContext(Param_listContext.class,0);
		}
		public Statement_listContext statement_list() {
			return getRuleContext(Statement_listContext.class,0);
		}
		public Func_declContext(ParserRuleContext parent, int invokingState) {
			super(parent, invokingState);
		}
		@Override public int getRuleIndex() { return RULE_func_decl; }
	}

	public final Func_declContext func_decl() throws RecognitionException {
		Func_declContext _localctx = new Func_declContext(_ctx, getState());
		enterRule(_localctx, 96, RULE_func_decl);
		int _la;
		try {
			enterOuterAlt(_localctx, 1);
			{
			setState(569);
			match(FUNC);
			setState(570);
			match(IDENTIFIER);
			setState(571);
			match(LPAREN);
			setState(573);
			_errHandler.sync(this);
			_la = _input.LA(1);
			if ((((_la) & ~0x3f) == 0 && ((1L << _la) & 562949953421504L) != 0)) {
				{
				setState(572);
				param_list();
				}
			}

			setState(575);
			match(RPAREN);
			setState(576);
			match(LCURLY);
			setState(578);
			_errHandler.sync(this);
			_la = _input.LA(1);
			if ((((_la) & ~0x3f) == 0 && ((1L << _la) & 562949954363584L) != 0)) {
				{
				setState(577);
				statement_list();
				}
			}

			setState(580);
			match(RCURLY);
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
	public static class Param_listContext extends ParserRuleContext {
		public Identifier_listContext identifier_list() {
			return getRuleContext(Identifier_listContext.class,0);
		}
		public TerminalNode COMMA() { return getToken(BraKetParser.COMMA, 0); }
		public Default_listContext default_list() {
			return getRuleContext(Default_listContext.class,0);
		}
		public Param_listContext(ParserRuleContext parent, int invokingState) {
			super(parent, invokingState);
		}
		@Override public int getRuleIndex() { return RULE_param_list; }
	}

	public final Param_listContext param_list() throws RecognitionException {
		Param_listContext _localctx = new Param_listContext(_ctx, getState());
		enterRule(_localctx, 98, RULE_param_list);
		int _la;
		try {
			setState(588);
			_errHandler.sync(this);
			switch ( getInterpreter().adaptivePredict(_input,50,_ctx) ) {
			case 1:
				enterOuterAlt(_localctx, 1);
				{
				setState(582);
				identifier_list();
				setState(585);
				_errHandler.sync(this);
				_la = _input.LA(1);
				if (_la==COMMA) {
					{
					setState(583);
					match(COMMA);
					setState(584);
					default_list();
					}
				}

				}
				break;
			case 2:
				enterOuterAlt(_localctx, 2);
				{
				setState(587);
				default_list();
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
	public static class Identifier_listContext extends ParserRuleContext {
		public List<TerminalNode> IDENTIFIER() { return getTokens(BraKetParser.IDENTIFIER); }
		public TerminalNode IDENTIFIER(int i) {
			return getToken(BraKetParser.IDENTIFIER, i);
		}
		public List<TerminalNode> COMMA() { return getTokens(BraKetParser.COMMA); }
		public TerminalNode COMMA(int i) {
			return getToken(BraKetParser.COMMA, i);
		}
		public Identifier_listContext(ParserRuleContext parent, int invokingState) {
			super(parent, invokingState);
		}
		@Override public int getRuleIndex() { return RULE_identifier_list; }
	}

	public final Identifier_listContext identifier_list() throws RecognitionException {
		Identifier_listContext _localctx = new Identifier_listContext(_ctx, getState());
		enterRule(_localctx, 100, RULE_identifier_list);
		try {
			int _alt;
			enterOuterAlt(_localctx, 1);
			{
			setState(590);
			match(IDENTIFIER);
			setState(595);
			_errHandler.sync(this);
			_alt = getInterpreter().adaptivePredict(_input,51,_ctx);
			while ( _alt!=2 && _alt!=org.antlr.v4.runtime.atn.ATN.INVALID_ALT_NUMBER ) {
				if ( _alt==1 ) {
					{
					{
					setState(591);
					match(COMMA);
					setState(592);
					match(IDENTIFIER);
					}
					} 
				}
				setState(597);
				_errHandler.sync(this);
				_alt = getInterpreter().adaptivePredict(_input,51,_ctx);
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
	public static class Default_listContext extends ParserRuleContext {
		public List<Assign_statementContext> assign_statement() {
			return getRuleContexts(Assign_statementContext.class);
		}
		public Assign_statementContext assign_statement(int i) {
			return getRuleContext(Assign_statementContext.class,i);
		}
		public List<TerminalNode> COMMA() { return getTokens(BraKetParser.COMMA); }
		public TerminalNode COMMA(int i) {
			return getToken(BraKetParser.COMMA, i);
		}
		public Default_listContext(ParserRuleContext parent, int invokingState) {
			super(parent, invokingState);
		}
		@Override public int getRuleIndex() { return RULE_default_list; }
	}

	public final Default_listContext default_list() throws RecognitionException {
		Default_listContext _localctx = new Default_listContext(_ctx, getState());
		enterRule(_localctx, 102, RULE_default_list);
		int _la;
		try {
			enterOuterAlt(_localctx, 1);
			{
			setState(598);
			assign_statement();
			setState(603);
			_errHandler.sync(this);
			_la = _input.LA(1);
			while (_la==COMMA) {
				{
				{
				setState(599);
				match(COMMA);
				setState(600);
				assign_statement();
				}
				}
				setState(605);
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
	public static class Main_functionContext extends ParserRuleContext {
		public TerminalNode MAIN() { return getToken(BraKetParser.MAIN, 0); }
		public TerminalNode LPAREN() { return getToken(BraKetParser.LPAREN, 0); }
		public TerminalNode RPAREN() { return getToken(BraKetParser.RPAREN, 0); }
		public TerminalNode LCURLY() { return getToken(BraKetParser.LCURLY, 0); }
		public TerminalNode RCURLY() { return getToken(BraKetParser.RCURLY, 0); }
		public Param_listContext param_list() {
			return getRuleContext(Param_listContext.class,0);
		}
		public Statement_listContext statement_list() {
			return getRuleContext(Statement_listContext.class,0);
		}
		public Main_functionContext(ParserRuleContext parent, int invokingState) {
			super(parent, invokingState);
		}
		@Override public int getRuleIndex() { return RULE_main_function; }
	}

	public final Main_functionContext main_function() throws RecognitionException {
		Main_functionContext _localctx = new Main_functionContext(_ctx, getState());
		enterRule(_localctx, 104, RULE_main_function);
		int _la;
		try {
			enterOuterAlt(_localctx, 1);
			{
			setState(606);
			match(MAIN);
			setState(607);
			match(LPAREN);
			setState(609);
			_errHandler.sync(this);
			_la = _input.LA(1);
			if ((((_la) & ~0x3f) == 0 && ((1L << _la) & 562949953421504L) != 0)) {
				{
				setState(608);
				param_list();
				}
			}

			setState(611);
			match(RPAREN);
			setState(612);
			match(LCURLY);
			setState(614);
			_errHandler.sync(this);
			_la = _input.LA(1);
			if ((((_la) & ~0x3f) == 0 && ((1L << _la) & 562949954363584L) != 0)) {
				{
				setState(613);
				statement_list();
				}
			}

			setState(616);
			match(RCURLY);
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

	public boolean sempred(RuleContext _localctx, int ruleIndex, int predIndex) {
		switch (ruleIndex) {
		case 32:
			return string_expression_sempred((String_expressionContext)_localctx, predIndex);
		case 38:
			return dirac_expression_sempred((Dirac_expressionContext)_localctx, predIndex);
		case 42:
			return bool_or_sempred((Bool_orContext)_localctx, predIndex);
		case 43:
			return bool_and_sempred((Bool_andContext)_localctx, predIndex);
		}
		return true;
	}
	private boolean string_expression_sempred(String_expressionContext _localctx, int predIndex) {
		switch (predIndex) {
		case 0:
			return precpred(_ctx, 3);
		}
		return true;
	}
	private boolean dirac_expression_sempred(Dirac_expressionContext _localctx, int predIndex) {
		switch (predIndex) {
		case 1:
			return precpred(_ctx, 7);
		case 2:
			return precpred(_ctx, 6);
		}
		return true;
	}
	private boolean bool_or_sempred(Bool_orContext _localctx, int predIndex) {
		switch (predIndex) {
		case 3:
			return precpred(_ctx, 2);
		}
		return true;
	}
	private boolean bool_and_sempred(Bool_andContext _localctx, int predIndex) {
		switch (predIndex) {
		case 4:
			return precpred(_ctx, 2);
		}
		return true;
	}

	public static final String _serializedATN =
		"\u0004\u00011\u026b\u0002\u0000\u0007\u0000\u0002\u0001\u0007\u0001\u0002"+
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
		"(\u0007(\u0002)\u0007)\u0002*\u0007*\u0002+\u0007+\u0002,\u0007,\u0002"+
		"-\u0007-\u0002.\u0007.\u0002/\u0007/\u00020\u00070\u00021\u00071\u0002"+
		"2\u00072\u00023\u00073\u00024\u00074\u0001\u0000\u0003\u0000l\b\u0000"+
		"\u0001\u0000\u0003\u0000o\b\u0000\u0001\u0000\u0003\u0000r\b\u0000\u0001"+
		"\u0000\u0003\u0000u\b\u0000\u0001\u0001\u0001\u0001\u0005\u0001y\b\u0001"+
		"\n\u0001\f\u0001|\t\u0001\u0001\u0002\u0001\u0002\u0001\u0002\u0001\u0002"+
		"\u0001\u0002\u0001\u0002\u0003\u0002\u0084\b\u0002\u0001\u0003\u0001\u0003"+
		"\u0001\u0003\u0005\u0003\u0089\b\u0003\n\u0003\f\u0003\u008c\t\u0003\u0001"+
		"\u0004\u0004\u0004\u008f\b\u0004\u000b\u0004\f\u0004\u0090\u0001\u0005"+
		"\u0001\u0005\u0001\u0005\u0001\u0006\u0004\u0006\u0097\b\u0006\u000b\u0006"+
		"\f\u0006\u0098\u0001\u0007\u0001\u0007\u0001\u0007\u0001\u0007\u0001\u0007"+
		"\u0001\u0007\u0001\u0007\u0001\u0007\u0001\u0007\u0003\u0007\u00a4\b\u0007"+
		"\u0001\b\u0001\b\u0001\b\u0001\b\u0001\b\u0001\b\u0001\b\u0001\b\u0001"+
		"\b\u0001\b\u0003\b\u00b0\b\b\u0001\t\u0001\t\u0001\t\u0001\t\u0005\t\u00b6"+
		"\b\t\n\t\f\t\u00b9\t\t\u0001\t\u0001\t\u0001\n\u0001\n\u0001\n\u0001\n"+
		"\u0001\n\u0001\n\u0001\n\u0001\n\u0001\n\u0001\n\u0001\n\u0003\n\u00c8"+
		"\b\n\u0001\u000b\u0001\u000b\u0001\u000b\u0001\u000b\u0001\u000b\u0001"+
		"\u000b\u0001\u000b\u0001\u000b\u0001\u000b\u0003\u000b\u00d3\b\u000b\u0001"+
		"\f\u0001\f\u0001\f\u0001\f\u0001\f\u0001\f\u0001\f\u0001\f\u0001\f\u0001"+
		"\f\u0001\f\u0001\f\u0001\f\u0001\f\u0001\f\u0001\f\u0001\f\u0003\f\u00e6"+
		"\b\f\u0001\r\u0001\r\u0001\r\u0001\r\u0001\r\u0001\r\u0001\r\u0001\r\u0001"+
		"\r\u0001\r\u0001\r\u0001\r\u0003\r\u00f4\b\r\u0001\u000e\u0001\u000e\u0001"+
		"\u000e\u0001\u000e\u0005\u000e\u00fa\b\u000e\n\u000e\f\u000e\u00fd\t\u000e"+
		"\u0003\u000e\u00ff\b\u000e\u0001\u000e\u0001\u000e\u0001\u000f\u0001\u000f"+
		"\u0003\u000f\u0105\b\u000f\u0001\u000f\u0001\u000f\u0001\u0010\u0001\u0010"+
		"\u0001\u0010\u0001\u0010\u0001\u0010\u0001\u0010\u0001\u0010\u0001\u0010"+
		"\u0001\u0010\u0001\u0010\u0003\u0010\u0113\b\u0010\u0001\u0011\u0001\u0011"+
		"\u0001\u0011\u0001\u0011\u0005\u0011\u0119\b\u0011\n\u0011\f\u0011\u011c"+
		"\t\u0011\u0001\u0011\u0001\u0011\u0001\u0012\u0004\u0012\u0121\b\u0012"+
		"\u000b\u0012\f\u0012\u0122\u0001\u0013\u0001\u0013\u0001\u0013\u0001\u0013"+
		"\u0001\u0013\u0001\u0013\u0001\u0013\u0003\u0013\u012c\b\u0013\u0001\u0014"+
		"\u0001\u0014\u0001\u0014\u0001\u0014\u0001\u0014\u0001\u0014\u0001\u0014"+
		"\u0001\u0014\u0001\u0014\u0003\u0014\u0137\b\u0014\u0001\u0015\u0001\u0015"+
		"\u0001\u0015\u0003\u0015\u013c\b\u0015\u0001\u0015\u0001\u0015\u0001\u0016"+
		"\u0001\u0016\u0001\u0016\u0005\u0016\u0143\b\u0016\n\u0016\f\u0016\u0146"+
		"\t\u0016\u0001\u0017\u0001\u0017\u0001\u0017\u0001\u0017\u0001\u0017\u0003"+
		"\u0017\u014d\b\u0017\u0001\u0018\u0001\u0018\u0001\u0018\u0001\u0019\u0001"+
		"\u0019\u0001\u0019\u0001\u0019\u0001\u0019\u0001\u0019\u0001\u0019\u0001"+
		"\u0019\u0005\u0019\u015a\b\u0019\n\u0019\f\u0019\u015d\t\u0019\u0001\u0019"+
		"\u0003\u0019\u0160\b\u0019\u0001\u001a\u0001\u001a\u0001\u001a\u0001\u001a"+
		"\u0001\u001a\u0001\u001a\u0001\u001a\u0001\u001a\u0001\u001b\u0001\u001b"+
		"\u0001\u001b\u0001\u001b\u0001\u001b\u0001\u001c\u0001\u001c\u0001\u001c"+
		"\u0001\u001c\u0001\u001c\u0001\u001c\u0001\u001c\u0001\u001c\u0001\u001c"+
		"\u0001\u001c\u0001\u001c\u0001\u001c\u0001\u001d\u0001\u001d\u0001\u001d"+
		"\u0001\u001d\u0001\u001d\u0001\u001d\u0001\u001d\u0001\u001d\u0001\u001e"+
		"\u0001\u001e\u0001\u001e\u0001\u001e\u0001\u001e\u0001\u001e\u0001\u001e"+
		"\u0001\u001e\u0001\u001e\u0001\u001f\u0001\u001f\u0001\u001f\u0001\u001f"+
		"\u0001\u001f\u0001\u001f\u0001\u001f\u0001\u001f\u0001\u001f\u0001\u001f"+
		"\u0003\u001f\u0196\b\u001f\u0001 \u0001 \u0001 \u0003 \u019b\b \u0001"+
		" \u0001 \u0001 \u0005 \u01a0\b \n \f \u01a3\t \u0001!\u0001!\u0001!\u0001"+
		"!\u0001!\u0001!\u0001!\u0001!\u0001!\u0003!\u01ae\b!\u0001\"\u0001\"\u0001"+
		"\"\u0001\"\u0001\"\u0001\"\u0001\"\u0001\"\u0001\"\u0001\"\u0001\"\u0001"+
		"\"\u0001\"\u0001\"\u0001\"\u0001\"\u0001\"\u0003\"\u01c1\b\"\u0001#\u0001"+
		"#\u0001#\u0001#\u0001#\u0001#\u0001#\u0001#\u0001#\u0001#\u0001#\u0001"+
		"#\u0001#\u0001#\u0003#\u01d1\b#\u0001$\u0001$\u0001$\u0001$\u0001$\u0004"+
		"$\u01d8\b$\u000b$\f$\u01d9\u0001%\u0001%\u0001%\u0004%\u01df\b%\u000b"+
		"%\f%\u01e0\u0001&\u0001&\u0001&\u0001&\u0001&\u0001&\u0003&\u01e9\b&\u0001"+
		"&\u0001&\u0001&\u0001&\u0001&\u0001&\u0005&\u01f1\b&\n&\f&\u01f4\t&\u0001"+
		"\'\u0001\'\u0001\'\u0001\'\u0001\'\u0003\'\u01fb\b\'\u0001(\u0001(\u0001"+
		")\u0001)\u0001*\u0001*\u0001*\u0001*\u0001*\u0001*\u0005*\u0207\b*\n*"+
		"\f*\u020a\t*\u0001+\u0001+\u0001+\u0001+\u0001+\u0001+\u0005+\u0212\b"+
		"+\n+\f+\u0215\t+\u0001,\u0001,\u0001,\u0001,\u0001,\u0001,\u0001,\u0001"+
		",\u0001,\u0001,\u0001,\u0001,\u0001,\u0003,\u0224\b,\u0001-\u0001-\u0001"+
		"-\u0003-\u0229\b-\u0001.\u0001.\u0001.\u0001.\u0001.\u0001.\u0001.\u0001"+
		".\u0003.\u0233\b.\u0001/\u0004/\u0236\b/\u000b/\f/\u0237\u00010\u0001"+
		"0\u00010\u00010\u00030\u023e\b0\u00010\u00010\u00010\u00030\u0243\b0\u0001"+
		"0\u00010\u00011\u00011\u00011\u00031\u024a\b1\u00011\u00031\u024d\b1\u0001"+
		"2\u00012\u00012\u00052\u0252\b2\n2\f2\u0255\t2\u00013\u00013\u00013\u0005"+
		"3\u025a\b3\n3\f3\u025d\t3\u00014\u00014\u00014\u00034\u0262\b4\u00014"+
		"\u00014\u00014\u00034\u0267\b4\u00014\u00014\u00014\u0000\u0004@LTV5\u0000"+
		"\u0002\u0004\u0006\b\n\f\u000e\u0010\u0012\u0014\u0016\u0018\u001a\u001c"+
		"\u001e \"$&(*,.02468:<>@BDFHJLNPRTVXZ\\^`bdfh\u0000\u0001\u0001\u0000"+
		"#$\u02ac\u0000k\u0001\u0000\u0000\u0000\u0002v\u0001\u0000\u0000\u0000"+
		"\u0004\u0083\u0001\u0000\u0000\u0000\u0006\u0085\u0001\u0000\u0000\u0000"+
		"\b\u008e\u0001\u0000\u0000\u0000\n\u0092\u0001\u0000\u0000\u0000\f\u0096"+
		"\u0001\u0000\u0000\u0000\u000e\u00a3\u0001\u0000\u0000\u0000\u0010\u00af"+
		"\u0001\u0000\u0000\u0000\u0012\u00b1\u0001\u0000\u0000\u0000\u0014\u00c7"+
		"\u0001\u0000\u0000\u0000\u0016\u00d2\u0001\u0000\u0000\u0000\u0018\u00e5"+
		"\u0001\u0000\u0000\u0000\u001a\u00f3\u0001\u0000\u0000\u0000\u001c\u00f5"+
		"\u0001\u0000\u0000\u0000\u001e\u0102\u0001\u0000\u0000\u0000 \u0112\u0001"+
		"\u0000\u0000\u0000\"\u0114\u0001\u0000\u0000\u0000$\u0120\u0001\u0000"+
		"\u0000\u0000&\u012b\u0001\u0000\u0000\u0000(\u0136\u0001\u0000\u0000\u0000"+
		"*\u0138\u0001\u0000\u0000\u0000,\u013f\u0001\u0000\u0000\u0000.\u014c"+
		"\u0001\u0000\u0000\u00000\u014e\u0001\u0000\u0000\u00002\u0151\u0001\u0000"+
		"\u0000\u00004\u0161\u0001\u0000\u0000\u00006\u0169\u0001\u0000\u0000\u0000"+
		"8\u016e\u0001\u0000\u0000\u0000:\u017a\u0001\u0000\u0000\u0000<\u0182"+
		"\u0001\u0000\u0000\u0000>\u0195\u0001\u0000\u0000\u0000@\u019a\u0001\u0000"+
		"\u0000\u0000B\u01ad\u0001\u0000\u0000\u0000D\u01c0\u0001\u0000\u0000\u0000"+
		"F\u01d0\u0001\u0000\u0000\u0000H\u01d2\u0001\u0000\u0000\u0000J\u01db"+
		"\u0001\u0000\u0000\u0000L\u01e8\u0001\u0000\u0000\u0000N\u01fa\u0001\u0000"+
		"\u0000\u0000P\u01fc\u0001\u0000\u0000\u0000R\u01fe\u0001\u0000\u0000\u0000"+
		"T\u0200\u0001\u0000\u0000\u0000V\u020b\u0001\u0000\u0000\u0000X\u0223"+
		"\u0001\u0000\u0000\u0000Z\u0228\u0001\u0000\u0000\u0000\\\u0232\u0001"+
		"\u0000\u0000\u0000^\u0235\u0001\u0000\u0000\u0000`\u0239\u0001\u0000\u0000"+
		"\u0000b\u024c\u0001\u0000\u0000\u0000d\u024e\u0001\u0000\u0000\u0000f"+
		"\u0256\u0001\u0000\u0000\u0000h\u025e\u0001\u0000\u0000\u0000jl\u0003"+
		"\u0002\u0001\u0000kj\u0001\u0000\u0000\u0000kl\u0001\u0000\u0000\u0000"+
		"ln\u0001\u0000\u0000\u0000mo\u0003\b\u0004\u0000nm\u0001\u0000\u0000\u0000"+
		"no\u0001\u0000\u0000\u0000oq\u0001\u0000\u0000\u0000pr\u0003^/\u0000q"+
		"p\u0001\u0000\u0000\u0000qr\u0001\u0000\u0000\u0000rt\u0001\u0000\u0000"+
		"\u0000su\u0003h4\u0000ts\u0001\u0000\u0000\u0000tu\u0001\u0000\u0000\u0000"+
		"u\u0001\u0001\u0000\u0000\u0000vz\u0003\u0004\u0002\u0000wy\u0003\u0004"+
		"\u0002\u0000xw\u0001\u0000\u0000\u0000y|\u0001\u0000\u0000\u0000zx\u0001"+
		"\u0000\u0000\u0000z{\u0001\u0000\u0000\u0000{\u0003\u0001\u0000\u0000"+
		"\u0000|z\u0001\u0000\u0000\u0000}~\u0005\u0003\u0000\u0000~\u007f\u0005"+
		"1\u0000\u0000\u007f\u0080\u0005\u0004\u0000\u0000\u0080\u0084\u0003\u0006"+
		"\u0003\u0000\u0081\u0082\u0005\u0004\u0000\u0000\u0082\u0084\u00051\u0000"+
		"\u0000\u0083}\u0001\u0000\u0000\u0000\u0083\u0081\u0001\u0000\u0000\u0000"+
		"\u0084\u0005\u0001\u0000\u0000\u0000\u0085\u008a\u00051\u0000\u0000\u0086"+
		"\u0087\u0005\u0001\u0000\u0000\u0087\u0089\u00051\u0000\u0000\u0088\u0086"+
		"\u0001\u0000\u0000\u0000\u0089\u008c\u0001\u0000\u0000\u0000\u008a\u0088"+
		"\u0001\u0000\u0000\u0000\u008a\u008b\u0001\u0000\u0000\u0000\u008b\u0007"+
		"\u0001\u0000\u0000\u0000\u008c\u008a\u0001\u0000\u0000\u0000\u008d\u008f"+
		"\u0003\n\u0005\u0000\u008e\u008d\u0001\u0000\u0000\u0000\u008f\u0090\u0001"+
		"\u0000\u0000\u0000\u0090\u008e\u0001\u0000\u0000\u0000\u0090\u0091\u0001"+
		"\u0000\u0000\u0000\u0091\t\u0001\u0000\u0000\u0000\u0092\u0093\u0005\u0005"+
		"\u0000\u0000\u0093\u0094\u0003\u000e\u0007\u0000\u0094\u000b\u0001\u0000"+
		"\u0000\u0000\u0095\u0097\u0003\u000e\u0007\u0000\u0096\u0095\u0001\u0000"+
		"\u0000\u0000\u0097\u0098\u0001\u0000\u0000\u0000\u0098\u0096\u0001\u0000"+
		"\u0000\u0000\u0098\u0099\u0001\u0000\u0000\u0000\u0099\r\u0001\u0000\u0000"+
		"\u0000\u009a\u009b\u00051\u0000\u0000\u009b\u009c\u0005\u001e\u0000\u0000"+
		"\u009c\u00a4\u0003>\u001f\u0000\u009d\u009e\u0005\u0006\u0000\u0000\u009e"+
		"\u009f\u0005\u001e\u0000\u0000\u009f\u00a4\u0003B!\u0000\u00a0\u00a1\u0005"+
		"\u0007\u0000\u0000\u00a1\u00a2\u0005\u001e\u0000\u0000\u00a2\u00a4\u0003"+
		"B!\u0000\u00a3\u009a\u0001\u0000\u0000\u0000\u00a3\u009d\u0001\u0000\u0000"+
		"\u0000\u00a3\u00a0\u0001\u0000\u0000\u0000\u00a4\u000f\u0001\u0000\u0000"+
		"\u0000\u00a5\u00b0\u0005\b\u0000\u0000\u00a6\u00b0\u0005\t\u0000\u0000"+
		"\u00a7\u00b0\u0005\n\u0000\u0000\u00a8\u00b0\u0005\u000b\u0000\u0000\u00a9"+
		"\u00b0\u0003\u001c\u000e\u0000\u00aa\u00b0\u0003\u001e\u000f\u0000\u00ab"+
		"\u00b0\u0005\f\u0000\u0000\u00ac\u00b0\u0003\"\u0011\u0000\u00ad\u00b0"+
		"\u0005\u0015\u0000\u0000\u00ae\u00b0\u0005\u0014\u0000\u0000\u00af\u00a5"+
		"\u0001\u0000\u0000\u0000\u00af\u00a6\u0001\u0000\u0000\u0000\u00af\u00a7"+
		"\u0001\u0000\u0000\u0000\u00af\u00a8\u0001\u0000\u0000\u0000\u00af\u00a9"+
		"\u0001\u0000\u0000\u0000\u00af\u00aa\u0001\u0000\u0000\u0000\u00af\u00ab"+
		"\u0001\u0000\u0000\u0000\u00af\u00ac\u0001\u0000\u0000\u0000\u00af\u00ad"+
		"\u0001\u0000\u0000\u0000\u00af\u00ae\u0001\u0000\u0000\u0000\u00b0\u0011"+
		"\u0001\u0000\u0000\u0000\u00b1\u00b2\u0005(\u0000\u0000\u00b2\u00b7\u0003"+
		"\u0014\n\u0000\u00b3\u00b4\u0005\u0001\u0000\u0000\u00b4\u00b6\u0003\u0014"+
		"\n\u0000\u00b5\u00b3\u0001\u0000\u0000\u0000\u00b6\u00b9\u0001\u0000\u0000"+
		"\u0000\u00b7\u00b5\u0001\u0000\u0000\u0000\u00b7\u00b8\u0001\u0000\u0000"+
		"\u0000\u00b8\u00ba\u0001\u0000\u0000\u0000\u00b9\u00b7\u0001\u0000\u0000"+
		"\u0000\u00ba\u00bb\u0005)\u0000\u0000\u00bb\u0013\u0001\u0000\u0000\u0000"+
		"\u00bc\u00bd\u0005\u0018\u0000\u0000\u00bd\u00c8\u0005\b\u0000\u0000\u00be"+
		"\u00bf\u0005\u0019\u0000\u0000\u00bf\u00c8\u0005\b\u0000\u0000\u00c0\u00c8"+
		"\u0005\b\u0000\u0000\u00c1\u00c2\u0005\u0018\u0000\u0000\u00c2\u00c8\u0005"+
		"\t\u0000\u0000\u00c3\u00c4\u0005\u0019\u0000\u0000\u00c4\u00c8\u0005\t"+
		"\u0000\u0000\u00c5\u00c8\u0005\t\u0000\u0000\u00c6\u00c8\u0005\f\u0000"+
		"\u0000\u00c7\u00bc\u0001\u0000\u0000\u0000\u00c7\u00be\u0001\u0000\u0000"+
		"\u0000\u00c7\u00c0\u0001\u0000\u0000\u0000\u00c7\u00c1\u0001\u0000\u0000"+
		"\u0000\u00c7\u00c3\u0001\u0000\u0000\u0000\u00c7\u00c5\u0001\u0000\u0000"+
		"\u0000\u00c7\u00c6\u0001\u0000\u0000\u0000\u00c8\u0015\u0001\u0000\u0000"+
		"\u0000\u00c9\u00ca\u0003\u0018\f\u0000\u00ca\u00cb\u0005\u0018\u0000\u0000"+
		"\u00cb\u00cc\u0003\u0016\u000b\u0000\u00cc\u00d3\u0001\u0000\u0000\u0000"+
		"\u00cd\u00ce\u0003\u0018\f\u0000\u00ce\u00cf\u0005\u0019\u0000\u0000\u00cf"+
		"\u00d0\u0003\u0016\u000b\u0000\u00d0\u00d3\u0001\u0000\u0000\u0000\u00d1"+
		"\u00d3\u0003\u0018\f\u0000\u00d2\u00c9\u0001\u0000\u0000\u0000\u00d2\u00cd"+
		"\u0001\u0000\u0000\u0000\u00d2\u00d1\u0001\u0000\u0000\u0000\u00d3\u0017"+
		"\u0001\u0000\u0000\u0000\u00d4\u00d5\u0003\u001a\r\u0000\u00d5\u00d6\u0005"+
		"\u001a\u0000\u0000\u00d6\u00d7\u0003\u0018\f\u0000\u00d7\u00e6\u0001\u0000"+
		"\u0000\u0000\u00d8\u00d9\u0003\u001a\r\u0000\u00d9\u00da\u0005\u001b\u0000"+
		"\u0000\u00da\u00db\u0003\u0018\f\u0000\u00db\u00e6\u0001\u0000\u0000\u0000"+
		"\u00dc\u00dd\u0003\u001a\r\u0000\u00dd\u00de\u0005\u001d\u0000\u0000\u00de"+
		"\u00df\u0003\u0018\f\u0000\u00df\u00e6\u0001\u0000\u0000\u0000\u00e0\u00e1"+
		"\u0003\u001a\r\u0000\u00e1\u00e2\u0005\u001c\u0000\u0000\u00e2\u00e3\u0003"+
		"\u0018\f\u0000\u00e3\u00e6\u0001\u0000\u0000\u0000\u00e4\u00e6\u0003\u001a"+
		"\r\u0000\u00e5\u00d4\u0001\u0000\u0000\u0000\u00e5\u00d8\u0001\u0000\u0000"+
		"\u0000\u00e5\u00dc\u0001\u0000\u0000\u0000\u00e5\u00e0\u0001\u0000\u0000"+
		"\u0000\u00e5\u00e4\u0001\u0000\u0000\u0000\u00e6\u0019\u0001\u0000\u0000"+
		"\u0000\u00e7\u00e8\u0005(\u0000\u0000\u00e8\u00e9\u0003\u0016\u000b\u0000"+
		"\u00e9\u00ea\u0005)\u0000\u0000\u00ea\u00f4\u0001\u0000\u0000\u0000\u00eb"+
		"\u00f4\u0005\f\u0000\u0000\u00ec\u00ed\u0005\u0018\u0000\u0000\u00ed\u00f4"+
		"\u0003\u001a\r\u0000\u00ee\u00ef\u0005\u0019\u0000\u0000\u00ef\u00f4\u0003"+
		"\u001a\r\u0000\u00f0\u00f4\u0005\b\u0000\u0000\u00f1\u00f4\u0005\t\u0000"+
		"\u0000\u00f2\u00f4\u00051\u0000\u0000\u00f3\u00e7\u0001\u0000\u0000\u0000"+
		"\u00f3\u00eb\u0001\u0000\u0000\u0000\u00f3\u00ec\u0001\u0000\u0000\u0000"+
		"\u00f3\u00ee\u0001\u0000\u0000\u0000\u00f3\u00f0\u0001\u0000\u0000\u0000"+
		"\u00f3\u00f1\u0001\u0000\u0000\u0000\u00f3\u00f2\u0001\u0000\u0000\u0000"+
		"\u00f4\u001b\u0001\u0000\u0000\u0000\u00f5\u00fe\u0005*\u0000\u0000\u00f6"+
		"\u00fb\u0003>\u001f\u0000\u00f7\u00f8\u0005\u0001\u0000\u0000\u00f8\u00fa"+
		"\u0003>\u001f\u0000\u00f9\u00f7\u0001\u0000\u0000\u0000\u00fa\u00fd\u0001"+
		"\u0000\u0000\u0000\u00fb\u00f9\u0001\u0000\u0000\u0000\u00fb\u00fc\u0001"+
		"\u0000\u0000\u0000\u00fc\u00ff\u0001\u0000\u0000\u0000\u00fd\u00fb\u0001"+
		"\u0000\u0000\u0000\u00fe\u00f6\u0001\u0000\u0000\u0000\u00fe\u00ff\u0001"+
		"\u0000\u0000\u0000\u00ff\u0100\u0001\u0000\u0000\u0000\u0100\u0101\u0005"+
		"+\u0000\u0000\u0101\u001d\u0001\u0000\u0000\u0000\u0102\u0104\u0005,\u0000"+
		"\u0000\u0103\u0105\u0003 \u0010\u0000\u0104\u0103\u0001\u0000\u0000\u0000"+
		"\u0104\u0105\u0001\u0000\u0000\u0000\u0105\u0106\u0001\u0000\u0000\u0000"+
		"\u0106\u0107\u0005-\u0000\u0000\u0107\u001f\u0001\u0000\u0000\u0000\u0108"+
		"\u0109\u0003\u000e\u0007\u0000\u0109\u010a\u0005\u0001\u0000\u0000\u010a"+
		"\u010b\u0003 \u0010\u0000\u010b\u0113\u0001\u0000\u0000\u0000\u010c\u010d"+
		"\u0003`0\u0000\u010d\u010e\u0005\u0001\u0000\u0000\u010e\u010f\u0003 "+
		"\u0010\u0000\u010f\u0113\u0001\u0000\u0000\u0000\u0110\u0113\u0003\u000e"+
		"\u0007\u0000\u0111\u0113\u0003`0\u0000\u0112\u0108\u0001\u0000\u0000\u0000"+
		"\u0112\u010c\u0001\u0000\u0000\u0000\u0112\u0110\u0001\u0000\u0000\u0000"+
		"\u0112\u0111\u0001\u0000\u0000\u0000\u0113!\u0001\u0000\u0000\u0000\u0114"+
		"\u0115\u0005(\u0000\u0000\u0115\u011a\u0003\u0012\t\u0000\u0116\u0117"+
		"\u0005\u0001\u0000\u0000\u0117\u0119\u0003\u0012\t\u0000\u0118\u0116\u0001"+
		"\u0000\u0000\u0000\u0119\u011c\u0001\u0000\u0000\u0000\u011a\u0118\u0001"+
		"\u0000\u0000\u0000\u011a\u011b\u0001\u0000\u0000\u0000\u011b\u011d\u0001"+
		"\u0000\u0000\u0000\u011c\u011a\u0001\u0000\u0000\u0000\u011d\u011e\u0005"+
		")\u0000\u0000\u011e#\u0001\u0000\u0000\u0000\u011f\u0121\u0003&\u0013"+
		"\u0000\u0120\u011f\u0001\u0000\u0000\u0000\u0121\u0122\u0001\u0000\u0000"+
		"\u0000\u0122\u0120\u0001\u0000\u0000\u0000\u0122\u0123\u0001\u0000\u0000"+
		"\u0000\u0123%\u0001\u0000\u0000\u0000\u0124\u012c\u0003(\u0014\u0000\u0125"+
		"\u012c\u0003*\u0015\u0000\u0126\u012c\u00030\u0018\u0000\u0127\u012c\u0003"+
		"2\u0019\u0000\u0128\u012c\u00038\u001c\u0000\u0129\u012c\u0003:\u001d"+
		"\u0000\u012a\u012c\u0003<\u001e\u0000\u012b\u0124\u0001\u0000\u0000\u0000"+
		"\u012b\u0125\u0001\u0000\u0000\u0000\u012b\u0126\u0001\u0000\u0000\u0000"+
		"\u012b\u0127\u0001\u0000\u0000\u0000\u012b\u0128\u0001\u0000\u0000\u0000"+
		"\u012b\u0129\u0001\u0000\u0000\u0000\u012b\u012a\u0001\u0000\u0000\u0000"+
		"\u012c\'\u0001\u0000\u0000\u0000\u012d\u0137\u0003\u000e\u0007\u0000\u012e"+
		"\u012f\u0003H$\u0000\u012f\u0130\u0005\u001e\u0000\u0000\u0130\u0131\u0003"+
		">\u001f\u0000\u0131\u0137\u0001\u0000\u0000\u0000\u0132\u0133\u0003J%"+
		"\u0000\u0133\u0134\u0005\u001e\u0000\u0000\u0134\u0135\u0003>\u001f\u0000"+
		"\u0135\u0137\u0001\u0000\u0000\u0000\u0136\u012d\u0001\u0000\u0000\u0000"+
		"\u0136\u012e\u0001\u0000\u0000\u0000\u0136\u0132\u0001\u0000\u0000\u0000"+
		"\u0137)\u0001\u0000\u0000\u0000\u0138\u0139\u00051\u0000\u0000\u0139\u013b"+
		"\u0005(\u0000\u0000\u013a\u013c\u0003,\u0016\u0000\u013b\u013a\u0001\u0000"+
		"\u0000\u0000\u013b\u013c\u0001\u0000\u0000\u0000\u013c\u013d\u0001\u0000"+
		"\u0000\u0000\u013d\u013e\u0005)\u0000\u0000\u013e+\u0001\u0000\u0000\u0000"+
		"\u013f\u0144\u0003.\u0017\u0000\u0140\u0141\u0005\u0001\u0000\u0000\u0141"+
		"\u0143\u0003,\u0016\u0000\u0142\u0140\u0001\u0000\u0000\u0000\u0143\u0146"+
		"\u0001\u0000\u0000\u0000\u0144\u0142\u0001\u0000\u0000\u0000\u0144\u0145"+
		"\u0001\u0000\u0000\u0000\u0145-\u0001\u0000\u0000\u0000\u0146\u0144\u0001"+
		"\u0000\u0000\u0000\u0147\u014d\u0003(\u0014\u0000\u0148\u014d\u00051\u0000"+
		"\u0000\u0149\u014d\u0003\u0010\b\u0000\u014a\u014d\u0003H$\u0000\u014b"+
		"\u014d\u0003J%\u0000\u014c\u0147\u0001\u0000\u0000\u0000\u014c\u0148\u0001"+
		"\u0000\u0000\u0000\u014c\u0149\u0001\u0000\u0000\u0000\u014c\u014a\u0001"+
		"\u0000\u0000\u0000\u014c\u014b\u0001\u0000\u0000\u0000\u014d/\u0001\u0000"+
		"\u0000\u0000\u014e\u014f\u0005\r\u0000\u0000\u014f\u0150\u0003>\u001f"+
		"\u0000\u01501\u0001\u0000\u0000\u0000\u0151\u0152\u0005\u000e\u0000\u0000"+
		"\u0152\u0153\u0005(\u0000\u0000\u0153\u0154\u0003R)\u0000\u0154\u0155"+
		"\u0005)\u0000\u0000\u0155\u0156\u0005,\u0000\u0000\u0156\u0157\u0003$"+
		"\u0012\u0000\u0157\u015b\u0005-\u0000\u0000\u0158\u015a\u00034\u001a\u0000"+
		"\u0159\u0158\u0001\u0000\u0000\u0000\u015a\u015d\u0001\u0000\u0000\u0000"+
		"\u015b\u0159\u0001\u0000\u0000\u0000\u015b\u015c\u0001\u0000\u0000\u0000"+
		"\u015c\u015f\u0001\u0000\u0000\u0000\u015d\u015b\u0001\u0000\u0000\u0000"+
		"\u015e\u0160\u00036\u001b\u0000\u015f\u015e\u0001\u0000\u0000\u0000\u015f"+
		"\u0160\u0001\u0000\u0000\u0000\u01603\u0001\u0000\u0000\u0000\u0161\u0162"+
		"\u0005\u000f\u0000\u0000\u0162\u0163\u0005(\u0000\u0000\u0163\u0164\u0003"+
		"R)\u0000\u0164\u0165\u0005)\u0000\u0000\u0165\u0166\u0005,\u0000\u0000"+
		"\u0166\u0167\u0003$\u0012\u0000\u0167\u0168\u0005-\u0000\u0000\u01685"+
		"\u0001\u0000\u0000\u0000\u0169\u016a\u0005\u0010\u0000\u0000\u016a\u016b"+
		"\u0005,\u0000\u0000\u016b\u016c\u0003$\u0012\u0000\u016c\u016d\u0005-"+
		"\u0000\u0000\u016d7\u0001\u0000\u0000\u0000\u016e\u016f\u0005\u0011\u0000"+
		"\u0000\u016f\u0170\u0005(\u0000\u0000\u0170\u0171\u0003(\u0014\u0000\u0171"+
		"\u0172\u0005/\u0000\u0000\u0172\u0173\u0003R)\u0000\u0173\u0174\u0005"+
		"/\u0000\u0000\u0174\u0175\u0003(\u0014\u0000\u0175\u0176\u0005)\u0000"+
		"\u0000\u0176\u0177\u0005,\u0000\u0000\u0177\u0178\u0003$\u0012\u0000\u0178"+
		"\u0179\u0005-\u0000\u0000\u01799\u0001\u0000\u0000\u0000\u017a\u017b\u0005"+
		"\u0012\u0000\u0000\u017b\u017c\u0005(\u0000\u0000\u017c\u017d\u0003R)"+
		"\u0000\u017d\u017e\u0005)\u0000\u0000\u017e\u017f\u0005,\u0000\u0000\u017f"+
		"\u0180\u0003$\u0012\u0000\u0180\u0181\u0005-\u0000\u0000\u0181;\u0001"+
		"\u0000\u0000\u0000\u0182\u0183\u0005\u0013\u0000\u0000\u0183\u0184\u0005"+
		",\u0000\u0000\u0184\u0185\u0003$\u0012\u0000\u0185\u0186\u0005-\u0000"+
		"\u0000\u0186\u0187\u0005\u0012\u0000\u0000\u0187\u0188\u0005(\u0000\u0000"+
		"\u0188\u0189\u0003R)\u0000\u0189\u018a\u0005)\u0000\u0000\u018a=\u0001"+
		"\u0000\u0000\u0000\u018b\u0196\u00051\u0000\u0000\u018c\u0196\u0003B!"+
		"\u0000\u018d\u0196\u0003\u001c\u000e\u0000\u018e\u0196\u0003\u001e\u000f"+
		"\u0000\u018f\u0196\u0003H$\u0000\u0190\u0196\u0003J%\u0000\u0191\u0196"+
		"\u0003L&\u0000\u0192\u0196\u0003R)\u0000\u0193\u0196\u0003*\u0015\u0000"+
		"\u0194\u0196\u0003@ \u0000\u0195\u018b\u0001\u0000\u0000\u0000\u0195\u018c"+
		"\u0001\u0000\u0000\u0000\u0195\u018d\u0001\u0000\u0000\u0000\u0195\u018e"+
		"\u0001\u0000\u0000\u0000\u0195\u018f\u0001\u0000\u0000\u0000\u0195\u0190"+
		"\u0001\u0000\u0000\u0000\u0195\u0191\u0001\u0000\u0000\u0000\u0195\u0192"+
		"\u0001\u0000\u0000\u0000\u0195\u0193\u0001\u0000\u0000\u0000\u0195\u0194"+
		"\u0001\u0000\u0000\u0000\u0196?\u0001\u0000\u0000\u0000\u0197\u0198\u0006"+
		" \uffff\uffff\u0000\u0198\u019b\u0005\u000b\u0000\u0000\u0199\u019b\u0005"+
		"1\u0000\u0000\u019a\u0197\u0001\u0000\u0000\u0000\u019a\u0199\u0001\u0000"+
		"\u0000\u0000\u019b\u01a1\u0001\u0000\u0000\u0000\u019c\u019d\n\u0003\u0000"+
		"\u0000\u019d\u019e\u0005\u0018\u0000\u0000\u019e\u01a0\u0003@ \u0004\u019f"+
		"\u019c\u0001\u0000\u0000\u0000\u01a0\u01a3\u0001\u0000\u0000\u0000\u01a1"+
		"\u019f\u0001\u0000\u0000\u0000\u01a1\u01a2\u0001\u0000\u0000\u0000\u01a2"+
		"A\u0001\u0000\u0000\u0000\u01a3\u01a1\u0001\u0000\u0000\u0000\u01a4\u01a5"+
		"\u0003D\"\u0000\u01a5\u01a6\u0005\u0018\u0000\u0000\u01a6\u01a7\u0003"+
		"B!\u0000\u01a7\u01ae\u0001\u0000\u0000\u0000\u01a8\u01a9\u0003D\"\u0000"+
		"\u01a9\u01aa\u0005\u0019\u0000\u0000\u01aa\u01ab\u0003B!\u0000\u01ab\u01ae"+
		"\u0001\u0000\u0000\u0000\u01ac\u01ae\u0003D\"\u0000\u01ad\u01a4\u0001"+
		"\u0000\u0000\u0000\u01ad\u01a8\u0001\u0000\u0000\u0000\u01ad\u01ac\u0001"+
		"\u0000\u0000\u0000\u01aeC\u0001\u0000\u0000\u0000\u01af\u01b0\u0003F#"+
		"\u0000\u01b0\u01b1\u0005\u001a\u0000\u0000\u01b1\u01b2\u0003D\"\u0000"+
		"\u01b2\u01c1\u0001\u0000\u0000\u0000\u01b3\u01b4\u0003F#\u0000\u01b4\u01b5"+
		"\u0005\u001b\u0000\u0000\u01b5\u01b6\u0003D\"\u0000\u01b6\u01c1\u0001"+
		"\u0000\u0000\u0000\u01b7\u01b8\u0003F#\u0000\u01b8\u01b9\u0005\u001d\u0000"+
		"\u0000\u01b9\u01ba\u0003D\"\u0000\u01ba\u01c1\u0001\u0000\u0000\u0000"+
		"\u01bb\u01bc\u0003F#\u0000\u01bc\u01bd\u0005\u001c\u0000\u0000\u01bd\u01be"+
		"\u0003D\"\u0000\u01be\u01c1\u0001\u0000\u0000\u0000\u01bf\u01c1\u0003"+
		"F#\u0000\u01c0\u01af\u0001\u0000\u0000\u0000\u01c0\u01b3\u0001\u0000\u0000"+
		"\u0000\u01c0\u01b7\u0001\u0000\u0000\u0000\u01c0\u01bb\u0001\u0000\u0000"+
		"\u0000\u01c0\u01bf\u0001\u0000\u0000\u0000\u01c1E\u0001\u0000\u0000\u0000"+
		"\u01c2\u01c3\u0005(\u0000\u0000\u01c3\u01c4\u0003B!\u0000\u01c4\u01c5"+
		"\u0005)\u0000\u0000\u01c5\u01d1\u0001\u0000\u0000\u0000\u01c6\u01d1\u0005"+
		"\f\u0000\u0000\u01c7\u01c8\u0005\u0018\u0000\u0000\u01c8\u01d1\u0003F"+
		"#\u0000\u01c9\u01ca\u0005\u0019\u0000\u0000\u01ca\u01d1\u0003F#\u0000"+
		"\u01cb\u01d1\u0005\b\u0000\u0000\u01cc\u01d1\u0005\t\u0000\u0000\u01cd"+
		"\u01d1\u0005\n\u0000\u0000\u01ce\u01d1\u0003L&\u0000\u01cf\u01d1\u0005"+
		"1\u0000\u0000\u01d0\u01c2\u0001\u0000\u0000\u0000\u01d0\u01c6\u0001\u0000"+
		"\u0000\u0000\u01d0\u01c7\u0001\u0000\u0000\u0000\u01d0\u01c9\u0001\u0000"+
		"\u0000\u0000\u01d0\u01cb\u0001\u0000\u0000\u0000\u01d0\u01cc\u0001\u0000"+
		"\u0000\u0000\u01d0\u01cd\u0001\u0000\u0000\u0000\u01d0\u01ce\u0001\u0000"+
		"\u0000\u0000\u01d0\u01cf\u0001\u0000\u0000\u0000\u01d1G\u0001\u0000\u0000"+
		"\u0000\u01d2\u01d7\u00051\u0000\u0000\u01d3\u01d4\u0005*\u0000\u0000\u01d4"+
		"\u01d5\u0003B!\u0000\u01d5\u01d6\u0005+\u0000\u0000\u01d6\u01d8\u0001"+
		"\u0000\u0000\u0000\u01d7\u01d3\u0001\u0000\u0000\u0000\u01d8\u01d9\u0001"+
		"\u0000\u0000\u0000\u01d9\u01d7\u0001\u0000\u0000\u0000\u01d9\u01da\u0001"+
		"\u0000\u0000\u0000\u01daI\u0001\u0000\u0000\u0000\u01db\u01de\u00051\u0000"+
		"\u0000\u01dc\u01dd\u00050\u0000\u0000\u01dd\u01df\u00051\u0000\u0000\u01de"+
		"\u01dc\u0001\u0000\u0000\u0000\u01df\u01e0\u0001\u0000\u0000\u0000\u01e0"+
		"\u01de\u0001\u0000\u0000\u0000\u01e0\u01e1\u0001\u0000\u0000\u0000\u01e1"+
		"K\u0001\u0000\u0000\u0000\u01e2\u01e3\u0006&\uffff\uffff\u0000\u01e3\u01e9"+
		"\u0005\u0006\u0000\u0000\u01e4\u01e9\u0005\u0007\u0000\u0000\u01e5\u01e9"+
		"\u00051\u0000\u0000\u01e6\u01e9\u0003\u0012\t\u0000\u01e7\u01e9\u0003"+
		"\"\u0011\u0000\u01e8\u01e2\u0001\u0000\u0000\u0000\u01e8\u01e4\u0001\u0000"+
		"\u0000\u0000\u01e8\u01e5\u0001\u0000\u0000\u0000\u01e8\u01e6\u0001\u0000"+
		"\u0000\u0000\u01e8\u01e7\u0001\u0000\u0000\u0000\u01e9\u01f2\u0001\u0000"+
		"\u0000\u0000\u01ea\u01eb\n\u0007\u0000\u0000\u01eb\u01ec\u0005\u001a\u0000"+
		"\u0000\u01ec\u01f1\u0003L&\b\u01ed\u01ee\n\u0006\u0000\u0000\u01ee\u01ef"+
		"\u0005.\u0000\u0000\u01ef\u01f1\u0003L&\u0007\u01f0\u01ea\u0001\u0000"+
		"\u0000\u0000\u01f0\u01ed\u0001\u0000\u0000\u0000\u01f1\u01f4\u0001\u0000"+
		"\u0000\u0000\u01f2\u01f0\u0001\u0000\u0000\u0000\u01f2\u01f3\u0001\u0000"+
		"\u0000\u0000\u01f3M\u0001\u0000\u0000\u0000\u01f4\u01f2\u0001\u0000\u0000"+
		"\u0000\u01f5\u01fb\u0003P(\u0000\u01f6\u01fb\u0005\u001f\u0000\u0000\u01f7"+
		"\u01fb\u0005 \u0000\u0000\u01f8\u01fb\u0005!\u0000\u0000\u01f9\u01fb\u0005"+
		"\"\u0000\u0000\u01fa\u01f5\u0001\u0000\u0000\u0000\u01fa\u01f6\u0001\u0000"+
		"\u0000\u0000\u01fa\u01f7\u0001\u0000\u0000\u0000\u01fa\u01f8\u0001\u0000"+
		"\u0000\u0000\u01fa\u01f9\u0001\u0000\u0000\u0000\u01fbO\u0001\u0000\u0000"+
		"\u0000\u01fc\u01fd\u0007\u0000\u0000\u0000\u01fdQ\u0001\u0000\u0000\u0000"+
		"\u01fe\u01ff\u0003T*\u0000\u01ffS\u0001\u0000\u0000\u0000\u0200\u0201"+
		"\u0006*\uffff\uffff\u0000\u0201\u0202\u0003V+\u0000\u0202\u0208\u0001"+
		"\u0000\u0000\u0000\u0203\u0204\n\u0002\u0000\u0000\u0204\u0205\u0005%"+
		"\u0000\u0000\u0205\u0207\u0003T*\u0003\u0206\u0203\u0001\u0000\u0000\u0000"+
		"\u0207\u020a\u0001\u0000\u0000\u0000\u0208\u0206\u0001\u0000\u0000\u0000"+
		"\u0208\u0209\u0001\u0000\u0000\u0000\u0209U\u0001\u0000\u0000\u0000\u020a"+
		"\u0208\u0001\u0000\u0000\u0000\u020b\u020c\u0006+\uffff\uffff\u0000\u020c"+
		"\u020d\u0003X,\u0000\u020d\u0213\u0001\u0000\u0000\u0000\u020e\u020f\n"+
		"\u0002\u0000\u0000\u020f\u0210\u0005&\u0000\u0000\u0210\u0212\u0003V+"+
		"\u0003\u0211\u020e\u0001\u0000\u0000\u0000\u0212\u0215\u0001\u0000\u0000"+
		"\u0000\u0213\u0211\u0001\u0000\u0000\u0000\u0213\u0214\u0001\u0000\u0000"+
		"\u0000\u0214W\u0001\u0000\u0000\u0000\u0215\u0213\u0001\u0000\u0000\u0000"+
		"\u0216\u0217\u0003B!\u0000\u0217\u0218\u0003N\'\u0000\u0218\u0219\u0003"+
		"B!\u0000\u0219\u0224\u0001\u0000\u0000\u0000\u021a\u021b\u0003@ \u0000"+
		"\u021b\u021c\u0003P(\u0000\u021c\u021d\u0003@ \u0000\u021d\u0224\u0001"+
		"\u0000\u0000\u0000\u021e\u021f\u0003Z-\u0000\u021f\u0220\u0003P(\u0000"+
		"\u0220\u0221\u0003Z-\u0000\u0221\u0224\u0001\u0000\u0000\u0000\u0222\u0224"+
		"\u0003Z-\u0000\u0223\u0216\u0001\u0000\u0000\u0000\u0223\u021a\u0001\u0000"+
		"\u0000\u0000\u0223\u021e\u0001\u0000\u0000\u0000\u0223\u0222\u0001\u0000"+
		"\u0000\u0000\u0224Y\u0001\u0000\u0000\u0000\u0225\u0226\u0005\'\u0000"+
		"\u0000\u0226\u0229\u0003Z-\u0000\u0227\u0229\u0003\\.\u0000\u0228\u0225"+
		"\u0001\u0000\u0000\u0000\u0228\u0227\u0001\u0000\u0000\u0000\u0229[\u0001"+
		"\u0000\u0000\u0000\u022a\u022b\u0005(\u0000\u0000\u022b\u022c\u0003R)"+
		"\u0000\u022c\u022d\u0005)\u0000\u0000\u022d\u0233\u0001\u0000\u0000\u0000"+
		"\u022e\u0233\u0005\u0014\u0000\u0000\u022f\u0233\u0005\u0015\u0000\u0000"+
		"\u0230\u0233\u0005\b\u0000\u0000\u0231\u0233\u00051\u0000\u0000\u0232"+
		"\u022a\u0001\u0000\u0000\u0000\u0232\u022e\u0001\u0000\u0000\u0000\u0232"+
		"\u022f\u0001\u0000\u0000\u0000\u0232\u0230\u0001\u0000\u0000\u0000\u0232"+
		"\u0231\u0001\u0000\u0000\u0000\u0233]\u0001\u0000\u0000\u0000\u0234\u0236"+
		"\u0003`0\u0000\u0235\u0234\u0001\u0000\u0000\u0000\u0236\u0237\u0001\u0000"+
		"\u0000\u0000\u0237\u0235\u0001\u0000\u0000\u0000\u0237\u0238\u0001\u0000"+
		"\u0000\u0000\u0238_\u0001\u0000\u0000\u0000\u0239\u023a\u0005\u0017\u0000"+
		"\u0000\u023a\u023b\u00051\u0000\u0000\u023b\u023d\u0005(\u0000\u0000\u023c"+
		"\u023e\u0003b1\u0000\u023d\u023c\u0001\u0000\u0000\u0000\u023d\u023e\u0001"+
		"\u0000\u0000\u0000\u023e\u023f\u0001\u0000\u0000\u0000\u023f\u0240\u0005"+
		")\u0000\u0000\u0240\u0242\u0005,\u0000\u0000\u0241\u0243\u0003$\u0012"+
		"\u0000\u0242\u0241\u0001\u0000\u0000\u0000\u0242\u0243\u0001\u0000\u0000"+
		"\u0000\u0243\u0244\u0001\u0000\u0000\u0000\u0244\u0245\u0005-\u0000\u0000"+
		"\u0245a\u0001\u0000\u0000\u0000\u0246\u0249\u0003d2\u0000\u0247\u0248"+
		"\u0005\u0001\u0000\u0000\u0248\u024a\u0003f3\u0000\u0249\u0247\u0001\u0000"+
		"\u0000\u0000\u0249\u024a\u0001\u0000\u0000\u0000\u024a\u024d\u0001\u0000"+
		"\u0000\u0000\u024b\u024d\u0003f3\u0000\u024c\u0246\u0001\u0000\u0000\u0000"+
		"\u024c\u024b\u0001\u0000\u0000\u0000\u024dc\u0001\u0000\u0000\u0000\u024e"+
		"\u0253\u00051\u0000\u0000\u024f\u0250\u0005\u0001\u0000\u0000\u0250\u0252"+
		"\u00051\u0000\u0000\u0251\u024f\u0001\u0000\u0000\u0000\u0252\u0255\u0001"+
		"\u0000\u0000\u0000\u0253\u0251\u0001\u0000\u0000\u0000\u0253\u0254\u0001"+
		"\u0000\u0000\u0000\u0254e\u0001\u0000\u0000\u0000\u0255\u0253\u0001\u0000"+
		"\u0000\u0000\u0256\u025b\u0003(\u0014\u0000\u0257\u0258\u0005\u0001\u0000"+
		"\u0000\u0258\u025a\u0003(\u0014\u0000\u0259\u0257\u0001\u0000\u0000\u0000"+
		"\u025a\u025d\u0001\u0000\u0000\u0000\u025b\u0259\u0001\u0000\u0000\u0000"+
		"\u025b\u025c\u0001\u0000\u0000\u0000\u025cg\u0001\u0000\u0000\u0000\u025d"+
		"\u025b\u0001\u0000\u0000\u0000\u025e\u025f\u0005\u0016\u0000\u0000\u025f"+
		"\u0261\u0005(\u0000\u0000\u0260\u0262\u0003b1\u0000\u0261\u0260\u0001"+
		"\u0000\u0000\u0000\u0261\u0262\u0001\u0000\u0000\u0000\u0262\u0263\u0001"+
		"\u0000\u0000\u0000\u0263\u0264\u0005)\u0000\u0000\u0264\u0266\u0005,\u0000"+
		"\u0000\u0265\u0267\u0003$\u0012\u0000\u0266\u0265\u0001\u0000\u0000\u0000"+
		"\u0266\u0267\u0001\u0000\u0000\u0000\u0267\u0268\u0001\u0000\u0000\u0000"+
		"\u0268\u0269\u0005-\u0000\u0000\u0269i\u0001\u0000\u0000\u00007knqtz\u0083"+
		"\u008a\u0090\u0098\u00a3\u00af\u00b7\u00c7\u00d2\u00e5\u00f3\u00fb\u00fe"+
		"\u0104\u0112\u011a\u0122\u012b\u0136\u013b\u0144\u014c\u015b\u015f\u0195"+
		"\u019a\u01a1\u01ad\u01c0\u01d0\u01d9\u01e0\u01e8\u01f0\u01f2\u01fa\u0208"+
		"\u0213\u0223\u0228\u0232\u0237\u023d\u0242\u0249\u024c\u0253\u025b\u0261"+
		"\u0266";
	public static final ATN _ATN =
		new ATNDeserializer().deserialize(_serializedATN.toCharArray());
	static {
		_decisionToDFA = new DFA[_ATN.getNumberOfDecisions()];
		for (int i = 0; i < _ATN.getNumberOfDecisions(); i++) {
			_decisionToDFA[i] = new DFA(_ATN.getDecisionState(i), i);
		}
	}
}