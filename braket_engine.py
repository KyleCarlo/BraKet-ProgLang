"""
braket_engine.py
================
BraKet Language — Scanner, Parser, and Semantic Analyzer
Converted and optimized from Main.ipynb for use with the BraKet IDE.

Public API
----------
run_scanner(code)  -> list[TokenInfo]
run_parser(code)   -> ParserResult
run_semantic(code) -> SemanticResult

Each function is self-contained and safe to call independently.
All three share the same ANTLR4-generated lexer/parser (BraKetLexer / BraKetParser).

Requirements:
    pip install antlr4-python3-runtime==4.13.2
    antlr4 -Dlanguage=Python3 BraKet.g4 -visitor -no-listener
    (BraKetLexer.py, BraKetParser.py, BraKetVisitor.py must be on sys.path)
"""

from __future__ import annotations

import sys
from dataclasses import dataclass, field
from typing import Optional

from antlr4 import CommonTokenStream, InputStream
from antlr4.error.ErrorListener import ErrorListener

from BraKetLexer import BraKetLexer
from BraKetParser import BraKetParser
from BraKetVisitor import BraKetVisitor

# Interpreter pipeline (IC generator + tree-walking interpreter)
# Imported lazily so braket_engine still works without braket_interp on path.
try:
    from braket_interp import (
        ICGenerator, Interpreter, InterpreterResult,
        generate_ic, run_ic, ic_listing,
        snapshot_ic, DebugSnapshot,
    )
    _INTERP_AVAILABLE = True
except ImportError:
    _INTERP_AVAILABLE = False


# ══════════════════════════════════════════════════════════════════════════════
#  Shared helpers
# ══════════════════════════════════════════════════════════════════════════════

class _CollectingErrorListener(ErrorListener):
    """Collects ANTLR syntax errors into a plain list instead of printing them."""
    def __init__(self):
        super().__init__()
        self.errors: list[str] = []

    def syntaxError(self, recognizer, offendingSymbol, line, column, msg, e):
        self.errors.append(f"line {line}:{column}  {msg}")


def _build_parse_tree(code: str):
    """
    Lex + parse `code`, returning (token_stream, parser, tree, lex_errors, parse_errors).
    Errors are collected silently; ANTLR's default console listener is removed.
    """
    stream = InputStream(code)

    lexer = BraKetLexer(stream)
    lexer.removeErrorListeners()
    lex_err = _CollectingErrorListener()
    lexer.addErrorListener(lex_err)

    token_stream = CommonTokenStream(lexer)

    parser = BraKetParser(token_stream)
    parser.removeErrorListeners()
    parse_err = _CollectingErrorListener()
    parser.addErrorListener(parse_err)

    tree = parser.program()
    return token_stream, parser, tree, lex_err.errors, parse_err.errors


# ══════════════════════════════════════════════════════════════════════════════
#  Scanner
# ══════════════════════════════════════════════════════════════════════════════

@dataclass
class TokenInfo:
    index:  int
    text:   str
    type_name: str
    line:   int
    column: int


def run_scanner(code: str) -> list[TokenInfo]:
    """
    Tokenize `code` using the ANTLR4 BraKet lexer.

    Returns a list of TokenInfo (excluding the final EOF token).
    Errors encountered during lexing are silently collected and do NOT raise.
    """
    token_stream, _, _, _, _ = _build_parse_tree(code)
    token_stream.fill()

    results: list[TokenInfo] = []
    for i, tok in enumerate(token_stream.tokens):
        if tok.type == -1:          # EOF
            continue
        type_name = (
            BraKetParser.symbolicNames[tok.type]
            if 0 <= tok.type < len(BraKetParser.symbolicNames)
            else str(tok.type)
        )
        results.append(TokenInfo(
            index=i,
            text=tok.text,
            type_name=type_name,
            line=tok.line,
            column=tok.column,
        ))
    return results


# ══════════════════════════════════════════════════════════════════════════════
#  Parser
# ══════════════════════════════════════════════════════════════════════════════

@dataclass
class ParserResult:
    parse_tree_str:  str
    lex_errors:      list[str]
    parse_errors:    list[str]
    tokens:          list[TokenInfo]

    @property
    def has_errors(self) -> bool:
        return bool(self.lex_errors or self.parse_errors)


def run_parser(code: str) -> ParserResult:
    """
    Parse `code` and return a ParserResult containing:
      - parse_tree_str : ANTLR's toStringTree() representation
      - lex_errors     : list of lexer error strings
      - parse_errors   : list of parser error strings
      - tokens         : full token list (via run_scanner)
    """
    token_stream, parser, tree, lex_errors, parse_errors = _build_parse_tree(code)
    parse_tree_str = tree.toStringTree(recog=parser)

    return ParserResult(
        parse_tree_str=parse_tree_str,
        lex_errors=lex_errors,
        parse_errors=parse_errors,
        tokens=run_scanner(code),
    )


# ══════════════════════════════════════════════════════════════════════════════
#  Type system
# ══════════════════════════════════════════════════════════════════════════════

class BKType:
    INT      = "int"
    FLOAT    = "float"
    COMPLEX  = "complex"
    BOOL     = "bool"
    STRING   = "string"
    CHAR     = "char"
    ARRAY    = "array"
    STRUCT   = "struct"
    KET      = "ket"
    BRA      = "bra"
    OPERATOR = "op"
    FUNCTION = "function"
    POINTER  = "pointer"
    UNKNOWN  = "unknown"

    NUMERIC: frozenset[str] = frozenset({INT, FLOAT, COMPLEX})

    @staticmethod
    def promote(t1: str, t2: str) -> str:
        """Numeric type promotion: int < float < complex. UNKNOWN propagates."""
        if BKType.UNKNOWN in (t1, t2):    return BKType.UNKNOWN
        if BKType.COMPLEX in (t1, t2):    return BKType.COMPLEX
        if BKType.FLOAT   in (t1, t2):    return BKType.FLOAT
        if t1 == t2 == BKType.INT:        return BKType.INT
        return BKType.UNKNOWN

    @staticmethod
    def is_numeric(t: str) -> bool:
        return t in BKType.NUMERIC or t == BKType.UNKNOWN


# ══════════════════════════════════════════════════════════════════════════════
#  Symbol / Symbol Table
# ══════════════════════════════════════════════════════════════════════════════

@dataclass
class Symbol:
    name:          str
    bk_type:       str
    is_const:      bool  = False
    literal_value: object = None

    def __repr__(self):
        const = " [const]" if self.is_const else ""
        val   = f" = {self.literal_value}" if self.literal_value is not None else ""
        return f"  {self.name}: {self.bk_type}{const}{val}"


class SymbolTable:
    def __init__(self, parent: Optional[SymbolTable] = None, scope_name: str = "global"):
        self.parent:     Optional[SymbolTable]  = parent
        self.scope_name: str                    = scope_name
        self._symbols:   dict[str, Symbol]      = {}

    # ── public interface ──────────────────────────────────────

    def define(self, name: str, bk_type: str,
               is_const: bool = False, literal_value=None) -> Symbol:
        sym = Symbol(name, bk_type, is_const, literal_value)
        self._symbols[name] = sym
        return sym

    def lookup(self, name: str) -> Optional[Symbol]:
        return self._symbols.get(name) or (self.parent.lookup(name) if self.parent else None)

    def lookup_local(self, name: str) -> Optional[Symbol]:
        return self._symbols.get(name)

    def update_type(self, name: str, new_type: str, new_literal=None):
        scope = self._find_scope(name)
        if scope:
            scope._symbols[name].bk_type       = new_type
            scope._symbols[name].literal_value = new_literal

    def flat_symbols(self) -> dict[str, Symbol]:
        """All symbols visible from this scope (including parent scopes)."""
        result = {}
        if self.parent:
            result.update(self.parent.flat_symbols())
        result.update(self._symbols)
        return result

    # ── private ───────────────────────────────────────────────

    def _find_scope(self, name: str) -> Optional[SymbolTable]:
        if name in self._symbols:   return self
        return self.parent._find_scope(name) if self.parent else None

    def __repr__(self):
        lines = [f"\n╔══ Scope: {self.scope_name} ══"]
        lines += [str(s) for s in self._symbols.values()] or ["  (empty)"]
        lines.append("╚" + "═" * (len(self.scope_name) + 14))
        return "\n".join(lines)


# ══════════════════════════════════════════════════════════════════════════════
#  Diagnostics
# ══════════════════════════════════════════════════════════════════════════════

@dataclass
class Diagnostic:
    line:    int
    col:     int
    message: str
    kind:    str  # "error" | "warning"

    def __str__(self):
        icon = "✗" if self.kind == "error" else "⚠"
        return f"  {icon} [line {self.line}:{self.col}] {self.message}"


# ══════════════════════════════════════════════════════════════════════════════
#  Semantic Visitor
# ══════════════════════════════════════════════════════════════════════════════

_BUILTINS: frozenset[str] = frozenset({
    "print", "input", "dirac",
    "int", "float", "str", "bool", "complex",
    "type",
    "abs", "sqrt", "floor", "ceil", "round", "pow", "log", "exp",
    "max", "min", "sum",
    "real", "imag", "conj",
    "len", "range", "append", "pop",
    "norm", "dag", "normalize", "outer", "expect",
    "tensor", "dim", "trace", "det", "is_unitary", "identity", "zero_ket",
})

class _SemanticVisitor(BraKetVisitor):
    """
    Walks the parse tree performing:
      1. Symbol table construction  (define on first-ever assignment)
      2. Python-style type inference (type = type of RHS; updates on re-assign)
      3. Semantic error / warning reporting

    Design philosophy mirrors Python:
      - Variables have no declared type; type is inferred from the assigned value.
      - Reassigning a variable to a different type is ALLOWED (type updates, warn).
      - `const` variables are immutable; reassignment raises a semantic error.
    """

    def __init__(self):
        self.global_scope  = SymbolTable(scope_name="global")
        self.current_scope = self.global_scope
        self.diagnostics:  list[Diagnostic] = []
        self._scope_log:   list[SymbolTable] = []
        self._func_return_types: dict[str, str] = {}
        self._func_stack: list[str] = []

    # ── helpers ───────────────────────────────────────────────

    def _pos(self, ctx):
        if hasattr(ctx, "start") and ctx.start:
            return ctx.start.line, ctx.start.column
        return 0, 0

    def _error(self, ctx, msg: str):
        l, c = self._pos(ctx)
        self.diagnostics.append(Diagnostic(l, c, msg, "error"))

    def _warn(self, ctx, msg: str):
        l, c = self._pos(ctx)
        self.diagnostics.append(Diagnostic(l, c, msg, "warning"))

    def _push(self, name: str):
        self.current_scope = SymbolTable(parent=self.current_scope, scope_name=name)

    def _pop(self):
        self._scope_log.append(self.current_scope)
        self.current_scope = self.current_scope.parent

    def _assign(self, ctx, name: str, inferred_type: str,
                is_const: bool = False, literal_value=None):
        existing = self.current_scope.lookup(name)
        if existing is None:
            self.current_scope.define(name, inferred_type, is_const, literal_value)
            return
        if existing.is_const:
            self._error(ctx, f"Cannot reassign const '{name}'.")
            return
        old = existing.bk_type
        if (old != BKType.UNKNOWN and inferred_type != BKType.UNKNOWN and old != inferred_type):
            self._warn(ctx,
                f"'{name}' type changes from '{old}' → '{inferred_type}' "
                f"(Python-style reassignment).")
        self.current_scope.update_type(name, inferred_type, literal_value)

    # ── top-level ─────────────────────────────────────────────

    def visitProgram(self, ctx: BraKetParser.ProgramContext):
        # Pass 1: pre-scan every function for its return type so call
        # sites in main() see a known return type regardless of order.
        if ctx.func_decl_list():
            for func_ctx in ctx.func_decl_list().func_decl():
                self._prescan_func_return_type(func_ctx)
        # Pass 2: full semantic visit as normal
        self.visitChildren(ctx)

    def _prescan_func_return_type(self, ctx: BraKetParser.Func_declContext):
        """
        Two-step shallow pre-scan:
          Step A -- build a mini local type map by scanning assignments
                    in the function body (e.g. H = op literal => OPERATOR).
          Step B -- walk return statements using _infer_expr_type_shallow
                    with the local map to resolve types like H * state.
        No diagnostics are emitted here.
        """
        name = ctx.IDENTIFIER().getText()
        if not ctx.statement_list():
            return

        # Step A: seed local map with parameter names
        local_types: dict = {}
        if ctx.param_list() and ctx.param_list().identifier_list():
            for ident in ctx.param_list().identifier_list().IDENTIFIER():
                local_types[ident.getText()] = BKType.UNKNOWN

        # Step A: scan top-level assignments for structural type clues
        for stmt in ctx.statement_list().statement():
            if stmt.assign_statement() and stmt.assign_statement().var_decl():
                vd = stmt.assign_statement().var_decl()
                if vd.IDENTIFIER() and vd.expression():
                    lname = vd.IDENTIFIER().getText()
                    rtype = self._infer_expr_type_shallow(vd.expression(), local_types)
                    if rtype != BKType.UNKNOWN:
                        local_types[lname] = rtype
                elif vd.KET_IDENTIFIER():
                    raw = vd.KET_IDENTIFIER().getText()
                    local_types["|" + raw[1:-1] + ">"] = BKType.KET
                elif vd.BRA_IDENTIFIER():
                    raw = vd.BRA_IDENTIFIER().getText()
                    local_types["<" + raw[1:-1] + "|"] = BKType.BRA

        # Step B: infer return type with the local map
        for stmt in ctx.statement_list().statement():
            if stmt.return_statement():
                ret_type = self._infer_expr_type_shallow(
                    stmt.return_statement().expression(), local_types)
                existing = self._func_return_types.get(name, BKType.UNKNOWN)
                if existing == BKType.UNKNOWN:
                    self._func_return_types[name] = ret_type
                elif ret_type != BKType.UNKNOWN and ret_type != existing:
                    pass  # inconsistent -- reported in pass 2

    def _infer_expr_type_shallow(self, ctx, local_types: dict = None) -> str:
        """
        Determine BKType of an expression by structure only.
        Never emits diagnostics. local_types supplies function-local names.
        """
        if ctx is None:
            return BKType.UNKNOWN
        if local_types is None:
            local_types = {}
        if ctx.dirac_expression():
            return self._infer_dirac_type_shallow(ctx.dirac_expression(), local_types)
        if ctx.func_call_statement():
            callee = ctx.func_call_statement().IDENTIFIER().getText()
            return self._func_return_types.get(callee, BKType.UNKNOWN)
        if ctx.IDENTIFIER():
            iname = ctx.IDENTIFIER().getText()
            if iname in local_types:
                return local_types[iname]
            sym = self.global_scope.lookup(iname)
            return sym.bk_type if sym else BKType.UNKNOWN
        if ctx.bool_expression():   return BKType.BOOL
        if ctx.string_expression(): return BKType.STRING
        if ctx.array():             return BKType.ARRAY
        if ctx.struct():            return BKType.STRUCT
        return BKType.UNKNOWN

    def _infer_dirac_type_shallow(self, ctx, local_types: dict = None) -> str:
        """Shallow structural type inference for dirac_expression nodes."""
        if ctx is None:
            return BKType.UNKNOWN
        if local_types is None:
            local_types = {}
        if ctx.KET_IDENTIFIER():  return BKType.KET
        if ctx.BRA_IDENTIFIER():  return BKType.BRA
        if ctx.op():              return BKType.OPERATOR
        if ctx.braket_vector():   return BKType.UNKNOWN
        children = ctx.dirac_expression()
        if len(children) == 2:
            t1 = self._infer_dirac_type_shallow(children[0], local_types)
            t2 = self._infer_dirac_type_shallow(children[1], local_types)
            if ctx.MUL():    return self._dirac_mul(ctx, t1, t2)
            if ctx.TENSOR(): return self._dirac_kronecker(ctx, t1, t2)
        if ctx.IDENTIFIER():
            iname = ctx.IDENTIFIER().getText()
            if iname in local_types:
                return local_types[iname]
            sym = self.global_scope.lookup(iname)
            return sym.bk_type if sym else BKType.UNKNOWN
        return BKType.UNKNOWN

    def visitImport_statement(self, ctx):
        pass  # imports are not resolved semantically here

    # ── const ─────────────────────────────────────────────────

    def visitConst_decl(self, ctx: BraKetParser.Const_declContext):
        self._visit_var_decl_inner(ctx.var_decl(), is_const=True)

    # ── variable declaration ───────────────────────────────────

    def visitVar_decl(self, ctx: BraKetParser.Var_declContext):
        self._visit_var_decl_inner(ctx, is_const=False)

    def _visit_var_decl_inner(self, ctx: BraKetParser.Var_declContext, is_const: bool):
        if ctx.IDENTIFIER():
            name     = ctx.IDENTIFIER().getText()
            rhs_type = self._visit_expr(ctx.expression())
            literal  = self._try_literal(ctx.expression())
            # A plain variable cannot hold a ket or bra
            if rhs_type == BKType.KET:
                self._error(ctx,
                    f"Cannot assign a ket to plain variable '{name}'. "
                    f"Use ket syntax: |{name}> = ...")
            elif rhs_type == BKType.BRA:
                self._error(ctx,
                    f"Cannot assign a bra to plain variable '{name}'. "
                    f"Use bra syntax: <{name}| = ...")
            else:
                self._assign(ctx, name, rhs_type, is_const, literal)

        elif ctx.KET_IDENTIFIER():
            raw      = ctx.KET_IDENTIFIER().getText()   # |name>
            name     = "|" + raw[1:-1] + ">"
            rhs_type = self._visit_expr(ctx.expression())
            # Vector/matrix literals (braket_vector, op) are context-neutral —
            # the LHS determines whether they become ket/bra/operator.
            # Only reject if RHS is a typed non-ket value (e.g. function returning bra).
            if rhs_type not in (BKType.KET, BKType.UNKNOWN):
                self._error(ctx,
                    f"Cannot assign '{rhs_type}' to ket variable '{raw}'. "
                    f"RHS must return a ket.")
            self._assign(ctx, name, BKType.KET, is_const)

        else:                                           # BRA  <name|
            raw      = ctx.BRA_IDENTIFIER().getText()   # <name|
            name     = "<" + raw[1:-1] + "|"
            rhs_type = self._visit_expr(ctx.expression())
            # Same as above — vector literals are context-neutral.
            if rhs_type not in (BKType.BRA, BKType.UNKNOWN):
                self._error(ctx,
                    f"Cannot assign '{rhs_type}' to bra variable '{raw}'. "
                    f"RHS must return a bra.")
            self._assign(ctx, name, BKType.BRA, is_const)

    def _try_literal(self, expr_ctx) -> Optional[float]:
        try:
            return float(expr_ctx.getText().strip("()"))
        except Exception:
            return None

    # ── assign_statement ──────────────────────────────────────

    def visitAssign_statement(self, ctx: BraKetParser.Assign_statementContext):
        if ctx.var_decl():
            return self.visitVar_decl(ctx.var_decl())
        if ctx.array_access() and ctx.expression():
            self._visit_array_access(ctx.array_access())
            return self._visit_expr(ctx.expression())
        if ctx.struct_access() and ctx.expression():
            self._visit_struct_access(ctx.struct_access())
            return self._visit_expr(ctx.expression())
        if ctx.MUL():   # *ptr = expr
            ptr_name = ctx.IDENTIFIER().getText()
            sym = self.current_scope.lookup(ptr_name)
            if sym is None:
                self._error(ctx, f"Undeclared pointer '{ptr_name}'.")
            elif sym.bk_type not in (BKType.POINTER, BKType.UNKNOWN):
                self._warn(ctx, f"'{ptr_name}' (type '{sym.bk_type}') may not be a pointer.")
            return self._visit_expr(ctx.expression())
        if ctx.expression():
            return self._visit_expr(ctx.expression())
        return BKType.UNKNOWN

    # ── function / main ───────────────────────────────────────

    def visitFunc_decl(self, ctx: BraKetParser.Func_declContext):
        name = ctx.IDENTIFIER().getText()
        self.current_scope.define(name, BKType.FUNCTION)
        self._push(f"func:{name}")
        self._func_stack.append(name)
        if ctx.param_list():
            self._register_params(ctx.param_list())
        if ctx.statement_list():
            self.visitStatement_list(ctx.statement_list())
        self._func_stack.pop()
        self._pop()

    def visitMain_function(self, ctx: BraKetParser.Main_functionContext):
        self._push("main")
        if ctx.param_list():
            self._register_params(ctx.param_list())
        if ctx.statement_list():
            self.visitStatement_list(ctx.statement_list())
        self._pop()

    def _register_params(self, ctx: BraKetParser.Param_listContext):
        if ctx.identifier_list():
            for ident in ctx.identifier_list().IDENTIFIER():
                self.current_scope.define(ident.getText(), BKType.UNKNOWN)
        if ctx.default_list():
            for assign in ctx.default_list().assign_statement():
                self.visitAssign_statement(assign)

    # ── statements ────────────────────────────────────────────

    def visitStatement_list(self, ctx: BraKetParser.Statement_listContext):
        for stmt in ctx.statement():
            self.visitStatement(stmt)

    def visitStatement(self, ctx: BraKetParser.StatementContext):
        dispatch = {
            "assign_statement":      lambda: self.visitAssign_statement(ctx.assign_statement()),
            "if_statement":          lambda: self._visit_if(ctx.if_statement()),
            "for_statement":         lambda: self._visit_for(ctx.for_statement()),
            "while_statement":       lambda: self._visit_while(ctx.while_statement()),
            "do_statement":          lambda: self._visit_do(ctx.do_statement()),
            "func_call_statement":   lambda: self._visit_call(ctx.func_call_statement()),
            "return_statement":      lambda: self._visit_return(ctx.return_statement()),
        }
        for attr, fn in dispatch.items():
            if getattr(ctx, attr, lambda: None)():
                fn(); return

    def _visit_if(self, ctx: BraKetParser.If_statementContext):
        self._visit_bool_expr(ctx.bool_expression())
        self._push("if");   self.visitStatement_list(ctx.statement_list()); self._pop()
        for elif_ctx in ctx.elif_():
            self._visit_bool_expr(elif_ctx.bool_expression())
            self._push("elif"); self.visitStatement_list(elif_ctx.statement_list()); self._pop()
        if ctx.else_():
            self._push("else"); self.visitStatement_list(ctx.else_().statement_list()); self._pop()

    def _visit_for(self, ctx: BraKetParser.For_statementContext):
        self._push("for")
        assigns = ctx.assign_statement()
        self.visitAssign_statement(assigns[0])
        self._visit_bool_expr(ctx.bool_expression())
        self.visitAssign_statement(assigns[1])
        self.visitStatement_list(ctx.statement_list())
        self._pop()

    def _visit_while(self, ctx: BraKetParser.While_statementContext):
        self._visit_bool_expr(ctx.bool_expression())
        self._push("while"); self.visitStatement_list(ctx.statement_list()); self._pop()

    def _visit_do(self, ctx: BraKetParser.Do_statementContext):
        self._push("do"); self.visitStatement_list(ctx.statement_list()); self._pop()
        self._visit_bool_expr(ctx.bool_expression())

    def _visit_return(self, ctx: BraKetParser.Return_statementContext) -> str:
        ret_type = self._visit_expr(ctx.expression())
        if self._func_stack:
            fname = self._func_stack[-1]
            existing = self._func_return_types.get(fname, BKType.UNKNOWN)
            if existing == BKType.UNKNOWN:
                self._func_return_types[fname] = ret_type
            elif ret_type != BKType.UNKNOWN and ret_type != existing:
                self._warn(ctx,
                    f"Function '{fname}' has inconsistent return types: "
                    f"'{existing}' and '{ret_type}'.")
        return ret_type

    def _visit_call(self, ctx: BraKetParser.Func_call_statementContext) -> str:
        name = ctx.IDENTIFIER().getText()
        if name not in _BUILTINS and self.current_scope.lookup(name) is None:
            self._error(ctx, f"Call to undeclared function '{name}'.")
        if ctx.arg_list():
            self._visit_arg_list(ctx.arg_list())
        return self._func_return_types.get(name, BKType.UNKNOWN)

    def _visit_arg_list(self, ctx: BraKetParser.Arg_listContext):
        if ctx.arg():      self._visit_arg(ctx.arg())
        for sub in ctx.arg_list(): self._visit_arg_list(sub)

    def _visit_arg(self, ctx: BraKetParser.ArgContext):
        if ctx.assign_statement():
            self.visitAssign_statement(ctx.assign_statement())
        elif ctx.KET_IDENTIFIER():
            raw = ctx.KET_IDENTIFIER().getText()   # |name>
            key = "|" + raw[1:-1] + ">"
            if self.current_scope.lookup(key) is None:
                self._error(ctx, f"Ket '{raw}' used before assignment.")
        elif ctx.BRA_IDENTIFIER():
            raw = ctx.BRA_IDENTIFIER().getText()   # <name|
            key = "<" + raw[1:-1] + "|"
            if self.current_scope.lookup(key) is None:
                self._error(ctx, f"Bra '{raw}' used before assignment.")
        elif ctx.array_access():  self._visit_array_access(ctx.array_access())
        elif ctx.struct_access(): self._visit_struct_access(ctx.struct_access())
        elif ctx.expression():    self._visit_expr(ctx.expression())

    # ── expressions ───────────────────────────────────────────

    def _visit_expr(self, ctx: BraKetParser.ExpressionContext) -> str:
        # IMPORTANT: func_call_statement MUST be checked before IDENTIFIER.
        # ctx.IDENTIFIER() uses getToken() which searches all child tokens,
        # so it returns the function name token even when the expression is
        # a func_call_statement (e.g. hadamard(|ket0>)).
        # ctx.func_call_statement() uses getTypedRuleContext() which only
        # matches when that rule was actually parsed — so it is reliably None
        # for a plain identifier expression and non-None for a call.
        if ctx.func_call_statement(): return self._visit_call(ctx.func_call_statement())
        if ctx.array_access():        return self._visit_array_access(ctx.array_access())
        if ctx.struct_access():       return self._visit_struct_access(ctx.struct_access())
        if ctx.dirac_expression():    return self._visit_dirac(ctx.dirac_expression())
        if ctx.num_expression():      return self._visit_num_expr(ctx.num_expression())
        if ctx.bool_expression():     return self._visit_bool_expr(ctx.bool_expression())
        if ctx.string_expression():   return self._visit_str_expr(ctx.string_expression())
        if ctx.array():               return BKType.ARRAY
        if ctx.struct():              return BKType.STRUCT
        if ctx.IDENTIFIER():
            # Only reached for a plain bare identifier (not a call, not array/struct access)
            name = ctx.IDENTIFIER().getText()
            sym  = self.current_scope.lookup(name)
            if sym is None:
                self._error(ctx, f"Undeclared variable '{name}'.")
                return BKType.UNKNOWN
            return sym.bk_type
        return BKType.UNKNOWN

    # ── numeric ───────────────────────────────────────────────

    def _visit_num_expr(self, ctx: BraKetParser.Num_expressionContext) -> str:
        if ctx is None or ctx.num_term() is None: return BKType.UNKNOWN
        t1 = self._visit_num_term(ctx.num_term())
        if ctx.num_expression():
            t2 = self._visit_num_expr(ctx.num_expression())
            if not BKType.is_numeric(t1):
                self._error(ctx, f"Arithmetic on non-numeric type '{t1}'.")
            if not BKType.is_numeric(t2):
                self._error(ctx, f"Arithmetic on non-numeric type '{t2}'.")
            return BKType.promote(t1, t2)
        return t1

    def _visit_num_term(self, ctx: BraKetParser.Num_termContext) -> str:
        if ctx is None or ctx.num_factor() is None: return BKType.UNKNOWN
        t1 = self._visit_num_factor(ctx.num_factor())
        if ctx.num_term():
            t2 = self._visit_num_term(ctx.num_term())
            if ctx.DIV():
                rhs = ctx.num_term().getText().strip("()")
                if rhs in ("0", "0.0", "+0", "-0"):
                    self._error(ctx, "Division by zero detected.")
            return BKType.promote(t1, t2)
        return t1

    def _visit_num_factor(self, ctx: BraKetParser.Num_factorContext) -> str:
        if ctx.AMPERSAND():        # &var_name
            name = ctx.IDENTIFIER().getText()
            sym  = self.current_scope.lookup(name)
            if sym is None:
                self._error(ctx, f"Undeclared variable '{name}' for '&{name}'.")
            return BKType.POINTER
        if ctx.MUL() and not ctx.num_factor():   # *ptr (dereference)
            name = ctx.IDENTIFIER().getText()
            sym  = self.current_scope.lookup(name)
            if sym is None:
                self._error(ctx, f"Undeclared pointer '{name}'.")
            elif sym.bk_type not in (BKType.POINTER, BKType.UNKNOWN):
                self._warn(ctx, f"'{name}' (type '{sym.bk_type}') may not be a pointer.")
            return BKType.UNKNOWN
        if ctx.num_expression():   return self._visit_num_expr(ctx.num_expression())
        if ctx.COMPLEX():          return BKType.COMPLEX
        if ctx.INT():              return BKType.INT
        if ctx.FLOAT():            return BKType.FLOAT
        if ctx.CHAR():             return BKType.CHAR
        if ctx.num_factor():       return self._visit_num_factor(ctx.num_factor())  # unary ±
        if ctx.dirac_expression(): return self._visit_dirac(ctx.dirac_expression())
        if ctx.IDENTIFIER():
            name = ctx.IDENTIFIER().getText()
            sym  = self.current_scope.lookup(name)
            if sym is None:
                self._error(ctx, f"Undeclared variable '{name}' in numeric expression.")
                return BKType.UNKNOWN
            if sym.bk_type not in (BKType.KET, BKType.BRA, BKType.OPERATOR):
                if not BKType.is_numeric(sym.bk_type):
                    self._error(ctx,
                        f"'{name}' (type '{sym.bk_type}') cannot be used in arithmetic.")
            return sym.bk_type
        return BKType.UNKNOWN

    # ── boolean ───────────────────────────────────────────────

    def _visit_bool_expr(self, ctx: BraKetParser.Bool_expressionContext) -> str:
        self._visit_bool_or(ctx.bool_or()); return BKType.BOOL

    def _visit_bool_or(self, ctx: BraKetParser.Bool_orContext) -> str:
        for c in ctx.bool_or(): self._visit_bool_or(c)
        if ctx.bool_and():      self._visit_bool_and(ctx.bool_and())
        return BKType.BOOL

    def _visit_bool_and(self, ctx: BraKetParser.Bool_andContext) -> str:
        for c in ctx.bool_and(): self._visit_bool_and(c)
        if ctx.bool_cmp():       self._visit_bool_cmp(ctx.bool_cmp())
        return BKType.BOOL

    def _visit_bool_cmp(self, ctx: BraKetParser.Bool_cmpContext) -> str:
        num_exprs    = ctx.num_expression()
        str_exprs    = ctx.string_expression()
        bool_unaries = ctx.bool_unary()
        if len(num_exprs) == 2:
            t1 = self._visit_num_expr(num_exprs[0])
            t2 = self._visit_num_expr(num_exprs[1])
            for t, side in ((t1, "Left"), (t2, "Right")):
                if not BKType.is_numeric(t):
                    self._error(ctx, f"{side} side of comparison is non-numeric '{t}'.")
            if t1 != t2 and t1 != BKType.UNKNOWN and t2 != BKType.UNKNOWN:
                self._warn(ctx, f"Comparing '{t1}' and '{t2}'; implicit promotion applied.")
        elif len(str_exprs) == 2:
            self._visit_str_expr(str_exprs[0]); self._visit_str_expr(str_exprs[1])
        else:
            for bu in bool_unaries: self._visit_bool_unary(bu)
        return BKType.BOOL

    def _visit_bool_unary(self, ctx: BraKetParser.Bool_unaryContext) -> str:
        if ctx.bool_unary():  return self._visit_bool_unary(ctx.bool_unary())
        return self._visit_bool_primary(ctx.bool_primary())

    def _visit_bool_primary(self, ctx: BraKetParser.Bool_primaryContext) -> str:
        if ctx.IDENTIFIER():
            name = ctx.IDENTIFIER().getText()
            if self.current_scope.lookup(name) is None:
                self._error(ctx, f"Undeclared variable '{name}' in boolean expression.")
        if ctx.bool_expression():
            self._visit_bool_expr(ctx.bool_expression())
        return BKType.BOOL

    # ── string ────────────────────────────────────────────────

    def _visit_str_expr(self, ctx: BraKetParser.String_expressionContext) -> str:
        for child in ctx.string_expression():
            t = self._visit_str_expr(child)
            if t not in (BKType.STRING, BKType.UNKNOWN):
                self._error(ctx, f"Cannot concatenate non-string type '{t}'.")
        if ctx.IDENTIFIER():
            name = ctx.IDENTIFIER().getText()
            sym  = self.current_scope.lookup(name)
            if sym is None:
                self._error(ctx, f"Undeclared variable '{name}' in string expression.")
                return BKType.UNKNOWN
            if sym.bk_type not in (BKType.STRING, BKType.UNKNOWN):
                self._warn(ctx,
                    f"'{name}' has type '{sym.bk_type}'; ensure it is a string before concatenating.")
        return BKType.STRING

    # ── dirac / BraKet ────────────────────────────────────────

    def _visit_dirac(self, ctx: BraKetParser.Dirac_expressionContext) -> str:
        children = ctx.dirac_expression()
        if len(children) == 2:
            t1 = self._visit_dirac(children[0])
            t2 = self._visit_dirac(children[1])
            if ctx.MUL():    return self._dirac_mul(ctx, t1, t2)
            if ctx.TENSOR(): return self._dirac_kronecker(ctx, t1, t2)

        if ctx.KET_IDENTIFIER():
            raw = ctx.KET_IDENTIFIER().getText()
            key = "|" + raw[1:-1] + ">"
            if self.current_scope.lookup(key) is None:
                self._error(ctx, f"Ket '{raw}' used before assignment.")
            return BKType.KET

        if ctx.BRA_IDENTIFIER():
            raw = ctx.BRA_IDENTIFIER().getText()
            key = "<" + raw[1:-1] + "|"
            if self.current_scope.lookup(key) is None:
                self._error(ctx, f"Bra '{raw}' used before assignment.")
            return BKType.BRA

        if ctx.IDENTIFIER():
            name = ctx.IDENTIFIER().getText()
            sym  = self.current_scope.lookup(name)
            if sym is None:
                self._error(ctx, f"Undeclared identifier '{name}' in Dirac expression.")
                return BKType.UNKNOWN
            return sym.bk_type

        if ctx.braket_vector(): return BKType.UNKNOWN  # context-neutral: ket or bra depending on LHS
        if ctx.op():            return BKType.OPERATOR
        return BKType.UNKNOWN

    def _dirac_mul(self, ctx, t1: str, t2: str) -> str:
        N = BKType.is_numeric
        if t1 == BKType.BRA and t2 == BKType.KET:
            self._warn(ctx, "Inner product <bra|ket> → complex. "
                "Remember <bra| should be the conjugate transpose for complex amplitudes.")
            return BKType.COMPLEX
        if t1 == BKType.KET and t2 == BKType.KET:
            self._error(ctx, "ket * ket is undefined. Use '@' for outer product.")
            return BKType.UNKNOWN
        if t1 == BKType.BRA and t2 == BKType.BRA:
            self._error(ctx, "bra * bra is undefined.")
            return BKType.UNKNOWN
        if N(t1) and t2 in (BKType.KET, BKType.BRA): return t2
        if N(t2) and t1 in (BKType.KET, BKType.BRA): return t1
        if t1 == BKType.OPERATOR and t2 == BKType.KET:      return BKType.KET
        if t1 == BKType.OPERATOR and t2 == BKType.BRA:      return BKType.BRA
        if t1 == BKType.BRA      and t2 == BKType.OPERATOR: return BKType.BRA
        # Operator applied to an unknown-typed operand (e.g. a function parameter)
        # still produces a ket; bra applied to unknown operator still produces a bra.
        if t1 == BKType.OPERATOR and t2 == BKType.UNKNOWN:  return BKType.KET
        if t1 == BKType.UNKNOWN  and t2 == BKType.KET:      return BKType.KET
        if t1 == BKType.UNKNOWN  and t2 == BKType.BRA:      return BKType.BRA
        if t1 == BKType.BRA      and t2 == BKType.UNKNOWN:  return BKType.BRA
        if N(t1) and N(t2): return BKType.promote(t1, t2)
        if BKType.UNKNOWN in (t1, t2): return BKType.UNKNOWN
        self._warn(ctx, f"Unexpected '*' between Dirac types '{t1}' and '{t2}'.")
        return BKType.UNKNOWN

    def _dirac_kronecker(self, ctx, t1: str, t2: str) -> str:
        N = BKType.is_numeric
        if N(t1) and not N(t2): return t2
        if N(t2) and not N(t1): return t1
        if N(t1) and N(t2):     return BKType.promote(t1, t2)
        K, B, O = BKType.KET, BKType.BRA, BKType.OPERATOR
        table = {
            (K, K): K,   (B, B): B,   (K, B): O,
            (B, K): BKType.COMPLEX,   (O, O): O,
            (O, K): K,   (O, B): B,   (K, O): K,   (B, O): B,
        }
        return table.get((t1, t2), BKType.UNKNOWN)

    # ── access helpers ────────────────────────────────────────

    def _visit_array_access(self, ctx: BraKetParser.Array_accessContext) -> str:
        name = ctx.IDENTIFIER().getText()
        sym  = self.current_scope.lookup(name)
        if sym is None:
            self._error(ctx, f"Undeclared array '{name}'.")
        elif sym.bk_type not in (BKType.ARRAY, BKType.UNKNOWN):
            self._error(ctx, f"'{name}' is not an array (type: '{sym.bk_type}').")
        for ne in ctx.num_expression():
            self._visit_num_expr(ne)
        return BKType.UNKNOWN

    def _visit_struct_access(self, ctx: BraKetParser.Struct_accessContext) -> str:
        name = ctx.IDENTIFIER(0).getText()
        if self.current_scope.lookup(name) is None:
            self._error(ctx, f"Undeclared struct '{name}'.")
        return BKType.UNKNOWN


# ══════════════════════════════════════════════════════════════════════════════
#  Semantic Analysis — public result type and runner
# ══════════════════════════════════════════════════════════════════════════════

@dataclass
class SemanticResult:
    diagnostics:    list[Diagnostic]
    global_scope:   SymbolTable
    closed_scopes:  list[SymbolTable]   # scopes that were entered and exited
    syntax_errors:  list[str]           # from ANTLR lexer + parser

    @property
    def errors(self) -> list[Diagnostic]:
        return [d for d in self.diagnostics if d.kind == "error"]

    @property
    def warnings(self) -> list[Diagnostic]:
        return [d for d in self.diagnostics if d.kind == "warning"]

    @property
    def has_errors(self) -> bool:
        return bool(self.syntax_errors or self.errors)

    def all_symbols(self) -> dict[str, Symbol]:
        """Flat dict of every symbol defined in the global scope."""
        return dict(self.global_scope._symbols)


def run_semantic(code: str) -> SemanticResult:
    """
    Run the full semantic analysis pipeline on BraKet source code.
    Returns a SemanticResult with diagnostics, symbol table, and syntax errors.
    """
    _, _parser, tree, lex_errors, parse_errors = _build_parse_tree(code)

    visitor = _SemanticVisitor()
    visitor.visit(tree)

    return SemanticResult(
        diagnostics=visitor.diagnostics,
        global_scope=visitor.global_scope,
        closed_scopes=visitor._scope_log,
        syntax_errors=lex_errors + parse_errors,
    )


# ══════════════════════════════════════════════════════════════════════════════
#  Combined runner (convenience for IDE)
# ══════════════════════════════════════════════════════════════════════════════

@dataclass
class BraKetResult:
    """Everything the IDE needs after processing a BraKet source file."""
    tokens:          list
    parse_tree_str:  str
    sem:             object
    ic_listing:      str   = ""
    run:             object = None   # InterpreterResult | None
    debug_snapshots: list  = None    # list[DebugSnapshot], populated by analyze()

    @property
    def all_errors(self) -> list[str]:
        errs = list(self.sem.syntax_errors)
        errs += [str(d) for d in self.sem.errors]
        if self.run and self.run.error:
            errs.append(self.run.error)
        return errs

    @property
    def has_errors(self) -> bool:
        return bool(self.all_errors)

    @property
    def output(self) -> list[str]:
        return self.run.output if self.run else []


def analyze(code: str, input_cb=None, ready_cb=None, output_cb=None) -> BraKetResult:
    """
    One-stop entry point: tokenize, parse, and semantically analyse `code`.
    Returns a BraKetResult that the IDE can consume directly.

    input_cb(prompt)  — optional callable invoked when the program calls
                        input().  Must return a str.  If None, falls back to tkinter dialog.
    ready_cb(partial) — optional callable invoked after static analysis
                        (tokens, parse tree, semantics) but BEFORE the interpreter runs.
    output_cb(line)   — optional callable invoked live for each print() line.
    """
    # Single ANTLR pass shared by scanner + parser
    stream = InputStream(code)
    lexer  = BraKetLexer(stream) # LEXER
    lexer.removeErrorListeners()
    lex_err = _CollectingErrorListener()
    lexer.addErrorListener(lex_err)

    token_stream = CommonTokenStream(lexer)

    parser = BraKetParser(token_stream) # PARSER
    parser.removeErrorListeners()
    parse_err = _CollectingErrorListener()
    parser.addErrorListener(parse_err)

    tree = parser.program()
    token_stream.fill()
    
    # Collect tokens
    tokens: list[TokenInfo] = []
    for i, tok in enumerate(token_stream.tokens):
        if tok.type == -1: continue
        tname = (
            BraKetParser.symbolicNames[tok.type]
            if 0 <= tok.type < len(BraKetParser.symbolicNames) else str(tok.type)
        )
        tokens.append(TokenInfo(i, tok.text, tname, tok.line, tok.column))

    parse_tree_str = tree.toStringTree(recog=parser)

    # Semantic pass
    visitor = _SemanticVisitor() # SEMANTIC ANALYZER
    visitor.visit(tree)

    sem = SemanticResult(
        diagnostics=visitor.diagnostics,
        global_scope=visitor.global_scope,
        closed_scopes=visitor._scope_log,
        syntax_errors=lex_err.errors + parse_err.errors,
    )

    # ── IC generation + interpretation (only if no syntax/semantic errors) ──
    ic_str    = ""
    run_res   = None
    snapshots = []

    # Fire ready_cb now — static analysis is complete, interpreter hasn't run yet.
    # The IDE uses this to populate Scanner/Parse-Tree/Diagnostics before any
    # input() dialog appears.
    if ready_cb is not None:
        _partial = BraKetResult(
            tokens=tokens,
            parse_tree_str=parse_tree_str,
            sem=sem,
            ic_listing="",
            run=None,
            debug_snapshots=[],
        )
        ready_cb(_partial)

    if _INTERP_AVAILABLE and not (lex_err.errors + parse_err.errors):
        try:
            gen = ICGenerator()
            gen.generate(tree)
            ic_str  = ic_listing(gen.instructions)
            # Include function IC in listing
            for fname, (params, body) in gen.functions.items():
                param_str = ", ".join(params)
                ic_str += "\n\n# func " + fname + "(" + param_str + ")\n"
                ic_str += ic_listing(body)
            # Capture inputs during the real run, then replay them silently
            # for snapshot_ic so the dialog never opens a second time.
            _captured_inputs: list[str] = []
            _replay_index = [0]

            _original_input_cb = input_cb

            def _capturing_input_cb(prompt: str) -> str:
                val = _original_input_cb(prompt) if _original_input_cb else ""
                _captured_inputs.append(val)
                return val

            def _replaying_input_cb(prompt: str) -> str:
                idx = _replay_index[0]
                _replay_index[0] += 1
                return _captured_inputs[idx] if idx < len(_captured_inputs) else ""

            run_res = run_ic(gen.instructions, gen.functions,
                             output_cb=output_cb, input_cb=_capturing_input_cb)
            try:
                snapshots = snapshot_ic(gen.instructions, gen.functions, input_cb=_replaying_input_cb)
            except Exception:
                snapshots = []
        except Exception as e:
            run_res = type("_R", (), {
                "output": [], "error": "IC/Interpreter error: " + str(e),
                "symbol_table": {}, "ic_trace": [], "exec_log": []
            })()

    return BraKetResult(
        tokens=tokens,
        parse_tree_str=parse_tree_str,
        sem=sem,
        ic_listing=ic_str,
        run=run_res,
        debug_snapshots=snapshots,
    )


# ══════════════════════════════════════════════════════════════════════════════
#  CLI entry point (mirrors the notebook demo)
# ══════════════════════════════════════════════════════════════════════════════

def _cli_run(code: str, show_tokens: bool = True, file_dump: bool = False):
    result = analyze(code)

    print("--- Parse Tree ---")
    if file_dump:
        with open("ast.txt", "w", encoding="utf-8") as f:
            f.write(result.parse_tree_str)
        print("AST saved to ast.txt.")
    else:
        print(result.parse_tree_str)

    if show_tokens:
        print("\n--- Tokens ---")
        header = f"{'INDEX':<6} | {'TEXT':<10} | {'TYPE':<15} | {'LINE':<5} | {'COL':<5}"
        print(header); print("-" * 50)
        rows = []
        for t in result.tokens:
            rows.append(f"{t.index:<6} | {t.text:<10} | {t.type_name:<15} | {t.line:<5} | {t.column:<5}")
        if file_dump:
            with open("tokens.txt", "w", encoding="utf-8") as f:
                f.write(header + "\n" + "-" * 50 + "\n" + "\n".join(rows))
            print("Tokens saved to tokens.txt.")
        else:
            print("\n".join(rows))

    print("\n--- Errors ---")
    errs = result.all_errors
    if file_dump:
        with open("errors.txt", "w", encoding="utf-8") as f:
            f.write("\n".join(errs) if errs else "No errors.")
        print("Errors saved to errors.txt.")
    else:
        print("\n".join(errs) if errs else "No errors.")

    print("\n--- Semantic Warnings ---")
    for w in result.sem.warnings:
        print(w)
    if not result.sem.warnings:
        print("  None")


if __name__ == "__main__":
    sample = """
const |ket0> = (1,0)
const |ket1> = (0,1)
const op = ((1,0), (0,1))

main() {
    x = <ket1| @ <ket1| * |ket0> @ |ket0>
    y = ((1 < 2) || true) && 3 > 4
    z = +1+2i * -1
    print(x)
    return x
}
"""
    _cli_run(sample, show_tokens=True, file_dump=False)