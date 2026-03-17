grammar BraKet;
// FIX: EOF anchors the program rule to the full input.
// Any tokens that do not belong to import_list, const_decl_list, func_decl_list,
// or main_function will cause a parse error instead of being silently ignored.
program
    : import_list?
      const_decl_list?
      func_decl_list?
      main_function?
      EOF
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
    | KET_IDENTIFIER ASSIGN expression
    | BRA_IDENTIFIER ASSIGN expression
    ;

KET_IDENTIFIER
    : '|' IDENTIFIER '>'
    ;
BRA_IDENTIFIER
    : '<' IDENTIFIER '|'
    ;
value
    : INT
    | FLOAT
    | CHAR
    | STRING
    | array
    | struct
    | COMPLEX
    | op
    | BOOL_FALSE
    | BOOL_TRUE
    ;

braket_vector
    : LPAREN (braket_expression (COMMA braket_expression)*) RPAREN
    ;
braket_expression
    : braket_term ADD braket_expression
    | braket_term SUB braket_expression
    | braket_term
    ;
braket_term
    : braket_factor MUL braket_term
    | braket_factor DIV braket_term
    | braket_factor MOD braket_term
    | braket_factor EXP braket_term
    | braket_factor
    ;
braket_factor
    : LPAREN braket_expression RPAREN
    | func_call_statement          // e.g. sqrt(2), cos(theta)
    | COMPLEX
    | ADD braket_factor            // unary +
    | SUB braket_factor            // unary -
    | INT | FLOAT
    | IDENTIFIER
    ;

INT
    : DIGIT+
    ;
// FIX: removed '| INT' alternative from FLOAT to eliminate ambiguity with the INT token.
// Integers are now exclusively matched by INT; FLOAT only matches values with a decimal point.
FLOAT
    : INT? '.' DIGIT+
    ;
// FIX: CHAR and STRING now use dedicated fragments that exclude newlines,
// preventing multi-line string/char literals from being accepted by the lexer.
CHAR
    : '\'' CHAR_SYMBOL? '\''
    ;
STRING
    : '"' STR_SYMBOL* '"'
    ;
array
    : LSQUARE (expression (COMMA expression)*)? RSQUARE
    ;
struct
    : LCURLY struct_value? RCURLY
    ;
struct_value
    : var_decl COMMA struct_value
    | func_decl COMMA struct_value
    | var_decl
    | func_decl
    ;

COMPLEX
    : (ADD|SUB)? (INT | FLOAT) (ADD|SUB) (INT|FLOAT) IMAG_UNIT
    | (ADD|SUB)? (INT|FLOAT) IMAG_UNIT
    ;

fragment IMAG_UNIT
    : 'i'
    ;
op
    : LPAREN braket_vector (COMMA braket_vector)* RPAREN
    ;

/* PRODUCTIONS FOR STATEMENTS */
statement_list
    : statement+
    ;
statement
    : assign_statement
    | func_call_statement
    | return_statement
    | if_statement
    | for_statement
    | while_statement
    | do_statement
    ;

assign_statement
    : var_decl
    | array_access ASSIGN expression
    | struct_access ASSIGN expression
    ;

func_call_statement
    : IDENTIFIER LPAREN arg_list? RPAREN
    ;
arg_list
    : arg (COMMA arg_list)*
    ;
arg
    : assign_statement
    | KET_IDENTIFIER
    | BRA_IDENTIFIER
    | expression
    | array_access
    | struct_access
    ;
return_statement
    : RETURN expression
    ;

RETURN
    : 'return'
    ;

if_statement 
    : IF LPAREN bool_expression RPAREN LCURLY statement_list RCURLY elif* else?
    ;
elif
    : ELIF LPAREN bool_expression RPAREN LCURLY statement_list RCURLY
    ;
else
    : ELSE LCURLY statement_list RCURLY
    ;
IF:
    'if'
    ;
ELIF:
    'elif'
    ;
ELSE:
    'else'
    ;
for_statement
    : FOR LPAREN assign_statement SEMICOLON bool_expression SEMICOLON assign_statement RPAREN LCURLY statement_list RCURLY
    ;
while_statement
    : WHILE LPAREN bool_expression RPAREN LCURLY statement_list RCURLY
    ;
do_statement
    : DO LCURLY statement_list RCURLY WHILE LPAREN bool_expression RPAREN
    ;
FOR
    : 'for'
    ;
WHILE
    : 'while'
    ;
DO
    : 'do'
    ;

/* PRODUCTIONS FOR EXPRESSIONS */
expression
    : IDENTIFIER
    | num_expression
    | array
    | struct
    | array_access
    | struct_access
    | dirac_expression
    | bool_expression
    | func_call_statement
    | string_expression
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
    | COMPLEX
    | ADD num_factor        // Handles positive prefix (e.g., +5)
    | SUB num_factor        // Handles negative prefix (e.g., -5)
    | INT | FLOAT | CHAR 
    | dirac_expression
    | IDENTIFIER
    ;

array_access
    : IDENTIFIER (LSQUARE num_expression RSQUARE)+
    ;

struct_access
    : IDENTIFIER (DOT IDENTIFIER)+
    ;

dirac_expression
    : dirac_expression MUL dirac_expression
    | dirac_expression TENSOR dirac_expression
    | KET_IDENTIFIER
    | BRA_IDENTIFIER
    | IDENTIFIER
    | braket_vector
    | op
    ;

num_comp
    : eq_comp 
    | GT | LT | GTE | LTE
    ;
eq_comp
    : EQ | NEQ
    ;
bool_expression
    : bool_or
    ;
bool_or
    : bool_or LOGICAL_OR bool_or
    | bool_and
    ;
bool_and
    : bool_and LOGICAL_AND bool_and
    | bool_cmp
    ;
bool_cmp 
    : num_expression num_comp num_expression
    | string_expression eq_comp string_expression
    | bool_unary eq_comp bool_unary
    | bool_unary
    ;
bool_unary
    : NEG bool_unary
    | bool_primary
    ;
bool_primary
    : LPAREN bool_expression RPAREN
    | BOOL_TRUE
    | BOOL_FALSE
    | INT        // 0 = false, non-zero = true
    | IDENTIFIER
    ;
BOOL_TRUE
    : 'true'
    ;
BOOL_FALSE
    : 'false'
    ;

/* PRODUCTIONS FOR FUNCTION DECLARATION */
func_decl_list 
    : func_decl+
    ;
func_decl
    : FUNC IDENTIFIER LPAREN param_list? RPAREN LCURLY statement_list? RCURLY
    ;
param_list
    : identifier_list (COMMA default_list)?
    | default_list
    ;
identifier_list
    : IDENTIFIER (COMMA IDENTIFIER)*
    ;
default_list
    : assign_statement (COMMA assign_statement)*
    ;
main_function
    : MAIN LPAREN param_list? RPAREN LCURLY statement_list? RCURLY
    ;
MAIN
    : 'main'
    ;
FUNC
    : 'func'
    ;

/* BASIC OPERATIONS */
ADD: '+' ;
SUB: '-' ;
MUL: '*' ;
DIV: '/' ;
EXP: '**' ;
MOD: '%' ;
ASSIGN: '=' ;
GT: '>' ;
LT: '<' ;
GTE: '>=' ;
LTE: '<=' ;
EQ: '==' ;
NEQ: '!=' ;
LOGICAL_OR: '||' ;
LOGICAL_AND: '&&' ;
NEG: '!' ;

// OTHER SYMBOLS
LPAREN: '(' ;
RPAREN: ')' ;
LSQUARE: '[' ;
RSQUARE: ']' ;
LCURLY: '{' ;
RCURLY: '}' ;
TENSOR: '@';
SEMICOLON: ';' ;
DOT: '.' ;

// Helper fragments
fragment LET_DIG_USCORE : (LETTER | DIGIT | '_') ;
fragment LETTER : [a-zA-Z] ;
fragment DIGIT : [0-9] ;
fragment DIGIT_NONZERO : [1-9] ;
// FIX: STR_SYMBOL matches any character except a double-quote or newline (single-line strings)
fragment STR_SYMBOL : ~["\r\n] ;
// FIX: CHAR_SYMBOL matches any character except a single-quote or newline
fragment CHAR_SYMBOL : ~['\r\n] ;

IDENTIFIER
    : LETTER LET_DIG_USCORE*
    | '_' LET_DIG_USCORE*
    ;