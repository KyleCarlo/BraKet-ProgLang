# Generated from BraKet.g4 by ANTLR 4.13.2
from antlr4 import *
if "." in __name__:
    from .BraKetParser import BraKetParser
else:
    from BraKetParser import BraKetParser

# This class defines a complete generic visitor for a parse tree produced by BraKetParser.

class BraKetVisitor(ParseTreeVisitor):

    # Visit a parse tree produced by BraKetParser#program.
    def visitProgram(self, ctx:BraKetParser.ProgramContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by BraKetParser#statement.
    def visitStatement(self, ctx:BraKetParser.StatementContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by BraKetParser#assignment.
    def visitAssignment(self, ctx:BraKetParser.AssignmentContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by BraKetParser#expression.
    def visitExpression(self, ctx:BraKetParser.ExpressionContext):
        return self.visitChildren(ctx)



del BraKetParser