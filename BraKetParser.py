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
        4,1,9,82,2,0,7,0,2,1,7,1,2,2,7,2,2,3,7,3,2,4,7,4,2,5,7,5,2,6,7,6,
        2,7,7,7,2,8,7,8,2,9,7,9,1,0,3,0,22,8,0,1,0,3,0,25,8,0,1,1,1,1,5,
        1,29,8,1,10,1,12,1,32,9,1,1,2,1,2,1,2,1,2,1,2,1,2,3,2,40,8,2,1,3,
        1,3,1,3,5,3,45,8,3,10,3,12,3,48,9,3,1,4,4,4,51,8,4,11,4,12,4,52,
        1,5,1,5,1,5,1,6,4,6,59,8,6,11,6,12,6,60,1,7,1,7,1,7,1,7,1,8,1,8,
        1,9,1,9,1,9,3,9,72,8,9,1,9,1,9,1,9,5,9,77,8,9,10,9,12,9,80,9,9,1,
        9,0,1,18,10,0,2,4,6,8,10,12,14,16,18,0,0,80,0,21,1,0,0,0,2,26,1,
        0,0,0,4,39,1,0,0,0,6,41,1,0,0,0,8,50,1,0,0,0,10,54,1,0,0,0,12,58,
        1,0,0,0,14,62,1,0,0,0,16,66,1,0,0,0,18,71,1,0,0,0,20,22,3,2,1,0,
        21,20,1,0,0,0,21,22,1,0,0,0,22,24,1,0,0,0,23,25,3,8,4,0,24,23,1,
        0,0,0,24,25,1,0,0,0,25,1,1,0,0,0,26,30,3,4,2,0,27,29,3,4,2,0,28,
        27,1,0,0,0,29,32,1,0,0,0,30,28,1,0,0,0,30,31,1,0,0,0,31,3,1,0,0,
        0,32,30,1,0,0,0,33,34,5,3,0,0,34,35,5,6,0,0,35,36,5,4,0,0,36,40,
        3,6,3,0,37,38,5,4,0,0,38,40,5,6,0,0,39,33,1,0,0,0,39,37,1,0,0,0,
        40,5,1,0,0,0,41,46,5,6,0,0,42,43,5,1,0,0,43,45,5,6,0,0,44,42,1,0,
        0,0,45,48,1,0,0,0,46,44,1,0,0,0,46,47,1,0,0,0,47,7,1,0,0,0,48,46,
        1,0,0,0,49,51,3,10,5,0,50,49,1,0,0,0,51,52,1,0,0,0,52,50,1,0,0,0,
        52,53,1,0,0,0,53,9,1,0,0,0,54,55,5,5,0,0,55,56,3,14,7,0,56,11,1,
        0,0,0,57,59,3,14,7,0,58,57,1,0,0,0,59,60,1,0,0,0,60,58,1,0,0,0,60,
        61,1,0,0,0,61,13,1,0,0,0,62,63,5,6,0,0,63,64,5,9,0,0,64,65,3,16,
        8,0,65,15,1,0,0,0,66,67,3,18,9,0,67,17,1,0,0,0,68,69,6,9,-1,0,69,
        72,5,7,0,0,70,72,5,6,0,0,71,68,1,0,0,0,71,70,1,0,0,0,72,78,1,0,0,
        0,73,74,10,3,0,0,74,75,5,8,0,0,75,77,3,18,9,4,76,73,1,0,0,0,77,80,
        1,0,0,0,78,76,1,0,0,0,78,79,1,0,0,0,79,19,1,0,0,0,80,78,1,0,0,0,
        9,21,24,30,39,46,52,60,71,78
    ]

class BraKetParser ( Parser ):

    grammarFileName = "BraKet.g4"

    atn = ATNDeserializer().deserialize(serializedATN())

    decisionsToDFA = [ DFA(ds, i) for i, ds in enumerate(atn.decisionToState) ]

    sharedContextCache = PredictionContextCache()

    literalNames = [ "<INVALID>", "','", "<INVALID>", "'from'", "'import'", 
                     "'const'", "<INVALID>", "<INVALID>", "'+'", "'='" ]

    symbolicNames = [ "<INVALID>", "COMMA", "WS", "FROM", "IMPORT", "CONST", 
                      "IDENTIFIER", "STRING", "ADD", "ASSIGN" ]

    RULE_program = 0
    RULE_import_list = 1
    RULE_import_statement = 2
    RULE_func_list = 3
    RULE_const_decl_list = 4
    RULE_const_decl = 5
    RULE_var_decl_list = 6
    RULE_var_decl = 7
    RULE_expression = 8
    RULE_string_expression = 9

    ruleNames =  [ "program", "import_list", "import_statement", "func_list", 
                   "const_decl_list", "const_decl", "var_decl_list", "var_decl", 
                   "expression", "string_expression" ]

    EOF = Token.EOF
    COMMA=1
    WS=2
    FROM=3
    IMPORT=4
    CONST=5
    IDENTIFIER=6
    STRING=7
    ADD=8
    ASSIGN=9

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
            self.state = 21
            self._errHandler.sync(self)
            _la = self._input.LA(1)
            if _la==3 or _la==4:
                self.state = 20
                self.import_list()


            self.state = 24
            self._errHandler.sync(self)
            _la = self._input.LA(1)
            if _la==5:
                self.state = 23
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
            self.state = 26
            self.import_statement()
            self.state = 30
            self._errHandler.sync(self)
            _la = self._input.LA(1)
            while _la==3 or _la==4:
                self.state = 27
                self.import_statement()
                self.state = 32
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
            self.state = 39
            self._errHandler.sync(self)
            token = self._input.LA(1)
            if token in [3]:
                self.enterOuterAlt(localctx, 1)
                self.state = 33
                self.match(BraKetParser.FROM)
                self.state = 34
                self.match(BraKetParser.IDENTIFIER)
                self.state = 35
                self.match(BraKetParser.IMPORT)
                self.state = 36
                self.func_list()
                pass
            elif token in [4]:
                self.enterOuterAlt(localctx, 2)
                self.state = 37
                self.match(BraKetParser.IMPORT)
                self.state = 38
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
            self.state = 41
            self.match(BraKetParser.IDENTIFIER)
            self.state = 46
            self._errHandler.sync(self)
            _la = self._input.LA(1)
            while _la==1:
                self.state = 42
                self.match(BraKetParser.COMMA)
                self.state = 43
                self.match(BraKetParser.IDENTIFIER)
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
            self.state = 50 
            self._errHandler.sync(self)
            _la = self._input.LA(1)
            while True:
                self.state = 49
                self.const_decl()
                self.state = 52 
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
            self.state = 54
            self.match(BraKetParser.CONST)
            self.state = 55
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
            self.state = 58 
            self._errHandler.sync(self)
            _la = self._input.LA(1)
            while True:
                self.state = 57
                self.var_decl()
                self.state = 60 
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
            self.state = 62
            self.match(BraKetParser.IDENTIFIER)
            self.state = 63
            self.match(BraKetParser.ASSIGN)
            self.state = 64
            self.expression()
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


        def getRuleIndex(self):
            return BraKetParser.RULE_expression

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitExpression" ):
                return visitor.visitExpression(self)
            else:
                return visitor.visitChildren(self)




    def expression(self):

        localctx = BraKetParser.ExpressionContext(self, self._ctx, self.state)
        self.enterRule(localctx, 16, self.RULE_expression)
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 66
            self.string_expression(0)
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
        _startState = 18
        self.enterRecursionRule(localctx, 18, self.RULE_string_expression, _p)
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 71
            self._errHandler.sync(self)
            token = self._input.LA(1)
            if token in [7]:
                self.state = 69
                self.match(BraKetParser.STRING)
                pass
            elif token in [6]:
                self.state = 70
                self.match(BraKetParser.IDENTIFIER)
                pass
            else:
                raise NoViableAltException(self)

            self._ctx.stop = self._input.LT(-1)
            self.state = 78
            self._errHandler.sync(self)
            _alt = self._interp.adaptivePredict(self._input,8,self._ctx)
            while _alt!=2 and _alt!=ATN.INVALID_ALT_NUMBER:
                if _alt==1:
                    if self._parseListeners is not None:
                        self.triggerExitRuleEvent()
                    _prevctx = localctx
                    localctx = BraKetParser.String_expressionContext(self, _parentctx, _parentState)
                    self.pushNewRecursionContext(localctx, _startState, self.RULE_string_expression)
                    self.state = 73
                    if not self.precpred(self._ctx, 3):
                        from antlr4.error.Errors import FailedPredicateException
                        raise FailedPredicateException(self, "self.precpred(self._ctx, 3)")
                    self.state = 74
                    self.match(BraKetParser.ADD)
                    self.state = 75
                    self.string_expression(4) 
                self.state = 80
                self._errHandler.sync(self)
                _alt = self._interp.adaptivePredict(self._input,8,self._ctx)

        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.unrollRecursionContexts(_parentctx)
        return localctx



    def sempred(self, localctx:RuleContext, ruleIndex:int, predIndex:int):
        if self._predicates == None:
            self._predicates = dict()
        self._predicates[9] = self.string_expression_sempred
        pred = self._predicates.get(ruleIndex, None)
        if pred is None:
            raise Exception("No predicate with index:" + str(ruleIndex))
        else:
            return pred(localctx, predIndex)

    def string_expression_sempred(self, localctx:String_expressionContext, predIndex:int):
            if predIndex == 0:
                return self.precpred(self._ctx, 3)
         




