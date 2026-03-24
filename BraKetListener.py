# Generated from BraKet.g4 by ANTLR 4.13.2
from antlr4 import *
if "." in __name__:
    from .BraKetParser import BraKetParser
else:
    from BraKetParser import BraKetParser

# This class defines a complete listener for a parse tree produced by BraKetParser.
class BraKetListener(ParseTreeListener):

    # Enter a parse tree produced by BraKetParser#program.
    def enterProgram(self, ctx:BraKetParser.ProgramContext):
        pass

    # Exit a parse tree produced by BraKetParser#program.
    def exitProgram(self, ctx:BraKetParser.ProgramContext):
        pass


    # Enter a parse tree produced by BraKetParser#import_list.
    def enterImport_list(self, ctx:BraKetParser.Import_listContext):
        pass

    # Exit a parse tree produced by BraKetParser#import_list.
    def exitImport_list(self, ctx:BraKetParser.Import_listContext):
        pass


    # Enter a parse tree produced by BraKetParser#import_statement.
    def enterImport_statement(self, ctx:BraKetParser.Import_statementContext):
        pass

    # Exit a parse tree produced by BraKetParser#import_statement.
    def exitImport_statement(self, ctx:BraKetParser.Import_statementContext):
        pass


    # Enter a parse tree produced by BraKetParser#func_list.
    def enterFunc_list(self, ctx:BraKetParser.Func_listContext):
        pass

    # Exit a parse tree produced by BraKetParser#func_list.
    def exitFunc_list(self, ctx:BraKetParser.Func_listContext):
        pass


    # Enter a parse tree produced by BraKetParser#const_decl_list.
    def enterConst_decl_list(self, ctx:BraKetParser.Const_decl_listContext):
        pass

    # Exit a parse tree produced by BraKetParser#const_decl_list.
    def exitConst_decl_list(self, ctx:BraKetParser.Const_decl_listContext):
        pass


    # Enter a parse tree produced by BraKetParser#const_decl.
    def enterConst_decl(self, ctx:BraKetParser.Const_declContext):
        pass

    # Exit a parse tree produced by BraKetParser#const_decl.
    def exitConst_decl(self, ctx:BraKetParser.Const_declContext):
        pass


    # Enter a parse tree produced by BraKetParser#var_decl_list.
    def enterVar_decl_list(self, ctx:BraKetParser.Var_decl_listContext):
        pass

    # Exit a parse tree produced by BraKetParser#var_decl_list.
    def exitVar_decl_list(self, ctx:BraKetParser.Var_decl_listContext):
        pass


    # Enter a parse tree produced by BraKetParser#var_decl.
    def enterVar_decl(self, ctx:BraKetParser.Var_declContext):
        pass

    # Exit a parse tree produced by BraKetParser#var_decl.
    def exitVar_decl(self, ctx:BraKetParser.Var_declContext):
        pass


    # Enter a parse tree produced by BraKetParser#value.
    def enterValue(self, ctx:BraKetParser.ValueContext):
        pass

    # Exit a parse tree produced by BraKetParser#value.
    def exitValue(self, ctx:BraKetParser.ValueContext):
        pass


    # Enter a parse tree produced by BraKetParser#braket_vector.
    def enterBraket_vector(self, ctx:BraKetParser.Braket_vectorContext):
        pass

    # Exit a parse tree produced by BraKetParser#braket_vector.
    def exitBraket_vector(self, ctx:BraKetParser.Braket_vectorContext):
        pass


    # Enter a parse tree produced by BraKetParser#braket_expression.
    def enterBraket_expression(self, ctx:BraKetParser.Braket_expressionContext):
        pass

    # Exit a parse tree produced by BraKetParser#braket_expression.
    def exitBraket_expression(self, ctx:BraKetParser.Braket_expressionContext):
        pass


    # Enter a parse tree produced by BraKetParser#braket_term.
    def enterBraket_term(self, ctx:BraKetParser.Braket_termContext):
        pass

    # Exit a parse tree produced by BraKetParser#braket_term.
    def exitBraket_term(self, ctx:BraKetParser.Braket_termContext):
        pass


    # Enter a parse tree produced by BraKetParser#braket_factor.
    def enterBraket_factor(self, ctx:BraKetParser.Braket_factorContext):
        pass

    # Exit a parse tree produced by BraKetParser#braket_factor.
    def exitBraket_factor(self, ctx:BraKetParser.Braket_factorContext):
        pass


    # Enter a parse tree produced by BraKetParser#array.
    def enterArray(self, ctx:BraKetParser.ArrayContext):
        pass

    # Exit a parse tree produced by BraKetParser#array.
    def exitArray(self, ctx:BraKetParser.ArrayContext):
        pass


    # Enter a parse tree produced by BraKetParser#struct.
    def enterStruct(self, ctx:BraKetParser.StructContext):
        pass

    # Exit a parse tree produced by BraKetParser#struct.
    def exitStruct(self, ctx:BraKetParser.StructContext):
        pass


    # Enter a parse tree produced by BraKetParser#struct_value.
    def enterStruct_value(self, ctx:BraKetParser.Struct_valueContext):
        pass

    # Exit a parse tree produced by BraKetParser#struct_value.
    def exitStruct_value(self, ctx:BraKetParser.Struct_valueContext):
        pass


    # Enter a parse tree produced by BraKetParser#op.
    def enterOp(self, ctx:BraKetParser.OpContext):
        pass

    # Exit a parse tree produced by BraKetParser#op.
    def exitOp(self, ctx:BraKetParser.OpContext):
        pass


    # Enter a parse tree produced by BraKetParser#statement_list.
    def enterStatement_list(self, ctx:BraKetParser.Statement_listContext):
        pass

    # Exit a parse tree produced by BraKetParser#statement_list.
    def exitStatement_list(self, ctx:BraKetParser.Statement_listContext):
        pass


    # Enter a parse tree produced by BraKetParser#statement.
    def enterStatement(self, ctx:BraKetParser.StatementContext):
        pass

    # Exit a parse tree produced by BraKetParser#statement.
    def exitStatement(self, ctx:BraKetParser.StatementContext):
        pass


    # Enter a parse tree produced by BraKetParser#assign_statement.
    def enterAssign_statement(self, ctx:BraKetParser.Assign_statementContext):
        pass

    # Exit a parse tree produced by BraKetParser#assign_statement.
    def exitAssign_statement(self, ctx:BraKetParser.Assign_statementContext):
        pass


    # Enter a parse tree produced by BraKetParser#func_call_statement.
    def enterFunc_call_statement(self, ctx:BraKetParser.Func_call_statementContext):
        pass

    # Exit a parse tree produced by BraKetParser#func_call_statement.
    def exitFunc_call_statement(self, ctx:BraKetParser.Func_call_statementContext):
        pass


    # Enter a parse tree produced by BraKetParser#arg_list.
    def enterArg_list(self, ctx:BraKetParser.Arg_listContext):
        pass

    # Exit a parse tree produced by BraKetParser#arg_list.
    def exitArg_list(self, ctx:BraKetParser.Arg_listContext):
        pass


    # Enter a parse tree produced by BraKetParser#arg.
    def enterArg(self, ctx:BraKetParser.ArgContext):
        pass

    # Exit a parse tree produced by BraKetParser#arg.
    def exitArg(self, ctx:BraKetParser.ArgContext):
        pass


    # Enter a parse tree produced by BraKetParser#return_statement.
    def enterReturn_statement(self, ctx:BraKetParser.Return_statementContext):
        pass

    # Exit a parse tree produced by BraKetParser#return_statement.
    def exitReturn_statement(self, ctx:BraKetParser.Return_statementContext):
        pass


    # Enter a parse tree produced by BraKetParser#if_statement.
    def enterIf_statement(self, ctx:BraKetParser.If_statementContext):
        pass

    # Exit a parse tree produced by BraKetParser#if_statement.
    def exitIf_statement(self, ctx:BraKetParser.If_statementContext):
        pass


    # Enter a parse tree produced by BraKetParser#elif.
    def enterElif(self, ctx:BraKetParser.ElifContext):
        pass

    # Exit a parse tree produced by BraKetParser#elif.
    def exitElif(self, ctx:BraKetParser.ElifContext):
        pass


    # Enter a parse tree produced by BraKetParser#else.
    def enterElse(self, ctx:BraKetParser.ElseContext):
        pass

    # Exit a parse tree produced by BraKetParser#else.
    def exitElse(self, ctx:BraKetParser.ElseContext):
        pass


    # Enter a parse tree produced by BraKetParser#for_statement.
    def enterFor_statement(self, ctx:BraKetParser.For_statementContext):
        pass

    # Exit a parse tree produced by BraKetParser#for_statement.
    def exitFor_statement(self, ctx:BraKetParser.For_statementContext):
        pass


    # Enter a parse tree produced by BraKetParser#while_statement.
    def enterWhile_statement(self, ctx:BraKetParser.While_statementContext):
        pass

    # Exit a parse tree produced by BraKetParser#while_statement.
    def exitWhile_statement(self, ctx:BraKetParser.While_statementContext):
        pass


    # Enter a parse tree produced by BraKetParser#do_statement.
    def enterDo_statement(self, ctx:BraKetParser.Do_statementContext):
        pass

    # Exit a parse tree produced by BraKetParser#do_statement.
    def exitDo_statement(self, ctx:BraKetParser.Do_statementContext):
        pass


    # Enter a parse tree produced by BraKetParser#expression.
    def enterExpression(self, ctx:BraKetParser.ExpressionContext):
        pass

    # Exit a parse tree produced by BraKetParser#expression.
    def exitExpression(self, ctx:BraKetParser.ExpressionContext):
        pass


    # Enter a parse tree produced by BraKetParser#string_expression.
    def enterString_expression(self, ctx:BraKetParser.String_expressionContext):
        pass

    # Exit a parse tree produced by BraKetParser#string_expression.
    def exitString_expression(self, ctx:BraKetParser.String_expressionContext):
        pass


    # Enter a parse tree produced by BraKetParser#num_expression.
    def enterNum_expression(self, ctx:BraKetParser.Num_expressionContext):
        pass

    # Exit a parse tree produced by BraKetParser#num_expression.
    def exitNum_expression(self, ctx:BraKetParser.Num_expressionContext):
        pass


    # Enter a parse tree produced by BraKetParser#num_term.
    def enterNum_term(self, ctx:BraKetParser.Num_termContext):
        pass

    # Exit a parse tree produced by BraKetParser#num_term.
    def exitNum_term(self, ctx:BraKetParser.Num_termContext):
        pass


    # Enter a parse tree produced by BraKetParser#num_factor.
    def enterNum_factor(self, ctx:BraKetParser.Num_factorContext):
        pass

    # Exit a parse tree produced by BraKetParser#num_factor.
    def exitNum_factor(self, ctx:BraKetParser.Num_factorContext):
        pass


    # Enter a parse tree produced by BraKetParser#array_access.
    def enterArray_access(self, ctx:BraKetParser.Array_accessContext):
        pass

    # Exit a parse tree produced by BraKetParser#array_access.
    def exitArray_access(self, ctx:BraKetParser.Array_accessContext):
        pass


    # Enter a parse tree produced by BraKetParser#struct_access.
    def enterStruct_access(self, ctx:BraKetParser.Struct_accessContext):
        pass

    # Exit a parse tree produced by BraKetParser#struct_access.
    def exitStruct_access(self, ctx:BraKetParser.Struct_accessContext):
        pass


    # Enter a parse tree produced by BraKetParser#dirac_expression.
    def enterDirac_expression(self, ctx:BraKetParser.Dirac_expressionContext):
        pass

    # Exit a parse tree produced by BraKetParser#dirac_expression.
    def exitDirac_expression(self, ctx:BraKetParser.Dirac_expressionContext):
        pass


    # Enter a parse tree produced by BraKetParser#num_comp.
    def enterNum_comp(self, ctx:BraKetParser.Num_compContext):
        pass

    # Exit a parse tree produced by BraKetParser#num_comp.
    def exitNum_comp(self, ctx:BraKetParser.Num_compContext):
        pass


    # Enter a parse tree produced by BraKetParser#eq_comp.
    def enterEq_comp(self, ctx:BraKetParser.Eq_compContext):
        pass

    # Exit a parse tree produced by BraKetParser#eq_comp.
    def exitEq_comp(self, ctx:BraKetParser.Eq_compContext):
        pass


    # Enter a parse tree produced by BraKetParser#bool_expression.
    def enterBool_expression(self, ctx:BraKetParser.Bool_expressionContext):
        pass

    # Exit a parse tree produced by BraKetParser#bool_expression.
    def exitBool_expression(self, ctx:BraKetParser.Bool_expressionContext):
        pass


    # Enter a parse tree produced by BraKetParser#bool_or.
    def enterBool_or(self, ctx:BraKetParser.Bool_orContext):
        pass

    # Exit a parse tree produced by BraKetParser#bool_or.
    def exitBool_or(self, ctx:BraKetParser.Bool_orContext):
        pass


    # Enter a parse tree produced by BraKetParser#bool_and.
    def enterBool_and(self, ctx:BraKetParser.Bool_andContext):
        pass

    # Exit a parse tree produced by BraKetParser#bool_and.
    def exitBool_and(self, ctx:BraKetParser.Bool_andContext):
        pass


    # Enter a parse tree produced by BraKetParser#bool_cmp.
    def enterBool_cmp(self, ctx:BraKetParser.Bool_cmpContext):
        pass

    # Exit a parse tree produced by BraKetParser#bool_cmp.
    def exitBool_cmp(self, ctx:BraKetParser.Bool_cmpContext):
        pass


    # Enter a parse tree produced by BraKetParser#bool_unary.
    def enterBool_unary(self, ctx:BraKetParser.Bool_unaryContext):
        pass

    # Exit a parse tree produced by BraKetParser#bool_unary.
    def exitBool_unary(self, ctx:BraKetParser.Bool_unaryContext):
        pass


    # Enter a parse tree produced by BraKetParser#bool_primary.
    def enterBool_primary(self, ctx:BraKetParser.Bool_primaryContext):
        pass

    # Exit a parse tree produced by BraKetParser#bool_primary.
    def exitBool_primary(self, ctx:BraKetParser.Bool_primaryContext):
        pass


    # Enter a parse tree produced by BraKetParser#func_decl_list.
    def enterFunc_decl_list(self, ctx:BraKetParser.Func_decl_listContext):
        pass

    # Exit a parse tree produced by BraKetParser#func_decl_list.
    def exitFunc_decl_list(self, ctx:BraKetParser.Func_decl_listContext):
        pass


    # Enter a parse tree produced by BraKetParser#func_decl.
    def enterFunc_decl(self, ctx:BraKetParser.Func_declContext):
        pass

    # Exit a parse tree produced by BraKetParser#func_decl.
    def exitFunc_decl(self, ctx:BraKetParser.Func_declContext):
        pass


    # Enter a parse tree produced by BraKetParser#param_list.
    def enterParam_list(self, ctx:BraKetParser.Param_listContext):
        pass

    # Exit a parse tree produced by BraKetParser#param_list.
    def exitParam_list(self, ctx:BraKetParser.Param_listContext):
        pass


    # Enter a parse tree produced by BraKetParser#identifier_list.
    def enterIdentifier_list(self, ctx:BraKetParser.Identifier_listContext):
        pass

    # Exit a parse tree produced by BraKetParser#identifier_list.
    def exitIdentifier_list(self, ctx:BraKetParser.Identifier_listContext):
        pass


    # Enter a parse tree produced by BraKetParser#default_list.
    def enterDefault_list(self, ctx:BraKetParser.Default_listContext):
        pass

    # Exit a parse tree produced by BraKetParser#default_list.
    def exitDefault_list(self, ctx:BraKetParser.Default_listContext):
        pass


    # Enter a parse tree produced by BraKetParser#main_function.
    def enterMain_function(self, ctx:BraKetParser.Main_functionContext):
        pass

    # Exit a parse tree produced by BraKetParser#main_function.
    def exitMain_function(self, ctx:BraKetParser.Main_functionContext):
        pass



del BraKetParser