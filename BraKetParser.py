# Generated from BraKet.g4 by ANTLR 4.13.2
# encoding: utf-8
from antlr4 import *
from io import StringIO
import sys
if sys.version_info[1] > 5:
	from typing import TextIO
else:
	from typing.io import TextIO

def serializedATN():
    return [
        4,1,19,170,2,0,7,0,2,1,7,1,2,2,7,2,2,3,7,3,2,4,7,4,2,5,7,5,2,6,7,
        6,2,7,7,7,2,8,7,8,2,9,7,9,2,10,7,10,2,11,7,11,2,12,7,12,2,13,7,13,
        2,14,7,14,2,15,7,15,2,16,7,16,2,17,7,17,1,0,3,0,38,8,0,1,0,3,0,41,
        8,0,1,1,1,1,5,1,45,8,1,10,1,12,1,48,9,1,1,2,1,2,1,2,1,2,1,2,1,2,
        3,2,56,8,2,1,3,1,3,1,3,5,3,61,8,3,10,3,12,3,64,9,3,1,4,4,4,67,8,
        4,11,4,12,4,68,1,5,1,5,1,5,1,6,4,6,75,8,6,11,6,12,6,76,1,7,1,7,1,
        7,1,7,1,8,1,8,1,9,1,9,1,10,1,10,1,10,3,10,90,8,10,1,10,1,10,1,11,
        1,11,1,11,5,11,97,8,11,10,11,12,11,100,9,11,1,12,1,12,1,12,3,12,
        105,8,12,1,13,1,13,1,13,3,13,110,8,13,1,14,1,14,1,14,3,14,115,8,
        14,1,14,1,14,1,14,5,14,120,8,14,10,14,12,14,123,9,14,1,15,1,15,1,
        15,1,15,1,15,1,15,1,15,1,15,1,15,3,15,134,8,15,1,16,1,16,1,16,1,
        16,1,16,1,16,1,16,1,16,1,16,1,16,1,16,1,16,1,16,1,16,1,16,1,16,1,
        16,3,16,153,8,16,1,17,1,17,1,17,1,17,1,17,1,17,1,17,1,17,1,17,1,
        17,1,17,1,17,1,17,3,17,168,8,17,1,17,0,1,28,18,0,2,4,6,8,10,12,14,
        16,18,20,22,24,26,28,30,32,34,0,1,1,0,7,10,179,0,37,1,0,0,0,2,42,
        1,0,0,0,4,55,1,0,0,0,6,57,1,0,0,0,8,66,1,0,0,0,10,70,1,0,0,0,12,
        74,1,0,0,0,14,78,1,0,0,0,16,82,1,0,0,0,18,84,1,0,0,0,20,86,1,0,0,
        0,22,93,1,0,0,0,24,104,1,0,0,0,26,109,1,0,0,0,28,114,1,0,0,0,30,
        133,1,0,0,0,32,152,1,0,0,0,34,167,1,0,0,0,36,38,3,2,1,0,37,36,1,
        0,0,0,37,38,1,0,0,0,38,40,1,0,0,0,39,41,3,8,4,0,40,39,1,0,0,0,40,
        41,1,0,0,0,41,1,1,0,0,0,42,46,3,4,2,0,43,45,3,4,2,0,44,43,1,0,0,
        0,45,48,1,0,0,0,46,44,1,0,0,0,46,47,1,0,0,0,47,3,1,0,0,0,48,46,1,
        0,0,0,49,50,5,3,0,0,50,51,5,6,0,0,51,52,5,4,0,0,52,56,3,6,3,0,53,
        54,5,4,0,0,54,56,5,6,0,0,55,49,1,0,0,0,55,53,1,0,0,0,56,5,1,0,0,
        0,57,62,5,6,0,0,58,59,5,1,0,0,59,61,5,6,0,0,60,58,1,0,0,0,61,64,
        1,0,0,0,62,60,1,0,0,0,62,63,1,0,0,0,63,7,1,0,0,0,64,62,1,0,0,0,65,
        67,3,10,5,0,66,65,1,0,0,0,67,68,1,0,0,0,68,66,1,0,0,0,68,69,1,0,
        0,0,69,9,1,0,0,0,70,71,5,5,0,0,71,72,3,14,7,0,72,11,1,0,0,0,73,75,
        3,14,7,0,74,73,1,0,0,0,75,76,1,0,0,0,76,74,1,0,0,0,76,77,1,0,0,0,
        77,13,1,0,0,0,78,79,5,6,0,0,79,80,5,17,0,0,80,81,3,26,13,0,81,15,
        1,0,0,0,82,83,7,0,0,0,83,17,1,0,0,0,84,85,3,14,7,0,85,19,1,0,0,0,
        86,87,5,6,0,0,87,89,5,18,0,0,88,90,3,22,11,0,89,88,1,0,0,0,89,90,
        1,0,0,0,90,91,1,0,0,0,91,92,5,19,0,0,92,21,1,0,0,0,93,98,3,24,12,
        0,94,95,5,1,0,0,95,97,3,22,11,0,96,94,1,0,0,0,97,100,1,0,0,0,98,
        96,1,0,0,0,98,99,1,0,0,0,99,23,1,0,0,0,100,98,1,0,0,0,101,105,3,
        18,9,0,102,105,5,6,0,0,103,105,3,16,8,0,104,101,1,0,0,0,104,102,
        1,0,0,0,104,103,1,0,0,0,105,25,1,0,0,0,106,110,3,28,14,0,107,110,
        3,30,15,0,108,110,3,20,10,0,109,106,1,0,0,0,109,107,1,0,0,0,109,
        108,1,0,0,0,110,27,1,0,0,0,111,112,6,14,-1,0,112,115,5,10,0,0,113,
        115,5,6,0,0,114,111,1,0,0,0,114,113,1,0,0,0,115,121,1,0,0,0,116,
        117,10,3,0,0,117,118,5,11,0,0,118,120,3,28,14,4,119,116,1,0,0,0,
        120,123,1,0,0,0,121,119,1,0,0,0,121,122,1,0,0,0,122,29,1,0,0,0,123,
        121,1,0,0,0,124,125,3,32,16,0,125,126,5,11,0,0,126,127,3,30,15,0,
        127,134,1,0,0,0,128,129,3,32,16,0,129,130,5,12,0,0,130,131,3,30,
        15,0,131,134,1,0,0,0,132,134,3,32,16,0,133,124,1,0,0,0,133,128,1,
        0,0,0,133,132,1,0,0,0,134,31,1,0,0,0,135,136,3,34,17,0,136,137,5,
        13,0,0,137,138,3,32,16,0,138,153,1,0,0,0,139,140,3,34,17,0,140,141,
        5,14,0,0,141,142,3,32,16,0,142,153,1,0,0,0,143,144,3,34,17,0,144,
        145,5,16,0,0,145,146,3,32,16,0,146,153,1,0,0,0,147,148,3,34,17,0,
        148,149,5,15,0,0,149,150,3,32,16,0,150,153,1,0,0,0,151,153,3,34,
        17,0,152,135,1,0,0,0,152,139,1,0,0,0,152,143,1,0,0,0,152,147,1,0,
        0,0,152,151,1,0,0,0,153,33,1,0,0,0,154,155,5,18,0,0,155,156,3,30,
        15,0,156,157,5,19,0,0,157,168,1,0,0,0,158,159,5,11,0,0,159,168,3,
        34,17,0,160,161,5,12,0,0,161,168,3,34,17,0,162,168,5,7,0,0,163,168,
        5,8,0,0,164,168,5,9,0,0,165,168,1,0,0,0,166,168,5,6,0,0,167,154,
        1,0,0,0,167,158,1,0,0,0,167,160,1,0,0,0,167,162,1,0,0,0,167,163,
        1,0,0,0,167,164,1,0,0,0,167,165,1,0,0,0,167,166,1,0,0,0,168,35,1,
        0,0,0,16,37,40,46,55,62,68,76,89,98,104,109,114,121,133,152,167
    ]

class BraKetParser ( Parser ):

    grammarFileName = "BraKet.g4"

    atn = ATNDeserializer().deserialize(serializedATN())

    decisionsToDFA = [ DFA(ds, i) for i, ds in enumerate(atn.decisionToState) ]

    sharedContextCache = PredictionContextCache()

    literalNames = [ "<INVALID>", "','", "<INVALID>", "'from'", "'import'", 
                     "'const'", "<INVALID>", "<INVALID>", "<INVALID>", "<INVALID>", 
                     "<INVALID>", "'+'", "'-'", "'*'", "'/'", "'**'", "'%'", 
                     "'='", "'('", "')'" ]

    symbolicNames = [ "<INVALID>", "COMMA", "WS", "FROM", "IMPORT", "CONST", 
                      "IDENTIFIER", "INT", "FLOAT", "CHAR", "STRING", "ADD", 
                      "SUB", "MUL", "DIV", "EXP", "MOD", "ASSIGN", "LPAREN", 
                      "RPAREN" ]

    RULE_program = 0
    RULE_import_list = 1
    RULE_import_statement = 2
    RULE_func_list = 3
    RULE_const_decl_list = 4
    RULE_const_decl = 5
    RULE_var_decl_list = 6
    RULE_var_decl = 7
    RULE_value = 8
    RULE_assign_statement = 9
    RULE_func_call_statement = 10
    RULE_arg_list = 11
    RULE_arg = 12
    RULE_expression = 13
    RULE_string_expression = 14
    RULE_num_expression = 15
    RULE_num_term = 16
    RULE_num_factor = 17

    ruleNames =  [ "program", "import_list", "import_statement", "func_list", 
                   "const_decl_list", "const_decl", "var_decl_list", "var_decl", 
                   "value", "assign_statement", "func_call_statement", "arg_list", 
                   "arg", "expression", "string_expression", "num_expression", 
                   "num_term", "num_factor" ]

    EOF = Token.EOF
    COMMA=1
    WS=2
    FROM=3
    IMPORT=4
    CONST=5
    IDENTIFIER=6
    INT=7
    FLOAT=8
    CHAR=9
    STRING=10
    ADD=11
    SUB=12
    MUL=13
    DIV=14
    EXP=15
    MOD=16
    ASSIGN=17
    LPAREN=18
    RPAREN=19

    def __init__(self, input:TokenStream, output:TextIO = sys.stdout):
        super().__init__(input, output)
        self.checkVersion("4.13.2")
        self._interp = ParserATNSimulator(self, self.atn, self.decisionsToDFA, self.sharedContextCache)
        self._predicates = None




    class ProgramContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def import_list(self):
            return self.getTypedRuleContext(BraKetParser.Import_listContext,0)


        def const_decl_list(self):
            return self.getTypedRuleContext(BraKetParser.Const_decl_listContext,0)


        def getRuleIndex(self):
            return BraKetParser.RULE_program

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitProgram" ):
                return visitor.visitProgram(self)
            else:
                return visitor.visitChildren(self)




    def program(self):

        localctx = BraKetParser.ProgramContext(self, self._ctx, self.state)
        self.enterRule(localctx, 0, self.RULE_program)
        self._la = 0 # Token type
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 37
            self._errHandler.sync(self)
            _la = self._input.LA(1)
            if _la==3 or _la==4:
                self.state = 36
                self.import_list()


            self.state = 40
            self._errHandler.sync(self)
            _la = self._input.LA(1)
            if _la==5:
                self.state = 39
                self.const_decl_list()


        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class Import_listContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def import_statement(self, i:int=None):
            if i is None:
                return self.getTypedRuleContexts(BraKetParser.Import_statementContext)
            else:
                return self.getTypedRuleContext(BraKetParser.Import_statementContext,i)


        def getRuleIndex(self):
            return BraKetParser.RULE_import_list

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitImport_list" ):
                return visitor.visitImport_list(self)
            else:
                return visitor.visitChildren(self)




    def import_list(self):

        localctx = BraKetParser.Import_listContext(self, self._ctx, self.state)
        self.enterRule(localctx, 2, self.RULE_import_list)
        self._la = 0 # Token type
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 42
            self.import_statement()
            self.state = 46
            self._errHandler.sync(self)
            _la = self._input.LA(1)
            while _la==3 or _la==4:
                self.state = 43
                self.import_statement()
                self.state = 48
                self._errHandler.sync(self)
                _la = self._input.LA(1)

        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class Import_statementContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def FROM(self):
            return self.getToken(BraKetParser.FROM, 0)

        def IDENTIFIER(self):
            return self.getToken(BraKetParser.IDENTIFIER, 0)

        def IMPORT(self):
            return self.getToken(BraKetParser.IMPORT, 0)

        def func_list(self):
            return self.getTypedRuleContext(BraKetParser.Func_listContext,0)


        def getRuleIndex(self):
            return BraKetParser.RULE_import_statement

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitImport_statement" ):
                return visitor.visitImport_statement(self)
            else:
                return visitor.visitChildren(self)




    def import_statement(self):

        localctx = BraKetParser.Import_statementContext(self, self._ctx, self.state)
        self.enterRule(localctx, 4, self.RULE_import_statement)
        try:
            self.state = 55
            self._errHandler.sync(self)
            token = self._input.LA(1)
            if token in [3]:
                self.enterOuterAlt(localctx, 1)
                self.state = 49
                self.match(BraKetParser.FROM)
                self.state = 50
                self.match(BraKetParser.IDENTIFIER)
                self.state = 51
                self.match(BraKetParser.IMPORT)
                self.state = 52
                self.func_list()
                pass
            elif token in [4]:
                self.enterOuterAlt(localctx, 2)
                self.state = 53
                self.match(BraKetParser.IMPORT)
                self.state = 54
                self.match(BraKetParser.IDENTIFIER)
                pass
            else:
                raise NoViableAltException(self)

        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class Func_listContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def IDENTIFIER(self, i:int=None):
            if i is None:
                return self.getTokens(BraKetParser.IDENTIFIER)
            else:
                return self.getToken(BraKetParser.IDENTIFIER, i)

        def COMMA(self, i:int=None):
            if i is None:
                return self.getTokens(BraKetParser.COMMA)
            else:
                return self.getToken(BraKetParser.COMMA, i)

        def getRuleIndex(self):
            return BraKetParser.RULE_func_list

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitFunc_list" ):
                return visitor.visitFunc_list(self)
            else:
                return visitor.visitChildren(self)




    def func_list(self):

        localctx = BraKetParser.Func_listContext(self, self._ctx, self.state)
        self.enterRule(localctx, 6, self.RULE_func_list)
        self._la = 0 # Token type
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 57
            self.match(BraKetParser.IDENTIFIER)
            self.state = 62
            self._errHandler.sync(self)
            _la = self._input.LA(1)
            while _la==1:
                self.state = 58
                self.match(BraKetParser.COMMA)
                self.state = 59
                self.match(BraKetParser.IDENTIFIER)
                self.state = 64
                self._errHandler.sync(self)
                _la = self._input.LA(1)

        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class Const_decl_listContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def const_decl(self, i:int=None):
            if i is None:
                return self.getTypedRuleContexts(BraKetParser.Const_declContext)
            else:
                return self.getTypedRuleContext(BraKetParser.Const_declContext,i)


        def getRuleIndex(self):
            return BraKetParser.RULE_const_decl_list

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitConst_decl_list" ):
                return visitor.visitConst_decl_list(self)
            else:
                return visitor.visitChildren(self)




    def const_decl_list(self):

        localctx = BraKetParser.Const_decl_listContext(self, self._ctx, self.state)
        self.enterRule(localctx, 8, self.RULE_const_decl_list)
        self._la = 0 # Token type
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 66 
            self._errHandler.sync(self)
            _la = self._input.LA(1)
            while True:
                self.state = 65
                self.const_decl()
                self.state = 68 
                self._errHandler.sync(self)
                _la = self._input.LA(1)
                if not (_la==5):
                    break

        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class Const_declContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def CONST(self):
            return self.getToken(BraKetParser.CONST, 0)

        def var_decl(self):
            return self.getTypedRuleContext(BraKetParser.Var_declContext,0)


        def getRuleIndex(self):
            return BraKetParser.RULE_const_decl

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitConst_decl" ):
                return visitor.visitConst_decl(self)
            else:
                return visitor.visitChildren(self)




    def const_decl(self):

        localctx = BraKetParser.Const_declContext(self, self._ctx, self.state)
        self.enterRule(localctx, 10, self.RULE_const_decl)
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 70
            self.match(BraKetParser.CONST)
            self.state = 71
            self.var_decl()
        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class Var_decl_listContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def var_decl(self, i:int=None):
            if i is None:
                return self.getTypedRuleContexts(BraKetParser.Var_declContext)
            else:
                return self.getTypedRuleContext(BraKetParser.Var_declContext,i)


        def getRuleIndex(self):
            return BraKetParser.RULE_var_decl_list

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitVar_decl_list" ):
                return visitor.visitVar_decl_list(self)
            else:
                return visitor.visitChildren(self)




    def var_decl_list(self):

        localctx = BraKetParser.Var_decl_listContext(self, self._ctx, self.state)
        self.enterRule(localctx, 12, self.RULE_var_decl_list)
        self._la = 0 # Token type
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 74 
            self._errHandler.sync(self)
            _la = self._input.LA(1)
            while True:
                self.state = 73
                self.var_decl()
                self.state = 76 
                self._errHandler.sync(self)
                _la = self._input.LA(1)
                if not (_la==6):
                    break

        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class Var_declContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def IDENTIFIER(self):
            return self.getToken(BraKetParser.IDENTIFIER, 0)

        def ASSIGN(self):
            return self.getToken(BraKetParser.ASSIGN, 0)

        def expression(self):
            return self.getTypedRuleContext(BraKetParser.ExpressionContext,0)


        def getRuleIndex(self):
            return BraKetParser.RULE_var_decl

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitVar_decl" ):
                return visitor.visitVar_decl(self)
            else:
                return visitor.visitChildren(self)




    def var_decl(self):

        localctx = BraKetParser.Var_declContext(self, self._ctx, self.state)
        self.enterRule(localctx, 14, self.RULE_var_decl)
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 78
            self.match(BraKetParser.IDENTIFIER)
            self.state = 79
            self.match(BraKetParser.ASSIGN)
            self.state = 80
            self.expression()
        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class ValueContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def INT(self):
            return self.getToken(BraKetParser.INT, 0)

        def FLOAT(self):
            return self.getToken(BraKetParser.FLOAT, 0)

        def CHAR(self):
            return self.getToken(BraKetParser.CHAR, 0)

        def STRING(self):
            return self.getToken(BraKetParser.STRING, 0)

        def getRuleIndex(self):
            return BraKetParser.RULE_value

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitValue" ):
                return visitor.visitValue(self)
            else:
                return visitor.visitChildren(self)




    def value(self):

        localctx = BraKetParser.ValueContext(self, self._ctx, self.state)
        self.enterRule(localctx, 16, self.RULE_value)
        self._la = 0 # Token type
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 82
            _la = self._input.LA(1)
            if not((((_la) & ~0x3f) == 0 and ((1 << _la) & 1920) != 0)):
                self._errHandler.recoverInline(self)
            else:
                self._errHandler.reportMatch(self)
                self.consume()
        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class Assign_statementContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def var_decl(self):
            return self.getTypedRuleContext(BraKetParser.Var_declContext,0)


        def getRuleIndex(self):
            return BraKetParser.RULE_assign_statement

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitAssign_statement" ):
                return visitor.visitAssign_statement(self)
            else:
                return visitor.visitChildren(self)




    def assign_statement(self):

        localctx = BraKetParser.Assign_statementContext(self, self._ctx, self.state)
        self.enterRule(localctx, 18, self.RULE_assign_statement)
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 84
            self.var_decl()
        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class Func_call_statementContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def IDENTIFIER(self):
            return self.getToken(BraKetParser.IDENTIFIER, 0)

        def LPAREN(self):
            return self.getToken(BraKetParser.LPAREN, 0)

        def RPAREN(self):
            return self.getToken(BraKetParser.RPAREN, 0)

        def arg_list(self):
            return self.getTypedRuleContext(BraKetParser.Arg_listContext,0)


        def getRuleIndex(self):
            return BraKetParser.RULE_func_call_statement

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitFunc_call_statement" ):
                return visitor.visitFunc_call_statement(self)
            else:
                return visitor.visitChildren(self)




    def func_call_statement(self):

        localctx = BraKetParser.Func_call_statementContext(self, self._ctx, self.state)
        self.enterRule(localctx, 20, self.RULE_func_call_statement)
        self._la = 0 # Token type
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 86
            self.match(BraKetParser.IDENTIFIER)
            self.state = 87
            self.match(BraKetParser.LPAREN)
            self.state = 89
            self._errHandler.sync(self)
            _la = self._input.LA(1)
            if (((_la) & ~0x3f) == 0 and ((1 << _la) & 1984) != 0):
                self.state = 88
                self.arg_list()


            self.state = 91
            self.match(BraKetParser.RPAREN)
        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class Arg_listContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def arg(self):
            return self.getTypedRuleContext(BraKetParser.ArgContext,0)


        def COMMA(self, i:int=None):
            if i is None:
                return self.getTokens(BraKetParser.COMMA)
            else:
                return self.getToken(BraKetParser.COMMA, i)

        def arg_list(self, i:int=None):
            if i is None:
                return self.getTypedRuleContexts(BraKetParser.Arg_listContext)
            else:
                return self.getTypedRuleContext(BraKetParser.Arg_listContext,i)


        def getRuleIndex(self):
            return BraKetParser.RULE_arg_list

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitArg_list" ):
                return visitor.visitArg_list(self)
            else:
                return visitor.visitChildren(self)




    def arg_list(self):

        localctx = BraKetParser.Arg_listContext(self, self._ctx, self.state)
        self.enterRule(localctx, 22, self.RULE_arg_list)
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 93
            self.arg()
            self.state = 98
            self._errHandler.sync(self)
            _alt = self._interp.adaptivePredict(self._input,8,self._ctx)
            while _alt!=2 and _alt!=ATN.INVALID_ALT_NUMBER:
                if _alt==1:
                    self.state = 94
                    self.match(BraKetParser.COMMA)
                    self.state = 95
                    self.arg_list() 
                self.state = 100
                self._errHandler.sync(self)
                _alt = self._interp.adaptivePredict(self._input,8,self._ctx)

        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class ArgContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def assign_statement(self):
            return self.getTypedRuleContext(BraKetParser.Assign_statementContext,0)


        def IDENTIFIER(self):
            return self.getToken(BraKetParser.IDENTIFIER, 0)

        def value(self):
            return self.getTypedRuleContext(BraKetParser.ValueContext,0)


        def getRuleIndex(self):
            return BraKetParser.RULE_arg

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitArg" ):
                return visitor.visitArg(self)
            else:
                return visitor.visitChildren(self)




    def arg(self):

        localctx = BraKetParser.ArgContext(self, self._ctx, self.state)
        self.enterRule(localctx, 24, self.RULE_arg)
        try:
            self.state = 104
            self._errHandler.sync(self)
            la_ = self._interp.adaptivePredict(self._input,9,self._ctx)
            if la_ == 1:
                self.enterOuterAlt(localctx, 1)
                self.state = 101
                self.assign_statement()
                pass

            elif la_ == 2:
                self.enterOuterAlt(localctx, 2)
                self.state = 102
                self.match(BraKetParser.IDENTIFIER)
                pass

            elif la_ == 3:
                self.enterOuterAlt(localctx, 3)
                self.state = 103
                self.value()
                pass


        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class ExpressionContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def string_expression(self):
            return self.getTypedRuleContext(BraKetParser.String_expressionContext,0)


        def num_expression(self):
            return self.getTypedRuleContext(BraKetParser.Num_expressionContext,0)


        def func_call_statement(self):
            return self.getTypedRuleContext(BraKetParser.Func_call_statementContext,0)


        def getRuleIndex(self):
            return BraKetParser.RULE_expression

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitExpression" ):
                return visitor.visitExpression(self)
            else:
                return visitor.visitChildren(self)




    def expression(self):

        localctx = BraKetParser.ExpressionContext(self, self._ctx, self.state)
        self.enterRule(localctx, 26, self.RULE_expression)
        try:
            self.state = 109
            self._errHandler.sync(self)
            la_ = self._interp.adaptivePredict(self._input,10,self._ctx)
            if la_ == 1:
                self.enterOuterAlt(localctx, 1)
                self.state = 106
                self.string_expression(0)
                pass

            elif la_ == 2:
                self.enterOuterAlt(localctx, 2)
                self.state = 107
                self.num_expression()
                pass

            elif la_ == 3:
                self.enterOuterAlt(localctx, 3)
                self.state = 108
                self.func_call_statement()
                pass


        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class String_expressionContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def STRING(self):
            return self.getToken(BraKetParser.STRING, 0)

        def IDENTIFIER(self):
            return self.getToken(BraKetParser.IDENTIFIER, 0)

        def string_expression(self, i:int=None):
            if i is None:
                return self.getTypedRuleContexts(BraKetParser.String_expressionContext)
            else:
                return self.getTypedRuleContext(BraKetParser.String_expressionContext,i)


        def ADD(self):
            return self.getToken(BraKetParser.ADD, 0)

        def getRuleIndex(self):
            return BraKetParser.RULE_string_expression

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitString_expression" ):
                return visitor.visitString_expression(self)
            else:
                return visitor.visitChildren(self)



    def string_expression(self, _p:int=0):
        _parentctx = self._ctx
        _parentState = self.state
        localctx = BraKetParser.String_expressionContext(self, self._ctx, _parentState)
        _prevctx = localctx
        _startState = 28
        self.enterRecursionRule(localctx, 28, self.RULE_string_expression, _p)
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 114
            self._errHandler.sync(self)
            token = self._input.LA(1)
            if token in [10]:
                self.state = 112
                self.match(BraKetParser.STRING)
                pass
            elif token in [6]:
                self.state = 113
                self.match(BraKetParser.IDENTIFIER)
                pass
            else:
                raise NoViableAltException(self)

            self._ctx.stop = self._input.LT(-1)
            self.state = 121
            self._errHandler.sync(self)
            _alt = self._interp.adaptivePredict(self._input,12,self._ctx)
            while _alt!=2 and _alt!=ATN.INVALID_ALT_NUMBER:
                if _alt==1:
                    if self._parseListeners is not None:
                        self.triggerExitRuleEvent()
                    _prevctx = localctx
                    localctx = BraKetParser.String_expressionContext(self, _parentctx, _parentState)
                    self.pushNewRecursionContext(localctx, _startState, self.RULE_string_expression)
                    self.state = 116
                    if not self.precpred(self._ctx, 3):
                        from antlr4.error.Errors import FailedPredicateException
                        raise FailedPredicateException(self, "self.precpred(self._ctx, 3)")
                    self.state = 117
                    self.match(BraKetParser.ADD)
                    self.state = 118
                    self.string_expression(4) 
                self.state = 123
                self._errHandler.sync(self)
                _alt = self._interp.adaptivePredict(self._input,12,self._ctx)

        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.unrollRecursionContexts(_parentctx)
        return localctx


    class Num_expressionContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def num_term(self):
            return self.getTypedRuleContext(BraKetParser.Num_termContext,0)


        def ADD(self):
            return self.getToken(BraKetParser.ADD, 0)

        def num_expression(self):
            return self.getTypedRuleContext(BraKetParser.Num_expressionContext,0)


        def SUB(self):
            return self.getToken(BraKetParser.SUB, 0)

        def getRuleIndex(self):
            return BraKetParser.RULE_num_expression

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitNum_expression" ):
                return visitor.visitNum_expression(self)
            else:
                return visitor.visitChildren(self)




    def num_expression(self):

        localctx = BraKetParser.Num_expressionContext(self, self._ctx, self.state)
        self.enterRule(localctx, 30, self.RULE_num_expression)
        try:
            self.state = 133
            self._errHandler.sync(self)
            la_ = self._interp.adaptivePredict(self._input,13,self._ctx)
            if la_ == 1:
                self.enterOuterAlt(localctx, 1)
                self.state = 124
                self.num_term()
                self.state = 125
                self.match(BraKetParser.ADD)
                self.state = 126
                self.num_expression()
                pass

            elif la_ == 2:
                self.enterOuterAlt(localctx, 2)
                self.state = 128
                self.num_term()
                self.state = 129
                self.match(BraKetParser.SUB)
                self.state = 130
                self.num_expression()
                pass

            elif la_ == 3:
                self.enterOuterAlt(localctx, 3)
                self.state = 132
                self.num_term()
                pass


        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class Num_termContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def num_factor(self):
            return self.getTypedRuleContext(BraKetParser.Num_factorContext,0)


        def MUL(self):
            return self.getToken(BraKetParser.MUL, 0)

        def num_term(self):
            return self.getTypedRuleContext(BraKetParser.Num_termContext,0)


        def DIV(self):
            return self.getToken(BraKetParser.DIV, 0)

        def MOD(self):
            return self.getToken(BraKetParser.MOD, 0)

        def EXP(self):
            return self.getToken(BraKetParser.EXP, 0)

        def getRuleIndex(self):
            return BraKetParser.RULE_num_term

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitNum_term" ):
                return visitor.visitNum_term(self)
            else:
                return visitor.visitChildren(self)




    def num_term(self):

        localctx = BraKetParser.Num_termContext(self, self._ctx, self.state)
        self.enterRule(localctx, 32, self.RULE_num_term)
        try:
            self.state = 152
            self._errHandler.sync(self)
            la_ = self._interp.adaptivePredict(self._input,14,self._ctx)
            if la_ == 1:
                self.enterOuterAlt(localctx, 1)
                self.state = 135
                self.num_factor()
                self.state = 136
                self.match(BraKetParser.MUL)
                self.state = 137
                self.num_term()
                pass

            elif la_ == 2:
                self.enterOuterAlt(localctx, 2)
                self.state = 139
                self.num_factor()
                self.state = 140
                self.match(BraKetParser.DIV)
                self.state = 141
                self.num_term()
                pass

            elif la_ == 3:
                self.enterOuterAlt(localctx, 3)
                self.state = 143
                self.num_factor()
                self.state = 144
                self.match(BraKetParser.MOD)
                self.state = 145
                self.num_term()
                pass

            elif la_ == 4:
                self.enterOuterAlt(localctx, 4)
                self.state = 147
                self.num_factor()
                self.state = 148
                self.match(BraKetParser.EXP)
                self.state = 149
                self.num_term()
                pass

            elif la_ == 5:
                self.enterOuterAlt(localctx, 5)
                self.state = 151
                self.num_factor()
                pass


        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class Num_factorContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def LPAREN(self):
            return self.getToken(BraKetParser.LPAREN, 0)

        def num_expression(self):
            return self.getTypedRuleContext(BraKetParser.Num_expressionContext,0)


        def RPAREN(self):
            return self.getToken(BraKetParser.RPAREN, 0)

        def ADD(self):
            return self.getToken(BraKetParser.ADD, 0)

        def num_factor(self):
            return self.getTypedRuleContext(BraKetParser.Num_factorContext,0)


        def SUB(self):
            return self.getToken(BraKetParser.SUB, 0)

        def INT(self):
            return self.getToken(BraKetParser.INT, 0)

        def FLOAT(self):
            return self.getToken(BraKetParser.FLOAT, 0)

        def CHAR(self):
            return self.getToken(BraKetParser.CHAR, 0)

        def IDENTIFIER(self):
            return self.getToken(BraKetParser.IDENTIFIER, 0)

        def getRuleIndex(self):
            return BraKetParser.RULE_num_factor

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitNum_factor" ):
                return visitor.visitNum_factor(self)
            else:
                return visitor.visitChildren(self)




    def num_factor(self):

        localctx = BraKetParser.Num_factorContext(self, self._ctx, self.state)
        self.enterRule(localctx, 34, self.RULE_num_factor)
        try:
            self.state = 167
            self._errHandler.sync(self)
            la_ = self._interp.adaptivePredict(self._input,15,self._ctx)
            if la_ == 1:
                self.enterOuterAlt(localctx, 1)
                self.state = 154
                self.match(BraKetParser.LPAREN)
                self.state = 155
                self.num_expression()
                self.state = 156
                self.match(BraKetParser.RPAREN)
                pass

            elif la_ == 2:
                self.enterOuterAlt(localctx, 2)
                self.state = 158
                self.match(BraKetParser.ADD)
                self.state = 159
                self.num_factor()
                pass

            elif la_ == 3:
                self.enterOuterAlt(localctx, 3)
                self.state = 160
                self.match(BraKetParser.SUB)
                self.state = 161
                self.num_factor()
                pass

            elif la_ == 4:
                self.enterOuterAlt(localctx, 4)
                self.state = 162
                self.match(BraKetParser.INT)
                pass

            elif la_ == 5:
                self.enterOuterAlt(localctx, 5)
                self.state = 163
                self.match(BraKetParser.FLOAT)
                pass

            elif la_ == 6:
                self.enterOuterAlt(localctx, 6)
                self.state = 164
                self.match(BraKetParser.CHAR)
                pass

            elif la_ == 7:
                self.enterOuterAlt(localctx, 7)

                pass

            elif la_ == 8:
                self.enterOuterAlt(localctx, 8)
                self.state = 166
                self.match(BraKetParser.IDENTIFIER)
                pass


        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx



    def sempred(self, localctx:RuleContext, ruleIndex:int, predIndex:int):
        if self._predicates == None:
            self._predicates = dict()
        self._predicates[14] = self.string_expression_sempred
        pred = self._predicates.get(ruleIndex, None)
        if pred is None:
            raise Exception("No predicate with index:" + str(ruleIndex))
        else:
            return pred(localctx, predIndex)

    def string_expression_sempred(self, localctx:String_expressionContext, predIndex:int):
            if predIndex == 0:
                return self.precpred(self._ctx, 3)
         




