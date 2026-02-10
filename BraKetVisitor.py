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


    # Visit a parse tree produced by BraKetParser#value.
    def visitValue(self, ctx:BraKetParser.ValueContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by BraKetParser#braket_vector.
    def visitBraket_vector(self, ctx:BraKetParser.Braket_vectorContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by BraKetParser#braket_value.
    def visitBraket_value(self, ctx:BraKetParser.Braket_valueContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by BraKetParser#array.
    def visitArray(self, ctx:BraKetParser.ArrayContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by BraKetParser#op.
    def visitOp(self, ctx:BraKetParser.OpContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by BraKetParser#assign_statement.
    def visitAssign_statement(self, ctx:BraKetParser.Assign_statementContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by BraKetParser#func_call_statement.
    def visitFunc_call_statement(self, ctx:BraKetParser.Func_call_statementContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by BraKetParser#arg_list.
    def visitArg_list(self, ctx:BraKetParser.Arg_listContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by BraKetParser#arg.
    def visitArg(self, ctx:BraKetParser.ArgContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by BraKetParser#expression.
    def visitExpression(self, ctx:BraKetParser.ExpressionContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by BraKetParser#string_expression.
    def visitString_expression(self, ctx:BraKetParser.String_expressionContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by BraKetParser#num_expression.
    def visitNum_expression(self, ctx:BraKetParser.Num_expressionContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by BraKetParser#num_term.
    def visitNum_term(self, ctx:BraKetParser.Num_termContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by BraKetParser#num_factor.
    def visitNum_factor(self, ctx:BraKetParser.Num_factorContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by BraKetParser#dirac_expression.
    def visitDirac_expression(self, ctx:BraKetParser.Dirac_expressionContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by BraKetParser#num_comp.
    def visitNum_comp(self, ctx:BraKetParser.Num_compContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by BraKetParser#eq_comp.
    def visitEq_comp(self, ctx:BraKetParser.Eq_compContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by BraKetParser#bool_expression.
    def visitBool_expression(self, ctx:BraKetParser.Bool_expressionContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by BraKetParser#bool_or.
    def visitBool_or(self, ctx:BraKetParser.Bool_orContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by BraKetParser#bool_and.
    def visitBool_and(self, ctx:BraKetParser.Bool_andContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by BraKetParser#bool_cmp.
    def visitBool_cmp(self, ctx:BraKetParser.Bool_cmpContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by BraKetParser#bool_unary.
    def visitBool_unary(self, ctx:BraKetParser.Bool_unaryContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by BraKetParser#bool_primary.
    def visitBool_primary(self, ctx:BraKetParser.Bool_primaryContext):
        return self.visitChildren(ctx)



del BraKetParser