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
STRUCT_SET = "STRUCT_SET"
STRUCT_GET = "STRUCT_GET"


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
        params = self._get_param_names(ctx.param_list()) if ctx.param_list() else []

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
        self.functions[name] = (params, body_ic)

    def _get_param_names(self, ctx) -> list[str]:
        names = []
        if ctx.identifier_list():
            for ident in ctx.identifier_list().IDENTIFIER():
                names.append(ident.getText())
        if ctx.default_list():
            for assign in ctx.default_list().assign_statement():
                if assign.var_decl() and assign.var_decl().IDENTIFIER():
                    names.append(assign.var_decl().IDENTIFIER().getText())
        return names

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

    def _gen_var_decl(self, ctx, is_const=False):
        """
        var_decl : IDENTIFIER ASSIGN expression
                 | KET_IDENTIFIER ASSIGN num_expression
                 | BRA_IDENTIFIER ASSIGN num_expression
        """
        ln = self._line(ctx)
        if ctx.IDENTIFIER():
            name = ctx.IDENTIFIER().getText()
            val  = self._gen_expr(ctx.expression())
            self._emit(ASSIGN, name, val, line=ln)
            if is_const:
                self._const_names.add(name)

        elif ctx.KET_IDENTIFIER():
            raw  = ctx.KET_IDENTIFIER().getText()   # |name>
            name = raw                               # keep the full token as key
            val  = self._gen_braket_vector_or_num(ctx)
            self._emit(ASSIGN, name, val, line=ln)
            if is_const:
                self._const_names.add(name)

        elif ctx.BRA_IDENTIFIER():
            raw  = ctx.BRA_IDENTIFIER().getText()   # <name|
            name = raw
            val  = self._gen_braket_vector_or_num(ctx)
            self._emit(ASSIGN, name, val, line=ln)
            if is_const:
                self._const_names.add(name)

    def _gen_braket_vector_or_num(self, ctx):
        """For ket/bra declarations — the RHS is a num_expression (braket_vector)."""
        if ctx.num_expression():
            return self._gen_num_expr(ctx.num_expression())
        return None

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
        if ctx.arg_list():
            args.extend(self._collect_args(ctx.arg_list()))
        return args

    def _gen_arg(self, ctx):
        if ctx.assign_statement():
            # default arg — generate the assignment and return the var name
            self._gen_assign_stmt(ctx.assign_statement())
            if ctx.assign_statement().var_decl():
                return ctx.assign_statement().var_decl().IDENTIFIER().getText()
        if ctx.IDENTIFIER():
            return ctx.IDENTIFIER().getText()
        if ctx.array_access():
            return self._gen_array_access(ctx.array_access())
        if ctx.struct_access():
            return self._gen_struct_access(ctx.struct_access())
        if ctx.value():
            return self._gen_value_literal(ctx.value())
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
        if ctx.LPAREN() and ctx.num_expression():
            return self._gen_num_expr(ctx.num_expression())
        if ctx.COMPLEX():
            return self._parse_complex(ctx.COMPLEX().getText())
        if ctx.INT():
            return int(ctx.INT().getText())
        if ctx.FLOAT():
            return float(ctx.FLOAT().getText())
        if ctx.CHAR():
            raw = ctx.CHAR().getText()
            return raw[1] if len(raw) >= 3 else ""
        if ctx.num_factor():
            inner = self._gen_num_factor(ctx.num_factor())
            if ctx.SUB():
                t = self._tmp()
                self._emit(UNOP, t, "-", inner, line=self._line(ctx))
                return t
            return inner   # unary +
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
            return raw[1:-1]   # strip quotes
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
            self._emit(BINOP, t, left, op, line=self._line(ctx))
            self._instructions_last().c = right
            return t
        if ctx.KET_IDENTIFIER():
            return ctx.KET_IDENTIFIER().getText()
        if ctx.BRA_IDENTIFIER():
            return ctx.BRA_IDENTIFIER().getText()
        if ctx.IDENTIFIER():
            return ctx.IDENTIFIER().getText()
        if ctx.braket_vector():
            return self._gen_braket_vector(ctx.braket_vector())
        if ctx.op():
            return self._gen_op_matrix(ctx.op())
        return None

    def _gen_braket_vector(self, ctx) -> list:
        vals = []
        for bv in ctx.braket_value():
            if bv.COMPLEX():
                vals.append(self._parse_complex(bv.COMPLEX().getText()))
            elif bv.FLOAT():
                vals.append(float(bv.FLOAT().getText()))
            elif bv.INT():
                vals.append(int(bv.INT().getText()))
        return vals

    def _gen_op_matrix(self, ctx) -> list:
        rows = []
        for bvec in ctx.braket_vector():
            rows.append(self._gen_braket_vector(bvec))
        return rows

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
            return raw[1] if len(raw) >= 3 else ""
        if ctx.STRING():
            return ctx.STRING().getText()[1:-1]
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
    if isinstance(v, (BKVector, BKOperator, BKArray, BKStruct)):
        return repr(v)
    return str(v)


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
    output:       list[str]
    error:        Optional[str]
    symbol_table: dict[str, Any]   # global env after execution
    ic_trace:     list[str]        # formatted IC listing
    exec_log:     list[str]        # step-by-step execution log


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
    • Built-in functions: print, len, abs, sqrt, real, imag, conj, norm.
    """

    MAX_STEPS = 100_000   # loop guard

    def __init__(self,
                 instructions: list[ICInstruction],
                 functions:    dict[str, tuple[list[str], list[ICInstruction]]],
                 output_cb:    Callable[[str], None] | None = None):
        self.instructions = instructions
        self.functions    = functions
        self.output_cb    = output_cb or (lambda s: None)

        self._global_env: dict[str, Any] = {}
        self._call_stack: list[dict[str, Any]] = []
        self._param_buf:  list[Any] = []
        self._output:     list[str] = []
        self._exec_log:   list[str] = []
        self._steps       = 0

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

        return InterpreterResult(
            output       = self._output,
            error        = error,
            symbol_table = {k: v for k, v in self._global_env.items()
                            if not k.startswith("t")},
            ic_trace     = ic_trace,
            exec_log     = self._exec_log,
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
                # If a raw list came back (inline vector literal), wrap it now
                # using the variable name to determine ket vs bra kind.
                if isinstance(val, list):
                    name = ins.a if isinstance(ins.a, str) else ""
                    if name.startswith("<") and name.endswith("|"):
                        val = BKVector(val, "bra")
                    elif name.startswith("|") and name.endswith(">"):
                        val = BKVector(val, "ket")
                    elif val and isinstance(val[0], list):
                        val = BKOperator(val)
                    else:
                        val = BKVector(val, "ket")   # fallback
                env[ins.a] = val

            elif op == COPY:
                env[ins.a] = self._resolve(ins.b, env)

            elif op == BINOP:
                lv = self._resolve(ins.b, env)
                rv = self._resolve(ins.c, env)
                env[ins.a] = self._apply_binop(ins.b, ins.c, lv, rv, ins.op_str if hasattr(ins,'op_str') else self._binop_str(ins), ins.line)

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
            # Inline list literal — either a vector or a matrix.
            # We return raw lists here; the ASSIGN handler wraps them with the
            # correct kind ("ket" or "bra") once it knows the variable name.
            if v and isinstance(v[0], list):
                return BKOperator(v)
            # Return as-is — ASSIGN will wrap in BKVector with correct kind
            return v
        if isinstance(v, dict):
            return BKStruct(v)
        return v

    def _binop_str(self, ins: ICInstruction) -> str:
        return "+"   # fallback — overridden by _patched_run_ic via _op2

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
        if builtin is not _SENTINEL:
            return builtin

        if name not in self.functions:
            raise BKRuntimeError(f"Undefined function '{name}'", line)

        param_names, body_ic = self.functions[name]
        frame: dict[str, Any] = {}

        # Bind positional args
        for i, pname in enumerate(param_names):
            frame[pname] = args[i] if i < len(args) else None

        self._call_stack.append(frame)
        result = None
        try:
            self._run_ic(body_ic, frame)
        except _ReturnSignal as r:
            result = r.value
        finally:
            self._call_stack.pop()

        return result

    _SENTINEL = object()

    def _try_builtin(self, name: str, args: list, line: int) -> Any:
        if name == "print":
            parts = [_fmt(a) for a in args]
            s = " ".join(parts)
            self._output.append(s)
            self.output_cb(s)
            return None
        if name == "len":
            v = args[0] if args else None
            if isinstance(v, BKArray):  return len(v.data)
            if isinstance(v, str):      return len(v)
            if isinstance(v, BKVector): return len(v.data)
            raise BKRuntimeError("len() requires an array or string", line)
        if name == "abs":
            v = args[0] if args else 0
            return abs(v)
        if name == "sqrt":
            v = args[0] if args else 0
            return cmath.sqrt(v) if isinstance(v, complex) else math.sqrt(v)
        if name == "real":
            v = args[0] if args else 0
            return v.real if isinstance(v, complex) else float(v)
        if name == "imag":
            v = args[0] if args else 0
            return v.imag if isinstance(v, complex) else 0.0
        if name == "conj":
            v = args[0] if args else 0
            if isinstance(v, complex):   return v.conjugate()
            if isinstance(v, BKVector):
                return BKVector([x.conjugate() for x in v.data], v.kind)
            return v
        if name == "norm":
            v = args[0] if args else 0
            if isinstance(v, BKVector):
                return math.sqrt(sum(abs(x)**2 for x in v.data))
            if isinstance(v, complex): return abs(v)
            return abs(v)
        if name == "dag":
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
        if name == "str":
            return _fmt(args[0]) if args else ""
        if name == "int":
            v = args[0] if args else 0
            return int(v)
        if name == "float":
            v = args[0] if args else 0.0
            return float(v)
        if name == "range":
            if len(args) == 1:   return BKArray(list(range(int(args[0]))))
            if len(args) == 2:   return BKArray(list(range(int(args[0]), int(args[1]))))
            if len(args) >= 3:   return BKArray(list(range(int(args[0]), int(args[1]), int(args[2]))))
            return BKArray([])
        return self._SENTINEL


# ══════════════════════════════════════════════════════════════════════════════
#  BINOP operator storage fix
#  The ICGenerator stores BINOP as: emit(BINOP, dest, left, op)
#  then patches the last instruction's .c = right.
#  We store the actual operator string in ins._op2 so the interpreter
#  can read it reliably.
# ══════════════════════════════════════════════════════════════════════════════

_orig_emit = ICGenerator._emit

def _patched_emit(self, op, a=None, b=None, c=None, line=0, _op2=None):
    ins = ICInstruction(op, a, b, c, line)
    ins._op2 = _op2
    self._current_ic.append(ins)

ICGenerator._emit = _patched_emit


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
            # ── FIX: use the variable name (ins.a) to decide ket vs bra ──
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
            argc  = ins.c or 0
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
            env[ins.a] = BKArray([None] * (ins.b or 0))

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

        pc += 1

Interpreter._run_ic = _patched_run_ic


# ── Patch generators to store op in _op2 ─────────────────────

def _patched_gen_num_expr(self, ctx):
    if ctx is None: return 0
    left = self._gen_num_term(ctx.num_term())
    if ctx.num_expression():
        right = self._gen_num_expr(ctx.num_expression())
        op    = "+" if ctx.ADD() else "-"
        t     = self._tmp()
        ins   = ICInstruction(BINOP, t, left, right, self._line(ctx))
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
        t   = self._tmp()
        ins = ICInstruction(BINOP, t, left, right, self._line(ctx))
        ins._op2 = op
        self._current_ic.append(ins)
        return t
    return left

def _patched_gen_bool_or(self, ctx):
    bool_ors = ctx.bool_or()
    if bool_ors:
        left  = self._gen_bool_or(bool_ors[0])
        right = (self._gen_bool_or(bool_ors[1])
                 if len(bool_ors) > 1
                 else self._gen_bool_and(ctx.bool_and()))
        t   = self._tmp()
        ins = ICInstruction(BINOP, t, left, right, self._line(ctx))
        ins._op2 = "||"
        self._current_ic.append(ins)
        return t
    return self._gen_bool_and(ctx.bool_and())

def _patched_gen_bool_and(self, ctx):
    bool_ands = ctx.bool_and()
    if bool_ands:
        left  = self._gen_bool_and(bool_ands[0])
        right = (self._gen_bool_and(bool_ands[1])
                 if len(bool_ands) > 1
                 else self._gen_bool_cmp(ctx.bool_cmp()))
        t   = self._tmp()
        ins = ICInstruction(BINOP, t, left, right, self._line(ctx))
        ins._op2 = "&&"
        self._current_ic.append(ins)
        return t
    return self._gen_bool_cmp(ctx.bool_cmp())

def _patched_gen_bool_cmp(self, ctx):
    num_exprs    = ctx.num_expression()
    str_exprs    = ctx.string_expression()
    bool_unaries = ctx.bool_unary()

    def _make_cmp(left, right, op):
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
        return ctx.STRING().getText()[1:-1]
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
    if ctx.IDENTIFIER():     return ctx.IDENTIFIER().getText()
    if ctx.braket_vector():  return self._gen_braket_vector(ctx.braket_vector())
    if ctx.op():             return self._gen_op_matrix(ctx.op())
    return None

ICGenerator._gen_num_expr    = _patched_gen_num_expr
ICGenerator._gen_num_term    = _patched_gen_num_term
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
    gen = ICGenerator()
    gen.generate(tree)
    return gen.instructions, gen.functions


def run_ic(instructions:  list[ICInstruction],
           functions:     dict[str, tuple],
           output_cb:     Callable[[str], None] | None = None,
           max_steps:     int = 100_000) -> InterpreterResult:
    """
    Execute pre-generated IC instructions.
    output_cb is called with each printed string as it is produced.
    """
    interp = Interpreter(instructions, functions, output_cb)
    interp.MAX_STEPS = max_steps
    return interp.execute()


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
