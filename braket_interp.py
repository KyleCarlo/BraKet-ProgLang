"""
braket_interp.py
================
BraKet Language — Intermediate Code Generator + Tree-Walking Interpreter

Pipeline
--------
  ANTLR Parse Tree
       │
       ▼
  ICGenerator   →  list[ICInstruction]   (three-address / TAC-style IR)
       │
       ▼
  Interpreter   →  runtime output, symbol table, execution trace

Intermediate Code Design
------------------------
  Three-address code (TAC) with a flat instruction list.
  Each instruction is one of:

    ASSIGN    dest, src                 dest = src
    BINOP     dest, left, op, right     dest = left OP right
    UNOP      dest, op, src             dest = OP src
    COPY      dest, src                 dest = src  (variable copy)
    LABEL     name                      jump target
    JUMP      label                     unconditional goto
    JUMPF     cond, label               goto label if cond is falsy
    JUMPT     cond, label               goto label if cond is truthy
    PARAM     src                       push argument
    CALL      dest, func, argc          dest = call func(argc args)
    RETURN    src                       return src from function
    PRINT     src                       built-in print
    ARRAY_NEW dest, size                dest = new array[size]
    ARRAY_SET dest, index, src          dest[index] = src
    ARRAY_GET dest, src, index          dest = src[index]
    STRUCT_SET dest, field, src         dest.field = src
    STRUCT_GET dest, src, field         dest = src.field

  Temporaries are named  t0, t1, t2, …
  Labels are named       L0, L1, L2, …

Public API (used by braket_engine.py / IDE)
-------------------------------------------
  generate_ic(tree, parser) -> list[ICInstruction]
  run_ic(instructions, functions, output_cb, max_steps)
       -> InterpreterResult
"""

from __future__ import annotations

import math
import cmath
import operator
from dataclasses import dataclass, field
from typing import Any, Callable, Optional

# Optional Tkinter import for input() dialog — only used at runtime if called
try:
    import tkinter as _tk
    import tkinter.simpledialog as _tk_simpledialog
    _TK_AVAILABLE = True
except ImportError:
    _TK_AVAILABLE = False

# Optional matplotlib import for dirac() visual renderer
try:
    import matplotlib
    matplotlib.use("Agg")          # non-interactive backend — no display needed
    import matplotlib.pyplot as _plt
    import io as _io
    import base64 as _base64
    _MPL_AVAILABLE = True
except ImportError:
    _MPL_AVAILABLE = False

# ANTLR-generated files must be on sys.path
from BraKetParser import BraKetParser


# ══════════════════════════════════════════════════════════════════════════════
#  Intermediate Code — instruction set
# ══════════════════════════════════════════════════════════════════════════════

# Op codes
ASSIGN    = "ASSIGN"
BINOP     = "BINOP"
UNOP      = "UNOP"
COPY      = "COPY"
LABEL     = "LABEL"
JUMP      = "JUMP"
JUMPF     = "JUMPF"
JUMPT     = "JUMPT"
PARAM     = "PARAM"
CALL      = "CALL"
RETURN_OP = "RETURN"
PRINT_OP  = "PRINT"
ARRAY_NEW = "ARRAY_NEW"
ARRAY_SET = "ARRAY_SET"
ARRAY_GET = "ARRAY_GET"
STRUCT_SET  = "STRUCT_SET"
STRUCT_GET  = "STRUCT_GET"
ADDR_OF     = "ADDR_OF"      # dest = &var_name
DEREF       = "DEREF"        # dest = *ptr_name
DEREF_ASSIGN = "DEREF_ASSIGN" # *ptr_name = src


@dataclass
class ICInstruction:
    op:   str
    a:    Any = None   # dest / label / cond
    b:    Any = None   # src / left / func / index / field
    c:    Any = None   # right / argc / src2
    line: int = 0      # source line (for error reporting)

    def __str__(self) -> str:
        parts = [f"{self.op:<12}"]
        for x in (self.a, self.b, self.c):
            if x is not None:
                parts.append(str(x))
        return "  ".join(parts)


# ══════════════════════════════════════════════════════════════════════════════
#  String escape processing
# ══════════════════════════════════════════════════════════════════════════════

_ESCAPE_MAP: dict[str, str] = {
    'n': '\n', 't': '\t', 'r': '\r',
    '\\': '\\', '"': '"', "'": "'",
    '0': '\0', 'a': '\a', 'b': '\b',
    'f': '\f', 'v': '\v',
}

def _unescape(s: str) -> str:
    """Expand backslash escape sequences in a string/char literal body.

    Recognises: \\n \\t \\r \\\\ \\" \\' \\0 \\a \\b \\f \\v
    Unknown escapes are left as-is (e.g. \\x → \\x).
    """
    if '\\' not in s:
        return s
    result: list[str] = []
    i = 0
    while i < len(s):
        if s[i] == '\\' and i + 1 < len(s):
            result.append(_ESCAPE_MAP.get(s[i + 1], s[i + 1]))
            i += 2
        else:
            result.append(s[i])
            i += 1
    return ''.join(result)


# ══════════════════════════════════════════════════════════════════════════════
#  IC Generator  (Parse Tree → flat IC list)
# ══════════════════════════════════════════════════════════════════════════════

class ICGenerator:
    """
    Walks the ANTLR parse tree and emits a flat list of ICInstructions.

    Functions are stored in self.functions as  name -> (param_names, [IC]).
    The top-level (global const/var declarations) emit into self.instructions.
    main() body also emits into self.instructions after globals.
    """

    def __init__(self):
        self.instructions: list[ICInstruction] = []
        self.functions:    dict[str, tuple[list[str], list[ICInstruction]]] = {}
        self._tmp_count   = 0
        self._lbl_count   = 0
        self._current_ic: list[ICInstruction] = self.instructions  # active emit target
        self._const_names: set[str] = set()

    # ── helpers ───────────────────────────────────────────────

    def _tmp(self) -> str:
        name = f"t{self._tmp_count}"
        self._tmp_count += 1
        return name

    def _label(self) -> str:
        name = f"L{self._lbl_count}"
        self._lbl_count += 1
        return name

    def _emit(self, op, a=None, b=None, c=None, line=0):
        self._current_ic.append(ICInstruction(op, a, b, c, line))

    def _line(self, ctx) -> int:
        try:    return ctx.start.line
        except: return 0

    # ── top level ─────────────────────────────────────────────

    def generate(self, tree: BraKetParser.ProgramContext):
        """Entry point. Call after parsing."""
        ctx = tree
        if ctx.const_decl_list():
            self._gen_const_decl_list(ctx.const_decl_list())
        if ctx.func_decl_list():
            self._gen_func_decl_list(ctx.func_decl_list())
        if ctx.main_function():
            self._gen_main(ctx.main_function())
        return self.instructions

    # ── const declarations ────────────────────────────────────

    def _gen_const_decl_list(self, ctx):
        for c in ctx.const_decl():
            self._gen_var_decl(c.var_decl(), is_const=True)

    # ── function declarations ─────────────────────────────────

    def _gen_func_decl_list(self, ctx):
        for f in ctx.func_decl():
            self._gen_func_decl(f)

    def _gen_func_decl(self, ctx):
        name   = ctx.IDENTIFIER().getText()
        params, default_ics = self._get_param_info(ctx.param_list()) if ctx.param_list() else ([], [])

        # Save and swap emit target
        saved = self._current_ic
        body_ic: list[ICInstruction] = []
        self._current_ic = body_ic

        self._emit(LABEL, name)
        if ctx.statement_list():
            self._gen_statement_list(ctx.statement_list())
        # implicit return None
        self._emit(RETURN_OP, None, line=self._line(ctx))

        self._current_ic = saved
        self.functions[name] = (params, body_ic, default_ics)

    def _get_param_info(self, ctx) -> tuple[list[str], list[tuple]]:
        """Return (param_names, default_ics).

        default_ics is a list of (param_name, mini_ic, result_addr) for every
        parameter that has a default value.  mini_ic is the IC needed to compute
        the default (empty for plain literals); result_addr is the variable name
        or literal that holds the result after running mini_ic.
        """
        names: list[str] = []
        default_ics: list[tuple] = []

        if ctx.identifier_list():
            for ident in ctx.identifier_list().IDENTIFIER():
                names.append(ident.getText())

        if ctx.default_list():
            for assign in ctx.default_list().assign_statement():
                if assign.var_decl() and assign.var_decl().IDENTIFIER():
                    pname = assign.var_decl().IDENTIFIER().getText()
                    names.append(pname)
                    # Generate IC for the default expression into a mini-list
                    saved = self._current_ic
                    mini_ic: list[ICInstruction] = []
                    self._current_ic = mini_ic
                    result_addr = self._gen_rhs(assign.var_decl())
                    self._current_ic = saved
                    default_ics.append((pname, mini_ic, result_addr))

        return names, default_ics

    # ── main ──────────────────────────────────────────────────

    def _gen_main(self, ctx):
        self._emit(LABEL, "main", line=self._line(ctx))
        if ctx.statement_list():
            self._gen_statement_list(ctx.statement_list())
        self._emit(RETURN_OP, None)

    # ── statement list ────────────────────────────────────────

    def _gen_statement_list(self, ctx):
        for stmt in ctx.statement():
            self._gen_statement(stmt)

    def _gen_statement(self, ctx):
        if ctx.assign_statement():
            self._gen_assign_stmt(ctx.assign_statement())
        elif ctx.if_statement():
            self._gen_if(ctx.if_statement())
        elif ctx.for_statement():
            self._gen_for(ctx.for_statement())
        elif ctx.while_statement():
            self._gen_while(ctx.while_statement())
        elif ctx.do_statement():
            self._gen_do(ctx.do_statement())
        elif ctx.func_call_statement():
            t = self._tmp()
            self._gen_call(ctx.func_call_statement(), dest=t)
        elif ctx.return_statement():
            self._gen_return(ctx.return_statement())

    # ── assignments ───────────────────────────────────────────

    def _gen_assign_stmt(self, ctx):
        if ctx.var_decl():
            self._gen_var_decl(ctx.var_decl())
        elif ctx.array_access() and ctx.expression():
            # array[i] = expr
            idx  = self._gen_num_expr_from_access(ctx.array_access())
            val  = self._gen_expr(ctx.expression())
            name = ctx.array_access().IDENTIFIER().getText()
            self._emit(ARRAY_SET, name, idx, val, line=self._line(ctx))
        elif ctx.struct_access() and ctx.expression():
            # struct.field = expr
            val   = self._gen_expr(ctx.expression())
            name  = ctx.struct_access().IDENTIFIER(0).getText()
            field_name = ctx.struct_access().IDENTIFIER(1).getText()
            self._emit(STRUCT_SET, name, field_name, val, line=self._line(ctx))
        elif ctx.MUL():
            # *ptr = expr
            ptr_name = ctx.IDENTIFIER().getText()
            val      = self._gen_expr(ctx.expression())
            self._emit(DEREF_ASSIGN, ptr_name, val, line=self._line(ctx))

    def _gen_rhs(self, ctx):
        """
        Get the IC address for a var_decl RHS.
        Tries expression() first (new grammar), falls back to num_expression()
        for stale parsers that still route ket/bra RHS through num_expression.
        """
        if ctx.expression():
            return self._gen_expr(ctx.expression())
        if ctx.num_expression():
            return self._gen_num_expr(ctx.num_expression())
        return None

    def _gen_var_decl(self, ctx, is_const=False):
        """
        var_decl : IDENTIFIER    ASSIGN expression
                 | KET_IDENTIFIER ASSIGN expression   (new grammar)
                 | BRA_IDENTIFIER ASSIGN expression   (new grammar)
        Falls back to num_expression for ket/bra if parser not yet regenerated.
        """
        ln = self._line(ctx)
        if ctx.IDENTIFIER():
            name = ctx.IDENTIFIER().getText()
            val  = self._gen_rhs(ctx)
            self._emit(ASSIGN, name, val, line=ln)
            if is_const:
                self._const_names.add(name)

        elif ctx.KET_IDENTIFIER():
            raw  = ctx.KET_IDENTIFIER().getText()   # |name>
            name = raw                               # keep the full token as key
            val  = self._gen_rhs(ctx)
            self._emit(ASSIGN, name, val, line=ln)
            if is_const:
                self._const_names.add(name)

        elif ctx.BRA_IDENTIFIER():
            raw  = ctx.BRA_IDENTIFIER().getText()   # <name|
            name = raw
            val  = self._gen_rhs(ctx)
            self._emit(ASSIGN, name, val, line=ln)
            if is_const:
                self._const_names.add(name)

    def _gen_braket_vector_or_num(self, ctx):
        """For ket/bra declarations — tries expression then num_expression."""
        return self._gen_rhs(ctx)

    # ── if / elif / else ──────────────────────────────────────

    def _gen_if(self, ctx):
        end_label = self._label()

        # if
        cond = self._gen_bool_expr(ctx.bool_expression())
        next_label = self._label()
        self._emit(JUMPF, cond, next_label, line=self._line(ctx))
        self._gen_statement_list(ctx.statement_list())
        self._emit(JUMP, end_label)
        self._emit(LABEL, next_label)

        # elif chain
        for elif_ctx in ctx.elif_():
            cond = self._gen_bool_expr(elif_ctx.bool_expression())
            next_label = self._label()
            self._emit(JUMPF, cond, next_label, line=self._line(elif_ctx))
            self._gen_statement_list(elif_ctx.statement_list())
            self._emit(JUMP, end_label)
            self._emit(LABEL, next_label)

        # else
        if ctx.else_():
            self._gen_statement_list(ctx.else_().statement_list())

        self._emit(LABEL, end_label)

    # ── for ───────────────────────────────────────────────────

    def _gen_for(self, ctx):
        assigns = ctx.assign_statement()
        # init
        self._gen_assign_stmt(assigns[0])

        loop_label = self._label()
        end_label  = self._label()
        self._emit(LABEL, loop_label)

        # condition
        cond = self._gen_bool_expr(ctx.bool_expression())
        self._emit(JUMPF, cond, end_label, line=self._line(ctx))

        # body
        self._gen_statement_list(ctx.statement_list())

        # update
        self._gen_assign_stmt(assigns[1])
        self._emit(JUMP, loop_label)
        self._emit(LABEL, end_label)

    # ── while ─────────────────────────────────────────────────

    def _gen_while(self, ctx):
        loop_label = self._label()
        end_label  = self._label()
        self._emit(LABEL, loop_label)
        cond = self._gen_bool_expr(ctx.bool_expression())
        self._emit(JUMPF, cond, end_label, line=self._line(ctx))
        self._gen_statement_list(ctx.statement_list())
        self._emit(JUMP, loop_label)
        self._emit(LABEL, end_label)

    # ── do-while ──────────────────────────────────────────────

    def _gen_do(self, ctx):
        loop_label = self._label()
        self._emit(LABEL, loop_label)
        self._gen_statement_list(ctx.statement_list())
        cond = self._gen_bool_expr(ctx.bool_expression())
        self._emit(JUMPT, cond, loop_label, line=self._line(ctx))

    # ── return ────────────────────────────────────────────────

    def _gen_return(self, ctx):
        val = self._gen_expr(ctx.expression())
        self._emit(RETURN_OP, val, line=self._line(ctx))

    # ── function call ─────────────────────────────────────────

    def _gen_call(self, ctx, dest: str) -> str:
        name = ctx.IDENTIFIER().getText()
        args = []
        if ctx.arg_list():
            args = self._collect_args(ctx.arg_list())
        for a in args:
            self._emit(PARAM, a, line=self._line(ctx))
        self._emit(CALL, dest, name, len(args), line=self._line(ctx))
        return dest

    def _collect_args(self, ctx) -> list:
        args = []
        if ctx.arg():
            args.append(self._gen_arg(ctx.arg()))
        for sub in ctx.arg_list():
            args.extend(self._collect_args(sub))
        return args

    def _gen_arg(self, ctx):
        if ctx.assign_statement():
            # default arg — generate the assignment and return the var name
            self._gen_assign_stmt(ctx.assign_statement())
            if ctx.assign_statement().var_decl():
                return ctx.assign_statement().var_decl().IDENTIFIER().getText()
        elif ctx.KET_IDENTIFIER():
            # Pass ket by its full token name e.g. "|ket0>"
            return ctx.KET_IDENTIFIER().getText()
        elif ctx.BRA_IDENTIFIER():
            # Pass bra by its full token name e.g. "<phi|"
            return ctx.BRA_IDENTIFIER().getText()
        elif ctx.array_access():
            return self._gen_array_access(ctx.array_access())
        elif ctx.struct_access():
            return self._gen_struct_access(ctx.struct_access())
        elif ctx.expression():
            # Covers plain IDENTIFIER, literals, and all other expressions
            return self._gen_expr(ctx.expression())
        return None

    # ── expressions ───────────────────────────────────────────

    def _gen_expr(self, ctx) -> Any:
        """Dispatch to the correct sub-expression generator."""
        if ctx is None:
            return None
        if ctx.IDENTIFIER():
            return ctx.IDENTIFIER().getText()
        if ctx.dirac_expression():
            return self._gen_dirac(ctx.dirac_expression())
        if ctx.num_expression():
            return self._gen_num_expr(ctx.num_expression())
        if ctx.bool_expression():
            return self._gen_bool_expr(ctx.bool_expression())
        if ctx.string_expression():
            return self._gen_string_expr(ctx.string_expression())
        if ctx.array():
            return self._gen_array_literal(ctx.array())
        if ctx.struct():
            return self._gen_struct_literal(ctx.struct())
        if ctx.array_access():
            return self._gen_array_access(ctx.array_access())
        if ctx.struct_access():
            return self._gen_struct_access(ctx.struct_access())
        if ctx.func_call_statement():
            t = self._tmp()
            return self._gen_call(ctx.func_call_statement(), dest=t)
        return None

    # ── numeric expressions ───────────────────────────────────

    def _gen_num_expr(self, ctx) -> Any:
        if ctx is None:
            return 0
        left = self._gen_num_term(ctx.num_term())
        if ctx.num_expression():
            right = self._gen_num_expr(ctx.num_expression())
            op    = "+" if ctx.ADD() else "-"
            t     = self._tmp()
            self._emit(BINOP, t, left, op, line=self._line(ctx))
            self._instructions_last().c = right
            return t
        return left

    def _instructions_last(self) -> ICInstruction:
        return self._current_ic[-1]

    def _gen_num_term(self, ctx) -> Any:
        left = self._gen_num_factor(ctx.num_factor())
        if ctx.num_term():
            right = self._gen_num_term(ctx.num_term())
            if   ctx.MUL(): op = "*"
            elif ctx.DIV(): op = "/"
            elif ctx.MOD(): op = "%"
            elif ctx.EXP(): op = "**"
            else:           op = "*"
            t = self._tmp()
            self._emit(BINOP, t, left, op, line=self._line(ctx))
            self._instructions_last().c = right
            return t
        return left

    def _gen_num_factor(self, ctx) -> Any:
        if ctx.AMPERSAND():                          # &var_name
            var_name = ctx.IDENTIFIER().getText()
            t = self._tmp()
            self._emit(ADDR_OF, t, var_name, line=self._line(ctx))
            return t
        if ctx.MUL() and not ctx.num_factor():       # *ptr (not a unary ± with nested num_factor)
            var_name = ctx.IDENTIFIER().getText()
            t = self._tmp()
            self._emit(DEREF, t, var_name, line=self._line(ctx))
            return t
        if ctx.LPAREN() and ctx.num_expression():
            return self._gen_num_expr(ctx.num_expression())
        if ctx.func_call_statement():
            # Function call result used as a numeric operand: n + summation(n-1)
            t = self._tmp()
            return self._gen_call(ctx.func_call_statement(), dest=t)
        if ctx.COMPLEX():
            return self._parse_complex(ctx.COMPLEX().getText())
        if ctx.INT():
            return int(ctx.INT().getText())
        if ctx.FLOAT():
            return float(ctx.FLOAT().getText())
        if ctx.CHAR():
            raw = ctx.CHAR().getText()
            return _unescape(raw[1:-1])
        if ctx.num_factor():
            inner = self._gen_num_factor(ctx.num_factor())
            if ctx.SUB():
                t = self._tmp()
                self._emit(UNOP, t, "-", inner, line=self._line(ctx))
                return t
            return inner   # unary +
        if ctx.array_access():
            return self._gen_array_access(ctx.array_access())
        if ctx.dirac_expression():
            return self._gen_dirac(ctx.dirac_expression())
        if ctx.IDENTIFIER():
            return ctx.IDENTIFIER().getText()
        return 0

    def _parse_complex(self, text: str) -> complex:
        """Parse BraKet complex literals like +1+2i, -3+0.5i, 2i, 0.5i."""
        text = text.strip()
        try:
            # pure imaginary:  2i  or  0.5i
            if text.endswith("i") and "+" not in text[1:] and "-" not in text[1:]:
                return complex(0, float(text[:-1]) if text[:-1] else 1)
            # full:  +1+2i  or  -3+0.5i
            text = text.replace("i", "j")
            return complex(text)
        except Exception:
            return complex(0)

    # ── boolean expressions ───────────────────────────────────

    def _gen_bool_expr(self, ctx) -> Any:
        return self._gen_bool_or(ctx.bool_or())

    def _gen_bool_or(self, ctx) -> Any:
        bool_ors = ctx.bool_or()
        if bool_ors:
            left  = self._gen_bool_or(bool_ors[0])
            right = self._gen_bool_or(bool_ors[1]) if len(bool_ors) > 1 else self._gen_bool_and(ctx.bool_and())
            t = self._tmp()
            self._emit(BINOP, t, left, "||", line=self._line(ctx))
            self._instructions_last().c = right
            return t
        return self._gen_bool_and(ctx.bool_and())

    def _gen_bool_and(self, ctx) -> Any:
        bool_ands = ctx.bool_and()
        if bool_ands:
            left  = self._gen_bool_and(bool_ands[0])
            right = self._gen_bool_and(bool_ands[1]) if len(bool_ands) > 1 else self._gen_bool_cmp(ctx.bool_cmp())
            t = self._tmp()
            self._emit(BINOP, t, left, "&&", line=self._line(ctx))
            self._instructions_last().c = right
            return t
        return self._gen_bool_cmp(ctx.bool_cmp())

    def _gen_bool_cmp(self, ctx) -> Any:
        num_exprs    = ctx.num_expression()
        str_exprs    = ctx.string_expression()
        bool_unaries = ctx.bool_unary()

        if len(num_exprs) == 2:
            left  = self._gen_num_expr(num_exprs[0])
            right = self._gen_num_expr(num_exprs[1])
            op    = self._cmp_op(ctx.num_comp())
            t     = self._tmp()
            self._emit(BINOP, t, left, op, line=self._line(ctx))
            self._instructions_last().c = right
            return t

        if len(str_exprs) == 2:
            left  = self._gen_string_expr(str_exprs[0])
            right = self._gen_string_expr(str_exprs[1])
            op    = self._eq_op(ctx.eq_comp())
            t     = self._tmp()
            self._emit(BINOP, t, left, op, line=self._line(ctx))
            self._instructions_last().c = right
            return t

        if len(bool_unaries) == 2:
            left  = self._gen_bool_unary(bool_unaries[0])
            right = self._gen_bool_unary(bool_unaries[1])
            op    = self._eq_op(ctx.eq_comp())
            t     = self._tmp()
            self._emit(BINOP, t, left, op, line=self._line(ctx))
            self._instructions_last().c = right
            return t

        if len(bool_unaries) == 1:
            return self._gen_bool_unary(bool_unaries[0])

        return False

    def _gen_bool_unary(self, ctx) -> Any:
        if ctx.NEG():
            inner = self._gen_bool_unary(ctx.bool_unary())
            t     = self._tmp()
            self._emit(UNOP, t, "!", inner, line=self._line(ctx))
            return t
        return self._gen_bool_primary(ctx.bool_primary())

    def _gen_bool_primary(self, ctx) -> Any:
        if ctx.BOOL_TRUE():   return True
        if ctx.BOOL_FALSE():  return False
        if ctx.INT():         return int(ctx.INT().getText())
        if ctx.func_call_statement():
            # Function call result used as a boolean: if (isValid(x))
            t = self._tmp()
            return self._gen_call(ctx.func_call_statement(), dest=t)
        if ctx.IDENTIFIER():  return ctx.IDENTIFIER().getText()
        if ctx.bool_expression():
            return self._gen_bool_expr(ctx.bool_expression())
        return False

    def _cmp_op(self, ctx) -> str:
        if ctx is None: return "=="
        if ctx.eq_comp(): return self._eq_op(ctx.eq_comp())
        if ctx.GT():  return ">"
        if ctx.LT():  return "<"
        if ctx.GTE(): return ">="
        if ctx.LTE(): return "<="
        return "=="

    def _eq_op(self, ctx) -> str:
        if ctx is None: return "=="
        return "==" if ctx.EQ() else "!="

    # ── string expressions ────────────────────────────────────

    def _gen_string_expr(self, ctx) -> Any:
        parts = ctx.string_expression()
        if parts:
            left  = self._gen_string_expr(parts[0])
            right = self._gen_string_expr(parts[1]) if len(parts) > 1 else ""
            t     = self._tmp()
            self._emit(BINOP, t, left, "+", line=self._line(ctx))
            self._instructions_last().c = right
            return t
        if ctx.STRING():
            raw = ctx.STRING().getText()
            return _unescape(raw[1:-1])
        if ctx.IDENTIFIER():
            return ctx.IDENTIFIER().getText()
        return ""

    # ── dirac expressions ─────────────────────────────────────

    def _gen_dirac(self, ctx) -> Any:
        children = ctx.dirac_expression()
        if len(children) == 2:
            left  = self._gen_dirac(children[0])
            right = self._gen_dirac(children[1])
            op    = "*" if ctx.MUL() else "@"
            t     = self._tmp()
            
            ins = ICInstruction(BINOP, t, left, right, self._line(ctx))
            ins._op2 = op
            self._current_ic.append(ins)
            return t
        if ctx.KET_IDENTIFIER():
            return ctx.KET_IDENTIFIER().getText()
        if ctx.BRA_IDENTIFIER():
            return ctx.BRA_IDENTIFIER().getText()
        if ctx.func_call_statement():
            # Function call result used as a dirac operand: hadamard(|ket>), normalize(v)
            t = self._tmp()
            return self._gen_call(ctx.func_call_statement(), dest=t)
        if ctx.IDENTIFIER():
            return ctx.IDENTIFIER().getText()
        if ctx.braket_vector():
            return self._gen_braket_vector(ctx.braket_vector())
        if ctx.op():
            return self._gen_op_matrix(ctx.op())
        return None

    def _gen_braket_vector(self, ctx) -> str:
        """
        Build a row-vector from a braket_vector node.
        Each element is a full braket_expression — supports variables,
        arithmetic, negation, and function calls like sqrt(2).
        Emits ARRAY_NEW + ARRAY_SET + VEC_FROM_ARRAY and returns a temp name.
        """
        elems = ctx.braket_expression()
        elem_addrs = [self._gen_braket_expr(be) for be in elems]
        t = self._tmp()
        self._emit(ARRAY_NEW, t, len(elem_addrs), line=self._line(ctx))
        for i, addr in enumerate(elem_addrs):
            self._emit(ARRAY_SET, t, i, addr, line=self._line(ctx))
        self._emit("VEC_FROM_ARRAY", t, t, line=self._line(ctx))
        return t

    def _gen_braket_expr(self, ctx):
        """Generate IC for a braket_expression; return its address."""
        if ctx is None:
            return 0
        left = self._gen_braket_term(ctx.braket_term())
        if ctx.braket_expression():
            right = self._gen_braket_expr(ctx.braket_expression())
            op = "+" if ctx.ADD() else "-"
            t = self._tmp()
            ins = ICInstruction(BINOP, t, left, right, self._line(ctx))
            ins._op2 = op
            self._current_ic.append(ins)
            return t
        return left

    def _gen_braket_term(self, ctx):
        left = self._gen_braket_factor(ctx.braket_factor())
        if ctx.braket_term():
            right = self._gen_braket_term(ctx.braket_term())
            if   ctx.MUL(): op = "*"
            elif ctx.DIV(): op = "/"
            elif ctx.MOD(): op = "%"
            elif ctx.EXP(): op = "**"
            else:           op = "*"
            t = self._tmp()
            ins = ICInstruction(BINOP, t, left, right, self._line(ctx))
            ins._op2 = op
            self._current_ic.append(ins)
            return t
        return left

    def _gen_braket_factor(self, ctx):
        if ctx.LPAREN() and ctx.braket_expression():
            return self._gen_braket_expr(ctx.braket_expression())
        if ctx.func_call_statement():
            t = self._tmp()
            return self._gen_call(ctx.func_call_statement(), dest=t)
        if ctx.COMPLEX():
            return self._parse_complex(ctx.COMPLEX().getText())
        if ctx.INT():
            return int(ctx.INT().getText())
        if ctx.FLOAT():
            return float(ctx.FLOAT().getText())
        if ctx.braket_factor():            # unary +/-
            inner = self._gen_braket_factor(ctx.braket_factor())
            if ctx.SUB():
                t = self._tmp()
                ins = ICInstruction(UNOP, t, "-", inner, self._line(ctx))
                ins._op2 = None
                self._current_ic.append(ins)
                return t
            return inner
        if ctx.IDENTIFIER():
            return ctx.IDENTIFIER().getText()
        return 0

    def _gen_op_matrix(self, ctx) -> str:
        """
        Build a matrix (operator) from an op node.
        Collects row temps into a MAT_FROM_ROWS instruction so the
        interpreter builds a BKOperator at runtime.
        """
        row_temps = [self._gen_braket_vector(bvec)
                     for bvec in ctx.braket_vector()]
        t = self._tmp()
        self._emit(ARRAY_NEW, t, len(row_temps), line=self._line(ctx))
        for i, rt in enumerate(row_temps):
            self._emit(ARRAY_SET, t, i, rt, line=self._line(ctx))
        self._emit("MAT_FROM_ROWS", t, t, line=self._line(ctx))
        return t

    # ── array literals ────────────────────────────────────────

    def _gen_array_literal(self, ctx) -> str:
        exprs = ctx.expression()
        t     = self._tmp()
        self._emit(ARRAY_NEW, t, len(exprs), line=self._line(ctx))
        for i, e in enumerate(exprs):
            val = self._gen_expr(e)
            self._emit(ARRAY_SET, t, i, val, line=self._line(ctx))
        return t

    def _gen_array_access(self, ctx) -> str:
        name   = ctx.IDENTIFIER().getText()
        idx    = self._gen_num_expr(ctx.num_expression(0))
        t      = self._tmp()
        self._emit(ARRAY_GET, t, name, idx, line=self._line(ctx))
        return t

    def _gen_num_expr_from_access(self, ctx) -> Any:
        return self._gen_num_expr(ctx.num_expression(0))

    # ── struct literals ───────────────────────────────────────

    def _gen_struct_literal(self, ctx) -> dict:
        """Structs are represented as Python dicts at runtime."""
        t = self._tmp()
        self._emit(ASSIGN, t, {}, line=self._line(ctx))
        if ctx.struct_value():
            self._gen_struct_value(ctx.struct_value(), t)
        return t

    def _gen_struct_value(self, ctx, struct_tmp: str):
        if ctx.var_decl():
            vd   = ctx.var_decl()
            fname = vd.IDENTIFIER().getText() if vd.IDENTIFIER() else None
            if fname:
                val = self._gen_expr(vd.expression())
                self._emit(STRUCT_SET, struct_tmp, fname, val, line=self._line(ctx))
        if ctx.struct_value():
            self._gen_struct_value(ctx.struct_value(), struct_tmp)

    def _gen_struct_access(self, ctx) -> str:
        name  = ctx.IDENTIFIER(0).getText()
        fname = ctx.IDENTIFIER(1).getText()
        t     = self._tmp()
        self._emit(STRUCT_GET, t, name, fname, line=self._line(ctx))
        return t

    # ── value literals (used in args) ─────────────────────────

    def _gen_value_literal(self, ctx) -> Any:
        if ctx.INT():     return int(ctx.INT().getText())
        if ctx.FLOAT():   return float(ctx.FLOAT().getText())
        if ctx.CHAR():
            raw = ctx.CHAR().getText()
            return _unescape(raw[1:-1])
        if ctx.STRING():
            return _unescape(ctx.STRING().getText()[1:-1])
        if ctx.BOOL_TRUE():  return True
        if ctx.BOOL_FALSE(): return False
        if ctx.COMPLEX():    return self._parse_complex(ctx.COMPLEX().getText())
        if ctx.array():      return self._gen_array_literal(ctx.array())
        return None


# ══════════════════════════════════════════════════════════════════════════════
#  Runtime values
# ══════════════════════════════════════════════════════════════════════════════

class BKArray:
    """Mutable array wrapper."""
    def __init__(self, data: list):
        self.data = list(data)

    def __repr__(self):
        return f"[{', '.join(_fmt(x) for x in self.data)}]"


class BKStruct:
    """Record / struct wrapper."""
    def __init__(self, fields: dict):
        self.fields = dict(fields)

    def __repr__(self):
        inner = ", ".join(f"{k}={_fmt(v)}" for k, v in self.fields.items())
        return "{" + inner + "}"


def _is_tmp_name(name: object) -> bool:
    """Return True if *name* is an auto-generated temporary (t0, t1, …)."""
    return isinstance(name, str) and len(name) >= 2 and name[0] == 't' and name[1:].isdigit()


class BKPointer:
    """Pointer to a named variable in the interpreter's address space."""
    def __init__(self, var_name: str, address: int):
        self.var_name = var_name
        self.address  = address

    def __repr__(self):
        return f"*{self.var_name} @ 0x{self.address:08x}"


class BKVector:
    """Ket or bra state vector."""
    def __init__(self, data: list, kind: str = "ket"):
        self.data = [complex(x) for x in data]
        self.kind = kind   # "ket" or "bra"

    def __repr__(self):
        inner = ", ".join(_fmt_complex(x) for x in self.data)
        if self.kind == "ket":
            return f"|({inner})>"
        return f"<({inner})|"


class BKOperator:
    """Matrix / linear operator."""
    def __init__(self, rows: list):
        self.rows = [[complex(x) for x in row] for row in rows]

    @property
    def n_rows(self): return len(self.rows)

    @property
    def n_cols(self): return len(self.rows[0]) if self.rows else 0

    def __repr__(self):
        rows = [f"[{', '.join(_fmt_complex(x) for x in row)}]" for row in self.rows]
        return "(" + ", ".join(rows) + ")"


def _fmt_complex(z: complex) -> str:
    if z.imag == 0:
        r = z.real
        return str(int(r)) if r == int(r) else str(r)
    if z.real == 0:
        i = z.imag
        return f"{int(i) if i==int(i) else i}i"
    r = int(z.real) if z.real == int(z.real) else z.real
    i = int(z.imag) if z.imag == int(z.imag) else z.imag
    sign = "+" if z.imag >= 0 else ""
    return f"{r}{sign}{i}i"


def _fmt(v: Any) -> str:
    if isinstance(v, complex):  return _fmt_complex(v)
    if isinstance(v, float):
        return str(int(v)) if v == int(v) else str(v)
    if isinstance(v, bool):     return "true" if v else "false"
    if isinstance(v, (BKVector, BKOperator, BKArray, BKStruct, BKPointer)):
        return repr(v)
    return str(v)


# ══════════════════════════════════════════════════════════════════════════════
#  Dirac visual renderer  (used by the dirac() built-in)
#  Renders via matplotlib mathtext — no external TeX installation required.
# ══════════════════════════════════════════════════════════════════════════════

_DR_FONTSIZE = 16    # pt — base math font size
_DR_DPI      = 150   # render resolution


def _latex_num(z: Any) -> str:
    """Format a scalar value as a LaTeX math string fragment (no $ delimiters)."""
    if isinstance(z, complex):
        z = complex(z)
        def _r(v: float) -> str:
            return str(int(v)) if v == int(v) else f"{v:.4g}"
        if z.imag == 0:
            return _r(z.real)
        if z.real == 0:
            i = z.imag
            s = _r(abs(i))
            return f"{s}i" if i >= 0 else f"-{s}i"
        sign = "+" if z.imag >= 0 else "-"
        return f"{_r(z.real)}{sign}{_r(abs(z.imag))}i"
    if isinstance(z, float):
        return str(int(z)) if z == int(z) else f"{z:.4g}"
    if isinstance(z, bool):
        return r"\mathrm{true}" if z else r"\mathrm{false}"
    return str(z)


def _safe_label(label: str) -> str:
    """Strip characters unsafe for LaTeX mathrm from a label string."""
    return "".join(c for c in label if c.isalnum() or c == "_")


# Each _latex_* function returns (display_str, render_str):
#   display_str  — proper LaTeX using \begin{pmatrix} (for copy-paste)
#   render_str   — matplotlib-compatible using \substack (for rendering)


def _latex_ket(data: list, label: str = "") -> "tuple[str, str]":
    """(display, render) for a ket column vector. label → |label⟩ = pmatrix."""
    elems = [_latex_num(complex(x) if isinstance(x, (int, float, complex)) else x)
             for x in data]
    col_body = r" \\ ".join(elems)
    disp = r"\begin{pmatrix}" + col_body + r"\end{pmatrix}"
    rend = r"\left(\substack{" + col_body + r"}\right)"
    if label:
        lbl    = _safe_label(label)
        prefix = r"|\,\mathrm{" + lbl + r"}\,\rangle = "
        return prefix + disp, prefix + rend
    return disp, rend


def _latex_bra(data: list, label: str = "") -> "tuple[str, str]":
    """(display, render) for a bra row vector. label → ⟨label| = pmatrix."""
    elems = [_latex_num(complex(x) if isinstance(x, (int, float, complex)) else x)
             for x in data]
    disp = r"\begin{pmatrix}" + " & ".join(elems) + r"\end{pmatrix}"
    rend = r"\left(\substack{" + r"\quad".join(elems) + r"}\right)"
    if label:
        lbl    = _safe_label(label)
        prefix = r"\langle\,\mathrm{" + lbl + r"}\,| = "
        return prefix + disp, prefix + rend
    return disp, rend


def _latex_operator(rows_data: list, label: str = "") -> "tuple[str, str]":
    """(display, render) for a matrix operator."""
    disp_rows = [
        " & ".join(
            _latex_num(complex(x) if isinstance(x, (int, float, complex)) else x)
            for x in row
        )
        for row in rows_data
    ]
    rend_rows = [
        r"\quad".join(
            _latex_num(complex(x) if isinstance(x, (int, float, complex)) else x)
            for x in row
        )
        for row in rows_data
    ]
    disp = r"\begin{pmatrix}" + r" \\ ".join(disp_rows) + r"\end{pmatrix}"
    rend = r"\left(\substack{" + r" \\ ".join(rend_rows) + r"}\right)"
    if label:
        lbl    = _safe_label(label)
        prefix = r"\mathrm{" + lbl + r"} = "
        return prefix + disp, prefix + rend
    return disp, rend


def _latex_array(data: list, label: str = "") -> "tuple[str, str]":
    """(display, render) for a generic BKArray column."""
    elems = [
        _latex_num(x) if isinstance(x, (int, float, complex, bool))
        else r"\mathrm{" + str(x) + "}"
        for x in data
    ]
    body = r" \\ ".join(elems)
    disp = r"\begin{bmatrix}" + body + r"\end{bmatrix}"
    rend = r"\left[\substack{" + body + r"}\right]"
    if label:
        lbl    = _safe_label(label)
        prefix = r"\mathrm{" + lbl + r"} = "
        return prefix + disp, prefix + rend
    return disp, rend


def _latex_scalar(value: Any, label: str = "") -> "tuple[str, str]":
    """(display, render) for a plain scalar."""
    if isinstance(value, str):
        safe  = "".join(c for c in value if c.isalnum() or c in " _.,!?")
        v_str = r"\mathrm{" + safe + r"}"
    else:
        v_str = _latex_num(value)
    if label:
        lbl = _safe_label(label)
        s   = r"\mathrm{" + lbl + r"} = " + v_str
        return s, s
    return v_str, v_str


def _render_latex(render_inner: str) -> bytes:
    """
    Render a matplotlib-compatible math string (no $ delimiters) to PNG bytes.
    Uses substack-based notation; does NOT require a system TeX installation.
    """
    import matplotlib
    matplotlib.rcParams.update({
        "mathtext.fontset": "cm",
        "font.size":         _DR_FONTSIZE,
    })

    fig = _plt.figure(figsize=(0.01, 0.01))
    fig.patch.set_facecolor("white")

    text = fig.text(0.5, 0.5, f"${render_inner}$",
                    ha="center", va="center",
                    fontsize=_DR_FONTSIZE,
                    color="black")

    fig.canvas.draw()
    renderer = fig.canvas.get_renderer()
    bb = text.get_window_extent(renderer=renderer)

    pad_px = 30
    W_in = (bb.width  + 2 * pad_px) / _DR_DPI
    H_in = (bb.height + 2 * pad_px) / _DR_DPI
    fig.set_size_inches(max(W_in, 1.0), max(H_in, 0.5))

    buf = _io.BytesIO()
    fig.savefig(buf, format="png", dpi=_DR_DPI,
                bbox_inches="tight", facecolor="white")
    _plt.close(fig)
    buf.seek(0)
    return buf.read()


def render_dirac_value(value: Any, label: str = "") -> "tuple[bytes, str] | None":
    """
    Render any BraKet runtime value as a (png_bytes, display_latex_str) tuple.
      png_bytes        — rendered image using matplotlib-compatible substack notation
      display_latex_str — proper LaTeX string with \\begin{pmatrix} for copy-paste
    Returns None if matplotlib is unavailable or rendering fails.
    """
    if not _MPL_AVAILABLE:
        return None
    if isinstance(value, BKVector):
        disp, rend = (_latex_ket(value.data, label) if value.kind == "ket"
                      else _latex_bra(value.data, label))
    elif isinstance(value, BKOperator):
        disp, rend = _latex_operator(value.rows, label)
    elif isinstance(value, BKArray):
        if value.data:
            disp, rend = _latex_array(value.data, label)
        else:
            disp = rend = r"[\,]"
    else:
        disp, rend = _latex_scalar(value, label)
    try:
        png = _render_latex(rend)
    except Exception:
        return None
    return png, disp


def show_dirac_popup(value: Any, label: str = "", title: str = "dirac()") -> None:
    """
    Open a modal Tkinter Toplevel showing the rendered LaTeX Dirac notation image.
    Displays a copyable LaTeX source string and a Save Image button.
    Blocks execution until the popup is closed (wait_window).
    Does nothing if Tkinter or matplotlib is unavailable.
    """
    if not _TK_AVAILABLE or not _MPL_AVAILABLE:
        return
    result = render_dirac_value(value, label)
    if result is None:
        return
    png, latex_str = result

    if isinstance(value, BKVector):
        type_label = f"{'ket' if value.kind == 'ket' else 'bra'}  \u2014  dim {len(value.data)}"
    elif isinstance(value, BKOperator):
        type_label = f"operator  \u2014  {value.n_rows}\u00d7{value.n_cols}"
    elif isinstance(value, BKArray):
        type_label = f"array  \u2014  len {len(value.data)}"
    else:
        type_label = type(value).__name__

    try:
        WIN_BG = "#0f1117"
        HDR_BG = "#161b22"
        FG     = "#e6edf3"
        FG_DIM = "#8b949e"
        ACCENT = "#58a6ff"
        BTN_BG = "#21262d"

        win = _tk.Toplevel()
        win.title(title)
        win.resizable(True, True)
        win.configure(bg=WIN_BG)
        win.minsize(320, 240)

        # ── Header ────────────────────────────────────────────
        hdr = _tk.Frame(win, bg=HDR_BG, pady=8)
        hdr.pack(fill=_tk.X)
        _tk.Label(hdr, text=f"  {title}", bg=HDR_BG,
                  fg=ACCENT, font=("Segoe UI", 11, "bold")).pack(side=_tk.LEFT)
        _tk.Label(hdr, text=f"{type_label}  ", bg=HDR_BG,
                  fg=FG_DIM, font=("Segoe UI", 10)).pack(side=_tk.RIGHT)
        _tk.Frame(win, bg="#30363d", height=1).pack(fill=_tk.X)

        # ── LaTeX source (read-only, copyable) ────────────────
        lat_frm = _tk.Frame(win, bg=WIN_BG, padx=16, pady=6)
        lat_frm.pack(fill=_tk.X)
        _tk.Label(lat_frm, text="LaTeX:", bg=WIN_BG, fg=FG_DIM,
                  font=("Segoe UI", 9)).pack(anchor="w")
        lat_var   = _tk.StringVar(value=f"${latex_str}$")
        lat_entry = _tk.Entry(lat_frm, textvariable=lat_var,
                              bg="#1c2128", fg="#79c0ff",
                              font=("Consolas", 10), relief=_tk.FLAT, bd=4,
                              readonlybackground="#1c2128",
                              selectbackground=ACCENT)
        lat_entry.pack(fill=_tk.X)
        lat_entry.configure(state="readonly")
        _tk.Frame(win, bg="#30363d", height=1).pack(fill=_tk.X)

        # ── Rendered image ─────────────────────────────────────
        b64     = _base64.b64encode(png).decode("ascii")
        img_frm = _tk.Frame(win, bg="white", padx=24, pady=20)
        img_frm.pack(fill=_tk.BOTH, expand=True, padx=16, pady=12)
        img     = _tk.PhotoImage(data=b64)
        img_lbl = _tk.Label(img_frm, image=img, bg="white")
        img_lbl.image = img   # prevent GC
        img_lbl.pack()

        # ── Buttons ────────────────────────────────────────────
        _tk.Frame(win, bg="#30363d", height=1).pack(fill=_tk.X)
        btn_frm = _tk.Frame(win, bg=WIN_BG, pady=10)
        btn_frm.pack(fill=_tk.X)

        def _save() -> None:
            from tkinter import filedialog as _fd
            path = _fd.asksaveasfilename(
                parent=win,
                defaultextension=".png",
                filetypes=[("PNG image", "*.png"), ("All files", "*.*")],
                title="Save Dirac notation image",
                initialfile="dirac.png",
            )
            if path:
                with open(path, "wb") as _f:
                    _f.write(png)

        _tk.Button(btn_frm, text="Save Image", command=_save,
                   bg=BTN_BG, fg=FG, relief=_tk.FLAT,
                   font=("Segoe UI", 10, "bold"),
                   padx=20, pady=6, cursor="hand2",
                   activebackground=ACCENT,
                   activeforeground=WIN_BG).pack(side=_tk.LEFT, padx=16)
        _tk.Button(btn_frm, text="Close", command=win.destroy,
                   bg=BTN_BG, fg=FG, relief=_tk.FLAT,
                   font=("Segoe UI", 10, "bold"),
                   padx=20, pady=6, cursor="hand2",
                   activebackground="#f85149",
                   activeforeground=WIN_BG).pack(side=_tk.RIGHT, padx=16)

        win.lift()
        win.focus_force()
        win.wait_window()   # modal: pause execution until popup is closed
    except Exception:
        pass   # silently skip if display is unavailable (e.g. headless CI)


# ══════════════════════════════════════════════════════════════════════════════
#  Runtime exceptions
# ══════════════════════════════════════════════════════════════════════════════

class BKRuntimeError(Exception):
    def __init__(self, message: str, line: int = 0):
        super().__init__(message)
        self.line = line

class _ReturnSignal(Exception):
    def __init__(self, value):
        self.value = value


# ══════════════════════════════════════════════════════════════════════════════
#  Interpreter  (IC → runtime)
# ══════════════════════════════════════════════════════════════════════════════

@dataclass
class InterpreterResult:
    output:          list[str]
    error:           Optional[str]
    symbol_table:    dict[str, Any]              # global env after execution (user vars only)
    function_scopes: dict[str, dict[str, Any]]   # fname -> last-seen local frame
    ic_trace:        list[str]                   # formatted IC listing
    exec_log:        list[str]                   # step-by-step execution log
    var_addrs:       dict[str, int]              # variable name -> simulated address (incl. freed temps)
    tmp_table:       dict[str, Any]              # temporaries at end of execution (addresses freed)


class Interpreter:
    """
    Executes a flat IC instruction list.

    Execution model
    ───────────────
    • A single flat environment dict is used for globals.
    • Function calls push a new frame dict onto self._call_stack.
    • PARAM instructions accumulate into self._param_buf.
    • CALL pops self._param_buf, binds params, executes the function's IC.
    • RETURN raises _ReturnSignal which is caught by the call dispatcher.

    Built-in functions
    ──────────────────
    I/O       : print(*args)  input(prompt?)  dirac(v, label?)
    Type conv : int(v)  float(v)  str(v)  bool(v)  complex(r, i?)
    Type query: type(v)
    Math      : abs(v)  sqrt(v)  floor(v)  ceil(v)  round(v, n?)
                pow(a, b)  log(v, base?)  exp(v)
                max(*args)  min(*args)  sum(arr)
    Numeric   : real(v)  imag(v)  conj(v)
    Sequences : len(v)  range(stop)  range(start,stop)  range(start,stop,step)
                append(arr, val)  pop(arr)
    BraKet    : norm(v)  dag(v)  dirac(v, label?)
                normalize(ket)  outer(ket, bra)  expect(op, ket)
                tensor(a, b)  dim(v)  trace(op)  det(op)
                is_unitary(op)  identity(n)  zero_ket(n)
    """

    MAX_STEPS = 100_000   # loop guard

    def __init__(self,
                 instructions: list[ICInstruction],
                 functions:    dict[str, tuple[list[str], list[ICInstruction]]],
                 output_cb:    Callable[[str], None] | None = None,
                 tmp_names:    set | None = None,
                 input_cb:     Callable[[str], str] | None = None):
        self.instructions = instructions
        self.functions    = functions
        self.output_cb    = output_cb or (lambda s: None)
        self.input_cb     = input_cb  # callable(prompt) -> str, or None
        self._tmp_names   = tmp_names or set()  # temp variable names to hide from symbol table
    
        self._interactive = True   # False in _SnapshotInterpreter — suppresses dirac() popup

        self._global_env: dict[str, Any] = {}
        self._call_stack: list[dict[str, Any]] = []
        self._param_buf:  list[Any] = []
        self._output:     list[str] = []
        self._exec_log:   list[str] = []
        self._steps       = 0
        # Simulated address space for pointer support
        self._heap:      dict[int, Any] = {}
        self._var_addrs: dict[str, int] = {}
        self._addr_next: int = 0x1000
    
        # Captures the local frame of each user function after it returns,
        # so the IDE can display per-function symbol scopes.
        self._function_frames: dict[str, dict[str, Any]] = {}

    # ── public entry point ────────────────────────────────────

    def execute(self) -> InterpreterResult:
        ic_trace = [str(ins) for ins in self.instructions]
        error    = None
        try:
            self._run_ic(self.instructions, self._global_env)
        except _ReturnSignal:
            pass
        except BKRuntimeError as e:
            error = f"Runtime error (line {e.line}): {e}"
        except Exception as e:
            error = f"Internal error: {type(e).__name__}: {e}"

        # Collect temporaries before freeing their address slots
        _tmp_set = {k for k in self._global_env if _is_tmp_name(k)}
        _tmp_tbl = {k: v for k, v in self._global_env.items() if k in _tmp_set}
        _all_addrs = dict(self._var_addrs)   # snapshot includes freed temp addresses
        for _k in _tmp_set:
            self._var_addrs.pop(_k, None)    # free temp address slots

        return InterpreterResult(
            output          = self._output,
            error           = error,
            symbol_table    = {k: v for k, v in self._global_env.items()
                               if k not in self._tmp_names and not _is_tmp_name(k)},
            function_scopes = self._function_frames,
            ic_trace        = ic_trace,
            exec_log        = self._exec_log,
            var_addrs       = _all_addrs,
            tmp_table       = _tmp_tbl,
        )

    # ── IC runner ─────────────────────────────────────────────

    def _run_ic(self, ic: list[ICInstruction], env: dict):
        """Execute a list of IC instructions in environment `env`."""
        # Build label → index map
        labels: dict[str, int] = {}
        for i, ins in enumerate(ic):
            if ins.op == LABEL:
                labels[ins.a] = i

        pc = 0
        while pc < len(ic):
            ins = ic[pc]
            self._steps += 1
            if self._steps > self.MAX_STEPS:
                raise BKRuntimeError(
                    f"Execution limit ({self.MAX_STEPS} steps) exceeded — infinite loop?",
                    ins.line)

            self._exec_log.append(f"  [{pc:04d}]  {ins}")

            op = ins.op

            if op == LABEL:
                pc += 1; continue

            elif op == ASSIGN:
                val = self._resolve(ins.b, env)
                
                if isinstance(val, list):
                    name = ins.a if isinstance(ins.a, str) else ""
                    if name.startswith("<") and name.endswith("|"):
                        val = BKVector(val, "bra")          # <name| → bra
                    elif name.startswith("|") and name.endswith(">"):
                        val = BKVector(val, "ket")           # |name> → ket
                    elif val and isinstance(val[0], list):
                        val = BKOperator(val)                # nested list → matrix
                    else:
                        val = BKVector(val, "ket")           # bare list fallback → ket
                env[ins.a] = val

            elif op == COPY:
                env[ins.a] = self._resolve(ins.b, env)

            elif op == BINOP:
                op_str = getattr(ins, '_op2', '+')
                lv = self._resolve(ins.b, env)
                rv = self._resolve(ins.c, env)
                env[ins.a] = self._apply_binop(ins.b, ins.c, lv, rv, op_str, ins.line)

            elif op == UNOP:
                v = self._resolve(ins.c, env)
                env[ins.a] = self._apply_unop(ins.b, v, ins.line)

            elif op == JUMP:
                pc = labels.get(ins.a, pc + 1); continue

            elif op == JUMPF:
                cond = self._resolve(ins.a, env)
                if not self._truthy(cond):
                    pc = labels.get(ins.b, pc + 1); continue

            elif op == JUMPT:
                cond = self._resolve(ins.a, env)
                if self._truthy(cond):
                    pc = labels.get(ins.b, pc + 1); continue

            elif op == PARAM:
                self._param_buf.append(self._resolve(ins.a, env))

            elif op == CALL:
                dest  = ins.a
                fname = ins.b
                argc  = ins.c
                args  = self._param_buf[-argc:] if argc else []
                self._param_buf = self._param_buf[:-argc] if argc else self._param_buf
                result = self._call_function(fname, args, ins.line)
                env[dest] = result

            elif op == RETURN_OP:
                val = self._resolve(ins.a, env) if ins.a is not None else None
                raise _ReturnSignal(val)

            elif op == PRINT_OP:
                val = self._resolve(ins.a, env)
                s   = _fmt(val)
                self._output.append(s)
                self.output_cb(s)

            elif op == ARRAY_NEW:
                env[ins.a] = BKArray([None] * ins.b)

            elif op == ARRAY_SET:
                arr = self._resolve(ins.a, env)
                idx = int(self._resolve(ins.b, env))
                val = self._resolve(ins.c, env)
                if isinstance(arr, BKArray):
                    while len(arr.data) <= idx:
                        arr.data.append(None)
                    arr.data[idx] = val
                elif isinstance(arr, dict):
                    arr[idx] = val
                else:
                    env[ins.a] = BKArray([val])

            elif op == ARRAY_GET:
                arr = self._resolve(ins.b, env)
                idx = int(self._resolve(ins.c, env))
                if isinstance(arr, BKArray):
                    env[ins.a] = arr.data[idx]
                elif isinstance(arr, dict):
                    env[ins.a] = arr.get(idx)
                else:
                    raise BKRuntimeError(f"'{ins.b}' is not an array", ins.line)

            elif op == "VEC_FROM_ARRAY":
                arr = env.get(ins.b)
                if isinstance(arr, BKArray):
                    env[ins.a] = arr.data

            elif op == "MAT_FROM_ROWS":
                arr = env.get(ins.b)
                if isinstance(arr, BKArray):
                    rows = []
                    for row in arr.data:
                        if isinstance(row, list):
                            rows.append([complex(x) for x in row])
                        elif isinstance(row, BKVector):
                            rows.append(row.data)
                        else:
                            rows.append([complex(row)])
                    env[ins.a] = BKOperator(rows)

            elif op == STRUCT_SET:
                obj = self._resolve(ins.a, env)
                if isinstance(obj, BKStruct):
                    obj.fields[ins.b] = self._resolve(ins.c, env)
                elif isinstance(obj, dict):
                    obj[ins.b] = self._resolve(ins.c, env)
                else:
                    # create struct on the fly
                    env[ins.a] = BKStruct({ins.b: self._resolve(ins.c, env)})

            elif op == STRUCT_GET:
                obj = self._resolve(ins.b, env)
                if isinstance(obj, BKStruct):
                    env[ins.a] = obj.fields.get(ins.c)
                elif isinstance(obj, dict):
                    env[ins.a] = obj.get(ins.c)
                else:
                    raise BKRuntimeError(f"'{ins.b}' is not a struct", ins.line)

            pc += 1

    # ── resolve a value (literal or variable name) ────────────

    def _resolve(self, v: Any, env: dict) -> Any:
        if v is None:
            return None
        if isinstance(v, (int, float, complex, bool, str)):
            # Could be a variable name or a string literal
            if isinstance(v, str):
                # Try to look up in current frame, then global
                for frame in reversed(self._call_stack):
                    if v in frame: return frame[v]
                if v in env: return env[v]
                if v in self._global_env: return self._global_env[v]
                # Treat as string literal (already stripped of quotes)
                return v
            return v
        if isinstance(v, list):
            # Nested list → operator matrix. Wrap here since no name context needed.
            if v and isinstance(v[0], list):
                return BKOperator(v)
            # Flat list → raw vector data. Return as-is so the ASSIGN handler
            # can inspect the variable name and choose "ket" vs "bra" correctly.
            return v
        if isinstance(v, dict):
            return BKStruct(v)
        return v

    def _binop_str(self, ins: ICInstruction) -> str:
        """The BINOP instruction stores the operator in field `b` (position 2)."""
        # Layout: BINOP dest left op right
        # In ICInstruction: a=dest, b=left, c=right — BUT we stored op in b during emit
        # We stored as: emit(BINOP, dest, left, op); then patched c=right
        # So the operator is at ins.b... except left is also at b.
        # Let's recover from the raw instruction:
        # ins.a = dest, ins.b = left, ins.c = right  → op was placed between them
        # We need to store op differently.  See _fix below.
        return "+"   # fallback — see _fix_binop_storage below

    def _assign_var_addr(self, name: object) -> int:
        """Auto-assign a simulated memory address to any variable or temporary.

        User variables keep a stable address once assigned.
        Temporaries receive a fresh address each time they are overwritten
        (simulating the release and re-use of a temporary slot).
        """
        if not isinstance(name, str):
            return 0
        if name in self._var_addrs and not _is_tmp_name(name):
            return self._var_addrs[name]   # stable address for user variables
        # Temporaries: release old slot implicitly, allocate a new one
        self._addr_next += 4
        self._var_addrs[name] = self._addr_next
        return self._addr_next

    # ── binary operation evaluation ───────────────────────────

    def _apply_binop(self, left_name, right_name, lv: Any, rv: Any, op: str, line: int) -> Any:
        try:
            # Arithmetic
            if op == "+":  return self._add(lv, rv)
            if op == "-":  return self._sub(lv, rv)
            if op == "*":  return self._mul(lv, rv)
            if op == "/":
                if rv == 0 or rv == 0.0 or rv == complex(0):
                    raise BKRuntimeError("Division by zero", line)
                return self._div(lv, rv)
            if op == "%":  return lv % rv
            if op == "**": return self._pow(lv, rv)
            # Dirac tensor
            if op == "@":  return self._tensor(lv, rv)
            # Comparison
            if op == "==": return lv == rv
            if op == "!=": return lv != rv
            if op == "<":  return lv < rv
            if op == ">":  return lv > rv
            if op == "<=": return lv <= rv
            if op == ">=": return lv >= rv
            # Boolean
            if op == "&&": return bool(lv) and bool(rv)
            if op == "||": return bool(lv) or  bool(rv)
        except BKRuntimeError:
            raise
        except Exception as e:
            raise BKRuntimeError(f"Error in '{op}': {e}", line)
        raise BKRuntimeError(f"Unknown operator '{op}'", line)

    def _apply_unop(self, op: str, v: Any, line: int) -> Any:
        if op == "-":
            if isinstance(v, BKVector):
                return BKVector([-x for x in v.data], v.kind)
            if isinstance(v, BKOperator):
                return BKOperator([[-x for x in row] for row in v.rows])
            return -v
        if op == "!":
            return not self._truthy(v)
        raise BKRuntimeError(f"Unknown unary op '{op}'", line)

    # ── arithmetic helpers ────────────────────────────────────

    def _add(self, a, b):
        if isinstance(a, str) or isinstance(b, str):
            return str(_fmt(a)) + str(_fmt(b))
        if isinstance(a, BKVector) and isinstance(b, BKVector):
            return BKVector([x+y for x,y in zip(a.data, b.data)], a.kind)
        if isinstance(a, BKOperator) and isinstance(b, BKOperator):
            return BKOperator([[a.rows[i][j]+b.rows[i][j]
                                for j in range(a.n_cols)]
                               for i in range(a.n_rows)])
        return a + b

    def _sub(self, a, b):
        if isinstance(a, BKVector) and isinstance(b, BKVector):
            return BKVector([x-y for x,y in zip(a.data, b.data)], a.kind)
        return a - b

    def _mul(self, a, b):
        # scalar * vector / operator
        if isinstance(a, (int, float, complex)) and isinstance(b, BKVector):
            return BKVector([a*x for x in b.data], b.kind)
        if isinstance(a, BKVector) and isinstance(b, (int, float, complex)):
            return BKVector([b*x for x in a.data], a.kind)
        if isinstance(a, (int, float, complex)) and isinstance(b, BKOperator):
            return BKOperator([[a*x for x in row] for row in b.rows])
        if isinstance(a, BKOperator) and isinstance(b, (int, float, complex)):
            return BKOperator([[b*x for x in row] for row in a.rows])
        # bra * ket → inner product (complex scalar)
        if isinstance(a, BKVector) and a.kind == "bra" and isinstance(b, BKVector) and b.kind == "ket":
            return sum(x*y for x,y in zip(a.data, b.data))
        # operator * ket
        if isinstance(a, BKOperator) and isinstance(b, BKVector) and b.kind == "ket":
            result = []
            for row in a.rows:
                result.append(sum(row[j]*b.data[j] for j in range(len(b.data))))
            return BKVector(result, "ket")
        # operator * operator (matrix mult)
        if isinstance(a, BKOperator) and isinstance(b, BKOperator):
            n, m, p = a.n_rows, a.n_cols, b.n_cols
            rows = []
            for i in range(n):
                row = []
                for j in range(p):
                    row.append(sum(a.rows[i][k]*b.rows[k][j] for k in range(m)))
                rows.append(row)
            return BKOperator(rows)
        return a * b

    def _div(self, a, b):
        if isinstance(a, BKVector):
            return BKVector([x/b for x in a.data], a.kind)
        if isinstance(a, BKOperator):
            return BKOperator([[x/b for x in row] for row in a.rows])
        result = a / b
        # return int if it's a whole number and both inputs were int
        if isinstance(a, int) and isinstance(b, int) and result == int(result):
            return int(result)
        return result

    def _pow(self, a, b):
        return a ** b

    def _tensor(self, a, b):
        """Kronecker / tensor product (@)."""
        # scalar @ anything
        if isinstance(a, (int, float, complex)):
            return self._mul(a, b)
        if isinstance(b, (int, float, complex)):
            return self._mul(b, a)

        # ket ⊗ ket → larger ket
        if isinstance(a, BKVector) and isinstance(b, BKVector) and a.kind == "ket" and b.kind == "ket":
            result = [x*y for x in a.data for y in b.data]
            return BKVector(result, "ket")

        # bra ⊗ bra → larger bra
        if isinstance(a, BKVector) and isinstance(b, BKVector) and a.kind == "bra" and b.kind == "bra":
            result = [x*y for x in a.data for y in b.data]
            return BKVector(result, "bra")

        # ket ⊗ bra → outer product (operator)
        if isinstance(a, BKVector) and a.kind == "ket" and isinstance(b, BKVector) and b.kind == "bra":
            rows = [[x*y for y in b.data] for x in a.data]
            return BKOperator(rows)

        # bra ⊗ ket → full contraction (scalar)
        if isinstance(a, BKVector) and a.kind == "bra" and isinstance(b, BKVector) and b.kind == "ket":
            return sum(x*y for x,y in zip(a.data, b.data))

        # operator ⊗ operator (Kronecker product)
        if isinstance(a, BKOperator) and isinstance(b, BKOperator):
            rows = []
            for ar in a.rows:
                block_rows = [[] for _ in range(b.n_rows)]
                for ae in ar:
                    for r, br in enumerate(b.rows):
                        block_rows[r].extend([ae*be for be in br])
                rows.extend(block_rows)
            return BKOperator(rows)

        # operator ⊗ ket/bra
        if isinstance(a, BKOperator) and isinstance(b, BKVector):
            return self._mul(a, b)

        return self._mul(a, b)

    # ── truthiness ────────────────────────────────────────────

    def _truthy(self, v: Any) -> bool:
        if v is None:    return False
        if isinstance(v, bool):    return v
        if isinstance(v, (int, float)): return v != 0
        if isinstance(v, complex): return v != complex(0)
        if isinstance(v, str):     return len(v) > 0
        if isinstance(v, BKArray): return len(v.data) > 0
        return True

    # ── function calls ────────────────────────────────────────

    def _call_function(self, name: str, args: list, line: int) -> Any:
        # Built-ins
        builtin = self._try_builtin(name, args, line)
        if builtin is not self._SENTINEL:
            return builtin

        if name not in self.functions:
            raise BKRuntimeError(f"Undefined function '{name}'", line)

        param_names, body_ic, default_ics = self.functions[name]
        frame: dict[str, Any] = {}

        # Build a lookup from param name → (mini_ic, result_addr) for defaults
        defaults_map = {pname: (mic, addr) for pname, mic, addr in default_ics}

        # Bind positional args; fall back to default value or None
        for i, pname in enumerate(param_names):
            if i < len(args):
                frame[pname] = args[i]
            elif pname in defaults_map:
                mini_ic, result_addr = defaults_map[pname]
                tmp_env: dict[str, Any] = {}
                if mini_ic:
                    self._run_ic(mini_ic, tmp_env)
                frame[pname] = self._resolve(result_addr, tmp_env)
            else:
                frame[pname] = None

        self._call_stack.append(frame)
        result = None
        try:
            self._run_ic(body_ic, frame)
        except _ReturnSignal as r:
            result = r.value
        finally:
            self._call_stack.pop()
            # Save a snapshot of this function's local frame (user vars only)
            # so the IDE can show per-function symbols in the symbol table.
            self._function_frames[name] = {
                k: v for k, v in frame.items()
                if k not in self._tmp_names and not _is_tmp_name(k)
            }
            

        return result

    _SENTINEL = object()

    def _try_builtin(self, name: str, args: list, line: int) -> Any:

        # ── I/O ──────────────────────────────────────────────────────────────

        if name == "print":
            parts = [_fmt(a) for a in args]
            s = " ".join(parts)
            self._output.append(s)
            self.output_cb(s)
            return None

        if name == "input":
            prompt = _fmt(args[0]) if args else ""
            if self.input_cb is not None:
                # IDE-supplied callback: it handles all display (prompt + echo).
                # Do NOT append to _output here — the IDE already shows the value.
                val = self.input_cb(prompt) or ""
            elif _TK_AVAILABLE:
                val = _tk_simpledialog.askstring(
                    "Input", prompt or "Enter a value:") or ""
                self._output.append(f"{prompt}{val}")
                self.output_cb(f"{prompt}{val}")
            else:
                val = ""   # headless fallback
            return val

        # ── Type conversion ───────────────────────────────────────────────────

        if name == "int":
            v = args[0] if args else 0
            if isinstance(v, str):
                try:    return int(v.strip())
                except: raise BKRuntimeError(f"int(): cannot convert \'{v}\'", line)
            return int(v)

        if name == "float":
            v = args[0] if args else 0.0
            if isinstance(v, str):
                try:    return float(v.strip())
                except: raise BKRuntimeError(f"float(): cannot convert \'{v}\'", line)
            return float(v)

        if name == "str":
            return _fmt(args[0]) if args else ""

        if name == "bool":
            return self._truthy(args[0]) if args else False

        if name == "complex":
            r = args[0] if len(args) >= 1 else 0
            i = args[1] if len(args) >= 2 else 0
            return complex(r, i)

        # ── Type query ────────────────────────────────────────────────────────

        if name == "type":
            v = args[0] if args else None
            if isinstance(v, bool):       return "bool"
            if isinstance(v, int):        return "int"
            if isinstance(v, float):      return "float"
            if isinstance(v, complex):    return "complex"
            if isinstance(v, str):        return "string"
            if isinstance(v, BKVector):   return v.kind   # "ket" or "bra"
            if isinstance(v, BKOperator): return "op"
            if isinstance(v, BKArray):    return "array"
            if isinstance(v, BKStruct):   return "struct"
            if v is None:                 return "null"
            return "unknown"

        # ── Math ──────────────────────────────────────────────────────────────

        if name == "abs":
            v = args[0] if args else 0
            return abs(v)

        if name == "sqrt":
            v = args[0] if args else 0
            return cmath.sqrt(v) if isinstance(v, complex) else math.sqrt(abs(v))

        if name == "floor":
            v = args[0] if args else 0
            return int(math.floor(v.real if isinstance(v, complex) else v))

        if name == "ceil":
            v = args[0] if args else 0
            return int(math.ceil(v.real if isinstance(v, complex) else v))

        if name == "round":
            v = args[0] if args else 0
            n = int(args[1]) if len(args) >= 2 else 0
            return round(v, n)

        if name == "pow":
            if len(args) < 2:
                raise BKRuntimeError("pow() requires 2 arguments", line)
            return args[0] ** args[1]

        if name == "log":
            v = args[0] if args else 1
            if len(args) >= 2:
                base = args[1]
                return (cmath.log(v) / cmath.log(base) if isinstance(v, complex)
                        else math.log(v, base))
            return cmath.log(v) if isinstance(v, complex) else math.log(v)

        if name == "exp":
            v = args[0] if args else 0
            return cmath.exp(v) if isinstance(v, complex) else math.exp(v)

        if name == "max":
            if not args:
                raise BKRuntimeError("max() requires at least one argument", line)
            items = (args[0].data
                     if len(args) == 1 and isinstance(args[0], BKArray)
                     else args)
            return max(items)

        if name == "min":
            if not args:
                raise BKRuntimeError("min() requires at least one argument", line)
            items = (args[0].data
                     if len(args) == 1 and isinstance(args[0], BKArray)
                     else args)
            return min(items)

        if name == "sum":
            v = args[0] if args else None
            if isinstance(v, BKArray):
                return sum(v.data)
            raise BKRuntimeError("sum() requires an array", line)

        # ── Complex number components ─────────────────────────────────────────

        if name == "real":
            v = args[0] if args else 0
            return v.real if isinstance(v, complex) else float(v)

        if name == "imag":
            v = args[0] if args else 0
            return v.imag if isinstance(v, complex) else 0.0

        if name == "conj":
            v = args[0] if args else 0
            if isinstance(v, complex):
                return v.conjugate()
            if isinstance(v, BKVector):
                return BKVector([x.conjugate() for x in v.data], v.kind)
            if isinstance(v, BKOperator):
                return BKOperator([[x.conjugate() for x in row] for row in v.rows])
            return v

        # ── Sequences ─────────────────────────────────────────────────────────

        if name == "len":
            v = args[0] if args else None
            if isinstance(v, BKArray):  return len(v.data)
            if isinstance(v, str):      return len(v)
            if isinstance(v, BKVector): return len(v.data)
            raise BKRuntimeError("len() requires an array, string, or vector", line)

        if name == "range":
            if len(args) == 1:
                return BKArray(list(range(int(args[0]))))
            if len(args) == 2:
                return BKArray(list(range(int(args[0]), int(args[1]))))
            if len(args) >= 3:
                return BKArray(list(range(int(args[0]), int(args[1]), int(args[2]))))
            return BKArray([])

        if name == "append":
            if len(args) < 2:
                raise BKRuntimeError("append() requires array and value", line)
            arr, val = args[0], args[1]
            if isinstance(arr, BKArray):
                arr.data.append(val)
                return None
            raise BKRuntimeError("append() first argument must be an array", line)

        if name == "pop":
            v = args[0] if args else None
            if isinstance(v, BKArray):
                if not v.data:
                    raise BKRuntimeError("pop() on empty array", line)
                return v.data.pop()
            raise BKRuntimeError("pop() requires an array", line)

        # ── BraKet ────────────────────────────────────────────────────────────

        if name == "norm":
            v = args[0] if args else 0
            if isinstance(v, BKVector):
                return math.sqrt(sum(abs(x)**2 for x in v.data))
            if isinstance(v, complex):
                return abs(v)
            return abs(v)

        if name == "dag":
            # Hermitian conjugate (†): flip ket<->bra and conjugate each element;
            # for operators: conjugate transpose
            v = args[0] if args else None
            if isinstance(v, BKVector):
                new_kind = "bra" if v.kind == "ket" else "ket"
                return BKVector([x.conjugate() for x in v.data], new_kind)
            if isinstance(v, BKOperator):
                rows = [[v.rows[j][i].conjugate()
                         for j in range(v.n_rows)]
                        for i in range(v.n_cols)]
                return BKOperator(rows)
            return v

        if name == "dirac":
            # Render value as a visual notation in a popup window.
            # dirac(value)          — show vector/matrix/scalar
            # dirac(value, "label") — show |label⟩ = vector notation
            # Suppressed in _SnapshotInterpreter (step-debugger replay).
            if not self._interactive:
                return None
            v         = args[0] if args else None
            label_arg = str(args[1]) if len(args) >= 2 else ""
            if not _MPL_AVAILABLE:
                raise BKRuntimeError(
                    "dirac() requires matplotlib — run: pip install matplotlib",
                    line)
            show_dirac_popup(v, label=label_arg, title="dirac()")
            return None

        if name == "trace":
            # Sum of diagonal elements of a square operator.
            v = args[0] if args else None
            if not isinstance(v, BKOperator):
                raise BKRuntimeError("trace() requires an operator", line)
            if v.n_rows != v.n_cols:
                raise BKRuntimeError(
                    f"trace() requires a square operator, got {v.n_rows}×{v.n_cols}",
                    line)
            return sum(v.rows[i][i] for i in range(v.n_rows))

        if name == "det":
            # Determinant of a square operator via cofactor expansion.
            v = args[0] if args else None
            if not isinstance(v, BKOperator):
                raise BKRuntimeError("det() requires an operator", line)
            n = v.n_rows
            if n != v.n_cols:
                raise BKRuntimeError(
                    f"det() requires a square operator, got {n}×{v.n_cols}", line)
            def _det(m):
                if len(m) == 1:
                    return m[0][0]
                if len(m) == 2:
                    return m[0][0]*m[1][1] - m[0][1]*m[1][0]
                total = complex(0)
                for c in range(len(m)):
                    minor = [row[:c] + row[c+1:] for row in m[1:]]
                    sign  = (-1) ** c
                    total += sign * m[0][c] * _det(minor)
                return total
            return _det(v.rows)

        if name == "normalize":
            # Return v scaled so that norm(v) == 1.
            v = args[0] if args else None
            if isinstance(v, BKVector):
                n = math.sqrt(sum(abs(x)**2 for x in v.data))
                if n == 0:
                    raise BKRuntimeError("normalize() on zero vector", line)
                return BKVector([x / n for x in v.data], v.kind)
            raise BKRuntimeError("normalize() requires a ket or bra", line)

        if name == "outer":
            # Outer product |ket><bra| → BKOperator.
            if len(args) < 2:
                raise BKRuntimeError("outer() requires two arguments: ket and bra",
                                     line)
            ket, bra = args[0], args[1]
            if not (isinstance(ket, BKVector) and ket.kind == "ket"):
                raise BKRuntimeError("outer() first argument must be a ket", line)
            if not (isinstance(bra, BKVector) and bra.kind == "bra"):
                raise BKRuntimeError("outer() second argument must be a bra", line)
            rows = [[x * y for y in bra.data] for x in ket.data]
            return BKOperator(rows)

        if name == "expect":
            # Expectation value <ket|op|ket> → complex scalar.
            if len(args) < 2:
                raise BKRuntimeError(
                    "expect() requires two arguments: operator and ket", line)
            op, ket = args[0], args[1]
            if not isinstance(op, BKOperator):
                raise BKRuntimeError("expect() first argument must be an operator",
                                     line)
            if not (isinstance(ket, BKVector) and ket.kind == "ket"):
                raise BKRuntimeError("expect() second argument must be a ket", line)
            # op|ket>
            if op.n_cols != len(ket.data):
                raise BKRuntimeError(
                    f"expect(): operator ({op.n_rows}×{op.n_cols}) dimension "
                    f"mismatch with ket (dim {len(ket.data)})", line)
            op_ket = [sum(op.rows[r][c] * ket.data[c]
                          for c in range(op.n_cols))
                      for r in range(op.n_rows)]
            # <ket| · (op|ket>)  — bra is conjugate of ket
            return sum(ket.data[i].conjugate() * op_ket[i]
                       for i in range(len(ket.data)))

        if name == "tensor":
            # Kronecker / tensor product — callable form of the @ operator.
            if len(args) < 2:
                raise BKRuntimeError(
                    "tensor() requires two arguments", line)
            return self._tensor(args[0], args[1])

        if name == "dim":
            # Dimension of a ket/bra (int) or operator (tuple of ints).
            v = args[0] if args else None
            if isinstance(v, BKVector):
                return len(v.data)
            if isinstance(v, BKOperator):
                return BKArray([v.n_rows, v.n_cols])
            raise BKRuntimeError(
                "dim() requires a ket, bra, or operator", line)

        if name == "is_unitary":
            # Return true if op† × op ≈ identity (within tolerance).
            v = args[0] if args else None
            if not isinstance(v, BKOperator):
                raise BKRuntimeError("is_unitary() requires an operator", line)
            tol = 1e-9
            n   = v.n_rows
            if n != v.n_cols:
                return False
            # dag(v)
            dag_rows = [[v.rows[j][i].conjugate()
                         for j in range(n)] for i in range(n)]
            # dag @ v
            for r in range(n):
                for c in range(n):
                    val = sum(dag_rows[r][k] * v.rows[k][c] for k in range(n))
                    expected = complex(1) if r == c else complex(0)
                    if abs(val - expected) > tol:
                        return False
            return True

        if name == "identity":
            # Return an n×n identity operator.
            if not args:
                raise BKRuntimeError("identity() requires a size argument", line)
            n = int(args[0])
            if n <= 0:
                raise BKRuntimeError("identity() size must be positive", line)
            rows = [[complex(1) if r == c else complex(0)
                     for c in range(n)] for r in range(n)]
            return BKOperator(rows)

        if name == "zero_ket":
            # Return an n-dimensional zero ket.
            if not args:
                raise BKRuntimeError("zero_ket() requires a size argument", line)
            n = int(args[0])
            if n <= 0:
                raise BKRuntimeError("zero_ket() size must be positive", line)
            return BKVector([complex(0)] * n, "ket")

        return self._SENTINEL


# ══════════════════════════════════════════════════════════════════════════════
#  BINOP operator storage fix
#  The ICGenerator stores BINOP as: emit(BINOP, dest, left, op)
#  then patches the last instruction's .c = right.
#  So the layout is:  a=dest  b=left  c=right  — and op is stored separately.
#  We need to track op.  We fix this by storing op in a 4th slot.
# ══════════════════════════════════════════════════════════════════════════════

# Monkey-patch ICInstruction to add an `op2` field for BINOP operator string,
# and override _run_ic to use it.

_orig_emit = ICGenerator._emit

def _patched_emit(self, op, a=None, b=None, c=None, line=0, _op2=None):
    ins = ICInstruction(op, a, b, c, line)
    ins._op2 = _op2
    self._current_ic.append(ins)

ICGenerator._emit = _patched_emit


def _patched_emit_binop(gen, dest, left, op_str, line=0):
    """Emit a BINOP and return so caller can patch .c = right."""
    ins = ICInstruction(BINOP, dest, left, None, line)
    ins._op2 = op_str
    gen._current_ic.append(ins)

# Override _gen_num_expr, _gen_num_term, etc. to use _op2 properly
# We do this by overriding _apply_binop dispatch in Interpreter to read ins._op2

_orig_run_ic = Interpreter._run_ic

def _patched_run_ic(self, ic, env):
    """Extended run loop that reads _op2 for BINOP instructions."""
    labels: dict[str, int] = {}
    for i, ins in enumerate(ic):
        if ins.op == LABEL:
            labels[ins.a] = i

    pc = 0
    while pc < len(ic):
        ins = ic[pc]
        self._steps += 1
        if self._steps > self.MAX_STEPS:
            raise BKRuntimeError(
                f"Execution limit ({self.MAX_STEPS} steps) exceeded — infinite loop?",
                ins.line)

        self._exec_log.append(f"  [{pc:04d}]  {ins}")
        op = ins.op

        if op == LABEL:
            pc += 1; continue

        elif op == ASSIGN:
            val = self._resolve(ins.b, env)
            if isinstance(val, list):
                name = ins.a if isinstance(ins.a, str) else ""
                if name.startswith("<") and name.endswith("|"):
                    val = BKVector(val, "bra")
                elif name.startswith("|") and name.endswith(">"):
                    val = BKVector(val, "ket")
                elif val and isinstance(val[0], list):
                    val = BKOperator(val)
                else:
                    val = BKVector(val, "ket")
            elif isinstance(val, BKVector):
                name = ins.a if isinstance(ins.a, str) else ""
                if name.startswith("<") and name.endswith("|") and val.kind != "bra":
                    val = BKVector(val.data, "bra")
                elif name.startswith("|") and name.endswith(">") and val.kind != "ket":
                    val = BKVector(val.data, "ket")
            env[ins.a] = val
            self._assign_var_addr(ins.a)

        elif op == COPY:
            env[ins.a] = self._resolve(ins.b, env)
            self._assign_var_addr(ins.a)

        elif op == BINOP:
            op_str = getattr(ins, '_op2', '+')
            lv = self._resolve(ins.b, env)
            rv = self._resolve(ins.c, env)
            env[ins.a] = self._apply_binop(ins.b, ins.c, lv, rv, op_str, ins.line)
            self._assign_var_addr(ins.a)

        elif op == UNOP:
            v = self._resolve(ins.c, env)
            env[ins.a] = self._apply_unop(ins.b, v, ins.line)
            self._assign_var_addr(ins.a)

        elif op == JUMP:
            pc = labels.get(ins.a, pc + 1); continue

        elif op == JUMPF:
            cond = self._resolve(ins.a, env)
            if not self._truthy(cond):
                pc = labels.get(ins.b, pc + 1); continue

        elif op == JUMPT:
            cond = self._resolve(ins.a, env)
            if self._truthy(cond):
                pc = labels.get(ins.b, pc + 1); continue

        elif op == PARAM:
            self._param_buf.append(self._resolve(ins.a, env))

        elif op == CALL:
            dest  = ins.a
            fname = ins.b
            argc  = ins.c or 0
            args  = self._param_buf[-argc:] if argc else []
            self._param_buf = self._param_buf[:-argc] if argc else self._param_buf
            result = self._call_function(fname, args, ins.line)
            env[dest] = result
            self._assign_var_addr(dest)

        elif op == RETURN_OP:
            val = self._resolve(ins.a, env) if ins.a is not None else None
            raise _ReturnSignal(val)

        elif op == PRINT_OP:
            val = self._resolve(ins.a, env)
            s   = _fmt(val)
            self._output.append(s)
            self.output_cb(s)

        elif op == ARRAY_NEW:
            env[ins.a] = BKArray([None] * (ins.b or 0))
            self._assign_var_addr(ins.a)

        elif op == ARRAY_SET:
            arr = self._resolve(ins.a, env)
            idx = self._resolve(ins.b, env)
            val = self._resolve(ins.c, env)
            if isinstance(idx, float): idx = int(idx)
            if isinstance(arr, BKArray):
                while len(arr.data) <= idx:
                    arr.data.append(None)
                arr.data[idx] = val
            elif isinstance(arr, dict):
                arr[idx] = val

        elif op == ARRAY_GET:
            arr = self._resolve(ins.b, env)
            idx = self._resolve(ins.c, env)
            if isinstance(idx, float): idx = int(idx)
            if isinstance(arr, BKArray):
                env[ins.a] = arr.data[idx] if 0 <= idx < len(arr.data) else None
            elif isinstance(arr, dict):
                env[ins.a] = arr.get(idx)
            else:
                raise BKRuntimeError(f"'{ins.b}' is not an array", ins.line)
            self._assign_var_addr(ins.a)

        elif op == "VEC_FROM_ARRAY":
            arr = env.get(ins.b)
            if isinstance(arr, BKArray):
                env[ins.a] = arr.data
            self._assign_var_addr(ins.a)

        elif op == "MAT_FROM_ROWS":
            arr = env.get(ins.b)
            if isinstance(arr, BKArray):
                rows = []
                for row in arr.data:
                    if isinstance(row, list):
                        rows.append([complex(x) for x in row])
                    elif isinstance(row, BKVector):
                        rows.append(row.data)
                    else:
                        rows.append([complex(row)])
                env[ins.a] = BKOperator(rows)
            self._assign_var_addr(ins.a)

        elif op == STRUCT_SET:
            obj = self._resolve(ins.a, env)
            val = self._resolve(ins.c, env)
            if isinstance(obj, BKStruct):
                obj.fields[ins.b] = val
            elif isinstance(obj, dict):
                obj[ins.b] = val
            else:
                s = BKStruct({ins.b: val})
                env[ins.a] = s

        elif op == STRUCT_GET:
            obj = self._resolve(ins.b, env)
            if isinstance(obj, BKStruct):
                env[ins.a] = obj.fields.get(ins.c)
            elif isinstance(obj, dict):
                env[ins.a] = obj.get(ins.c)
            else:
                raise BKRuntimeError(f"'{ins.b}' is not a struct", ins.line)
            self._assign_var_addr(ins.a)

        elif op == ADDR_OF:
            var_name = ins.b
            if var_name not in self._var_addrs:
                self._addr_next += 4
                self._var_addrs[var_name] = self._addr_next
            addr = self._var_addrs[var_name]
            self._heap[addr] = self._resolve(var_name, env)
            env[ins.a] = BKPointer(var_name, addr)
            self._assign_var_addr(ins.a)

        elif op == DEREF:
            ptr = self._resolve(ins.b, env)
            if isinstance(ptr, BKPointer):
                val = self._resolve(ptr.var_name, env)
                # _resolve returns the name string when variable not found; fall back to heap
                if isinstance(val, str) and val == ptr.var_name:
                    val = self._heap.get(ptr.address)
                env[ins.a] = val
            elif isinstance(ptr, int):
                env[ins.a] = self._heap.get(ptr)
            else:
                raise BKRuntimeError(f"Cannot dereference '{ins.b}'", ins.line)

        elif op == DEREF_ASSIGN:
            ptr = self._resolve(ins.a, env)
            val = self._resolve(ins.b, env)
            if not isinstance(ptr, BKPointer):
                raise BKRuntimeError(f"'{ins.a}' is not a pointer", ins.line)
            # Update the pointed-to variable in whichever scope owns it
            for frame in reversed(self._call_stack):
                if ptr.var_name in frame:
                    frame[ptr.var_name] = val
                    break
            else:
                if ptr.var_name in env:
                    env[ptr.var_name] = val
                else:
                    self._global_env[ptr.var_name] = val
            self._heap[ptr.address] = val

        pc += 1

Interpreter._run_ic = _patched_run_ic


# ── Dead Temp Assignment Elimination ─────────────────────────

# Ops that are pure (no side effects) and safe to remove when their dest temp is unused.
_DTAE_ELIMINABLE = {ASSIGN, BINOP, UNOP, COPY, STRUCT_GET, ARRAY_GET, ADDR_OF, DEREF}

def _dtae_sources(ins) -> set:
    """Return the set of temp names read as sources by *ins*."""
    op = ins.op
    if op == ASSIGN:         cands = [ins.b]
    elif op == BINOP:        cands = [ins.b, ins.c]
    elif op == UNOP:         cands = [ins.c]           # ins.b is operator string
    elif op == COPY:         cands = [ins.b]
    elif op in (JUMPF, JUMPT): cands = [ins.a]
    elif op == PARAM:        cands = [ins.a]
    elif op == RETURN_OP:    cands = [ins.a]
    elif op == PRINT_OP:     cands = [ins.a]
    elif op == ARRAY_SET:    cands = [ins.a, ins.b, ins.c]
    elif op == ARRAY_GET:    cands = [ins.b, ins.c]
    elif op == STRUCT_SET:   cands = [ins.a, ins.c]
    elif op == STRUCT_GET:   cands = [ins.b]
    elif op == DEREF:        cands = [ins.b]
    elif op == DEREF_ASSIGN: cands = [ins.a, ins.b]
    else:                    cands = []
    return {v for v in cands if isinstance(v, str)}


def _elim_dead_temps(ic: list) -> list:
    """
    Dead Temp Assignment Elimination pass.

    Iteratively removes instructions whose destination is a temporary
    variable (t0, t1, ...) that is never read by any other instruction.
    Only pure ops (ASSIGN, BINOP, UNOP, COPY, STRUCT_GET, ARRAY_GET,
    ADDR_OF, DEREF) are eligible — CALL and ARRAY_NEW are kept because
    they may have side effects.

    Iterates until convergence so that chains of dead temps are fully pruned.
    """
    changed = True
    while changed:
        changed = False
        used: set = set()
        for ins in ic:
            used |= _dtae_sources(ins)
        new_ic = []
        for ins in ic:
            if (ins.op in _DTAE_ELIMINABLE
                    and isinstance(ins.a, str)
                    and ins.a not in used):
                changed = True
                continue
            new_ic.append(ins)
        ic = new_ic
    return ic


# ── Dead Assignment Elimination ────────────────────────────────

def _elim_dead_assignments(ic: list) -> list:
    """
    Dead Assignment Elimination pass.

    1. Algebraic identity simplification — reduces BINOP instructions whose
       result is trivially determined even when one operand is unknown:
         b * 0  →  0     0 * b  →  0
         b + 0  →  b     0 + b  →  b
         b - 0  →  b
         b * 1  →  b     1 * b  →  b
         b ** 0 →  1     b ** 1 →  b

    2. Self-assignment elimination — removes instructions that assign a
       variable the value it already holds:
         ASSIGN  a  a  →  removed
         COPY    a  a  →  removed

    Iterates until convergence so cascading simplifications fully resolve.
    For example:
        BINOP t0 b 0  →  ASSIGN t0 0   (zero-multiplication rule)
    Then after constant propagation substitutes t0→0 into the next BINOP:
        BINOP t1 x 0  →  ASSIGN t1 x   (additive identity rule)
    Then after _prop_temp_copies substitutes t1→x:
        COPY x x       →  removed       (self-assignment rule)
    """
    def _is_zero(v):
        return isinstance(v, (int, float)) and not isinstance(v, bool) and v == 0

    def _is_one(v):
        return isinstance(v, (int, float)) and not isinstance(v, bool) and v == 1

    changed = True
    while changed:
        changed = False
        new_ic = []
        for ins in ic:
            if ins.op == BINOP:
                left   = ins.b
                right  = ins.c
                op_str = getattr(ins, '_op2', '+')
                simplified = None

                if op_str == '*':
                    if _is_zero(left) or _is_zero(right):   simplified = 0
                    elif _is_one(right):                     simplified = left
                    elif _is_one(left):                      simplified = right
                elif op_str == '+':
                    if _is_zero(right):                      simplified = left
                    elif _is_zero(left):                     simplified = right
                elif op_str == '-':
                    if _is_zero(right):                      simplified = left
                elif op_str == '**':
                    if _is_zero(right):                      simplified = 1
                    elif _is_one(right):                     simplified = left

                if simplified is not None:
                    new_ins = ICInstruction(ASSIGN, ins.a, simplified, None, ins.line)
                    new_ins._op2 = None
                    new_ic.append(new_ins)
                    changed = True
                else:
                    new_ic.append(ins)

            elif ins.op in (ASSIGN, COPY) and ins.a == ins.b:
                # a = a  or  COPY a a — value unchanged, discard
                changed = True

            else:
                new_ic.append(ins)

        ic = new_ic

    return ic


# ── Temporary Copy Propagation ─────────────────────────────────

def _prop_temp_copies(ic: list) -> list:
    """
    Temporary Copy Propagation pass.

    For every single-definition temporary t that is assigned a plain user
    variable name v (ASSIGN t v), substitutes every read of t with v.
    This is the complement of constant propagation: where that pass
    propagates literals, this pass propagates variable names.

    This enables _elim_dead_assignments to detect self-assignments that
    arise from algebraic simplification chains.  Example:
        ASSIGN  t1  x          # produced when  x + 0  →  x
        COPY    x   t1         # becomes COPY x x → self-assignment → removed
    After removal, DTAE prunes the now-dead  ASSIGN t1 x.
    """
    def _sub(v, cmap):
        return cmap[v] if isinstance(v, str) and v in cmap else v

    changed = True
    while changed:
        changed = False

        # Single-def temps whose value is a non-temp user variable name
        def_count: dict = {}
        _def_ops = {ASSIGN, BINOP, UNOP, COPY, ARRAY_GET, STRUCT_GET,
                    ARRAY_NEW, CALL, ADDR_OF, DEREF}
        for ins in ic:
            if ins.op in _def_ops and isinstance(ins.a, str):
                def_count[ins.a] = def_count.get(ins.a, 0) + 1

        copy_map: dict = {}
        for ins in ic:
            if (ins.op == ASSIGN
                    and _is_tmp_name(ins.a)
                    and def_count.get(ins.a, 0) == 1
                    and isinstance(ins.b, str)
                    and not _is_tmp_name(ins.b)):
                copy_map[ins.a] = ins.b

        if not copy_map:
            break

        new_ic = []
        for ins in ic:
            if ins.op == BINOP:
                b = _sub(ins.b, copy_map)
                c = _sub(ins.c, copy_map)
                if b is not ins.b or c is not ins.c:
                    new_ins = ICInstruction(BINOP, ins.a, b, c, ins.line)
                    new_ins._op2 = getattr(ins, '_op2', '+')
                    new_ic.append(new_ins)
                    changed = True
                else:
                    new_ic.append(ins)
            elif ins.op == UNOP:
                c = _sub(ins.c, copy_map)
                if c is not ins.c:
                    new_ins = ICInstruction(UNOP, ins.a, ins.b, c, ins.line)
                    new_ins._op2 = None
                    new_ic.append(new_ins)
                    changed = True
                else:
                    new_ic.append(ins)
            elif ins.op in (ASSIGN, COPY):
                b = _sub(ins.b, copy_map)
                if b is not ins.b:
                    new_ins = ICInstruction(ins.op, ins.a, b, None, ins.line)
                    new_ins._op2 = None
                    new_ic.append(new_ins)
                    changed = True
                else:
                    new_ic.append(ins)
            elif ins.op in (JUMPF, JUMPT):
                a = _sub(ins.a, copy_map)
                if a is not ins.a:
                    new_ins = ICInstruction(ins.op, a, ins.b, ins.c, ins.line)
                    new_ins._op2 = getattr(ins, '_op2', None)
                    new_ic.append(new_ins)
                    changed = True
                else:
                    new_ic.append(ins)
            elif ins.op in (PARAM, RETURN_OP, PRINT_OP):
                a = _sub(ins.a, copy_map)
                if a is not ins.a:
                    new_ins = ICInstruction(ins.op, a, ins.b, ins.c, ins.line)
                    new_ins._op2 = getattr(ins, '_op2', None)
                    new_ic.append(new_ins)
                    changed = True
                else:
                    new_ic.append(ins)
            else:
                new_ic.append(ins)

        ic = new_ic

    return ic


# ── Constant folding helper ───────────────────────────────────

def _const_fold(left, op, right):
    """Try to evaluate a binary operation at compile time.
    Returns (result, True) when both operands are numeric literals,
    (None, False) otherwise.  Division/modulo by zero is left for
    the runtime so the error is reported with a proper source line."""
    if not (isinstance(left, (int, float, complex))
            and isinstance(right, (int, float, complex))):
        return None, False
    try:
        if op == "+":  return left + right, True
        if op == "-":  return left - right, True
        if op == "*":  return left * right, True
        if op == "/":
            if right == 0: return None, False
            return left / right, True
        if op == "%":
            if right == 0: return None, False
            return left % right, True
        if op == "**": return left ** right, True
        if op == "==": return left == right, True
        if op == "!=": return left != right, True
        if op == "<":  return left <  right, True
        if op == ">":  return left >  right, True
        if op == "<=": return left <= right, True
        if op == ">=": return left >= right, True
    except Exception:
        pass
    return None, False


# ── Constant Propagation ──────────────────────────────────────

def _const_propagate(ic: list) -> list:
    """
    Constant Propagation pass.

    Repeatedly finds variables that are assigned exactly once with a
    compile-time numeric/bool literal, substitutes that value into every
    instruction that reads the variable, and folds any BINOP/UNOP whose
    operands are now all literals.  Iterates until no more substitutions
    are possible; DTAE is run afterwards to remove the now-dead assignments.

    Example:
        y = 3        # from constant-folded (1 + 2)
        t0 = y * 4   # BINOP → substituted → t0 = 3 * 4 → folded → t0 = 12
        z  = t0      # ASSIGN → substituted → z = 12
    After DTAE: only  z = 12  survives.
    """
    def _is_num_lit(v):
        return isinstance(v, bool) or isinstance(v, (int, float, complex))

    def _sub(v, cmap):
        return cmap[v] if (isinstance(v, str) and v in cmap) else v

    changed = True
    while changed:
        changed = False

        # Count how many instructions define each name (as dest = ins.a)
        def_count: dict = {}
        _def_ops = {ASSIGN, BINOP, UNOP, COPY, ARRAY_GET, STRUCT_GET,
                    ARRAY_NEW, CALL, ADDR_OF, DEREF}
        for ins in ic:
            if ins.op in _def_ops and isinstance(ins.a, str):
                def_count[ins.a] = def_count.get(ins.a, 0) + 1

        # Build constant map: only single-def ASSIGN whose value is a numeric literal
        const_map: dict = {}
        for ins in ic:
            if (ins.op == ASSIGN
                    and isinstance(ins.a, str)
                    and def_count.get(ins.a, 0) == 1
                    and _is_num_lit(ins.b)):
                const_map[ins.a] = ins.b

        if not const_map:
            break

        new_ic = []
        for ins in ic:
            if ins.op == BINOP:
                left   = _sub(ins.b, const_map)
                right  = _sub(ins.c, const_map)
                op_str = getattr(ins, '_op2', '+')
                folded, ok = _const_fold(left, op_str, right)
                if ok:
                    new_ins = ICInstruction(ASSIGN, ins.a, folded, None, ins.line)
                    new_ins._op2 = None
                    changed = True
                else:
                    new_ins = ICInstruction(BINOP, ins.a, left, right, ins.line)
                    new_ins._op2 = op_str
                    if left is not ins.b or right is not ins.c:
                        changed = True
                new_ic.append(new_ins)

            elif ins.op == UNOP:
                operand = _sub(ins.c, const_map)
                op_str  = ins.b
                folded  = None
                if _is_num_lit(operand):
                    try:
                        if op_str == "-" and not isinstance(operand, bool):
                            folded = -operand
                        elif op_str == "!":
                            folded = not operand
                    except Exception:
                        pass
                if folded is not None:
                    new_ins = ICInstruction(ASSIGN, ins.a, folded, None, ins.line)
                    new_ins._op2 = None
                    changed = True
                else:
                    new_ins = ICInstruction(UNOP, ins.a, op_str, operand, ins.line)
                    new_ins._op2 = None
                    if operand is not ins.c:
                        changed = True
                new_ic.append(new_ins)

            elif ins.op == ASSIGN:
                new_b = _sub(ins.b, const_map)
                if new_b is not ins.b:
                    new_ins = ICInstruction(ASSIGN, ins.a, new_b, None, ins.line)
                    new_ins._op2 = None
                    new_ic.append(new_ins)
                    changed = True
                else:
                    new_ic.append(ins)

            else:
                # JUMPF/JUMPT: substitute all constants so branch simplification can fire.
                # PARAM/RETURN/PRINT: substitute only temps — preserves user variable
                # assignments that are directly observed (printed, returned).
                if ins.op in (JUMPF, JUMPT):
                    a = _sub(ins.a, const_map)
                elif ins.op in (PARAM, RETURN_OP, PRINT_OP):
                    tmp_only = {k: v for k, v in const_map.items() if _is_tmp_name(k)}
                    a = _sub(ins.a, tmp_only)
                else:
                    a = ins.a
                new_ins = ICInstruction(ins.op, a, ins.b, ins.c, ins.line)
                new_ins._op2 = getattr(ins, '_op2', None)
                if a is not ins.a:
                    changed = True
                new_ic.append(new_ins)

        ic = new_ic

    return ic


# ── Branch Simplification ─────────────────────────────────────

def _simplify_branches(ic: list) -> list:
    """
    Branch Simplification pass.

    When a JUMPF/JUMPT condition is a compile-time constant (exposed by
    constant propagation), replace it with either an unconditional JUMP or
    remove it entirely:
      JUMPF  falsy,  label  →  JUMP label   (always taken)
      JUMPF  truthy, label  →  (removed, never taken)
      JUMPT  truthy, label  →  JUMP label   (always taken)
      JUMPT  falsy,  label  →  (removed, never taken)
    """
    def _is_literal(v):
        return isinstance(v, bool) or isinstance(v, (int, float, complex))

    def _truthy(v):
        if isinstance(v, complex): return bool(v.real or v.imag)
        return bool(v)

    new_ic = []
    for ins in ic:
        if ins.op == JUMPF and _is_literal(ins.a):
            if not _truthy(ins.a):              # always taken → unconditional jump
                new_ins = ICInstruction(JUMP, ins.b, None, None, ins.line)
                new_ins._op2 = None
                new_ic.append(new_ins)
            # else: never taken → drop entirely
        elif ins.op == JUMPT and _is_literal(ins.a):
            if _truthy(ins.a):                  # always taken → unconditional jump
                new_ins = ICInstruction(JUMP, ins.b, None, None, ins.line)
                new_ins._op2 = None
                new_ic.append(new_ins)
            # else: never taken → drop entirely
        else:
            new_ic.append(ins)
    return new_ic


# ── Unreachable Code Elimination ──────────────────────────────

def _elim_unreachable(ic: list) -> list:
    """
    Unreachable Code Elimination pass.

    Performs a forward reachability analysis from instruction 0.
    Instructions that cannot be reached by any control-flow path are removed.

    Control-flow rules:
      JUMP L          → only successor is label L (no fall-through)
      JUMPF/JUMPT …L  → successors are next instruction AND label L
      RETURN          → no successors
      everything else → fall-through to next instruction
    """
    if not ic:
        return ic

    # Build label → instruction index map
    label_idx: dict = {}
    for i, ins in enumerate(ic):
        if ins.op == LABEL:
            label_idx[ins.a] = i

    # Forward BFS from instruction 0
    reachable: set = set()
    worklist = [0]
    while worklist:
        i = worklist.pop()
        if i < 0 or i >= len(ic) or i in reachable:
            continue
        reachable.add(i)
        ins = ic[i]
        if ins.op == JUMP:
            t = label_idx.get(ins.a)
            if t is not None:
                worklist.append(t)
        elif ins.op in (JUMPF, JUMPT):
            worklist.append(i + 1)
            t = label_idx.get(ins.b)
            if t is not None:
                worklist.append(t)
        elif ins.op == RETURN_OP:
            pass
        else:
            worklist.append(i + 1)

    return [ins for i, ins in enumerate(ic) if i in reachable]


# ── Also patch _gen_num_expr / _gen_num_term / _gen_num_factor ─

def _patched_gen_num_expr(self, ctx):
    if ctx is None: return 0
    left = self._gen_num_term(ctx.num_term())
    if ctx.num_expression():
        right = self._gen_num_expr(ctx.num_expression())
        op    = "+" if ctx.ADD() else "-"
        folded, ok = _const_fold(left, op, right)
        if ok:
            return folded
        t   = self._tmp()
        ins = ICInstruction(BINOP, t, left, right, self._line(ctx))
        ins._op2 = op
        self._current_ic.append(ins)
        return t
    return left

def _patched_gen_num_term(self, ctx):
    left = self._gen_num_factor(ctx.num_factor())
    if ctx.num_term():
        right = self._gen_num_term(ctx.num_term())
        if   ctx.MUL(): op = "*"
        elif ctx.DIV(): op = "/"
        elif ctx.MOD(): op = "%"
        elif ctx.EXP(): op = "**"
        else:           op = "*"
        folded, ok = _const_fold(left, op, right)
        if ok:
            return folded
        t   = self._tmp()
        ins = ICInstruction(BINOP, t, left, right, self._line(ctx))
        ins._op2 = op
        self._current_ic.append(ins)
        return t
    return left

def _patched_gen_num_factor(self, ctx):
    if ctx.AMPERSAND():
        t = self._tmp()
        self._current_ic.append(ICInstruction(ADDR_OF, t, ctx.IDENTIFIER().getText(), None, self._line(ctx)))
        return t
    if ctx.MUL() and not ctx.num_factor():
        t = self._tmp()
        self._current_ic.append(ICInstruction(DEREF, t, ctx.IDENTIFIER().getText(), None, self._line(ctx)))
        return t
    if ctx.LPAREN() and ctx.num_expression():
        return self._gen_num_expr(ctx.num_expression())
    if ctx.func_call_statement():
        t = self._tmp()
        return self._gen_call(ctx.func_call_statement(), dest=t)
    if ctx.COMPLEX():
        return self._parse_complex(ctx.COMPLEX().getText())
    if ctx.INT():
        return int(ctx.INT().getText())
    if ctx.FLOAT():
        return float(ctx.FLOAT().getText())
    if ctx.CHAR():
        return _unescape(ctx.CHAR().getText()[1:-1])
    if ctx.num_factor():
        inner = self._gen_num_factor(ctx.num_factor())
        if ctx.SUB():
            if isinstance(inner, (int, float, complex)) and not isinstance(inner, bool):
                return -inner          # fold unary minus on a literal
            t = self._tmp()
            self._current_ic.append(ICInstruction(UNOP, t, "-", inner, self._line(ctx)))
            return t
        return inner   # unary +
    if ctx.array_access():
        return self._gen_array_access(ctx.array_access())
    if ctx.dirac_expression():
        return self._gen_dirac(ctx.dirac_expression())
    if ctx.IDENTIFIER():
        return ctx.IDENTIFIER().getText()
    return 0

def _patched_gen_bool_or(self, ctx):
    bool_ors = ctx.bool_or()
    if bool_ors:
        left  = self._gen_bool_or(bool_ors[0])
        # Constant folding: left is a compile-time bool
        if isinstance(left, bool):
            if left:    # true || anything → True (right side never emitted)
                return True
            # false || anything → just the right side
            return (self._gen_bool_or(bool_ors[1])
                    if len(bool_ors) > 1
                    else self._gen_bool_and(ctx.bool_and()))
        t     = self._tmp()
        l_sc  = self._label()   # short-circuit label (left was true)
        l_end = self._label()   # end label
        ln    = self._line(ctx)
        # if left is true, skip right entirely
        self._current_ic.append(ICInstruction(JUMPT, left, l_sc, None, ln))
        # left was false — evaluate right
        right = (self._gen_bool_or(bool_ors[1])
                 if len(bool_ors) > 1
                 else self._gen_bool_and(ctx.bool_and()))
        self._current_ic.append(ICInstruction(COPY,  t, right, None, ln))
        self._current_ic.append(ICInstruction(JUMP,  l_end, None, None, ln))
        # short-circuit path: left was true → result is True
        self._current_ic.append(ICInstruction(LABEL, l_sc,  None, None, ln))
        self._current_ic.append(ICInstruction(ASSIGN, t, True, None, ln))
        self._current_ic.append(ICInstruction(LABEL, l_end, None, None, ln))
        return t
    return self._gen_bool_and(ctx.bool_and())

def _patched_gen_bool_and(self, ctx):
    bool_ands = ctx.bool_and()
    if bool_ands:
        left  = self._gen_bool_and(bool_ands[0])
        # Constant folding: left is a compile-time bool
        if isinstance(left, bool):
            if not left:  # false && anything → False (right side never emitted)
                return False
            # true && anything → just the right side
            return (self._gen_bool_and(bool_ands[1])
                    if len(bool_ands) > 1
                    else self._gen_bool_cmp(ctx.bool_cmp()))
        t     = self._tmp()
        l_sc  = self._label()   # short-circuit label (left was false)
        l_end = self._label()   # end label
        ln    = self._line(ctx)
        # if left is false, skip right entirely
        self._current_ic.append(ICInstruction(JUMPF, left, l_sc, None, ln))
        # left was true — evaluate right
        right = (self._gen_bool_and(bool_ands[1])
                 if len(bool_ands) > 1
                 else self._gen_bool_cmp(ctx.bool_cmp()))
        self._current_ic.append(ICInstruction(COPY,  t, right, None, ln))
        self._current_ic.append(ICInstruction(JUMP,  l_end, None, None, ln))
        # short-circuit path: left was false → result is False
        self._current_ic.append(ICInstruction(LABEL, l_sc,  None, None, ln))
        self._current_ic.append(ICInstruction(ASSIGN, t, False, None, ln))
        self._current_ic.append(ICInstruction(LABEL, l_end, None, None, ln))
        return t
    return self._gen_bool_cmp(ctx.bool_cmp())

def _patched_gen_bool_cmp(self, ctx):
    num_exprs    = ctx.num_expression()
    str_exprs    = ctx.string_expression()
    bool_unaries = ctx.bool_unary()

    def _make_cmp(left, right, op):
        folded, ok = _const_fold(left, op, right)
        if ok:
            return folded
        t   = self._tmp()
        ins = ICInstruction(BINOP, t, left, right, self._line(ctx))
        ins._op2 = op
        self._current_ic.append(ins)
        return t

    if len(num_exprs) == 2:
        return _make_cmp(self._gen_num_expr(num_exprs[0]),
                         self._gen_num_expr(num_exprs[1]),
                         self._cmp_op(ctx.num_comp()))
    if len(str_exprs) == 2:
        return _make_cmp(self._gen_string_expr(str_exprs[0]),
                         self._gen_string_expr(str_exprs[1]),
                         self._eq_op(ctx.eq_comp()))
    if len(bool_unaries) == 2:
        return _make_cmp(self._gen_bool_unary(bool_unaries[0]),
                         self._gen_bool_unary(bool_unaries[1]),
                         self._eq_op(ctx.eq_comp()))
    if len(bool_unaries) == 1:
        return self._gen_bool_unary(bool_unaries[0])
    return False

def _patched_gen_string_expr(self, ctx):
    parts = ctx.string_expression()
    if parts:
        left  = self._gen_string_expr(parts[0])
        right = self._gen_string_expr(parts[1]) if len(parts) > 1 else ""
        t   = self._tmp()
        ins = ICInstruction(BINOP, t, left, right, self._line(ctx))
        ins._op2 = "+"
        self._current_ic.append(ins)
        return t
    if ctx.STRING():
        return _unescape(ctx.STRING().getText()[1:-1])
    if ctx.IDENTIFIER():
        return ctx.IDENTIFIER().getText()
    return ""

def _patched_gen_dirac(self, ctx):
    children = ctx.dirac_expression()
    if len(children) == 2:
        left  = self._gen_dirac(children[0])
        right = self._gen_dirac(children[1])
        op    = "*" if ctx.MUL() else "@"
        t   = self._tmp()
        ins = ICInstruction(BINOP, t, left, right, self._line(ctx))
        ins._op2 = op
        self._current_ic.append(ins)
        return t
    if ctx.KET_IDENTIFIER(): return ctx.KET_IDENTIFIER().getText()
    if ctx.BRA_IDENTIFIER(): return ctx.BRA_IDENTIFIER().getText()
    if ctx.func_call_statement():
        # Function call result used as a dirac operand: hadamard(|ket>), normalize(v)
        t = self._tmp()
        return self._gen_call(ctx.func_call_statement(), dest=t)
    if ctx.IDENTIFIER():     return ctx.IDENTIFIER().getText()
    if ctx.braket_vector():  return self._gen_braket_vector(ctx.braket_vector())
    if ctx.op():             return self._gen_op_matrix(ctx.op())
    return None

ICGenerator._gen_num_expr    = _patched_gen_num_expr
ICGenerator._gen_num_term    = _patched_gen_num_term
ICGenerator._gen_num_factor  = _patched_gen_num_factor
ICGenerator._gen_bool_or     = _patched_gen_bool_or
ICGenerator._gen_bool_and    = _patched_gen_bool_and
ICGenerator._gen_bool_cmp    = _patched_gen_bool_cmp
ICGenerator._gen_string_expr = _patched_gen_string_expr
ICGenerator._gen_dirac       = _patched_gen_dirac


# ══════════════════════════════════════════════════════════════════════════════
#  Public convenience functions
# ══════════════════════════════════════════════════════════════════════════════

def generate_ic(tree, parser=None) -> tuple[list[ICInstruction],
                                            dict[str, tuple]]:
    """
    Generate intermediate code from an ANTLR parse tree.
    Returns (global_instructions, functions_dict).
    """
    def _optimize(ic):
        for _ in range(4):          # iterate to handle cascading simplifications
            prev = len(ic)
            ic = _const_propagate(ic)
            ic = _elim_dead_assignments(ic)   # algebraic identities (b*0→0, b+0→b, …)
            ic = _prop_temp_copies(ic)        # expose self-assignments via temp substitution
            ic = _elim_dead_assignments(ic)   # remove self-assignments revealed above
            ic = _simplify_branches(ic)
            ic = _elim_unreachable(ic)
            ic = _elim_dead_temps(ic)
            if len(ic) == prev:
                break
        return ic

    gen = ICGenerator()
    gen.generate(tree)
    instructions = _optimize(gen.instructions)
    functions = {
        name: (params, _optimize(body_ic), defaults)
        for name, (params, body_ic, defaults) in gen.functions.items()
    }
    return instructions, functions


def run_ic(instructions:  list[ICInstruction],
           functions:     dict[str, tuple],
           output_cb:     Callable[[str], None] | None = None,
           max_steps:     int = 100_000,
           input_cb:      Callable[[str], str] | None = None) -> InterpreterResult:
    """
    Execute pre-generated IC instructions.
    output_cb is called with each printed string as it is produced.
    input_cb(prompt) is called when input() is evaluated; it must return a str.
    """
    interp = Interpreter(instructions, functions, output_cb, input_cb=input_cb)
    interp.MAX_STEPS = max_steps
    return interp.execute()


# ══════════════════════════════════════════════════════════════════════════════
#  Step Debugger  —  pre-records every IC step as a snapshot
# ══════════════════════════════════════════════════════════════════════════════

import copy as _copy

@dataclass
class DebugSnapshot:
    """State of the program at one IC step."""
    step:        int            # 0-based sequential step index
    pc:          int            # IC instruction index
    source_line: int            # source line number (0 = unknown)
    instr_str:   str            # human-readable IC instruction
    env:         dict           # shallow copy of the user-visible env (no temps)
    output:      list[str]      # program output accumulated so far
    changed:     set            # names changed by this step
    var_addrs:   dict           # variable name -> simulated address at this step


def _user_env(env: dict) -> dict:
    """Return all symbols (user variables and temporaries)."""
    return dict(env)


class _SnapshotInterpreter(Interpreter):
    """
    Interpreter subclass that records a DebugSnapshot after *every* IC step
    (before incrementing PC). Temporaries are excluded from snapshots.
    """

    def __init__(self, instructions, functions, output_cb=None, input_cb=None):
        super().__init__(instructions, functions, output_cb, input_cb=input_cb)
        self._interactive = False   # suppress dirac() popup and other UI calls
        self.snapshots: list[DebugSnapshot] = []
        self._snap_step = 0

    def _run_ic(self, ic: list[ICInstruction], env: dict):
        labels: dict[str, int] = {}
        for i, ins in enumerate(ic):
            if ins.op == LABEL:
                labels[ins.a] = i

        pc = 0
        while pc < len(ic):
            ins = ic[pc]
            self._steps += 1
            if self._steps > self.MAX_STEPS:
                raise BKRuntimeError(
                    f"Execution limit ({self.MAX_STEPS} steps) exceeded — infinite loop?",
                    ins.line)

            self._exec_log.append(f"  [{pc:04d}]  {ins}")

            # snapshot BEFORE executing (shows what is ABOUT to run)
            before = _user_env({**self._global_env, **env})

            op = ins.op

            if op == LABEL:
                pc += 1; continue

            elif op == ASSIGN:
                val = self._resolve(ins.b, env)
                if isinstance(val, list):
                    name = ins.a if isinstance(ins.a, str) else ""
                    if name.startswith("<") and name.endswith("|"):
                        val = BKVector(val, "bra")
                    elif name.startswith("|") and name.endswith(">"):
                        val = BKVector(val, "ket")
                    elif val and isinstance(val[0], list):
                        val = BKOperator(val)
                    else:
                        val = BKVector(val, "ket")
                env[ins.a] = val
                self._assign_var_addr(ins.a)

            elif op == COPY:
                env[ins.a] = self._resolve(ins.b, env)
                self._assign_var_addr(ins.a)

            elif op == BINOP:
                op_str = getattr(ins, '_op2', '+')
                lv = self._resolve(ins.b, env)
                rv = self._resolve(ins.c, env)
                env[ins.a] = self._apply_binop(ins.b, ins.c, lv, rv, op_str, ins.line)
                self._assign_var_addr(ins.a)

            elif op == UNOP:
                v = self._resolve(ins.c, env)
                env[ins.a] = self._apply_unop(ins.b, v, ins.line)
                self._assign_var_addr(ins.a)

            elif op == JUMP:
                # record before jumping
                after = _user_env({**self._global_env, **env})
                self._record(pc, ins, before, after)
                pc = labels.get(ins.a, pc + 1); continue

            elif op == JUMPF:
                cond = self._resolve(ins.a, env)
                after = _user_env({**self._global_env, **env})
                self._record(pc, ins, before, after)
                if not self._truthy(cond):
                    pc = labels.get(ins.b, pc + 1); continue
                pc += 1; continue

            elif op == JUMPT:
                cond = self._resolve(ins.a, env)
                after = _user_env({**self._global_env, **env})
                self._record(pc, ins, before, after)
                if self._truthy(cond):
                    pc = labels.get(ins.b, pc + 1); continue
                pc += 1; continue

            elif op == PARAM:
                self._param_buf.append(self._resolve(ins.a, env))

            elif op == CALL:
                dest  = ins.a
                fname = ins.b
                argc  = ins.c
                args  = self._param_buf[-argc:] if argc else []
                self._param_buf = self._param_buf[:-argc] if argc else self._param_buf
                result = self._call_function(fname, args, ins.line)
                env[dest] = result
                self._assign_var_addr(dest)

            elif op == RETURN_OP:
                val = self._resolve(ins.a, env) if ins.a is not None else None
                after = _user_env({**self._global_env, **env})
                self._record(pc, ins, before, after)
                raise _ReturnSignal(val)

            elif op == PRINT_OP:
                val = self._resolve(ins.a, env)
                s   = _fmt(val)
                self._output.append(s)
                self.output_cb(s)

            elif op == ARRAY_NEW:
                env[ins.a] = BKArray([None] * ins.b)
                self._assign_var_addr(ins.a)

            elif op == ARRAY_SET:
                arr = self._resolve(ins.a, env)
                idx = int(self._resolve(ins.b, env))
                val = self._resolve(ins.c, env)
                if isinstance(arr, BKArray):
                    while len(arr.data) <= idx:
                        arr.data.append(None)
                    arr.data[idx] = val
                elif isinstance(arr, dict):
                    arr[idx] = val
                else:
                    env[ins.a] = BKArray([val])

            elif op == ARRAY_GET:
                arr = self._resolve(ins.b, env)
                idx = int(self._resolve(ins.c, env))
                if isinstance(arr, BKArray):
                    env[ins.a] = arr.data[idx]
                elif isinstance(arr, dict):
                    env[ins.a] = arr.get(idx)
                else:
                    raise BKRuntimeError(f"'{ins.b}' is not an array", ins.line)
                self._assign_var_addr(ins.a)

            elif op == "VEC_FROM_ARRAY":
                arr = env.get(ins.b)
                if isinstance(arr, BKArray):
                    env[ins.a] = arr.data
                self._assign_var_addr(ins.a)

            elif op == "MAT_FROM_ROWS":
                arr = env.get(ins.b)
                if isinstance(arr, BKArray):
                    rows = []
                    for row in arr.data:
                        if isinstance(row, list):
                            rows.append([complex(x) for x in row])
                        elif isinstance(row, BKVector):
                            rows.append(row.data)
                        else:
                            rows.append([complex(row)])
                    env[ins.a] = BKOperator(rows)
                self._assign_var_addr(ins.a)

            elif op == STRUCT_SET:
                obj = self._resolve(ins.a, env)
                if isinstance(obj, BKStruct):
                    obj.fields[ins.b] = self._resolve(ins.c, env)
                elif isinstance(obj, dict):
                    obj[ins.b] = self._resolve(ins.c, env)
                else:
                    env[ins.a] = BKStruct({ins.b: self._resolve(ins.c, env)})

            elif op == STRUCT_GET:
                obj = self._resolve(ins.b, env)
                if isinstance(obj, BKStruct):
                    env[ins.a] = obj.fields.get(ins.c)
                elif isinstance(obj, dict):
                    env[ins.a] = obj.get(ins.c)
                else:
                    raise BKRuntimeError(f"'{ins.b}' is not a struct", ins.line)
                self._assign_var_addr(ins.a)

            elif op == ADDR_OF:
                var_name = ins.b
                if var_name not in self._var_addrs:
                    self._addr_next += 4
                    self._var_addrs[var_name] = self._addr_next
                addr = self._var_addrs[var_name]
                self._heap[addr] = self._resolve(var_name, env)
                env[ins.a] = BKPointer(var_name, addr)
                self._assign_var_addr(ins.a)

            elif op == DEREF:
                ptr = self._resolve(ins.b, env)
                if isinstance(ptr, BKPointer):
                    val = self._resolve(ptr.var_name, env)
                    if isinstance(val, str) and val == ptr.var_name:
                        val = self._heap.get(ptr.address)
                    env[ins.a] = val
                elif isinstance(ptr, int):
                    env[ins.a] = self._heap.get(ptr)
                else:
                    raise BKRuntimeError(f"Cannot dereference '{ins.b}'", ins.line)
                self._assign_var_addr(ins.a)

            elif op == DEREF_ASSIGN:
                ptr = self._resolve(ins.a, env)
                val = self._resolve(ins.b, env)
                if not isinstance(ptr, BKPointer):
                    raise BKRuntimeError(f"'{ins.a}' is not a pointer", ins.line)
                for frame in reversed(self._call_stack):
                    if ptr.var_name in frame:
                        frame[ptr.var_name] = val
                        break
                else:
                    if ptr.var_name in env:
                        env[ptr.var_name] = val
                    else:
                        self._global_env[ptr.var_name] = val
                self._heap[ptr.address] = val

            # record snapshot AFTER executing
            after = _user_env({**self._global_env, **env})
            changed = {k for k in after if str(after.get(k)) != str(before.get(k))}
            changed |= {k for k in before if k not in after}
            self._record(pc, ins, before, after, changed)
            pc += 1

    def _record(self, pc: int, ins: ICInstruction,
                before: dict, after: dict, changed: set | None = None):
        if changed is None:
            changed = set()
        # Build a human-readable instruction string
        op2 = getattr(ins, '_op2', None)
        if ins.op == BINOP:
            s = f"[{pc:04d}] BINOP  {ins.a} = {ins.b} {op2 or '?'} {ins.c}"
        elif ins.op == ASSIGN:
            s = f"[{pc:04d}] ASSIGN {ins.a} ← {ins.b}"
        elif ins.op == COPY:
            s = f"[{pc:04d}] COPY   {ins.a} ← {ins.b}"
        elif ins.op == JUMP:
            s = f"[{pc:04d}] JUMP   → {ins.a}"
        elif ins.op == JUMPF:
            s = f"[{pc:04d}] JUMPF  if_false({ins.a}) → {ins.b}"
        elif ins.op == JUMPT:
            s = f"[{pc:04d}] JUMPT  if_true({ins.a}) → {ins.b}"
        elif ins.op == PRINT_OP:
            s = f"[{pc:04d}] PRINT  {ins.a}"
        elif ins.op == CALL:
            s = f"[{pc:04d}] CALL   {ins.a} = {ins.b}({ins.c} args)"
        elif ins.op == RETURN_OP:
            s = f"[{pc:04d}] RETURN {ins.a}"
        else:
            parts = [x for x in (ins.a, ins.b, ins.c) if x is not None]
            s = f"[{pc:04d}] {ins.op:<10} {'  '.join(str(p) for p in parts)}"

        self.snapshots.append(DebugSnapshot(
            step        = self._snap_step,
            pc          = pc,
            source_line = ins.line,
            instr_str   = s,
            env         = dict(after),
            output      = list(self._output),
            changed     = set(changed),
            var_addrs   = dict(self._var_addrs),
        ))
        self._snap_step += 1


def snapshot_ic(instructions: list[ICInstruction],
                functions:    dict[str, tuple],
                max_steps:    int = 10_000,
                input_cb:     Callable[[str], str] | None = None) -> list[DebugSnapshot]:
    """
    Run the interpreter and return a list of DebugSnapshots — one per
    executed IC instruction.  Used by the IDE step-debugger.
    """
    interp = _SnapshotInterpreter(instructions, functions, input_cb=input_cb)
    interp.MAX_STEPS = max_steps
    try:
        interp._run_ic(interp.instructions, interp._global_env)
    except _ReturnSignal:
        pass
    except BKRuntimeError:
        pass
    except Exception:
        pass
    return interp.snapshots


def ic_listing(instructions: list[ICInstruction]) -> str:
    """Return a human-readable IC listing string."""
    lines = []
    for i, ins in enumerate(instructions):
        op2 = getattr(ins, '_op2', None)
        if ins.op == BINOP:
            line = (f"  {i:04d}  {ins.op:<12} {ins.a}  =  {ins.b}  "
                    f"{op2 or '?'}  {ins.c}")
        elif ins.op == LABEL:
            line = f"\n{ins.a}:"
        elif ins.op == JUMP:
            line = f"  {i:04d}  {ins.op:<12} → {ins.a}"
        elif ins.op in (JUMPF, JUMPT):
            label = "if_false" if ins.op == JUMPF else "if_true"
            line  = f"  {i:04d}  {ins.op:<12} {label}({ins.a})  → {ins.b}"
        elif ins.op == CALL:
            line = f"  {i:04d}  {ins.op:<12} {ins.a}  =  {ins.b}({ins.c} args)"
        elif ins.op == PARAM:
            line = f"  {i:04d}  {ins.op:<12} {ins.a}"
        elif ins.op == RETURN_OP:
            line = f"  {i:04d}  {ins.op:<12} {ins.a}"
        elif ins.op == ASSIGN:
            line = f"  {i:04d}  {ins.op:<12} {ins.a}  ←  {ins.b}"
        else:
            parts = [x for x in (ins.a, ins.b, ins.c) if x is not None]
            line  = f"  {i:04d}  {ins.op:<12} {'  '.join(str(p) for p in parts)}"
        lines.append(line)
    return "\n".join(lines)