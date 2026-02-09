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


    # Visit a parse tree produced by BraKetParser#import_list.
    def visitImport_list(self, ctx:BraKetParser.Import_listContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by BraKetParser#import_statement.
    def visitImport_statement(self, ctx:BraKetParser.Import_statementContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by BraKetParser#func_list.
    def visitFunc_list(self, ctx:BraKetParser.Func_listContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by BraKetParser#const_decl_list.
    def visitConst_decl_list(self, ctx:BraKetParser.Const_decl_listContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by BraKetParser#const_decl.
    def visitConst_decl(self, ctx:BraKetParser.Const_declContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by BraKetParser#var_decl_list.
    def visitVar_decl_list(self, ctx:BraKetParser.Var_decl_listContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by BraKetParser#var_decl.
    def visitVar_decl(self, ctx:BraKetParser.Var_declContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by BraKetParser#expression.
    def visitExpression(self, ctx:BraKetParser.ExpressionContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by BraKetParser#string_expression.
    def visitString_expression(self, ctx:BraKetParser.String_expressionContext):
        return self.visitChildren(ctx)



del BraKetParser