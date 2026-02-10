grammar BraKet;
program
    : import_list?
      const_decl_list?
    //   func_decl_list?
    //   main_function?
    //   EOF
    ;

/* Newlines & whitespace */
COMMA   : ',';
WS : [ \t\r\n]+ -> skip ;

/* PRODUCTIONS FOR IMPORTING FILES AND FUNCTIONS */
import_list 
    : import_statement (import_statement)*
    ;
import_statement
    : FROM IDENTIFIER IMPORT func_list
    | IMPORT IDENTIFIER
    ;
func_list
    : IDENTIFIER (COMMA IDENTIFIER)*
    ;
FROM
    : 'from' 
    ;
IMPORT
    : 'import'
    ;


/* PRODUCTIONS FOR CONSTANT DECLARATION */
const_decl_list
    : const_decl+
    ;
const_decl
    : CONST var_decl
    ;
CONST
    : 'const'
    ;

/* PRODUCTIONS FOR VARIABLE DECLARATION */
var_decl_list
    : var_decl+
    ;
var_decl
    : IDENTIFIER ASSIGN expression
    ;
IDENTIFIER
    : LETTER LET_DIG_USCORE*
    | '_' LET_DIG_USCORE*
    ;
// KET_IDENTIFIER
//     : '|' IDENTIFIER '>'
//     ;
// BRA_IDENTIFIER
//     : '<' IDENTIFIER '|'
//     ;
value
    : INT
    | FLOAT
    | CHAR
    | STRING
    // | array
    // | struct
    // | COMPLEX
    // | op 
    ;

// braket_vector
//     : '(' braket_elements ')'
//     ;
// braket_elements
//     : (braket_value (',' braket_value)*)?
//     ; 
// braket_value
//     : INT
//     | FLOAT
//     | COMPLEX
//     ;

INT
    : DIGIT*
    ;
FLOAT
    : INT? '.' DIGIT+
    | INT
    ;
CHAR
    : '\''SYMBOL'\''
    ;
STRING
    : '"'SYMBOL*'"'
    ;
// array
//     : '[' element_list ']'
//     ;
// element_list
//     : (value (', ' value)*)?
//     ;
// struct
//     : '{' struct_value '}'
//     ;
// struct_value
//     : var_decl', ' struct_value
//     | func_decl', ' struct_value
//     | var_decl
//     | func_decl
//     | /* empty */ ;
// COMPLEX
//     : (INT | FLOAT) ADD (INT | FLOAT) 'i'
//     | (INT | FLOAT) SUB (INT | FLOAT) 'i'
//     | (INT | FLOAT) 'i'
//     ;
// op
//     : '[' op_list ']'
//     ;
// op_list
//     : '['op_value']' (',' '['op_value']')*
//     ;
// op_value
//     : braket_value (', ' braket_value)*
//     ;

// /* PRODUCTIONS FOR STATEMENTS */
// statement_list
//     : statement NEWLINE statement_list
//     | statement
//     | /* empty */
//     ;
// statement
//     : assign_statement
//     | func_call_statement
//     | return_statement
//     | if_statement
//     | for_statement
//     | while_statement
//     | do_statement
//     | var_decl
//     ;

assign_statement
    : var_decl
    ;

func_call_statement
    : IDENTIFIER LPAREN arg_list? RPAREN
    ;
arg_list
    : arg (COMMA arg_list)*
    ;
arg
    : assign_statement
    | IDENTIFIER
    | value
    ;
// return_statement
//     : 'return' expression
//     ;

// if_statement 
//     : 'if' '(' bool_expression ')' '{' statement_list '}' elif else
//     ;
// elif
//     : 'elif' '(' bool_expression ')' '{' statement_list '}'
//     | /* empty */
//     ;
// else
//     : 'else' '{' statement_list '}'
//     | /* empty */
//     ;

// for_statement
//     : 'for' '(' assign_statement ';' bool_expression ';' assign_statement ')' '{' statement_list '}'
//     ;
// while_statement
//     : 'while' '(' bool_expression ')' '{' statement_list '}'
//     ;
// do_statement
//     : 'do' '{' statement_list '}' 'while' '(' bool_expression ')'
//     ;

/* PRODUCTIONS FOR EXPRESSIONS */
expression
    : string_expression
    | num_expression
    // | dirac_expression
    // | bool_expression
    | func_call_statement
    ;

string_expression
    : string_expression ADD string_expression
    | STRING
    | IDENTIFIER
    ;

num_expression
    : num_term ADD num_expression
    | num_term SUB num_expression
    | num_term
    ;
num_term
    : num_factor MUL num_term
    | num_factor DIV num_term
    | num_factor MOD num_term
    | num_factor EXP num_term
    | num_factor
    ;
num_factor
    : LPAREN num_expression RPAREN
    | ADD num_factor        // Handles positive prefix (e.g., +5)
    | SUB num_factor        // Handles negative prefix (e.g., -5)
    | INT | FLOAT | CHAR 
    // | COMPLEX
    // | dirac_expression
    | 
    | IDENTIFIER
    ;

// dirac_expression
//     : dirac_expression '*' dirac_expression
//     | dirac_expression '@' dirac_expression
//     | KET_IDENTIFIER
//     | BRA_IDENTIFIER
//     | IDENTIFIER
//     | braket_vector
//     | op
//     ;

// bool_expression
//     : num_expression num_comp num_expression
//     | string_expression eq_comp string_expression
//     | bool_logical eq_comp bool_logical
//     | bool_logical
//     ;
// num_comp
//     : eq_comp 
//     | '>' | '<' | '>=' | '<='
//     ;
// eq_comp
//     : '==' | '!='
//     ;
// bool_logical
//     : bool_term '||' bool_logical
//     | bool_term
//     ;
// bool_term
//     : bool_factor '&&' bool_term
//     | bool_factor
//     ;
// bool_factor
//     : '(' bool_logical ')'
//     | '!' bool_logical
//     | 'true' | 'false'
//     | IDENTIFIER
//     ;

// /* PRODUCTIONS FOR FUNCTION DECLARATION */
// func_decl_list 
//     : func_decl NEWLINE func_decl_list
//     | func_decl
//     ;
// func_decl
//     : 'op' IDENTIFIER '(' param_list ')' '{' statement_list '}'
//     ;
// param_list
//     : identifier_list',' default_list
//     | identifier_list
//     | default_list
//     ;
// identifier_list
//     : IDENTIFIER',' identifier_list
//     | IDENTIFIER
//     | /* empty */
//     ;
// default_list
//     : assign_statement',' default_list
//     | assign_statement
//     | /* empty */
//     ;

// main_function
//     : 'main' '(' ')' '{' statement_list '}'
//     ;

// /* BASIC OPERATIONS */
ADD: '+' ;
SUB: '-' ;
MUL: '*' ;
DIV: '/' ;
EXP: '**' ;
MOD: '%' ;
ASSIGN: '=' ;

// OTHER SYMBOLS
LPAREN: '(' ;
RPAREN: ')' ;

// /* Helper fragments / Other Productions*/
fragment LET_DIG_USCORE : (LETTER | DIGIT | '_') ;
fragment LETTER : [a-zA-Z] ;
fragment DIGIT : [0-9] ;
fragment DIGIT_NONZERO : [1-9] ;
// //fragment SIGN : [+-] ;
fragment SYMBOL: . ;

