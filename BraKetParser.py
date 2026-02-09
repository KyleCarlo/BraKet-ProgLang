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
        4,1,11,51,2,0,7,0,2,1,7,1,2,2,7,2,2,3,7,3,1,0,5,0,10,8,0,10,0,12,
        0,13,9,0,1,0,1,0,1,1,1,1,3,1,19,8,1,1,2,1,2,1,2,1,2,1,3,1,3,1,3,
        1,3,1,3,1,3,1,3,3,3,32,8,3,1,3,1,3,1,3,1,3,1,3,1,3,1,3,1,3,1,3,1,
        3,1,3,1,3,5,3,46,8,3,10,3,12,3,49,9,3,1,3,0,1,6,4,0,2,4,6,0,0,54,
        0,11,1,0,0,0,2,18,1,0,0,0,4,20,1,0,0,0,6,31,1,0,0,0,8,10,3,2,1,0,
        9,8,1,0,0,0,10,13,1,0,0,0,11,9,1,0,0,0,11,12,1,0,0,0,12,14,1,0,0,
        0,13,11,1,0,0,0,14,15,5,0,0,1,15,1,1,0,0,0,16,19,3,4,2,0,17,19,3,
        6,3,0,18,16,1,0,0,0,18,17,1,0,0,0,19,3,1,0,0,0,20,21,5,8,0,0,21,
        22,5,1,0,0,22,23,3,6,3,0,23,5,1,0,0,0,24,25,6,3,-1,0,25,32,5,8,0,
        0,26,32,5,9,0,0,27,28,5,6,0,0,28,29,3,6,3,0,29,30,5,7,0,0,30,32,
        1,0,0,0,31,24,1,0,0,0,31,26,1,0,0,0,31,27,1,0,0,0,32,47,1,0,0,0,
        33,34,10,5,0,0,34,35,5,2,0,0,35,46,3,6,3,6,36,37,10,4,0,0,37,38,
        5,3,0,0,38,46,3,6,3,5,39,40,10,3,0,0,40,41,5,4,0,0,41,46,3,6,3,4,
        42,43,10,2,0,0,43,44,5,5,0,0,44,46,3,6,3,3,45,33,1,0,0,0,45,36,1,
        0,0,0,45,39,1,0,0,0,45,42,1,0,0,0,46,49,1,0,0,0,47,45,1,0,0,0,47,
        48,1,0,0,0,48,7,1,0,0,0,49,47,1,0,0,0,5,11,18,31,45,47
    ]

class BraKetParser ( Parser ):

    grammarFileName = "BraKet.g4"

    atn = ATNDeserializer().deserialize(serializedATN())

    decisionsToDFA = [ DFA(ds, i) for i, ds in enumerate(atn.decisionToState) ]

    sharedContextCache = PredictionContextCache()

    literalNames = [ "<INVALID>", "'='", "'+'", "'-'", "'*'", "'/'", "'('", 
                     "')'" ]

    symbolicNames = [ "<INVALID>", "<INVALID>", "<INVALID>", "<INVALID>", 
                      "<INVALID>", "<INVALID>", "<INVALID>", "<INVALID>", 
                      "IDENTIFIER", "NUMBER", "NEWLINE", "WS" ]

    RULE_program = 0
    RULE_statement = 1
    RULE_assignment = 2
    RULE_expression = 3

    ruleNames =  [ "program", "statement", "assignment", "expression" ]

    EOF = Token.EOF
    T__0=1
    T__1=2
    T__2=3
    T__3=4
    T__4=5
    T__5=6
    T__6=7
    IDENTIFIER=8
    NUMBER=9
    NEWLINE=10
    WS=11

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

        def EOF(self):
            return self.getToken(BraKetParser.EOF, 0)

        def statement(self, i:int=None):
            if i is None:
                return self.getTypedRuleContexts(BraKetParser.StatementContext)
            else:
                return self.getTypedRuleContext(BraKetParser.StatementContext,i)


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
            self.state = 11
            self._errHandler.sync(self)
            _la = self._input.LA(1)
            while (((_la) & ~0x3f) == 0 and ((1 << _la) & 832) != 0):
                self.state = 8
                self.statement()
                self.state = 13
                self._errHandler.sync(self)
                _la = self._input.LA(1)

            self.state = 14
            self.match(BraKetParser.EOF)
        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class StatementContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def assignment(self):
            return self.getTypedRuleContext(BraKetParser.AssignmentContext,0)


        def expression(self):
            return self.getTypedRuleContext(BraKetParser.ExpressionContext,0)


        def getRuleIndex(self):
            return BraKetParser.RULE_statement

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitStatement" ):
                return visitor.visitStatement(self)
            else:
                return visitor.visitChildren(self)




    def statement(self):

        localctx = BraKetParser.StatementContext(self, self._ctx, self.state)
        self.enterRule(localctx, 2, self.RULE_statement)
        try:
            self.state = 18
            self._errHandler.sync(self)
            la_ = self._interp.adaptivePredict(self._input,1,self._ctx)
            if la_ == 1:
                self.enterOuterAlt(localctx, 1)
                self.state = 16
                self.assignment()
                pass

            elif la_ == 2:
                self.enterOuterAlt(localctx, 2)
                self.state = 17
                self.expression(0)
                pass


        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class AssignmentContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def IDENTIFIER(self):
            return self.getToken(BraKetParser.IDENTIFIER, 0)

        def expression(self):
            return self.getTypedRuleContext(BraKetParser.ExpressionContext,0)


        def getRuleIndex(self):
            return BraKetParser.RULE_assignment

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitAssignment" ):
                return visitor.visitAssignment(self)
            else:
                return visitor.visitChildren(self)




    def assignment(self):

        localctx = BraKetParser.AssignmentContext(self, self._ctx, self.state)
        self.enterRule(localctx, 4, self.RULE_assignment)
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 20
            self.match(BraKetParser.IDENTIFIER)
            self.state = 21
            self.match(BraKetParser.T__0)
            self.state = 22
            self.expression(0)
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

        def IDENTIFIER(self):
            return self.getToken(BraKetParser.IDENTIFIER, 0)

        def NUMBER(self):
            return self.getToken(BraKetParser.NUMBER, 0)

        def expression(self, i:int=None):
            if i is None:
                return self.getTypedRuleContexts(BraKetParser.ExpressionContext)
            else:
                return self.getTypedRuleContext(BraKetParser.ExpressionContext,i)


        def getRuleIndex(self):
            return BraKetParser.RULE_expression

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitExpression" ):
                return visitor.visitExpression(self)
            else:
                return visitor.visitChildren(self)



    def expression(self, _p:int=0):
        _parentctx = self._ctx
        _parentState = self.state
        localctx = BraKetParser.ExpressionContext(self, self._ctx, _parentState)
        _prevctx = localctx
        _startState = 6
        self.enterRecursionRule(localctx, 6, self.RULE_expression, _p)
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 31
            self._errHandler.sync(self)
            token = self._input.LA(1)
            if token in [8]:
                self.state = 25
                self.match(BraKetParser.IDENTIFIER)
                pass
            elif token in [9]:
                self.state = 26
                self.match(BraKetParser.NUMBER)
                pass
            elif token in [6]:
                self.state = 27
                self.match(BraKetParser.T__5)
                self.state = 28
                self.expression(0)
                self.state = 29
                self.match(BraKetParser.T__6)
                pass
            else:
                raise NoViableAltException(self)

            self._ctx.stop = self._input.LT(-1)
            self.state = 47
            self._errHandler.sync(self)
            _alt = self._interp.adaptivePredict(self._input,4,self._ctx)
            while _alt!=2 and _alt!=ATN.INVALID_ALT_NUMBER:
                if _alt==1:
                    if self._parseListeners is not None:
                        self.triggerExitRuleEvent()
                    _prevctx = localctx
                    self.state = 45
                    self._errHandler.sync(self)
                    la_ = self._interp.adaptivePredict(self._input,3,self._ctx)
                    if la_ == 1:
                        localctx = BraKetParser.ExpressionContext(self, _parentctx, _parentState)
                        self.pushNewRecursionContext(localctx, _startState, self.RULE_expression)
                        self.state = 33
                        if not self.precpred(self._ctx, 5):
                            from antlr4.error.Errors import FailedPredicateException
                            raise FailedPredicateException(self, "self.precpred(self._ctx, 5)")
                        self.state = 34
                        self.match(BraKetParser.T__1)
                        self.state = 35
                        self.expression(6)
                        pass

                    elif la_ == 2:
                        localctx = BraKetParser.ExpressionContext(self, _parentctx, _parentState)
                        self.pushNewRecursionContext(localctx, _startState, self.RULE_expression)
                        self.state = 36
                        if not self.precpred(self._ctx, 4):
                            from antlr4.error.Errors import FailedPredicateException
                            raise FailedPredicateException(self, "self.precpred(self._ctx, 4)")
                        self.state = 37
                        self.match(BraKetParser.T__2)
                        self.state = 38
                        self.expression(5)
                        pass

                    elif la_ == 3:
                        localctx = BraKetParser.ExpressionContext(self, _parentctx, _parentState)
                        self.pushNewRecursionContext(localctx, _startState, self.RULE_expression)
                        self.state = 39
                        if not self.precpred(self._ctx, 3):
                            from antlr4.error.Errors import FailedPredicateException
                            raise FailedPredicateException(self, "self.precpred(self._ctx, 3)")
                        self.state = 40
                        self.match(BraKetParser.T__3)
                        self.state = 41
                        self.expression(4)
                        pass

                    elif la_ == 4:
                        localctx = BraKetParser.ExpressionContext(self, _parentctx, _parentState)
                        self.pushNewRecursionContext(localctx, _startState, self.RULE_expression)
                        self.state = 42
                        if not self.precpred(self._ctx, 2):
                            from antlr4.error.Errors import FailedPredicateException
                            raise FailedPredicateException(self, "self.precpred(self._ctx, 2)")
                        self.state = 43
                        self.match(BraKetParser.T__4)
                        self.state = 44
                        self.expression(3)
                        pass

             
                self.state = 49
                self._errHandler.sync(self)
                _alt = self._interp.adaptivePredict(self._input,4,self._ctx)

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
        self._predicates[3] = self.expression_sempred
        pred = self._predicates.get(ruleIndex, None)
        if pred is None:
            raise Exception("No predicate with index:" + str(ruleIndex))
        else:
            return pred(localctx, predIndex)

    def expression_sempred(self, localctx:ExpressionContext, predIndex:int):
            if predIndex == 0:
                return self.precpred(self._ctx, 5)
         

            if predIndex == 1:
                return self.precpred(self._ctx, 4)
         

            if predIndex == 2:
                return self.precpred(self._ctx, 3)
         

            if predIndex == 3:
                return self.precpred(self._ctx, 2)
         




