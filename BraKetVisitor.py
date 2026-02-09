# Generated from BraKet.g4 by ANTLR 4.13.2
from antlr4 import *
if "." in __name__:
    from .BraKetParser import BraKetParser
else:
    from BraKetParser import BraKetParser

# This class defines a complete generic visitor for a parse tree produced by BraKetParser.

class BraKetVisitor(ParseTreeVisitor):

    # Visit a parse tree produced by BraKetParser#prog.
    def visitProg(self, ctx:BraKetParser.ProgContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by BraKetParser#expr.
    def visitExpr(self, ctx:BraKetParser.ExprContext):
        return self.visitChildren(ctx)



del BraKetParser