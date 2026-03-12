# ide.py
import tkinter as tk
from tkinter import ttk, scrolledtext, filedialog
from tkinter import font as tkfont
import re

# ─────────────────────────────────────────────────────────────
#  Minimal built-in interpreter (no ANTLR dependency needed to
#  demo the IDE panels).  Replace run_code / tokenize / parse_tree
#  with your real ANTLR-backed versions when ready.
# ─────────────────────────────────────────────────────────────

TOKEN_SPEC = [
    ("COMMENT",  r"//[^\n]*"),
    ("FLOAT",    r"\b\d+\.\d*\b"),
    ("INT",      r"\b\d+\b"),
    ("STRING",   r'"[^"\n]*"'),
    ("KEYWORD",  r"\b(if|else|while|print|true|false)\b"),
    ("ID",       r"\b[a-zA-Z_]\w*\b"),
    ("OP",       r"==|!=|<=|>=|[+\-*/<>=!]"),
    ("PUNCT",    r"[(){};,]"),
    ("WS",       r"\s+"),
    ("UNKNOWN",  r"."),
]
_MASTER = re.compile("|".join(f"(?P<{n}>{p})" for n, p in TOKEN_SPEC))

def tokenize(source: str):
    tokens = []
    for m in _MASTER.finditer(source):
        kind = m.lastgroup
        val  = m.group()
        if kind in ("WS", "COMMENT"):
            if kind == "COMMENT":
                tokens.append((kind, val, m.start()))
            continue
        tokens.append((kind, val, m.start()))
    return tokens


# ── tiny recursive-descent interpreter ──────────────────────

class Lexer:
    def __init__(self, source):
        self.tokens = [(k, v) for k, v, _ in tokenize(source) if k != "COMMENT"]
        self.pos    = 0
    def peek(self):
        return self.tokens[self.pos] if self.pos < len(self.tokens) else ("EOF", "")
    def consume(self, *kinds):
        k, v = self.peek()
        if kinds and k not in kinds:
            raise SyntaxError(f"Expected {kinds}, got {k!r} ({v!r})")
        self.pos += 1
        return k, v
    def match(self, kind, val=None):
        k, v = self.peek()
        if k == kind and (val is None or v == val):
            self.pos += 1
            return True
        return False


class Parser:
    """Returns a nested list AST and a parse-tree string for display."""

    def __init__(self, source):
        self.lex  = Lexer(source)
        self.tree_lines = []

    def _indent(self, depth):
        return "  " * depth

    def parse(self):
        stmts = self.program(0)
        return stmts

    def program(self, d):
        self.tree_lines.append(f"{self._indent(d)}Program")
        nodes = []
        while self.lex.peek()[0] != "EOF":
            nodes.append(self.statement(d + 1))
        return ("program", nodes)

    def statement(self, d):
        k, v = self.lex.peek()
        if k == "KEYWORD" and v == "print":
            return self.print_stmt(d)
        if k == "KEYWORD" and v == "if":
            return self.if_stmt(d)
        if k == "KEYWORD" and v == "while":
            return self.while_stmt(d)
        if k == "ID":
            return self.assign_stmt(d)
        raise SyntaxError(f"Unexpected token {v!r}")

    def print_stmt(self, d):
        self.tree_lines.append(f"{self._indent(d)}PrintStmt")
        self.lex.consume("KEYWORD")   # print
        self.lex.consume("PUNCT")     # (
        e = self.expr(d + 1)
        self.lex.consume("PUNCT")     # )
        self.lex.consume("PUNCT")     # ;
        return ("print", e)

    def if_stmt(self, d):
        self.tree_lines.append(f"{self._indent(d)}IfStmt")
        self.lex.consume("KEYWORD")
        self.lex.consume("PUNCT")
        cond = self.expr(d + 1)
        self.lex.consume("PUNCT")
        self.lex.consume("PUNCT")     # {
        body = []
        while self.lex.peek()[1] != "}":
            body.append(self.statement(d + 2))
        self.lex.consume("PUNCT")     # }
        return ("if", cond, body)

    def while_stmt(self, d):
        self.tree_lines.append(f"{self._indent(d)}WhileStmt")
        self.lex.consume("KEYWORD")
        self.lex.consume("PUNCT")
        cond = self.expr(d + 1)
        self.lex.consume("PUNCT")
        self.lex.consume("PUNCT")
        body = []
        while self.lex.peek()[1] != "}":
            body.append(self.statement(d + 2))
        self.lex.consume("PUNCT")
        return ("while", cond, body)

    def assign_stmt(self, d):
        _, name = self.lex.consume("ID")
        self.tree_lines.append(f"{self._indent(d)}AssignStmt  [{name}]")
        self.lex.consume("OP")        # =
        e = self.expr(d + 1)
        self.lex.consume("PUNCT")     # ;
        return ("assign", name, e)

    def expr(self, d):
        node = self.comparison(d)
        return node

    def comparison(self, d):
        left = self.additive(d)
        k, v = self.lex.peek()
        if k == "OP" and v in ("<", ">", "==", "!=", "<=", ">="):
            self.lex.consume()
            right = self.additive(d)
            self.tree_lines.append(f"{self._indent(d)}BinaryOp  [{v}]")
            return ("binop", v, left, right)
        return left

    def additive(self, d):
        left = self.multiplicative(d)
        while True:
            k, v = self.lex.peek()
            if k == "OP" and v in ("+", "-"):
                self.lex.consume()
                right = self.multiplicative(d)
                self.tree_lines.append(f"{self._indent(d)}BinaryOp  [{v}]")
                left = ("binop", v, left, right)
            else:
                break
        return left

    def multiplicative(self, d):
        left = self.primary(d)
        while True:
            k, v = self.lex.peek()
            if k == "OP" and v in ("*", "/"):
                self.lex.consume()
                right = self.primary(d)
                self.tree_lines.append(f"{self._indent(d)}BinaryOp  [{v}]")
                left = ("binop", v, left, right)
            else:
                break
        return left

    def primary(self, d):
        k, v = self.lex.peek()
        if k == "INT":
            self.lex.consume()
            self.tree_lines.append(f"{self._indent(d)}IntLiteral  [{v}]")
            return ("int", int(v))
        if k == "FLOAT":
            self.lex.consume()
            self.tree_lines.append(f"{self._indent(d)}FloatLiteral  [{v}]")
            return ("float", float(v))
        if k == "STRING":
            self.lex.consume()
            self.tree_lines.append(f"{self._indent(d)}StringLiteral  [{v}]")
            return ("str", v[1:-1])
        if k == "KEYWORD" and v in ("true", "false"):
            self.lex.consume()
            self.tree_lines.append(f"{self._indent(d)}BoolLiteral  [{v}]")
            return ("bool", v == "true")
        if k == "ID":
            self.lex.consume()
            self.tree_lines.append(f"{self._indent(d)}Identifier  [{v}]")
            return ("id", v)
        if k == "PUNCT" and v == "(":
            self.lex.consume()
            e = self.expr(d)
            self.lex.consume("PUNCT")
            return e
        raise SyntaxError(f"Unexpected {v!r}")


class Interpreter:
    def __init__(self):
        self.variables  = {}   # symbol table: name -> value
        self.output     = []
        self.mem_log    = []   # runtime memory events

    def run(self, node):
        kind = node[0]
        if kind == "program":
            for s in node[1]:
                self.run(s)
        elif kind == "assign":
            _, name, expr = node
            val = self.eval(expr)
            self.variables[name] = val
            self.mem_log.append(("STORE", name, val))
        elif kind == "print":
            val = self.eval(node[1])
            self.output.append(str(val))
            self.mem_log.append(("PRINT", str(val), ""))
        elif kind == "if":
            if self.eval(node[1]):
                for s in node[2]: self.run(s)
        elif kind == "while":
            limit = 0
            while self.eval(node[1]):
                for s in node[2]: self.run(s)
                limit += 1
                if limit > 1000:
                    raise RuntimeError("Infinite loop detected (>1000 iterations)")

    def eval(self, node):
        kind = node[0]
        if kind in ("int", "float", "str", "bool"):
            return node[1]
        if kind == "id":
            name = node[1]
            if name not in self.variables:
                raise NameError(f"Undefined variable '{name}'")
            self.mem_log.append(("LOAD", name, self.variables[name]))
            return self.variables[name]
        if kind == "binop":
            _, op, l, r = node
            lv, rv = self.eval(l), self.eval(r)
            ops = {"+": lv+rv, "-": lv-rv, "*": lv*rv,
                   "<": lv<rv, ">": lv>rv, "==": lv==rv,
                   "!=": lv!=rv, "<=": lv<=rv, ">=": lv>=rv}
            if op == "/":
                if rv == 0: raise ZeroDivisionError("Division by zero")
                return lv / rv
            return ops[op]
        raise RuntimeError(f"Unknown AST node: {kind}")


def run_code(source: str):
    """Returns (output_str, error_str, tokens, parse_tree_str, symbol_table, mem_log)"""
    try:
        tokens = tokenize(source)
        p      = Parser(source)
        ast    = p.parse()
        interp = Interpreter()
        interp.run(ast)
        return (
            "\n".join(interp.output),
            None,
            tokens,
            "\n".join(p.tree_lines),
            dict(interp.variables),
            interp.mem_log,
        )
    except Exception as e:
        toks = []
        try: toks = tokenize(source)
        except: pass
        return (None, str(e), toks, "", {}, [])


# ─────────────────────────────────────────────────────────────
#  IDE
# ─────────────────────────────────────────────────────────────

DARK_BG   = "#0f1117"
PANEL_BG  = "#161b22"
BORDER    = "#30363d"
ACCENT    = "#58a6ff"
GREEN     = "#3fb950"
ORANGE    = "#d29922"
RED       = "#f85149"
PURPLE    = "#bc8cff"
CYAN      = "#76e3ea"
FG        = "#e6edf3"
FG_DIM    = "#8b949e"
# Font objects are created in IDE.__init__ using tkfont.Font for live zoom support
FONT_SIZE_DEFAULT = 14

TOKEN_COLORS = {
    "KEYWORD": "#ff7b72",
    "ID":      "#79c0ff",
    "INT":     "#a5d6ff",
    "FLOAT":   "#a5d6ff",
    "STRING":  "#a8d7a8",
    "OP":      "#f0883e",
    "PUNCT":   FG_DIM,
    "COMMENT": "#6e7681",
    "UNKNOWN": RED,
}

SAMPLE = '''\
x = 10;
y = 3;
z = x + y * 2;
print(z);

i = 0;
while (i < 3) {
    print(i);
    i = i + 1;
}

if (z > 10) {
    print("big number");
}
'''


class IDE:
    FONT_SIZE_MIN = 8
    FONT_SIZE_MAX = 32

    def __init__(self, root):
        self.root = root
        self.root.title("MyLang IDE")
        self.root.geometry("1300x820")
        self.root.configure(bg=DARK_BG)
        self.current_file = None
        self.font_size = FONT_SIZE_DEFAULT

        # Named font objects — updating these instantly reflows ALL widgets using them
        self.font_mono = tkfont.Font(family="Consolas", size=self.font_size)
        self.font_tree = tkfont.Font(family="Consolas", size=self.font_size - 1)

        self._configure_styles()
        self._build_ui()
        # Now that font objects exist, apply them to the Treeview style
        ttk.Style().configure("Treeview",
                               font=self.font_tree,
                               rowheight=int(self.font_size * 2.0))
        self._setup_editor_tags()
        self._bind_shortcuts()
        # Load sample code
        self.editor.insert("1.0", SAMPLE)
        self._on_key()

    # ── Zoom ─────────────────────────────────────────────────

    def _zoom(self, delta):
        new_size = max(self.FONT_SIZE_MIN,
                       min(self.FONT_SIZE_MAX, self.font_size + delta))
        self.font_size = new_size
        tree_size = max(self.FONT_SIZE_MIN, new_size - 1)

        # Updating named Font objects instantly reflows every widget using them
        self.font_mono.configure(size=new_size)
        self.font_tree.configure(size=tree_size)

        # Row height must be updated separately on the style
        style = ttk.Style()
        style.configure("Treeview", rowheight=int(new_size * 2.0))

        self.status_var.set(f"  🔎 {new_size}pt  (Ctrl+0 to reset)")
        self._update_line_numbers()

    def zoom_in(self,   event=None): self._zoom(+1)
    def zoom_out(self,  event=None): self._zoom(-1)
    def zoom_reset(self, event=None): self._zoom(14 - self.font_size)

    # ── styles ───────────────────────────────────────────────

    def _configure_styles(self):
        style = ttk.Style()
        style.theme_use("clam")
        style.configure("TNotebook",
                         background=PANEL_BG, borderwidth=0, tabmargins=0)
        style.configure("TNotebook.Tab",
                         background=DARK_BG, foreground=FG_DIM,
                         font=("Segoe UI", 10, "bold"),
                         padding=[14, 6], borderwidth=0)
        style.map("TNotebook.Tab",
                  background=[("selected", PANEL_BG)],
                  foreground=[("selected", ACCENT)])
        style.configure("Treeview",
                         background=PANEL_BG, foreground=FG,
                         fieldbackground=PANEL_BG,
                         font=("Consolas", 13), rowheight=28, borderwidth=0)
        style.configure("Treeview.Heading",
                         background=DARK_BG, foreground=ACCENT,
                         font=("Segoe UI", 10, "bold"), relief="flat")
        style.map("Treeview", background=[("selected", "#1f3a5f")])
        style.configure("VSash.TPanedwindow", background=BORDER)

    # ── UI layout ─────────────────────────────────────────────

    def _build_ui(self):
        self._build_toolbar()

        # Main horizontal split: editor | debug panels
        h_pane = tk.PanedWindow(self.root, orient=tk.HORIZONTAL,
                                 bg=BORDER, sashwidth=5,
                                 sashrelief=tk.FLAT, bd=0,
                                 sashcursor="sb_h_double_arrow")
        h_pane.pack(fill=tk.BOTH, expand=True)

        # ── Left: editor + output ────────────────────────────
        left = tk.Frame(h_pane, bg=DARK_BG)
        v_pane = tk.PanedWindow(left, orient=tk.VERTICAL,
                                 bg=BORDER, sashwidth=5,
                                 sashrelief=tk.FLAT, bd=0,
                                 sashcursor="sb_v_double_arrow")
        v_pane.pack(fill=tk.BOTH, expand=True)

        editor_frame = self._build_editor(v_pane)
        v_pane.add(editor_frame, height=480)

        output_frame = self._build_output(v_pane)
        v_pane.add(output_frame, height=140)

        h_pane.add(left, width=660)

        # ── Right: debug notebook ────────────────────────────
        right = tk.Frame(h_pane, bg=PANEL_BG)
        self._build_debug_notebook(right)
        h_pane.add(right, width=600)

    def _build_toolbar(self):
        bar = tk.Frame(self.root, bg="#0d1117", pady=0)
        bar.pack(fill=tk.X)

        # Logo
        tk.Label(bar, text="  ⬡ MyLang", bg="#0d1117",
                 fg=ACCENT, font=("Segoe UI", 14, "bold")).pack(side=tk.LEFT, padx=(6, 16))

        btn_cfg = [
            ("⊞ New",  self.new_file,  "#21262d", FG),
            ("⊘ Open", self.open_file, "#21262d", FG),
            ("⊙ Save", self.save_file, "#21262d", FG),
            ("▶  Run", self.run_code,  GREEN,     "#0d1117"),
        ]
        for label, cmd, bg, fg in btn_cfg:
            b = tk.Button(bar, text=label, command=cmd,
                          bg=bg, fg=fg, relief=tk.FLAT,
                          font=("Segoe UI", 11, "bold"),
                          padx=14, pady=6,
                          activebackground=ACCENT,
                          activeforeground="#0d1117",
                          cursor="hand2", bd=0)
            b.pack(side=tk.LEFT, padx=2, pady=4)

        # Zoom controls (right side)
        tk.Frame(bar, bg="#30363d", width=1).pack(side=tk.RIGHT, fill=tk.Y, pady=4, padx=4)
        for label, cmd in [("−", self.zoom_out), ("⊙", self.zoom_reset), ("+", self.zoom_in)]:
            tk.Button(bar, text=label, command=cmd,
                      bg="#21262d", fg=FG, relief=tk.FLAT,
                      font=("Segoe UI", 12, "bold"),
                      padx=8, pady=6,
                      activebackground=ACCENT, activeforeground="#0d1117",
                      cursor="hand2", bd=0
                      ).pack(side=tk.RIGHT, padx=1, pady=4)

        self.status_var = tk.StringVar(value="Ready")
        tk.Label(bar, textvariable=self.status_var,
                 bg="#0d1117", fg=FG_DIM,
                 font=("Segoe UI", 10)).pack(side=tk.RIGHT, padx=10)

        sep = tk.Frame(self.root, bg=BORDER, height=1)
        sep.pack(fill=tk.X)

    def _build_editor(self, parent):
        frame = tk.Frame(parent, bg=DARK_BG)

        # Header
        hdr = tk.Frame(frame, bg="#0d1117")
        hdr.pack(fill=tk.X)
        tk.Label(hdr, text="  EDITOR", bg="#0d1117",
                 fg=FG_DIM, font=("Segoe UI", 10, "bold")).pack(side=tk.LEFT, pady=3)
        self.file_label = tk.Label(hdr, text="untitled.ml",
                                   bg="#0d1117", fg=ACCENT,
                                   font=("Segoe UI", 10))
        self.file_label.pack(side=tk.LEFT, padx=6)

        body = tk.Frame(frame, bg=DARK_BG)
        body.pack(fill=tk.BOTH, expand=True)

        # Line numbers
        self.line_numbers = tk.Text(body, width=4, bg="#0d1117",
                                    fg="#3d444d", state=tk.DISABLED,
                                    relief=tk.FLAT, font=self.font_mono,
                                    padx=4, cursor="arrow")
        self.line_numbers.pack(side=tk.LEFT, fill=tk.Y)

        tk.Frame(body, bg=BORDER, width=1).pack(side=tk.LEFT, fill=tk.Y)

        self.editor = scrolledtext.ScrolledText(
            body, wrap=tk.NONE, bg=DARK_BG, fg=FG,
            insertbackground=ACCENT, font=self.font_mono,
            relief=tk.FLAT, undo=True, padx=10, pady=6,
            selectbackground="#1f3a5f", selectforeground=FG)
        self.editor.pack(fill=tk.BOTH, expand=True)
        self.editor.bind("<KeyRelease>", self._on_key)
        self.editor.bind("<ButtonRelease>", self._update_cursor_pos)

        return frame

    def _build_output(self, parent):
        frame = tk.Frame(parent, bg=PANEL_BG)
        hdr = tk.Frame(frame, bg="#0d1117")
        hdr.pack(fill=tk.X)
        tk.Label(hdr, text="  OUTPUT", bg="#0d1117",
                 fg=FG_DIM, font=("Segoe UI", 10, "bold")).pack(side=tk.LEFT, pady=3)
        tk.Button(hdr, text="✕ Clear", command=self._clear_output,
                  bg="#0d1117", fg=FG_DIM, relief=tk.FLAT,
                  font=("Segoe UI", 10), cursor="hand2", bd=0
                  ).pack(side=tk.RIGHT, padx=6)

        self.output = scrolledtext.ScrolledText(
            frame, bg=PANEL_BG, fg=GREEN,
            font=self.font_mono, state=tk.DISABLED,
            relief=tk.FLAT, padx=10, pady=6,
            insertbackground=GREEN)
        self.output.pack(fill=tk.BOTH, expand=True)
        self.output.tag_config("error", foreground=RED)
        self.output.tag_config("info",  foreground=FG_DIM)
        return frame

    def _build_debug_notebook(self, parent):
        self.nb = ttk.Notebook(parent)
        self.nb.pack(fill=tk.BOTH, expand=True, padx=1, pady=1)

        self._build_scanner_tab()
        self._build_parser_tab()
        self._build_symtable_tab()
        self._build_memory_tab()

    # ── Scanner tab ──────────────────────────────────────────

    def _build_scanner_tab(self):
        frame = tk.Frame(self.nb, bg=PANEL_BG)
        self.nb.add(frame, text="  🔍 Scanner  ")

        hdr = tk.Frame(frame, bg=PANEL_BG)
        hdr.pack(fill=tk.X, padx=8, pady=(6, 2))
        tk.Label(hdr, text="Token Stream", bg=PANEL_BG,
                 fg=ACCENT, font=("Segoe UI", 10, "bold")).pack(side=tk.LEFT)
        self.token_count_var = tk.StringVar(value="0 tokens")
        tk.Label(hdr, textvariable=self.token_count_var,
                 bg=PANEL_BG, fg=FG_DIM, font=("Segoe UI", 10)).pack(side=tk.RIGHT)

        cols = ("#", "Type", "Value", "Pos")
        self.token_tree = ttk.Treeview(frame, columns=cols,
                                        show="headings", selectmode="browse")
        widths = [40, 90, 200, 60]
        for col, w in zip(cols, widths):
            self.token_tree.heading(col, text=col)
            self.token_tree.column(col, width=w, minwidth=w, anchor=tk.W)

        sb = ttk.Scrollbar(frame, orient=tk.VERTICAL,
                            command=self.token_tree.yview)
        self.token_tree.configure(yscrollcommand=sb.set)
        self.token_tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=(6, 0), pady=4)
        sb.pack(side=tk.RIGHT, fill=tk.Y, pady=4, padx=(0, 4))

        # colour tags on treeview rows via tag_configure
        for ttype, color in TOKEN_COLORS.items():
            self.token_tree.tag_configure(ttype, foreground=color)

    # ── Parser tab ───────────────────────────────────────────

    def _build_parser_tab(self):
        frame = tk.Frame(self.nb, bg=PANEL_BG)
        self.nb.add(frame, text="  🌳 Parse Tree  ")

        hdr = tk.Frame(frame, bg=PANEL_BG)
        hdr.pack(fill=tk.X, padx=8, pady=(6, 2))
        tk.Label(hdr, text="AST / Parse Tree", bg=PANEL_BG,
                 fg=ACCENT, font=("Segoe UI", 10, "bold")).pack(side=tk.LEFT)

        self.parse_tree_text = scrolledtext.ScrolledText(
            frame, bg=PANEL_BG, fg=FG,
            font=self.font_tree, relief=tk.FLAT,
            padx=10, pady=6, state=tk.DISABLED)
        self.parse_tree_text.pack(fill=tk.BOTH, expand=True, padx=4, pady=4)

        self.parse_tree_text.tag_config("node",    foreground=CYAN)
        self.parse_tree_text.tag_config("leaf",    foreground=GREEN)
        self.parse_tree_text.tag_config("bracket", foreground=ORANGE)
        self.parse_tree_text.tag_config("indent",  foreground="#30363d")

    # ── Symbol Table tab ─────────────────────────────────────

    def _build_symtable_tab(self):
        frame = tk.Frame(self.nb, bg=PANEL_BG)
        self.nb.add(frame, text="  📋 Symbols  ")

        hdr = tk.Frame(frame, bg=PANEL_BG)
        hdr.pack(fill=tk.X, padx=8, pady=(6, 2))
        tk.Label(hdr, text="Symbol Table", bg=PANEL_BG,
                 fg=ACCENT, font=("Segoe UI", 10, "bold")).pack(side=tk.LEFT)
        self.sym_count_var = tk.StringVar(value="0 symbols")
        tk.Label(hdr, textvariable=self.sym_count_var,
                 bg=PANEL_BG, fg=FG_DIM, font=("Segoe UI", 10)).pack(side=tk.RIGHT)

        cols = ("Name", "Type", "Value")
        self.sym_tree = ttk.Treeview(frame, columns=cols,
                                      show="headings", selectmode="browse")
        for col, w in zip(cols, [120, 90, 200]):
            self.sym_tree.heading(col, text=col)
            self.sym_tree.column(col, width=w, minwidth=w, anchor=tk.W)

        sb = ttk.Scrollbar(frame, orient=tk.VERTICAL,
                            command=self.sym_tree.yview)
        self.sym_tree.configure(yscrollcommand=sb.set)
        self.sym_tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=(6, 0), pady=4)
        sb.pack(side=tk.RIGHT, fill=tk.Y, pady=4, padx=(0, 4))

        self.sym_tree.tag_configure("int",   foreground="#a5d6ff")
        self.sym_tree.tag_configure("float", foreground="#ffa657")
        self.sym_tree.tag_configure("str",   foreground=GREEN)
        self.sym_tree.tag_configure("bool",  foreground=PURPLE)

    # ── Runtime Memory tab ───────────────────────────────────

    def _build_memory_tab(self):
        frame = tk.Frame(self.nb, bg=PANEL_BG)
        self.nb.add(frame, text="  💾 Memory  ")

        hdr = tk.Frame(frame, bg=PANEL_BG)
        hdr.pack(fill=tk.X, padx=8, pady=(6, 2))
        tk.Label(hdr, text="Runtime Memory Log", bg=PANEL_BG,
                 fg=ACCENT, font=("Segoe UI", 10, "bold")).pack(side=tk.LEFT)
        tk.Button(hdr, text="✕ Clear", command=self._clear_mem_log,
                  bg=PANEL_BG, fg=FG_DIM, relief=tk.FLAT,
                  font=("Segoe UI", 10), cursor="hand2", bd=0
                  ).pack(side=tk.RIGHT)

        cols = ("#", "Op", "Name / Value", "Data")
        self.mem_tree = ttk.Treeview(frame, columns=cols,
                                      show="headings", selectmode="browse")
        for col, w in zip(cols, [40, 70, 160, 140]):
            self.mem_tree.heading(col, text=col)
            self.mem_tree.column(col, width=w, minwidth=w, anchor=tk.W)

        sb = ttk.Scrollbar(frame, orient=tk.VERTICAL,
                            command=self.mem_tree.yview)
        self.mem_tree.configure(yscrollcommand=sb.set)
        self.mem_tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=(6, 0), pady=4)
        sb.pack(side=tk.RIGHT, fill=tk.Y, pady=4, padx=(0, 4))

        self.mem_tree.tag_configure("STORE", foreground=GREEN)
        self.mem_tree.tag_configure("LOAD",  foreground=CYAN)
        self.mem_tree.tag_configure("PRINT", foreground=ORANGE)

        self._mem_row = 0

    # ── Editor helpers ────────────────────────────────────────

    def _setup_editor_tags(self):
        hl = {
            "keyword": "#ff7b72",
            "string":  "#a8d7a8",
            "number":  "#a5d6ff",
            "op":      "#f0883e",
            "comment": "#6e7681",
            "id":      FG,
        }
        for tag, color in hl.items():
            self.editor.tag_config(tag, foreground=color)

    def _highlight(self):
        for tag in ("keyword", "string", "number", "op", "comment", "id"):
            self.editor.tag_remove(tag, "1.0", tk.END)
        patterns = [
            ("comment", r"//[^\n]*"),
            ("string",  r'"[^"\n]*"'),
            ("keyword", r"\b(if|else|while|print|true|false)\b"),
            ("number",  r"\b\d+\.?\d*\b"),
            ("op",      r"[+\-*/<>=!]=?|[{}();,]"),
            ("id",      r"\b[a-zA-Z_]\w*\b"),
        ]
        content = self.editor.get("1.0", tk.END)
        for tag, pat in patterns:
            for m in re.finditer(pat, content):
                s = f"1.0+{m.start()}c"
                e = f"1.0+{m.end()}c"
                self.editor.tag_add(tag, s, e)

    def _update_line_numbers(self):
        content   = self.editor.get("1.0", tk.END)
        line_count = content.count("\n")
        nums = "\n".join(str(i) for i in range(1, line_count + 1))
        self.line_numbers.config(state=tk.NORMAL)
        self.line_numbers.delete("1.0", tk.END)
        self.line_numbers.insert("1.0", nums)
        self.line_numbers.config(state=tk.DISABLED)

    def _update_cursor_pos(self, event=None):
        pos  = self.editor.index(tk.INSERT)
        line, col = pos.split(".")
        self.status_var.set(f"Ln {line}, Col {int(col)+1}")

    def _on_key(self, event=None):
        self._highlight()
        self._update_line_numbers()
        self._update_cursor_pos()

    # ── Panel updaters ────────────────────────────────────────

    def _update_scanner(self, tokens):
        self.token_tree.delete(*self.token_tree.get_children())
        for i, (kind, val, pos) in enumerate(tokens, 1):
            display_val = val if len(val) <= 30 else val[:27] + "…"
            self.token_tree.insert("", tk.END,
                                    values=(i, kind, display_val, pos),
                                    tags=(kind,))
        self.token_count_var.set(f"{len(tokens)} tokens")

    def _update_parse_tree(self, tree_text: str):
        self.parse_tree_text.config(state=tk.NORMAL)
        self.parse_tree_text.delete("1.0", tk.END)
        if not tree_text:
            self.parse_tree_text.insert(tk.END, "(no tree — fix errors first)",
                                          "node")
            self.parse_tree_text.config(state=tk.DISABLED)
            return

        for line in tree_text.splitlines():
            stripped = line.lstrip()
            indent   = line[: len(line) - len(stripped)]
            # colour indent guides
            self.parse_tree_text.insert(tk.END, indent, "indent")
            # detect leaf vs node
            if "[" in stripped:
                node_part, rest = stripped.split("[", 1)
                self.parse_tree_text.insert(tk.END, node_part, "node")
                self.parse_tree_text.insert(tk.END, "[", "bracket")
                val_part, _ = rest.split("]", 1)
                self.parse_tree_text.insert(tk.END, val_part, "leaf")
                self.parse_tree_text.insert(tk.END, "]\n", "bracket")
            else:
                self.parse_tree_text.insert(tk.END, stripped + "\n", "node")

        self.parse_tree_text.config(state=tk.DISABLED)

    def _update_symbol_table(self, symbols: dict):
        self.sym_tree.delete(*self.sym_tree.get_children())
        for name, val in sorted(symbols.items()):
            typ = type(val).__name__
            tag = typ if typ in ("int", "float", "str", "bool") else "str"
            self.sym_tree.insert("", tk.END,
                                  values=(name, typ, repr(val)),
                                  tags=(tag,))
        self.sym_count_var.set(f"{len(symbols)} symbol{'s' if len(symbols)!=1 else ''}")

    def _update_memory_log(self, mem_log: list):
        for op, name, val in mem_log:
            self._mem_row += 1
            label = "←" if op == "STORE" else ("→" if op == "LOAD" else "»")
            self.mem_tree.insert("", tk.END,
                                  values=(self._mem_row,
                                          f"{label} {op}",
                                          str(name),
                                          str(val)),
                                  tags=(op,))
        # auto-scroll
        children = self.mem_tree.get_children()
        if children:
            self.mem_tree.see(children[-1])

    # ── Run ───────────────────────────────────────────────────

    def run_code(self):
        source = self.editor.get("1.0", tk.END)
        self.status_var.set("Running…")
        self.root.update_idletasks()

        result = run_code(source)
        out, err, tokens, tree_str, symbols, mem_log = result

        # Output panel
        self.output.config(state=tk.NORMAL)
        self.output.delete("1.0", tk.END)
        if err:
            self.output.insert(tk.END, f"❌  {err}\n", "error")
            self.status_var.set("Error")
        else:
            if out:
                self.output.insert(tk.END, out + "\n")
            else:
                self.output.insert(tk.END, "(no output)\n", "info")
            self.status_var.set("✓ Done")
        self.output.config(state=tk.DISABLED)

        # Debug panels
        self._update_scanner(tokens)
        self._update_parse_tree(tree_str)
        self._update_symbol_table(symbols)
        self._update_memory_log(mem_log)

    # ── File ops ──────────────────────────────────────────────

    def new_file(self):
        self.editor.delete("1.0", tk.END)
        self.current_file = None
        self.file_label.config(text="untitled.ml")
        self._on_key()

    def open_file(self):
        path = filedialog.askopenfilename(
            filetypes=[("MyLang", "*.ml"), ("All", "*.*")])
        if path:
            with open(path) as f:
                self.editor.delete("1.0", tk.END)
                self.editor.insert("1.0", f.read())
            self.current_file = path
            self.file_label.config(text=path.split("/")[-1])
            self._on_key()

    def save_file(self):
        path = self.current_file or filedialog.asksaveasfilename(
            defaultextension=".ml",
            filetypes=[("MyLang", "*.ml"), ("All", "*.*")])
        if path:
            with open(path, "w") as f:
                f.write(self.editor.get("1.0", tk.END))
            self.current_file = path
            self.file_label.config(text=path.split("/")[-1])
            self.status_var.set("Saved")

    def _clear_output(self):
        self.output.config(state=tk.NORMAL)
        self.output.delete("1.0", tk.END)
        self.output.config(state=tk.DISABLED)

    def _clear_mem_log(self):
        self.mem_tree.delete(*self.mem_tree.get_children())
        self._mem_row = 0

    def _bind_shortcuts(self):
        self.root.bind("<Control-r>", lambda e: self.run_code())
        self.root.bind("<F5>",        lambda e: self.run_code())
        self.root.bind("<Control-s>", lambda e: self.save_file())
        self.root.bind("<Control-o>", lambda e: self.open_file())
        self.root.bind("<Control-n>", lambda e: self.new_file())
        # Zoom — bind on root AND editor so editor keypress does not swallow events
        for widget in (self.root, self.editor):
            widget.bind("<Control-equal>",       lambda e: self.zoom_in()    or "break")
            widget.bind("<Control-plus>",        lambda e: self.zoom_in()    or "break")
            widget.bind("<Control-minus>",       lambda e: self.zoom_out()   or "break")
            widget.bind("<Control-0>",           lambda e: self.zoom_reset() or "break")
            widget.bind("<Control-KP_Add>",      lambda e: self.zoom_in()    or "break")
            widget.bind("<Control-KP_Subtract>", lambda e: self.zoom_out()   or "break")
            widget.bind("<Control-MouseWheel>",
                        lambda e: self.zoom_in() if e.delta > 0 else self.zoom_out())


if __name__ == "__main__":
    root = tk.Tk()
    IDE(root)
    root.mainloop()