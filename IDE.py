# ide.py  —  BraKet IDE
# Integrated with braket_engine.py (ANTLR4-backed scanner / parser / semantic analyser).
#
# Layout
# ──────
#   Left  : Editor (with line numbers) + Output/Diagnostics panel
#   Right : Debug notebook
#             🔍 Scanner   — full ANTLR token stream
#             🌳 Parse Tree — ANTLR toStringTree output
#             📋 Symbols   — global symbol table (name / BKType / const?)
#             ⚠  Diagnostics — semantic errors & warnings with line:col

import tkinter as tk
from tkinter import ttk, scrolledtext, filedialog, simpledialog as _tk_simpledialog
from tkinter import font as tkfont
import re

# ── Engine import ────────────────────────────────────────────
# braket_engine.py (and the ANTLR-generated BraKetLexer/Parser/Visitor)
# must be on sys.path.  A graceful fallback is provided so the IDE can
# still open even when ANTLR files are absent.
try:
    from braket_engine import analyze, BraKetResult, TokenInfo
    _ENGINE_AVAILABLE = True
except ImportError:
    _ENGINE_AVAILABLE = False


# ─────────────────────────────────────────────────────────────
#  Fallback stub (used when ANTLR runtime / generated files are missing)
# ─────────────────────────────────────────────────────────────
if not _ENGINE_AVAILABLE:
    import re as _re

    _STUB_SPEC = [
        ("FLOAT",       r"\b\d+\.\d*\b"),
        ("INT",         r"\b\d+\b"),
        ("STRING",      r'"[^"\n]*"'),
        ("CHAR",        r"'[^'\n]?'"),
        ("KEYWORD",     r"\b(if|elif|else|while|for|do|func|main|const|"
                        r"return|from|import|true|false)\b"),
        ("IDENTIFIER",  r"\b[a-zA-Z_]\w*\b"),
        ("KET_IDENTIFIER",         r"\|[a-zA-Z_]\w*>"),
        ("BRA_IDENTIFIER",         r"<[a-zA-Z_]\w*\|"),
        ("OPERATION",          r"\*\*|==|!=|<=|>=|&&|\|\||[+\-*/<>=!@%]"),
        ("OTHERS",       r"[(){}\[\];,.]"),
        ("WS",          r"[ \t\r\n]+"),
        ("UNKNOWN",     r"."),
    ]
    _STUB_RE = _re.compile("|".join(f"(?P<{n}>{p})" for n, p in _STUB_SPEC))

    class _StubToken:
        def __init__(self, i, text, type_name, line, col):
            self.index = i; self.text = text; self.type_name = type_name
            self.line = line; self.column = col

    class _StubResult:
        def __init__(self, tokens):
            self.tokens = tokens
            self.parse_tree_str = "(ANTLR engine not available — install antlr4-python3-runtime)"
            class _Sem:
                syntax_errors = ["ANTLR engine not available."]
                diagnostics   = []
                def errors(self):   return []
                def warnings(self): return []
                def has_errors(self): return True
                global_scope = type("S", (), {"_symbols": {}})()
            self.sem = _Sem()
            self.all_errors = _Sem.syntax_errors
            self.has_errors = True
            self.ic_listing = ""
            self.run        = None

    def analyze(code: str):                     # type: ignore[misc]
        tokens, line, col = [], 1, 0
        for m in _STUB_RE.finditer(code):
            kind, val = m.lastgroup, m.group()
            for ch in code[:m.start()]:
                if ch == "\n": line += 1; col = 0
                else: col += 1
            if kind == "WS": continue
            tokens.append(_StubToken(len(tokens), val, kind, line, col))
        return _StubResult(tokens)


# ─────────────────────────────────────────────────────────────
#  Colour palette
# ─────────────────────────────────────────────────────────────
DARK_BG  = "#0f1117"
PANEL_BG = "#161b22"
BORDER   = "#30363d"
ACCENT   = "#58a6ff"
GREEN    = "#3fb950"
ORANGE   = "#d29922"
RED      = "#f85149"
PURPLE   = "#bc8cff"
CYAN     = "#76e3ea"
PINK     = "#ff79c6"
FG       = "#e6edf3"
FG_DIM   = "#8b949e"

FONT_SIZE_DEFAULT = 14

# ── Token → colour mapping (ANTLR symbolic names) ────────────
TOKEN_COLORS = {
    # keywords
    "IF": "#ff7b72", "ELIF": "#ff7b72", "ELSE": "#ff7b72",
    "WHILE": "#ff7b72", "FOR": "#ff7b72", "DO": "#ff7b72",
    "FUNC": "#ff7b72", "MAIN": "#ff7b72", "CONST": "#ff7b72",
    "RETURN": "#ff7b72", "FROM": "#ff7b72", "IMPORT": "#ff7b72",
    "BOOL_TRUE": "#ff7b72", "BOOL_FALSE": "#ff7b72",
    # literals
    "INT":     "#a5d6ff",
    "FLOAT":   "#ffa657",
    "COMPLEX": "#e8b4f8",
    "STRING":  "#a8d7a8",
    "CHAR":    "#a8d7a8",
    # identifiers
    "IDENTIFIER":     "#79c0ff",
    "KET_IDENTIFIER": CYAN,
    "BRA_IDENTIFIER": PINK,
    # operators
    "ADD": "#f0883e", "SUB": "#f0883e", "MUL": "#f0883e",
    "DIV": "#f0883e", "EXP": "#f0883e", "MOD": "#f0883e",
    "ASSIGN": FG, "EQ": "#f0883e", "NEQ": "#f0883e",
    "GT": "#f0883e", "LT": "#f0883e", "GTE": "#f0883e", "LTE": "#f0883e",
    "LOGICAL_AND": "#f0883e", "LOGICAL_OR": "#f0883e", "NEG": "#f0883e",
    "TENSOR": PURPLE,
    # punctuation / misc
    "LPAREN": FG_DIM, "RPAREN": FG_DIM,
    "LSQUARE": FG_DIM, "RSQUARE": FG_DIM,
    "LCURLY": FG_DIM, "RCURLY": FG_DIM,
    "SEMICOLON": FG_DIM, "COMMA": FG_DIM, "DOT": FG_DIM,
    # fallback / stub names
    "KEYWORD": "#ff7b72",
    "OP":      "#f0883e",
    "PUNCT":   FG_DIM,
    "KET":     CYAN,
    "BRA":     PINK,
    "UNKNOWN": RED,
}

# ── BKType → colour mapping (symbol table) ───────────────────
BKTYPE_COLORS = {
    "int":      "#a5d6ff",
    "float":    "#ffa657",
    "complex":  "#e8b4f8",
    "bool":     PURPLE,
    "string":   "#a8d7a8",
    "char":     "#a8d7a8",
    "array":    CYAN,
    "struct":   ORANGE,
    "ket":      CYAN,
    "bra":      PINK,
    "operator": "#ff7b72",
    "function": GREEN,
    "pointer":  "#ff9d3a",
    "unknown":  FG_DIM,
}

# ── Sample BraKet code ────────────────────────────────────────
# TODO: Edit this also
# SAMPLE = """\
# func double_in_place(ptr) {
#     *ptr = *ptr * 2
# }

# func swap(pa, pb) {
#     temp = *pa
#     *pa  = *pb
#     *pb  = temp
# }

# func sum_via_ptrs(pa, pb) {
#     return *pa + *pb
# }

# main() {
#     print("-- Basic pointer --")
#     x   = 10
#     ptr = &x
#     print(ptr)
#     print(*ptr)

#     print("-- Modify via pointer --")
#     *ptr = 42
#     print(x)

#     print("-- Two pointers, same variable --")
#     y  = 100
#     p1 = &y
#     p2 = &y
#     *p1 = 55
#     print(*p2)

#     print("-- Function: double in place --")
#     n  = 7
#     pn = &n
#     double_in_place(pn)
#     print(n)

#     print("-- Function: sum via ptrs --")
#     a  = 3
#     b  = 8
#     pa = &a
#     pb = &b
#     print(sum_via_ptrs(pa, pb))

#     print("-- Function: swap --")
#     u = 100
#     v = 200
#     swap(&u, &v)
#     print(u)
#     print(v)

#     print("-- Pointer in condition --")
#     val = 5
#     pv  = &val
#     if (*pv > 3) {
#         print("greater than 3")
#     } else {
#         print("not greater than 3")
#     }
# }"""
SAMPLE = """\
const |ket0> = (1, 0)
const |ket1> = (0, 1)
const PI = 3.14159

func hadamard(state) {
    H = ((0.707, 0.707), (0.707, -0.707))
    return H * state
}

func get_1(){
    return 1
}

func get_state(){
    return get_1()
}

func factorial(n){
    if(n==0 || n == 1){
        return 1
    }
    val = factorial(n - 1)
    return val * n
}
    
main() {
    print("Variable Declaration")
    var_test = 5
    y      = 3.14
    flag   = true
    print(var_test)
    
    print("Structures")
    struct_test = {
    	x = 0,
     	y = 1
    }
    print(struct_test.y)
    
    print("Assignment")
    assign_test  = "BraKet"
    print(assign_test)
    assign_test = 1
    print(assign_test)
    
    print("Simple Math")
    math_test = 1+3*2
    print(math_test)
    
    print("Complex Math")
    |psi>  = |ket0> @ |ket1>
    <phi|  = (0.707, 0.707)
    inner  = <phi| * |psi>
    print(inner)

    print("Conditional Statements")
    x = 3
    if (x > 3) {
        x = x + 1
    } elif (x == 3) {
        x = 0
    } else {
        x = -1
    }
    print(x)

    print("Iterative Statements")
    print("--while--")
    i = 0
    while (i < 3) {
        i = i + 1
    }
    print(i)
    
    print("--for--")
    loop = 1
    for(i = 0; i<3; i=i+1){
    	loop = loop*2
    }
    print(loop)
    
    print("--do while--")
    x=0
    do{
    	print("hi")
     	x = x+1
    } while(x<=2)
    
    print("Complex Boolean")
    x=0
    y=3
    print((x-y-2>3-y+x)&&(x-3<2)||(x+3<y))
    
    print("Function Calling")
    |ket> = (1,1)
    func_var = hadamard(|ket>)
    print(func_var)
    
    print("Function Calling Another Function")
    print(hadamard(get_state()))
    
    print("Recursion")
    print(factorial(3))
    
    print("Nested Loop")
    val = 0
    for(i = 0; i<3; i=i+1){
    	for(j = 0; j < 3; j = j+1){
     	    val = i*j
          	 print(val)
         }
     }
}
"""


# ─────────────────────────────────────────────────────────────
#  IDE
# ─────────────────────────────────────────────────────────────
class IDE:
    FONT_SIZE_MIN = 8
    FONT_SIZE_MAX = 32

    def __init__(self, root: tk.Tk):
        self.root         = root
        self.root.title("BraKet IDE")
        self.root.geometry("1380x860")
        self.root.configure(bg=DARK_BG)
        self.current_file = None
        self.font_size    = FONT_SIZE_DEFAULT

        # ── step-debugger state ───────────────────────────────
        self._debug_snapshots  = []   # list[DebugSnapshot] from last run
        self._debug_step       = 0    # current step index
        self._debug_active     = False

        self.font_mono = tkfont.Font(family="Consolas", size=self.font_size)
        self.font_tree = tkfont.Font(family="Consolas", size=self.font_size - 1)

        self._configure_styles()
        self._build_ui()
        ttk.Style().configure("Treeview",
                               font=self.font_tree,
                               rowheight=int(self.font_size * 2.0))
        self._setup_editor_tags()
        self._bind_shortcuts()
        self.editor.insert("1.0", SAMPLE)
        self._on_key()

    # ── zoom ─────────────────────────────────────────────────

    def _zoom(self, delta: int):
        new_size = max(self.FONT_SIZE_MIN, min(self.FONT_SIZE_MAX, self.font_size + delta))
        self.font_size = new_size
        self.font_mono.configure(size=new_size)
        self.font_tree.configure(size=max(self.FONT_SIZE_MIN, new_size - 1))
        ttk.Style().configure("Treeview", rowheight=int(new_size * 2.0))
        self.status_var.set(f"  🔎 {new_size}pt  (Ctrl+0 to reset)")
        digit_w = self.font_mono.measure("0") * 4 + 10
        self.line_numbers.config(width=max(40, digit_w))
        self._update_line_numbers()

    def zoom_in(self,    event=None): self._zoom(+1)
    def zoom_out(self,   event=None): self._zoom(-1)
    def zoom_reset(self, event=None): self._zoom(FONT_SIZE_DEFAULT - self.font_size)

    # ── ttk styles ────────────────────────────────────────────

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

    # ── UI layout ─────────────────────────────────────────────

    def _build_ui(self):
        self._build_toolbar()

        h_pane = tk.PanedWindow(self.root, orient=tk.HORIZONTAL,
                                 bg=BORDER, sashwidth=5,
                                 sashrelief=tk.FLAT, bd=0)
        h_pane.pack(fill=tk.BOTH, expand=True)

        # Left: editor + output
        left   = tk.Frame(h_pane, bg=DARK_BG)
        v_pane = tk.PanedWindow(left, orient=tk.VERTICAL,
                                 bg=BORDER, sashwidth=5,
                                 sashrelief=tk.FLAT, bd=0,
                                 sashcursor="sb_v_double_arrow")
        v_pane.pack(fill=tk.BOTH, expand=True)
        v_pane.add(self._build_editor(v_pane),  height=500)
        v_pane.add(self._build_output(v_pane),  height=160)
        h_pane.add(left, width=680)

        # Right: debug notebook
        right = tk.Frame(h_pane, bg=PANEL_BG)
        self._build_debug_notebook(right)
        h_pane.add(right, width=660)

    # ── toolbar ───────────────────────────────────────────────

    def _build_toolbar(self):
        bar = tk.Frame(self.root, bg="#0d1117", pady=0)
        bar.pack(fill=tk.X)

        tk.Label(bar, text="  ⟨⟩ BraKet", bg="#0d1117",
                 fg=ACCENT, font=("Segoe UI", 14, "bold")).pack(side=tk.LEFT, padx=(6, 16))

        for label, cmd, bg, fg in [
            ("⊞ New",   self.new_file,  "#21262d", FG),
            ("⊘ Open",  self.open_file, "#21262d", FG),
            ("⊙ Save",  self.save_file, "#21262d", FG),
            ("▶  Run",  self.run_code,  GREEN,     "#0d1117"),
            ("🐛 Debug", self.start_debug, "#1f3a5f", ACCENT),
        ]:
            tk.Button(bar, text=label, command=cmd,
                      bg=bg, fg=fg, relief=tk.FLAT,
                      font=("Segoe UI", 11, "bold"),
                      padx=14, pady=6,
                      activebackground=ACCENT, activeforeground="#0d1117",
                      cursor="hand2", bd=0).pack(side=tk.LEFT, padx=2, pady=4)

        tk.Frame(bar, bg="#30363d", width=1).pack(side=tk.RIGHT, fill=tk.Y, pady=4, padx=4)
        for label, cmd in [("−", self.zoom_out), ("⊙", self.zoom_reset), ("+", self.zoom_in)]:
            tk.Button(bar, text=label, command=cmd,
                      bg="#21262d", fg=FG, relief=tk.FLAT,
                      font=("Segoe UI", 12, "bold"), padx=8, pady=6,
                      activebackground=ACCENT, activeforeground="#0d1117",
                      cursor="hand2", bd=0).pack(side=tk.RIGHT, padx=1, pady=4)

        self.status_var = tk.StringVar(value="  Ready")
        tk.Label(bar, textvariable=self.status_var,
                 bg="#0d1117", fg=FG_DIM,
                 font=("Segoe UI", 10)).pack(side=tk.RIGHT, padx=10)

        tk.Frame(self.root, bg=BORDER, height=1).pack(fill=tk.X)

    # ── editor ────────────────────────────────────────────────

    def _build_editor(self, parent):
        frame = tk.Frame(parent, bg=DARK_BG)

        hdr = tk.Frame(frame, bg="#0d1117")
        hdr.pack(fill=tk.X)
        tk.Label(hdr, text="  EDITOR", bg="#0d1117",
                 fg=FG_DIM, font=("Segoe UI", 10, "bold")).pack(side=tk.LEFT, pady=3)
        self.file_label = tk.Label(hdr, text="untitled.bk",
                                   bg="#0d1117", fg=ACCENT, font=("Segoe UI", 10))
        self.file_label.pack(side=tk.LEFT, padx=6)

        body = tk.Frame(frame, bg=DARK_BG)
        body.pack(fill=tk.BOTH, expand=True)

        # Canvas for line numbers. Numbers are drawn using dlineinfo() pixel
        # coordinates queried directly from the editor widget, so they are
        # always pixel-perfectly aligned at every scroll position.
        self.line_numbers = tk.Canvas(body, width=40, bg="#0d1117",
                                      highlightthickness=0, bd=0)
        self.line_numbers.pack(side=tk.LEFT, fill=tk.Y)
        tk.Frame(body, bg=BORDER, width=1).pack(side=tk.LEFT, fill=tk.Y)

        vscroll = tk.Scrollbar(body, orient=tk.VERTICAL, bg=PANEL_BG,
                               troughcolor=DARK_BG, relief=tk.FLAT, width=10)
        vscroll.pack(side=tk.RIGHT, fill=tk.Y)

        hscroll = tk.Scrollbar(body, orient=tk.HORIZONTAL, bg=PANEL_BG,
                               troughcolor=DARK_BG, relief=tk.FLAT, width=10)
        hscroll.pack(side=tk.BOTTOM, fill=tk.X)

        self.editor = tk.Text(
            body, wrap=tk.NONE, bg=DARK_BG, fg=FG,
            insertbackground=ACCENT, font=self.font_mono,
            relief=tk.FLAT, undo=True, padx=10, pady=6,
            selectbackground="#1f3a5f", selectforeground=FG,
            spacing1=0, spacing2=0, spacing3=0,
            yscrollcommand=self._on_editor_scroll,
            xscrollcommand=hscroll.set)
        self.editor.pack(fill=tk.BOTH, expand=True)

        vscroll.config(command=self.editor.yview)
        hscroll.config(command=self.editor.xview)

        self.editor.bind("<KeyRelease>",            self._on_key)
        self.editor.bind("<ButtonRelease>",         self._update_cursor_pos)
        self.editor.bind("<Return>",                self._on_return)
        self.editor.bind("<Tab>",                   self._on_tab)
        self.editor.bind("<Shift-Tab>",             self._on_shift_tab)
        # Auto-pair: opening characters
        self.editor.bind("<KeyPress-parenleft>",    self._on_open_paren)
        self.editor.bind("<KeyPress-bracketleft>",  self._on_open_bracket)
        self.editor.bind("<KeyPress-braceleft>",    self._on_open_brace)
        self.editor.bind("<KeyPress-quotedbl>",     self._on_quote_dbl)
        self.editor.bind("<KeyPress-apostrophe>",   self._on_quote_single)
        # Auto-pair: closing characters (skip-over or dedent)
        self.editor.bind("<KeyPress-parenright>",   self._on_close_paren)
        self.editor.bind("<KeyPress-bracketright>", self._on_close_bracket)
        self.editor.bind("<KeyPress-braceright>",   self._on_closing_brace)
        self.editor.bind("<Configure>",             lambda e: self._redraw_line_numbers())
        return frame

    # ── output / diagnostics panel ────────────────────────────

    def _build_output(self, parent):
        frame = tk.Frame(parent, bg=PANEL_BG)

        hdr = tk.Frame(frame, bg="#0d1117")
        hdr.pack(fill=tk.X)
        tk.Label(hdr, text="  OUTPUT / DIAGNOSTICS", bg="#0d1117",
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
        self.output.tag_config("error",   foreground=RED)
        self.output.tag_config("warning", foreground=ORANGE)
        self.output.tag_config("info",    foreground=FG_DIM)
        self.output.tag_config("success", foreground=GREEN)
        return frame

    # ── debug notebook ────────────────────────────────────────

    def _build_debug_notebook(self, parent):
        self.nb = ttk.Notebook(parent)
        self.nb.pack(fill=tk.BOTH, expand=True, padx=1, pady=1)
        self._build_scanner_tab()
        self._build_parser_tab()
        self._build_symtable_tab()
        self._diag_tab_frame = self._build_diag_tab()   # keep reference for auto-select
        self._build_ic_tab()
        self._build_trace_tab()


    # ── Intermediate Code tab ─────────────────────────────────

    def _build_ic_tab(self):
        frame = tk.Frame(self.nb, bg=PANEL_BG)
        self.nb.add(frame, text="  ⚙  IC  ")

        hdr = tk.Frame(frame, bg=PANEL_BG)
        hdr.pack(fill=tk.X, padx=8, pady=(6, 2))
        tk.Label(hdr, text="Intermediate Code (TAC)", bg=PANEL_BG,
                 fg=ACCENT, font=("Segoe UI", 10, "bold")).pack(side=tk.LEFT)
        self.ic_count_var = tk.StringVar(value="")
        tk.Label(hdr, textvariable=self.ic_count_var,
                 bg=PANEL_BG, fg=FG_DIM, font=("Segoe UI", 10)).pack(side=tk.RIGHT)

        self.ic_text = scrolledtext.ScrolledText(
            frame, bg=PANEL_BG, fg=FG,
            font=self.font_tree, relief=tk.FLAT,
            padx=10, pady=6, state=tk.DISABLED)
        self.ic_text.pack(fill=tk.BOTH, expand=True, padx=4, pady=4)
        self.ic_text.tag_config("label",  foreground=ACCENT,  font=("Consolas", self.font_size - 1, "bold"))
        self.ic_text.tag_config("op",     foreground=ORANGE)
        self.ic_text.tag_config("dest",   foreground=GREEN)
        self.ic_text.tag_config("jump",   foreground=PURPLE)
        self.ic_text.tag_config("call",   foreground=CYAN)
        self.ic_text.tag_config("ret",    foreground="#ff7b72")
        self.ic_text.tag_config("assign", foreground=FG)
        self.ic_text.tag_config("comment",foreground=FG_DIM)

    # ── Scanner tab ───────────────────────────────────────────

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

        cols = ("#", "Type", "Value", "Line", "Col")
        self.token_tree = ttk.Treeview(frame, columns=cols,
                                        show="headings", selectmode="browse")
        for col, w in zip(cols, [40, 130, 200, 50, 50]):
            self.token_tree.heading(col, text=col)
            self.token_tree.column(col, width=w, minwidth=w, anchor=tk.W)

        sb = ttk.Scrollbar(frame, orient=tk.VERTICAL, command=self.token_tree.yview)
        self.token_tree.configure(yscrollcommand=sb.set)
        self.token_tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=(6, 0), pady=4)
        sb.pack(side=tk.RIGHT, fill=tk.Y, pady=4, padx=(0, 4))

        for ttype, color in TOKEN_COLORS.items():
            self.token_tree.tag_configure(ttype, foreground=color)

    # ── Parser tab ────────────────────────────────────────────

    def _build_parser_tab(self):
        frame = tk.Frame(self.nb, bg=PANEL_BG)
        self.nb.add(frame, text="  🌳 Parse Tree  ")

        hdr = tk.Frame(frame, bg=PANEL_BG)
        hdr.pack(fill=tk.X, padx=8, pady=(6, 2))
        tk.Label(hdr, text="ANTLR Parse Tree", bg=PANEL_BG,
                 fg=ACCENT, font=("Segoe UI", 10, "bold")).pack(side=tk.LEFT)

        self.parse_tree_text = scrolledtext.ScrolledText(
            frame, bg=PANEL_BG, fg=FG,
            font=self.font_tree, relief=tk.FLAT,
            padx=10, pady=6, state=tk.DISABLED)
        self.parse_tree_text.pack(fill=tk.BOTH, expand=True, padx=4, pady=4)
        self.parse_tree_text.tag_config("rule",    foreground=ACCENT)
        self.parse_tree_text.tag_config("token",   foreground=GREEN)
        self.parse_tree_text.tag_config("paren",   foreground=FG_DIM)
        self.parse_tree_text.tag_config("error",   foreground=RED)

    # ── Symbol Table tab ──────────────────────────────────────

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

        # "tree headings" shows the expand/collapse arrow column plus named columns
        cols = ("Name", "BKType", "Const?", "Value", "Address")
        self.sym_tree = ttk.Treeview(frame, columns=cols,
                                      show="tree headings", selectmode="browse")
        # The implicit #0 tree column holds the scope group label
        self.sym_tree.heading("#0",      text="Scope")
        self.sym_tree.column( "#0",      width=120, minwidth=80, anchor=tk.W)
        for col, w in zip(cols, [130, 90, 55, 160, 100]):
            self.sym_tree.heading(col, text=col)
            self.sym_tree.column(col, width=w, minwidth=w, anchor=tk.W)

        sb = ttk.Scrollbar(frame, orient=tk.VERTICAL, command=self.sym_tree.yview)
        self.sym_tree.configure(yscrollcommand=sb.set)
        self.sym_tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=(6, 0), pady=4)
        sb.pack(side=tk.RIGHT, fill=tk.Y, pady=4, padx=(0, 4))

        self.sym_tree.tag_configure("scope_global", foreground=ACCENT,
                                    font=("Segoe UI", 10, "bold"))
        self.sym_tree.tag_configure("scope_func",   foreground=ORANGE,
                                    font=("Segoe UI", 10, "bold"))
        self.sym_tree.tag_configure("scope_block",  foreground=FG_DIM,
                                    font=("Segoe UI", 10, "bold"))
        for bktype, color in BKTYPE_COLORS.items():
            self.sym_tree.tag_configure(bktype, foreground=color)

    # ── Diagnostics tab ───────────────────────────────────────

    def _build_diag_tab(self):
        frame = tk.Frame(self.nb, bg=PANEL_BG)
        self.nb.add(frame, text="  ⚠  Diagnostics  ")

        hdr = tk.Frame(frame, bg=PANEL_BG)
        hdr.pack(fill=tk.X, padx=8, pady=(6, 2))
        tk.Label(hdr, text="Errors & Warnings", bg=PANEL_BG,
                 fg=ACCENT, font=("Segoe UI", 10, "bold")).pack(side=tk.LEFT)
        self.diag_count_var = tk.StringVar(value="")
        tk.Label(hdr, textvariable=self.diag_count_var,
                 bg=PANEL_BG, fg=FG_DIM, font=("Segoe UI", 10)).pack(side=tk.RIGHT)

        cols = ("Kind", "Line", "Col", "Message")
        self.diag_tree = ttk.Treeview(frame, columns=cols,
                                       show="headings", selectmode="browse")
        for col, w in zip(cols, [70, 50, 50, 360]):
            self.diag_tree.heading(col, text=col)
            self.diag_tree.column(col, width=w, minwidth=w, anchor=tk.W)

        sb = ttk.Scrollbar(frame, orient=tk.VERTICAL, command=self.diag_tree.yview)
        self.diag_tree.configure(yscrollcommand=sb.set)
        self.diag_tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=(6, 0), pady=4)
        sb.pack(side=tk.RIGHT, fill=tk.Y, pady=4, padx=(0, 4))

        self.diag_tree.tag_configure("error",   foreground=RED)
        self.diag_tree.tag_configure("warning", foreground=ORANGE)
        self.diag_tree.tag_configure("syntax",  foreground="#ff9580")

        # Double-click → jump to line in editor
        self.diag_tree.bind("<Double-1>", self._jump_to_diag)

        return frame   # caller stores this for reference-based tab selection

    # ── editor helpers ────────────────────────────────────────

    def _setup_editor_tags(self):
        cfg = {
            "kw":      "#ff7b72",
            "string":  "#a8d7a8",
            "number":  "#a5d6ff",
            "complex": "#e8b4f8",
            "op":      "#f0883e",
            "ket":     CYAN,
            "bra":     PINK,
            "tensor":  PURPLE,
            "id":      FG,
            "comment": "#6a9955",   # green — configured last = highest tag priority
        }
        for tag, color in cfg.items():
            self.editor.tag_config(tag, foreground=color)
        # error underline
        self.editor.tag_config("err_line", underline=True, foreground=RED)
        self.editor.tag_config("debug_line",
                               background="#2d3b1e",
                               foreground="#b5f0a0")

    def _highlight(self):
        for tag in ("kw", "string", "number", "complex", "op",
                    "ket", "bra", "tensor", "comment", "id"):
            self.editor.tag_remove(tag, "1.0", tk.END)

        patterns = [
            ("string",  r'"[^"\n]*"'),
            ("string",  r"'[^'\n]?'"),
            ("kw",      r"\b(if|elif|else|while|for|do|func|main|const|"
                        r"return|from|import|true|false)\b"),
            ("complex", r"[+\-]?\d*\.?\d+[+\-]\d*\.?\d*i\b|[+\-]?\d*\.?\d+i\b"),
            ("number",  r"\b\d+\.?\d*\b"),
            ("ket",     r"\|[a-zA-Z_]\w*>"),
            ("bra",     r"<[a-zA-Z_]\w*\|"),
            ("tensor",  r"@"),
            ("op",      r"\*\*|==|!=|<=|>=|&&|\|\||[+\-*/<>=!%]"),
            ("id",      r"\b[a-zA-Z_]\w*\b"),
            # Comments applied last so they override all other tags inside them
            ("comment", r"//[^\n]*"),
            ("comment", r"(?s)/\*.*?\*/"),
        ]
        content = self.editor.get("1.0", tk.END)
        for tag, pat in patterns:
            for m in re.finditer(pat, content):
                s = f"1.0+{m.start()}c"
                e = f"1.0+{m.end()}c"
                self.editor.tag_add(tag, s, e)

    def _on_editor_scroll(self, first, last):
        """Called by editor yscrollcommand; updates scrollbar and redraws numbers."""
        for w in self.editor.master.pack_slaves():
            if isinstance(w, tk.Scrollbar) and str(w.cget('orient')) == 'vertical':
                w.set(first, last)
                break
        self._redraw_line_numbers()

    def _redraw_line_numbers(self):
        """
        Redraw line numbers on the Canvas by querying dlineinfo() for every
        visible line in the editor. dlineinfo() returns the exact pixel bbox
        of each line as rendered by the editor itself, so the numbers are
        always pixel-perfectly aligned regardless of scroll position or zoom.
        """
        self.line_numbers.delete("all")
        canvas_w = self.line_numbers.winfo_width()
        if canvas_w < 2:
            return

        i = self.editor.index("@0,0")          # first visible index
        while True:
            info = self.editor.dlineinfo(i)     # (x, y, w, h, baseline)
            if info is None:
                break
            y        = info[1]                  # pixel top of this line
            h        = info[3]                  # total line height in pixels
            line_num = int(str(i).split(".")[0])
            self.line_numbers.create_text(
                canvas_w - 4,
                y + h // 2,
                anchor=tk.E,
                text=str(line_num),
                fill="#3d444d",
                font=self.font_mono)
            # Advance to the next line
            next_i = self.editor.index(f"{i} +1line")
            if next_i == i:
                break
            i = next_i

    def _update_line_numbers(self):
        """Called on key events; schedules a canvas redraw after the event loop settles."""
        self.root.after_idle(self._redraw_line_numbers)
    def _update_cursor_pos(self, event=None):
        pos  = self.editor.index(tk.INSERT)
        line, col = pos.split(".")
        self.status_var.set(f"  Ln {line}, Col {int(col)+1}")

    def _on_return(self, event=None):
        """Newline with smart indent.

        - Matches current line's indent.
        - Adds +4 after a line ending with '{'.
        - When cursor sits between '{' and '}' (auto-pair), splits into three
          lines: opening line, indented cursor line, closing-brace line.
        """
        insert_pos = self.editor.index(tk.INSERT)
        line_num   = insert_pos.split(".")[0]
        line_text  = self.editor.get(f"{line_num}.0", f"{line_num}.end")
        indent     = len(line_text) - len(line_text.lstrip())
        next_char  = self.editor.get(insert_pos, f"{insert_pos}+1c")

        if next_char == "}" and line_text[:int(insert_pos.split(".")[1])].rstrip().endswith("{"):
            # Cursor is between { and } — split into three lines
            self.editor.insert(tk.INSERT, "\n" + " " * (indent + 4) + "\n" + " " * indent)
            # Place cursor on the middle (body) line
            self.editor.mark_set(tk.INSERT, f"{int(line_num) + 1}.{indent + 4}")
        else:
            extra = 4 if line_text.rstrip().endswith("{") else 0
            self.editor.insert(tk.INSERT, "\n" + " " * (indent + extra))

        self._on_key()
        return "break"

    def _on_tab(self, event=None):
        """Insert 4 spaces instead of a tab character."""
        self.editor.insert(tk.INSERT, "    ")
        self._on_key()
        return "break"

    def _on_shift_tab(self, event=None):
        """Remove up to 4 leading spaces from the current line (dedent)."""
        insert_pos = self.editor.index(tk.INSERT)
        line_num   = insert_pos.split(".")[0]
        line_start = f"{line_num}.0"
        line_text  = self.editor.get(line_start, f"{line_num}.end")
        spaces     = len(line_text) - len(line_text.lstrip(" "))
        remove     = min(4, spaces)
        if remove:
            self.editor.delete(line_start, f"{line_num}.{remove}")
        self._on_key()
        return "break"

    # ── auto-pair helpers ─────────────────────────────────────

    def _insert_pair(self, open_ch, close_ch):
        """Insert open+close and leave cursor between them."""
        self.editor.insert(tk.INSERT, open_ch + close_ch)
        pos = self.editor.index(tk.INSERT)
        self.editor.mark_set(tk.INSERT, f"{pos}-1c")
        self._on_key()
        return "break"

    def _skip_or_insert(self, close_ch):
        """Skip over an auto-inserted closer; otherwise insert it normally."""
        pos       = self.editor.index(tk.INSERT)
        next_char = self.editor.get(pos, f"{pos}+1c")
        if next_char == close_ch:
            self.editor.mark_set(tk.INSERT, f"{pos}+1c")
            self._on_key()
            return "break"
        self.editor.insert(tk.INSERT, close_ch)
        self._on_key()
        return "break"

    def _on_open_paren(self,   event=None): return self._insert_pair("(", ")")
    def _on_open_bracket(self, event=None): return self._insert_pair("[", "]")
    def _on_open_brace(self,   event=None): return self._insert_pair("{", "}")
    def _on_close_paren(self,  event=None): return self._skip_or_insert(")")
    def _on_close_bracket(self,event=None): return self._skip_or_insert("]")

    def _on_quote_dbl(self, event=None):
        pos       = self.editor.index(tk.INSERT)
        next_char = self.editor.get(pos, f"{pos}+1c")
        if next_char == '"':          # skip over existing closing quote
            self.editor.mark_set(tk.INSERT, f"{pos}+1c")
            self._on_key()
            return "break"
        return self._insert_pair('"', '"')

    def _on_quote_single(self, event=None):
        pos       = self.editor.index(tk.INSERT)
        next_char = self.editor.get(pos, f"{pos}+1c")
        if next_char == "'":          # skip over existing closing quote
            self.editor.mark_set(tk.INSERT, f"{pos}+1c")
            self._on_key()
            return "break"
        return self._insert_pair("'", "'")

    def _on_closing_brace(self, event=None):
        """Skip-over auto-inserted '}', or auto-dedent when at line start."""
        insert_pos    = self.editor.index(tk.INSERT)
        line_num      = insert_pos.split(".")[0]
        line_start    = f"{line_num}.0"
        before_cursor = self.editor.get(line_start, insert_pos)
        next_char     = self.editor.get(insert_pos, f"{insert_pos}+1c")

        if next_char == "}":                      # skip over auto-inserted '}'
            self.editor.mark_set(tk.INSERT, f"{insert_pos}+1c")
            self._on_key()
            return "break"

        if before_cursor.strip() == "":           # auto-dedent at line start
            spaces = len(before_cursor)
            remove = min(4, spaces)
            if remove:
                self.editor.delete(line_start, f"{line_num}.{remove}")

        self.editor.insert(tk.INSERT, "}")
        self._on_key()
        return "break"

    def _on_key(self, event=None):
        self._highlight()
        self._update_line_numbers()
        self._update_cursor_pos()

    # ── panel updaters ────────────────────────────────────────

    def _update_scanner(self, tokens):
        self.token_tree.delete(*self.token_tree.get_children())
        for tok in tokens:
            display = tok.text if len(tok.text) <= 28 else tok.text[:25] + "…"
            tag     = tok.type_name if tok.type_name in TOKEN_COLORS else "IDENTIFIER"
            self.token_tree.insert("", tk.END,
                                    values=(tok.index + 1, tok.type_name,
                                            display, tok.line, tok.column),
                                    tags=(tag,))
        self.token_count_var.set(f"{len(tokens)} token{'s' if len(tokens) != 1 else ''}")

    def _update_parse_tree(self, tree_text: str):
        self.parse_tree_text.config(state=tk.NORMAL)
        self.parse_tree_text.delete("1.0", tk.END)

        if not tree_text or tree_text.startswith("(ANTLR"):
            self.parse_tree_text.insert(tk.END, tree_text or "(no tree)", "error")
            self.parse_tree_text.config(state=tk.DISABLED)
            return

        # Pretty-print: indent on each '(' and de-indent on ')'
        depth = 0
        i     = 0
        while i < len(tree_text):
            ch = tree_text[i]
            if ch == "(":
                self.parse_tree_text.insert(tk.END, "\n" + "  " * depth, "paren")
                self.parse_tree_text.insert(tk.END, "(", "paren")
                depth += 1
                # rule name follows immediately
                j = i + 1
                while j < len(tree_text) and tree_text[j] not in (" ", "(", ")"):
                    j += 1
                rule = tree_text[i+1:j]
                self.parse_tree_text.insert(tk.END, rule, "rule")
                i = j
                continue
            elif ch == ")":
                depth = max(0, depth - 1)
                self.parse_tree_text.insert(tk.END, ")", "paren")
            elif ch == " ":
                # token value between spaces
                j = i + 1
                while j < len(tree_text) and tree_text[j] not in ("(", ")"):
                    j += 1
                val = tree_text[i:j].strip()
                if val:
                    self.parse_tree_text.insert(tk.END, " " + val, "token")
                i = j
                continue
            i += 1

        self.parse_tree_text.config(state=tk.DISABLED)

    def _update_symbol_table(self, global_scope, closed_scopes=None):
        """Populate symbol table from semantic analysis scopes (no runtime values)."""
        self.sym_tree.delete(*self.sym_tree.get_children())
        
        total = 0

        def _insert_scope(scope, label, scope_tag):
            nonlocal total
            syms = scope._symbols
            if not syms:
                return
            # Parent row — scope header (no symbol columns)
            parent = self.sym_tree.insert(
                "", tk.END, text=f"  {label}",
                values=("", "", "", "", ""), tags=(scope_tag,), open=True)
            for name, sym in sorted(syms.items()):
                bkt      = sym.bk_type
                is_const = "✓" if sym.is_const else ""
                val_str  = str(sym.literal_value) if sym.literal_value is not None else "—"
                tag      = bkt if bkt in BKTYPE_COLORS else "unknown"
                self.sym_tree.insert(parent, tk.END, text="",
                                      values=(name, bkt, is_const, val_str, "—"),
                                      tags=(tag,))
                total += 1

        # Always show the global scope first
        _insert_scope(global_scope, "global", "scope_global")

        # Then each closed scope (functions, main, if/for/while blocks)
        if closed_scopes:
            for scope in closed_scopes:
                sname = scope.scope_name
                if sname.startswith("func:"):
                    label     = f"func  {sname[5:]}"
                    scope_tag = "scope_func"
                elif sname == "main":
                    label     = "main"
                    scope_tag = "scope_func"
                else:
                    label     = sname
                    scope_tag = "scope_block"
                _insert_scope(scope, label, scope_tag)

        self.sym_count_var.set(f"{total} symbol{'s' if total != 1 else ''}")

    def _update_runtime_symbols(self, symbol_table: dict,
                                 function_scopes: dict | None = None,
                                 var_addrs: dict | None = None,
                                 tmp_table: dict | None = None):
        """Populate symbol table from the interpreter's live runtime values."""
        self.sym_tree.delete(*self.sym_tree.get_children())
        total = 0
        var_addrs = var_addrs or {}

        type_map = {
            "int": "int", "float": "float", "complex": "complex",
            "bool": "bool", "str": "string",
            "BKVector": "ket/bra", "BKOperator": "operator",
            "BKArray": "array", "BKStruct": "struct",
            "BKPointer": "pointer",
            "NoneType": "unknown",
        }

        def _insert_runtime_scope(label, scope_tag, items, freed=False):
            nonlocal total
            if not items:
                return
            parent = self.sym_tree.insert(
                "", tk.END, text=f"  {label}",
                values=("", "", "", "", ""), tags=(scope_tag,), open=True)
            for name, val in sorted(items):
                type_name = type(val).__name__
                bkt       = type_map.get(type_name, type_name)
                val_str   = str(val)
                val_str   = val_str[:38] + "…" if len(val_str) > 38 else val_str
                addr      = var_addrs.get(name)
                if addr is not None:
                    addr_str = f"0x{addr:04X} [freed]" if freed else f"0x{addr:04X}"
                else:
                    addr_str = "—"
                tag       = bkt if bkt in BKTYPE_COLORS else "unknown"
                self.sym_tree.insert(parent, tk.END, text="",
                                      values=(name, bkt, "", val_str, addr_str),
                                      tags=(tag,))
                total += 1

        # Global / main scope
        _insert_runtime_scope("global / main", "scope_global",
                               symbol_table.items())

        # Per-function scopes
        if function_scopes:
            for fname, frame in sorted(function_scopes.items()):
                _insert_runtime_scope(f"func  {fname}", "scope_func",
                                       frame.items())

        # Temporaries (addresses freed at end of execution)
        if tmp_table:
            _insert_runtime_scope("temporaries (freed)", "scope_block",
                                   tmp_table.items(), freed=True)

        self.sym_count_var.set(
            f"{total} symbol{'s' if total != 1 else ''} (runtime)")

    def _update_ic(self, ic_str: str):
        NL = "\n"
        self.ic_text.config(state=tk.NORMAL)
        self.ic_text.delete("1.0", tk.END)
        if not ic_str:
            self.ic_text.insert(tk.END, "(no IC — fix errors first)", "comment")
            self.ic_text.config(state=tk.DISABLED)
            self.ic_count_var.set("")
            return
        lines = ic_str.splitlines()
        for line in lines:
            stripped = line.strip()
            if stripped.endswith(":") and not stripped.startswith("#"):
                self.ic_text.insert(tk.END, NL + line + NL, "label")
            elif stripped.startswith("#"):
                self.ic_text.insert(tk.END, line + NL, "comment")
            elif any(kw in stripped for kw in ("JUMP", "JUMPF", "JUMPT")):
                self.ic_text.insert(tk.END, line + NL, "jump")
            elif stripped.startswith("CALL") or "= call" in stripped:
                self.ic_text.insert(tk.END, line + NL, "call")
            elif stripped.startswith("RETURN"):
                self.ic_text.insert(tk.END, line + NL, "ret")
            elif "BINOP" in stripped or "UNOP" in stripped:
                self.ic_text.insert(tk.END, line + NL, "op")
            elif "ASSIGN" in stripped or "COPY" in stripped:
                self.ic_text.insert(tk.END, line + NL, "assign")
            else:
                self.ic_text.insert(tk.END, line + NL, "op")
        instr_count = sum(1 for l in lines
                          if l.strip() and not l.strip().endswith(":")
                          and not l.strip().startswith("#"))
        self.ic_count_var.set(f"{instr_count} instructions")
        self.ic_text.config(state=tk.DISABLED)

    def _update_diagnostics(self, sem_result, syntax_errors: list):
        self.diag_tree.delete(*self.diag_tree.get_children())

        total_errors   = 0
        total_warnings = 0

        # Syntax errors first
        for msg in syntax_errors:
            parts = msg.split("  ", 1)
            loc   = parts[0] if len(parts) > 1 else ""
            text  = parts[1] if len(parts) > 1 else msg
            line_num, col_num = 0, 0
            m = re.match(r"line (\d+):(\d+)", loc)
            if m:
                line_num, col_num = int(m.group(1)), int(m.group(2))
            self.diag_tree.insert("", tk.END,
                                   values=("Syntax", line_num, col_num, text),
                                   tags=("syntax",))
            total_errors += 1

        # Semantic diagnostics
        for d in sem_result.diagnostics:
            kind_label = "Semantic" if d.kind == "error" else "Warning"
            self.diag_tree.insert("", tk.END,
                                   values=(kind_label, d.line, d.col, d.message),
                                   tags=(d.kind,))
            if d.kind == "error":   total_errors   += 1
            else:                   total_warnings += 1

        parts = []
        if total_errors:   parts.append(f"{total_errors} error{'s' if total_errors > 1 else ''}")
        if total_warnings: parts.append(f"{total_warnings} warning{'s' if total_warnings > 1 else ''}")
        self.diag_count_var.set("  ".join(parts) if parts else "No issues ✓")

    # ── jump to diagnostic line ───────────────────────────────

    def _jump_to_diag(self, event=None):
        sel = self.diag_tree.selection()
        if not sel:
            return
        values = self.diag_tree.item(sel[0], "values")
        try:
            line = int(values[1])
            if line > 0:
                self.editor.see(f"{line}.0")
                self.editor.mark_set(tk.INSERT, f"{line}.0")
                self.editor.focus_set()
        except (ValueError, IndexError):
            pass
        
        # ── Trace / Step Debugger tab ─────────────────────────────

    def _build_trace_tab(self):
        frame = tk.Frame(self.nb, bg=PANEL_BG)
        self.nb.add(frame, text="  🐛 Trace  ")

        # ── top bar: controls ─────────────────────────────────
        ctrl = tk.Frame(frame, bg="#0d1117")
        ctrl.pack(fill=tk.X, padx=6, pady=(6, 2))

        tk.Label(ctrl, text="Step Debugger", bg="#0d1117",
                 fg=ACCENT, font=("Segoe UI", 10, "bold")).pack(side=tk.LEFT)

        self._trace_step_var = tk.StringVar(value="No trace — press 🐛 Debug")
        tk.Label(ctrl, textvariable=self._trace_step_var,
                 bg="#0d1117", fg=FG_DIM,
                 font=("Segoe UI", 10)).pack(side=tk.RIGHT, padx=6)

        # ── button row ────────────────────────────────────────
        btn_row = tk.Frame(frame, bg=PANEL_BG)
        btn_row.pack(fill=tk.X, padx=6, pady=2)

        btn_cfg = dict(relief=tk.FLAT, font=("Segoe UI", 11, "bold"),
                       padx=10, pady=5, cursor="hand2", bd=0,
                       activeforeground="#0d1117")

        self._btn_back = tk.Button(btn_row, text="◀  Back",
                                   command=self.debug_back,
                                   bg="#21262d", fg=FG, **btn_cfg,
                                   activebackground=ACCENT)
        self._btn_back.pack(side=tk.LEFT, padx=2)

        self._btn_next = tk.Button(btn_row, text="Next  ▶",
                                   command=self.debug_next,
                                   bg="#21262d", fg=FG, **btn_cfg,
                                   activebackground=ACCENT)
        self._btn_next.pack(side=tk.LEFT, padx=2)

        self._btn_end = tk.Button(btn_row, text="▶▶ End",
                                  command=self.debug_end,
                                  bg="#21262d", fg=FG_DIM, **btn_cfg,
                                  activebackground=PURPLE)
        self._btn_end.pack(side=tk.LEFT, padx=2)

        self._btn_reset = tk.Button(btn_row, text="⟳ Reset",
                                    command=self.debug_reset,
                                    bg="#21262d", fg=FG_DIM, **btn_cfg,
                                    activebackground=ORANGE)
        self._btn_reset.pack(side=tk.LEFT, padx=2)

        tk.Label(btn_row, text="F9=Back  F10=Next",
                 bg=PANEL_BG, fg=FG_DIM,
                 font=("Segoe UI", 9)).pack(side=tk.RIGHT, padx=6)

        # ── current instruction display ───────────────────────
        instr_frame = tk.Frame(frame, bg="#0d1117", pady=3)
        instr_frame.pack(fill=tk.X, padx=6, pady=(2, 0))
        tk.Label(instr_frame, text="IC Instruction:", bg="#0d1117",
                 fg=FG_DIM, font=("Segoe UI", 9)).pack(side=tk.LEFT, padx=(4, 6))
        self._trace_instr_var = tk.StringVar(value="—")
        tk.Label(instr_frame, textvariable=self._trace_instr_var,
                 bg="#0d1117", fg=CYAN,
                 font=("Consolas", 10)).pack(side=tk.LEFT)

        # ── output so far ─────────────────────────────────────
        out_frame = tk.Frame(frame, bg=PANEL_BG)
        out_frame.pack(fill=tk.X, padx=6, pady=(4, 0))
        tk.Label(out_frame, text="Output so far:", bg=PANEL_BG,
                 fg=FG_DIM, font=("Segoe UI", 9, "bold")).pack(anchor=tk.W)
        self._trace_output = tk.Text(out_frame, bg="#0d1117", fg=GREEN,
                                     font=("Consolas", 10),
                                     height=3, relief=tk.FLAT,
                                     state=tk.DISABLED, padx=6, pady=4)
        self._trace_output.pack(fill=tk.X)

        # ── symbol table ──────────────────────────────────────
        sym_frame = tk.Frame(frame, bg=PANEL_BG)
        sym_frame.pack(fill=tk.BOTH, expand=True, padx=6, pady=(6, 4))
        tk.Label(sym_frame, text="Symbol Values", bg=PANEL_BG,
                 fg=ACCENT, font=("Segoe UI", 10, "bold")).pack(anchor=tk.W)

        cols = ("Name", "BKType", "Value", "Address")
        self._trace_sym_tree = ttk.Treeview(sym_frame, columns=cols,
                                             show="headings",
                                             selectmode="browse")
        for col, w in zip(cols, [130, 90, 210, 100]):
            self._trace_sym_tree.heading(col, text=col)
            self._trace_sym_tree.column(col, width=w, minwidth=w, anchor=tk.W)

        tsb = ttk.Scrollbar(sym_frame, orient=tk.VERTICAL,
                            command=self._trace_sym_tree.yview)
        self._trace_sym_tree.configure(yscrollcommand=tsb.set)
        self._trace_sym_tree.pack(side=tk.LEFT, fill=tk.BOTH,
                                   expand=True, pady=2)
        tsb.pack(side=tk.RIGHT, fill=tk.Y, pady=2, padx=(0, 2))

        # colour tags
        for bktype, color in BKTYPE_COLORS.items():
            self._trace_sym_tree.tag_configure(bktype, foreground=color)
        self._trace_sym_tree.tag_configure("changed",
                                            background="#1a3320",
                                            foreground="#56d364")

    # ── debugger state helpers ────────────────────────────────

    def _update_trace_readiness(self):
        """Called after run_code — enables/disables trace buttons."""
        has = bool(self._debug_snapshots)
        state = tk.NORMAL if has else tk.DISABLED
        for btn in (self._btn_back, self._btn_next,
                    self._btn_end, self._btn_reset):
            btn.config(state=state)
        if has:
            self._trace_step_var.set(
                f"Ready — {len(self._debug_snapshots)} steps  (press 🐛 Debug or F10)")
        else:
            self._trace_step_var.set("No trace — run code first")

    def _clear_debug_highlight(self):
        self.editor.tag_remove("debug_line", "1.0", tk.END)

    def _apply_debug_snapshot(self, snap):
        """Render a single DebugSnapshot into the Trace UI."""
        total = len(self._debug_snapshots)
        self._trace_step_var.set(
            f"Step {snap.step + 1} / {total}  "
            f"(src line {snap.source_line if snap.source_line else '?'})")
        self._trace_instr_var.set(snap.instr_str)

        # ── highlight source line in editor ───────────────────
        self._clear_debug_highlight()
        if snap.source_line and snap.source_line > 0:
            lstart = f"{snap.source_line}.0"
            lend   = f"{snap.source_line}.end"
            self.editor.tag_add("debug_line", lstart, lend)
            self.editor.see(lstart)

        # ── output panel ──────────────────────────────────────
        self._trace_output.config(state=tk.NORMAL)
        self._trace_output.delete("1.0", tk.END)
        if snap.output:
            self._trace_output.insert(tk.END, "\n".join(snap.output))
        self._trace_output.config(state=tk.DISABLED)

        # ── symbol table ──────────────────────────────────────
        self._trace_sym_tree.delete(*self._trace_sym_tree.get_children())
        type_map = {
            "int": "int", "float": "float", "complex": "complex",
            "bool": "bool", "str": "string",
            "BKVector": "ket/bra", "BKOperator": "operator",
            "BKArray": "array", "BKStruct": "struct",
            "BKPointer": "pointer",
            "NoneType": "unknown",
        }
        for name, val in sorted(snap.env.items()):
            type_name = type(val).__name__
            bkt  = type_map.get(type_name, type_name)
            val_str = str(val)
            if len(val_str) > 50:
                val_str = val_str[:47] + "…"
            addr     = snap.var_addrs.get(name)
            addr_str = f"0x{addr:04X}" if addr is not None else "—"
            tag = "changed" if name in snap.changed else (
                bkt if bkt in BKTYPE_COLORS else "unknown")
            self._trace_sym_tree.insert("", tk.END,
                                         values=(name, bkt, val_str, addr_str),
                                         tags=(tag,))

    # ── public debugger commands ──────────────────────────────

    def start_debug(self, event=None):
        """Enter debug mode: run if needed, switch to Trace tab, go to step 0."""
        if not self._debug_snapshots:
            self.run_code()
        if not self._debug_snapshots:
            return
        self._debug_active = True
        self._debug_step   = 0
        self.nb.select(5)   # Trace tab index
        self._apply_debug_snapshot(self._debug_snapshots[0])

    def debug_next(self, event=None):
        if not self._debug_snapshots:
            return
        if self._debug_step < len(self._debug_snapshots) - 1:
            self._debug_step += 1
        self.nb.select(5)
        self._apply_debug_snapshot(self._debug_snapshots[self._debug_step])

    def debug_back(self, event=None):
        if not self._debug_snapshots:
            return
        if self._debug_step > 0:
            self._debug_step -= 1
        self.nb.select(5)
        self._apply_debug_snapshot(self._debug_snapshots[self._debug_step])

    def debug_end(self, event=None):
        if not self._debug_snapshots:
            return
        self._debug_step = len(self._debug_snapshots) - 1
        self.nb.select(5)
        self._apply_debug_snapshot(self._debug_snapshots[self._debug_step])

    def debug_reset(self, event=None):
        if not self._debug_snapshots:
            return
        self._debug_step = 0
        self.nb.select(5)
        self._apply_debug_snapshot(self._debug_snapshots[0])
    # ── Run ───────────────────────────────────────────────────

    def run_code(self, event=None):
        source = self.editor.get("1.0", tk.END)
        self.status_var.set("  Analysing…")
        self.root.update_idletasks()

        def _input_cb(prompt: str) -> str:
            """Called by the interpreter whenever input() is executed.
            Shows the prompt inline in the output panel, then opens a
            modal dialog on the main Tk thread and echoes the typed value."""
            self.output.config(state=tk.NORMAL)
            if prompt:
                self.output.insert(tk.END, prompt, "info")
            self.output.config(state=tk.DISABLED)
            self.root.update_idletasks()
            val = _tk_simpledialog.askstring(
                "Program Input",
                prompt or "Enter a value:",
                parent=self.root,
            ) or ""
            self.output.config(state=tk.NORMAL)
            self.output.insert(tk.END, val + "\n", "success")
            self.output.config(state=tk.DISABLED)
            self.root.update_idletasks()
            return val

        def _ready_cb(partial):
            """Called after static analysis, before interpreter runs.
            Clears the output panel, writes the analysis header, and updates
            all static debug panels — before any input() dialog appears."""
            p_syn = partial.sem.syntax_errors if hasattr(partial.sem, "syntax_errors") else []
            p_sem = [d for d in partial.sem.diagnostics if d.kind == "error"]
            p_warn = [d for d in partial.sem.diagnostics if d.kind == "warning"]

            self.output.config(state=tk.NORMAL)
            self.output.delete("1.0", tk.END)
            if p_syn or p_sem:
                self.output.insert(tk.END,
                    f"❌  {len(p_syn) + len(p_sem)} error(s)"
                    f"{',' if p_warn else ''} ", "error")
                if p_warn:
                    self.output.insert(tk.END, f"{len(p_warn)} warning(s)\n", "warning")
                else:
                    self.output.insert(tk.END, "\n")
                for e in p_syn:
                    self.output.insert(tk.END, f"  [syntax]  {e}\n", "error")
                for d in p_sem:
                    self.output.insert(tk.END, f"  [line {d.line}:{d.col}]  {d.message}\n", "error")
                self.status_var.set(f"  ✗ {len(p_syn)+len(p_sem)} error(s)")
            else:
                self.output.insert(tk.END, "✓  Analysis complete — no errors\n", "success")
                if p_warn:
                    self.output.insert(tk.END, f"⚠  {len(p_warn)} warning(s)\n", "warning")
                self.status_var.set("  ✓ Done")
            for w in p_warn:
                self.output.insert(tk.END, f"  [line {w.line}:{w.col}]  {w.message}\n", "warning")
            # "── Program Output ──" header, written once before any live lines
            # (only when there are no errors — otherwise the interpreter won't run)
            if not (p_syn or p_sem):
                self.output.insert(tk.END, "\n── Program Output ──\n", "info")
            self.output.config(state=tk.DISABLED)

            self._update_scanner(partial.tokens)
            self._update_parse_tree(partial.parse_tree_str)
            self._update_diagnostics(partial.sem, p_syn)
            self.root.update_idletasks()

        def _output_cb(line: str):
            """Streams each print() line into the output panel live."""
            self.output.config(state=tk.NORMAL)
            self.output.insert(tk.END, line + "\n", "success")
            self.output.config(state=tk.DISABLED)
            self.root.update_idletasks()

        try:
            result = analyze(source, input_cb=_input_cb, ready_cb=_ready_cb,
                             output_cb=_output_cb) # CALLS ENGINE
        except Exception as exc:
            self._write_output(f"Internal engine error:\n{exc}\n", "error")
            self.status_var.set("  Engine error")
            return

        # Analysis header and program output were already written live by
        # _ready_cb and _output_cb.  Only handle runtime errors and the
        # remaining debug panels here.
        syn_errs = result.sem.syntax_errors if hasattr(result.sem, "syntax_errors") else []
        sem_errs = [d for d in result.sem.diagnostics if d.kind == "error"]

        try:
            if result.run and result.run.error:
                self.output.config(state=tk.NORMAL)
                self.output.insert(tk.END, "\n❌ " + result.run.error + "\n", "error")
                self.output.config(state=tk.DISABLED)
        finally:
            self.output.config(state=tk.DISABLED)

        # ── Store debug snapshots ────────────────────────────
        self._debug_snapshots = getattr(result, "debug_snapshots", []) or []
        self._debug_step      = 0
        self._debug_active    = False
        self._update_trace_readiness()

        # ── Debug panels ──────────────────────────────────────
        self._update_scanner(result.tokens)
        self._update_parse_tree(result.parse_tree_str)
        # Use runtime symbol table if available, else fall back to semantic scope
        if result.run and result.run.symbol_table:
            self._update_runtime_symbols(result.run.symbol_table,
                                        result.run.function_scopes,
                                        getattr(result.run, "var_addrs", None),
                                        getattr(result.run, "tmp_table", None))
        else:
            self._update_symbol_table(result.sem.global_scope,
                                    result.sem.closed_scopes)
        self._update_ic(result.ic_listing)
        self._update_diagnostics(result.sem, syn_errs)

        # Auto-switch: errors → Diagnostics, else output if there is program output
        if syn_errs or sem_errs:
            self.nb.select(4)   # diagnostics tab (now index 4)
        elif result.run and result.run.output:
            pass  # stay on current tab; output is in the output panel

    def _write_output(self, text: str, tag: str = ""):
        self.output.config(state=tk.NORMAL)
        self.output.delete("1.0", tk.END)
        self.output.insert(tk.END, text, tag)
        self.output.config(state=tk.DISABLED)

    # ── file ops ──────────────────────────────────────────────

    def new_file(self, event=None):
        self.editor.delete("1.0", tk.END)
        self.current_file = None
        self.file_label.config(text="untitled.bk")
        self._on_key()

    def open_file(self, event=None):
        path = filedialog.askopenfilename(
            filetypes=[("BraKet", "*.bk"), ("All files", "*.*")])
        if path:
            with open(path, encoding="utf-8") as f:
                self.editor.delete("1.0", tk.END)
                self.editor.insert("1.0", f.read())
            self.current_file = path
            self.file_label.config(text=path.split("/")[-1])
            self._on_key()

    def save_file(self, event=None):
        path = self.current_file or filedialog.asksaveasfilename(
            defaultextension=".bk",
            filetypes=[("BraKet", "*.bk"), ("All files", "*.*")])
        if path:
            with open(path, "w", encoding="utf-8") as f:
                f.write(self.editor.get("1.0", tk.END))
            self.current_file = path
            self.file_label.config(text=path.split("/")[-1])
            self.status_var.set("  Saved")

    def _clear_output(self):
        self.output.config(state=tk.NORMAL)
        self.output.delete("1.0", tk.END)
        self.output.config(state=tk.DISABLED)

    # ── keyboard shortcuts ────────────────────────────────────

    def _bind_shortcuts(self):
        self.root.bind("<Control-r>", self.run_code)
        self.root.bind("<F5>",        self.run_code)
        self.root.bind("<F6>",        self.start_debug)
        self.root.bind("<F10>",       self.debug_next)
        self.root.bind("<F9>",        self.debug_back)
        self.root.bind("<Control-s>", self.save_file)
        self.root.bind("<Control-o>", self.open_file)
        self.root.bind("<Control-n>", self.new_file)
        for widget in (self.root, self.editor):
            widget.bind("<Control-equal>",       lambda e: self.zoom_in()    or "break")
            widget.bind("<Control-plus>",        lambda e: self.zoom_in()    or "break")
            widget.bind("<Control-minus>",       lambda e: self.zoom_out()   or "break")
            widget.bind("<Control-0>",           lambda e: self.zoom_reset() or "break")
            widget.bind("<Control-KP_Add>",      lambda e: self.zoom_in()    or "break")
            widget.bind("<Control-KP_Subtract>", lambda e: self.zoom_out()   or "break")
            widget.bind("<Control-MouseWheel>",
                        lambda e: self.zoom_in() if e.delta > 0 else self.zoom_out())


# ─────────────────────────────────────────────────────────────
if __name__ == "__main__":
    root = tk.Tk()
    IDE(root)
    root.mainloop()