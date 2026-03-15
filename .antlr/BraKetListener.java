// Generated from c:/Users/Monica/Desktop/Braket-Proglang/BraKet.g4 by ANTLR 4.13.1
import org.antlr.v4.runtime.tree.ParseTreeListener;

/**
 * This interface defines a complete listener for a parse tree produced by
 * {@link BraKetParser}.
 */
public interface BraKetListener extends ParseTreeListener {
	/**
	 * Enter a parse tree produced by {@link BraKetParser#program}.
	 * @param ctx the parse tree
	 */
	void enterProgram(BraKetParser.ProgramContext ctx);
	/**
	 * Exit a parse tree produced by {@link BraKetParser#program}.
	 * @param ctx the parse tree
	 */
	void exitProgram(BraKetParser.ProgramContext ctx);
	/**
	 * Enter a parse tree produced by {@link BraKetParser#import_list}.
	 * @param ctx the parse tree
	 */
	void enterImport_list(BraKetParser.Import_listContext ctx);
	/**
	 * Exit a parse tree produced by {@link BraKetParser#import_list}.
	 * @param ctx the parse tree
	 */
	void exitImport_list(BraKetParser.Import_listContext ctx);
	/**
	 * Enter a parse tree produced by {@link BraKetParser#import_statement}.
	 * @param ctx the parse tree
	 */
	void enterImport_statement(BraKetParser.Import_statementContext ctx);
	/**
	 * Exit a parse tree produced by {@link BraKetParser#import_statement}.
	 * @param ctx the parse tree
	 */
	void exitImport_statement(BraKetParser.Import_statementContext ctx);
	/**
	 * Enter a parse tree produced by {@link BraKetParser#func_list}.
	 * @param ctx the parse tree
	 */
	void enterFunc_list(BraKetParser.Func_listContext ctx);
	/**
	 * Exit a parse tree produced by {@link BraKetParser#func_list}.
	 * @param ctx the parse tree
	 */
	void exitFunc_list(BraKetParser.Func_listContext ctx);
	/**
	 * Enter a parse tree produced by {@link BraKetParser#const_decl_list}.
	 * @param ctx the parse tree
	 */
	void enterConst_decl_list(BraKetParser.Const_decl_listContext ctx);
	/**
	 * Exit a parse tree produced by {@link BraKetParser#const_decl_list}.
	 * @param ctx the parse tree
	 */
	void exitConst_decl_list(BraKetParser.Const_decl_listContext ctx);
	/**
	 * Enter a parse tree produced by {@link BraKetParser#const_decl}.
	 * @param ctx the parse tree
	 */
	void enterConst_decl(BraKetParser.Const_declContext ctx);
	/**
	 * Exit a parse tree produced by {@link BraKetParser#const_decl}.
	 * @param ctx the parse tree
	 */
	void exitConst_decl(BraKetParser.Const_declContext ctx);
	/**
	 * Enter a parse tree produced by {@link BraKetParser#var_decl_list}.
	 * @param ctx the parse tree
	 */
	void enterVar_decl_list(BraKetParser.Var_decl_listContext ctx);
	/**
	 * Exit a parse tree produced by {@link BraKetParser#var_decl_list}.
	 * @param ctx the parse tree
	 */
	void exitVar_decl_list(BraKetParser.Var_decl_listContext ctx);
	/**
	 * Enter a parse tree produced by {@link BraKetParser#var_decl}.
	 * @param ctx the parse tree
	 */
	void enterVar_decl(BraKetParser.Var_declContext ctx);
	/**
	 * Exit a parse tree produced by {@link BraKetParser#var_decl}.
	 * @param ctx the parse tree
	 */
	void exitVar_decl(BraKetParser.Var_declContext ctx);
	/**
	 * Enter a parse tree produced by {@link BraKetParser#value}.
	 * @param ctx the parse tree
	 */
	void enterValue(BraKetParser.ValueContext ctx);
	/**
	 * Exit a parse tree produced by {@link BraKetParser#value}.
	 * @param ctx the parse tree
	 */
	void exitValue(BraKetParser.ValueContext ctx);
	/**
	 * Enter a parse tree produced by {@link BraKetParser#braket_vector}.
	 * @param ctx the parse tree
	 */
	void enterBraket_vector(BraKetParser.Braket_vectorContext ctx);
	/**
	 * Exit a parse tree produced by {@link BraKetParser#braket_vector}.
	 * @param ctx the parse tree
	 */
	void exitBraket_vector(BraKetParser.Braket_vectorContext ctx);
	/**
	 * Enter a parse tree produced by {@link BraKetParser#braket_value}.
	 * @param ctx the parse tree
	 */
	void enterBraket_value(BraKetParser.Braket_valueContext ctx);
	/**
	 * Exit a parse tree produced by {@link BraKetParser#braket_value}.
	 * @param ctx the parse tree
	 */
	void exitBraket_value(BraKetParser.Braket_valueContext ctx);
	/**
	 * Enter a parse tree produced by {@link BraKetParser#array}.
	 * @param ctx the parse tree
	 */
	void enterArray(BraKetParser.ArrayContext ctx);
	/**
	 * Exit a parse tree produced by {@link BraKetParser#array}.
	 * @param ctx the parse tree
	 */
	void exitArray(BraKetParser.ArrayContext ctx);
	/**
	 * Enter a parse tree produced by {@link BraKetParser#struct}.
	 * @param ctx the parse tree
	 */
	void enterStruct(BraKetParser.StructContext ctx);
	/**
	 * Exit a parse tree produced by {@link BraKetParser#struct}.
	 * @param ctx the parse tree
	 */
	void exitStruct(BraKetParser.StructContext ctx);
	/**
	 * Enter a parse tree produced by {@link BraKetParser#struct_value}.
	 * @param ctx the parse tree
	 */
	void enterStruct_value(BraKetParser.Struct_valueContext ctx);
	/**
	 * Exit a parse tree produced by {@link BraKetParser#struct_value}.
	 * @param ctx the parse tree
	 */
	void exitStruct_value(BraKetParser.Struct_valueContext ctx);
	/**
	 * Enter a parse tree produced by {@link BraKetParser#op}.
	 * @param ctx the parse tree
	 */
	void enterOp(BraKetParser.OpContext ctx);
	/**
	 * Exit a parse tree produced by {@link BraKetParser#op}.
	 * @param ctx the parse tree
	 */
	void exitOp(BraKetParser.OpContext ctx);
	/**
	 * Enter a parse tree produced by {@link BraKetParser#statement_list}.
	 * @param ctx the parse tree
	 */
	void enterStatement_list(BraKetParser.Statement_listContext ctx);
	/**
	 * Exit a parse tree produced by {@link BraKetParser#statement_list}.
	 * @param ctx the parse tree
	 */
	void exitStatement_list(BraKetParser.Statement_listContext ctx);
	/**
	 * Enter a parse tree produced by {@link BraKetParser#statement}.
	 * @param ctx the parse tree
	 */
	void enterStatement(BraKetParser.StatementContext ctx);
	/**
	 * Exit a parse tree produced by {@link BraKetParser#statement}.
	 * @param ctx the parse tree
	 */
	void exitStatement(BraKetParser.StatementContext ctx);
	/**
	 * Enter a parse tree produced by {@link BraKetParser#assign_statement}.
	 * @param ctx the parse tree
	 */
	void enterAssign_statement(BraKetParser.Assign_statementContext ctx);
	/**
	 * Exit a parse tree produced by {@link BraKetParser#assign_statement}.
	 * @param ctx the parse tree
	 */
	void exitAssign_statement(BraKetParser.Assign_statementContext ctx);
	/**
	 * Enter a parse tree produced by {@link BraKetParser#func_call_statement}.
	 * @param ctx the parse tree
	 */
	void enterFunc_call_statement(BraKetParser.Func_call_statementContext ctx);
	/**
	 * Exit a parse tree produced by {@link BraKetParser#func_call_statement}.
	 * @param ctx the parse tree
	 */
	void exitFunc_call_statement(BraKetParser.Func_call_statementContext ctx);
	/**
	 * Enter a parse tree produced by {@link BraKetParser#arg_list}.
	 * @param ctx the parse tree
	 */
	void enterArg_list(BraKetParser.Arg_listContext ctx);
	/**
	 * Exit a parse tree produced by {@link BraKetParser#arg_list}.
	 * @param ctx the parse tree
	 */
	void exitArg_list(BraKetParser.Arg_listContext ctx);
	/**
	 * Enter a parse tree produced by {@link BraKetParser#arg}.
	 * @param ctx the parse tree
	 */
	void enterArg(BraKetParser.ArgContext ctx);
	/**
	 * Exit a parse tree produced by {@link BraKetParser#arg}.
	 * @param ctx the parse tree
	 */
	void exitArg(BraKetParser.ArgContext ctx);
	/**
	 * Enter a parse tree produced by {@link BraKetParser#return_statement}.
	 * @param ctx the parse tree
	 */
	void enterReturn_statement(BraKetParser.Return_statementContext ctx);
	/**
	 * Exit a parse tree produced by {@link BraKetParser#return_statement}.
	 * @param ctx the parse tree
	 */
	void exitReturn_statement(BraKetParser.Return_statementContext ctx);
	/**
	 * Enter a parse tree produced by {@link BraKetParser#if_statement}.
	 * @param ctx the parse tree
	 */
	void enterIf_statement(BraKetParser.If_statementContext ctx);
	/**
	 * Exit a parse tree produced by {@link BraKetParser#if_statement}.
	 * @param ctx the parse tree
	 */
	void exitIf_statement(BraKetParser.If_statementContext ctx);
	/**
	 * Enter a parse tree produced by {@link BraKetParser#elif}.
	 * @param ctx the parse tree
	 */
	void enterElif(BraKetParser.ElifContext ctx);
	/**
	 * Exit a parse tree produced by {@link BraKetParser#elif}.
	 * @param ctx the parse tree
	 */
	void exitElif(BraKetParser.ElifContext ctx);
	/**
	 * Enter a parse tree produced by {@link BraKetParser#else}.
	 * @param ctx the parse tree
	 */
	void enterElse(BraKetParser.ElseContext ctx);
	/**
	 * Exit a parse tree produced by {@link BraKetParser#else}.
	 * @param ctx the parse tree
	 */
	void exitElse(BraKetParser.ElseContext ctx);
	/**
	 * Enter a parse tree produced by {@link BraKetParser#for_statement}.
	 * @param ctx the parse tree
	 */
	void enterFor_statement(BraKetParser.For_statementContext ctx);
	/**
	 * Exit a parse tree produced by {@link BraKetParser#for_statement}.
	 * @param ctx the parse tree
	 */
	void exitFor_statement(BraKetParser.For_statementContext ctx);
	/**
	 * Enter a parse tree produced by {@link BraKetParser#while_statement}.
	 * @param ctx the parse tree
	 */
	void enterWhile_statement(BraKetParser.While_statementContext ctx);
	/**
	 * Exit a parse tree produced by {@link BraKetParser#while_statement}.
	 * @param ctx the parse tree
	 */
	void exitWhile_statement(BraKetParser.While_statementContext ctx);
	/**
	 * Enter a parse tree produced by {@link BraKetParser#do_statement}.
	 * @param ctx the parse tree
	 */
	void enterDo_statement(BraKetParser.Do_statementContext ctx);
	/**
	 * Exit a parse tree produced by {@link BraKetParser#do_statement}.
	 * @param ctx the parse tree
	 */
	void exitDo_statement(BraKetParser.Do_statementContext ctx);
	/**
	 * Enter a parse tree produced by {@link BraKetParser#expression}.
	 * @param ctx the parse tree
	 */
	void enterExpression(BraKetParser.ExpressionContext ctx);
	/**
	 * Exit a parse tree produced by {@link BraKetParser#expression}.
	 * @param ctx the parse tree
	 */
	void exitExpression(BraKetParser.ExpressionContext ctx);
	/**
	 * Enter a parse tree produced by {@link BraKetParser#string_expression}.
	 * @param ctx the parse tree
	 */
	void enterString_expression(BraKetParser.String_expressionContext ctx);
	/**
	 * Exit a parse tree produced by {@link BraKetParser#string_expression}.
	 * @param ctx the parse tree
	 */
	void exitString_expression(BraKetParser.String_expressionContext ctx);
	/**
	 * Enter a parse tree produced by {@link BraKetParser#num_expression}.
	 * @param ctx the parse tree
	 */
	void enterNum_expression(BraKetParser.Num_expressionContext ctx);
	/**
	 * Exit a parse tree produced by {@link BraKetParser#num_expression}.
	 * @param ctx the parse tree
	 */
	void exitNum_expression(BraKetParser.Num_expressionContext ctx);
	/**
	 * Enter a parse tree produced by {@link BraKetParser#num_term}.
	 * @param ctx the parse tree
	 */
	void enterNum_term(BraKetParser.Num_termContext ctx);
	/**
	 * Exit a parse tree produced by {@link BraKetParser#num_term}.
	 * @param ctx the parse tree
	 */
	void exitNum_term(BraKetParser.Num_termContext ctx);
	/**
	 * Enter a parse tree produced by {@link BraKetParser#num_factor}.
	 * @param ctx the parse tree
	 */
	void enterNum_factor(BraKetParser.Num_factorContext ctx);
	/**
	 * Exit a parse tree produced by {@link BraKetParser#num_factor}.
	 * @param ctx the parse tree
	 */
	void exitNum_factor(BraKetParser.Num_factorContext ctx);
	/**
	 * Enter a parse tree produced by {@link BraKetParser#array_access}.
	 * @param ctx the parse tree
	 */
	void enterArray_access(BraKetParser.Array_accessContext ctx);
	/**
	 * Exit a parse tree produced by {@link BraKetParser#array_access}.
	 * @param ctx the parse tree
	 */
	void exitArray_access(BraKetParser.Array_accessContext ctx);
	/**
	 * Enter a parse tree produced by {@link BraKetParser#struct_access}.
	 * @param ctx the parse tree
	 */
	void enterStruct_access(BraKetParser.Struct_accessContext ctx);
	/**
	 * Exit a parse tree produced by {@link BraKetParser#struct_access}.
	 * @param ctx the parse tree
	 */
	void exitStruct_access(BraKetParser.Struct_accessContext ctx);
	/**
	 * Enter a parse tree produced by {@link BraKetParser#dirac_expression}.
	 * @param ctx the parse tree
	 */
	void enterDirac_expression(BraKetParser.Dirac_expressionContext ctx);
	/**
	 * Exit a parse tree produced by {@link BraKetParser#dirac_expression}.
	 * @param ctx the parse tree
	 */
	void exitDirac_expression(BraKetParser.Dirac_expressionContext ctx);
	/**
	 * Enter a parse tree produced by {@link BraKetParser#num_comp}.
	 * @param ctx the parse tree
	 */
	void enterNum_comp(BraKetParser.Num_compContext ctx);
	/**
	 * Exit a parse tree produced by {@link BraKetParser#num_comp}.
	 * @param ctx the parse tree
	 */
	void exitNum_comp(BraKetParser.Num_compContext ctx);
	/**
	 * Enter a parse tree produced by {@link BraKetParser#eq_comp}.
	 * @param ctx the parse tree
	 */
	void enterEq_comp(BraKetParser.Eq_compContext ctx);
	/**
	 * Exit a parse tree produced by {@link BraKetParser#eq_comp}.
	 * @param ctx the parse tree
	 */
	void exitEq_comp(BraKetParser.Eq_compContext ctx);
	/**
	 * Enter a parse tree produced by {@link BraKetParser#bool_expression}.
	 * @param ctx the parse tree
	 */
	void enterBool_expression(BraKetParser.Bool_expressionContext ctx);
	/**
	 * Exit a parse tree produced by {@link BraKetParser#bool_expression}.
	 * @param ctx the parse tree
	 */
	void exitBool_expression(BraKetParser.Bool_expressionContext ctx);
	/**
	 * Enter a parse tree produced by {@link BraKetParser#bool_or}.
	 * @param ctx the parse tree
	 */
	void enterBool_or(BraKetParser.Bool_orContext ctx);
	/**
	 * Exit a parse tree produced by {@link BraKetParser#bool_or}.
	 * @param ctx the parse tree
	 */
	void exitBool_or(BraKetParser.Bool_orContext ctx);
	/**
	 * Enter a parse tree produced by {@link BraKetParser#bool_and}.
	 * @param ctx the parse tree
	 */
	void enterBool_and(BraKetParser.Bool_andContext ctx);
	/**
	 * Exit a parse tree produced by {@link BraKetParser#bool_and}.
	 * @param ctx the parse tree
	 */
	void exitBool_and(BraKetParser.Bool_andContext ctx);
	/**
	 * Enter a parse tree produced by {@link BraKetParser#bool_cmp}.
	 * @param ctx the parse tree
	 */
	void enterBool_cmp(BraKetParser.Bool_cmpContext ctx);
	/**
	 * Exit a parse tree produced by {@link BraKetParser#bool_cmp}.
	 * @param ctx the parse tree
	 */
	void exitBool_cmp(BraKetParser.Bool_cmpContext ctx);
	/**
	 * Enter a parse tree produced by {@link BraKetParser#bool_unary}.
	 * @param ctx the parse tree
	 */
	void enterBool_unary(BraKetParser.Bool_unaryContext ctx);
	/**
	 * Exit a parse tree produced by {@link BraKetParser#bool_unary}.
	 * @param ctx the parse tree
	 */
	void exitBool_unary(BraKetParser.Bool_unaryContext ctx);
	/**
	 * Enter a parse tree produced by {@link BraKetParser#bool_primary}.
	 * @param ctx the parse tree
	 */
	void enterBool_primary(BraKetParser.Bool_primaryContext ctx);
	/**
	 * Exit a parse tree produced by {@link BraKetParser#bool_primary}.
	 * @param ctx the parse tree
	 */
	void exitBool_primary(BraKetParser.Bool_primaryContext ctx);
	/**
	 * Enter a parse tree produced by {@link BraKetParser#func_decl_list}.
	 * @param ctx the parse tree
	 */
	void enterFunc_decl_list(BraKetParser.Func_decl_listContext ctx);
	/**
	 * Exit a parse tree produced by {@link BraKetParser#func_decl_list}.
	 * @param ctx the parse tree
	 */
	void exitFunc_decl_list(BraKetParser.Func_decl_listContext ctx);
	/**
	 * Enter a parse tree produced by {@link BraKetParser#func_decl}.
	 * @param ctx the parse tree
	 */
	void enterFunc_decl(BraKetParser.Func_declContext ctx);
	/**
	 * Exit a parse tree produced by {@link BraKetParser#func_decl}.
	 * @param ctx the parse tree
	 */
	void exitFunc_decl(BraKetParser.Func_declContext ctx);
	/**
	 * Enter a parse tree produced by {@link BraKetParser#param_list}.
	 * @param ctx the parse tree
	 */
	void enterParam_list(BraKetParser.Param_listContext ctx);
	/**
	 * Exit a parse tree produced by {@link BraKetParser#param_list}.
	 * @param ctx the parse tree
	 */
	void exitParam_list(BraKetParser.Param_listContext ctx);
	/**
	 * Enter a parse tree produced by {@link BraKetParser#identifier_list}.
	 * @param ctx the parse tree
	 */
	void enterIdentifier_list(BraKetParser.Identifier_listContext ctx);
	/**
	 * Exit a parse tree produced by {@link BraKetParser#identifier_list}.
	 * @param ctx the parse tree
	 */
	void exitIdentifier_list(BraKetParser.Identifier_listContext ctx);
	/**
	 * Enter a parse tree produced by {@link BraKetParser#default_list}.
	 * @param ctx the parse tree
	 */
	void enterDefault_list(BraKetParser.Default_listContext ctx);
	/**
	 * Exit a parse tree produced by {@link BraKetParser#default_list}.
	 * @param ctx the parse tree
	 */
	void exitDefault_list(BraKetParser.Default_listContext ctx);
	/**
	 * Enter a parse tree produced by {@link BraKetParser#main_function}.
	 * @param ctx the parse tree
	 */
	void enterMain_function(BraKetParser.Main_functionContext ctx);
	/**
	 * Exit a parse tree produced by {@link BraKetParser#main_function}.
	 * @param ctx the parse tree
	 */
	void exitMain_function(BraKetParser.Main_functionContext ctx);
}