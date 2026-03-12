# interpreter.py
from antlr4 import *
from BraKetLexer import BraKetLexer
from BraKetParser import BraKetParser
from BraKetVisitor import BraKetVisitor

class Interpreter(BraKetVisitor):
    def __init__(self):
        self.variables = {}  # symbol table
        self.output = []     # captured output

    def visitProgram(self, ctx):
        for stmt in ctx.statement():
            self.visit(stmt)

    def visitAssignment(self, ctx):
        name = ctx.ID().getText()
        value = self.visit(ctx.expr())
        self.variables[name] = value

    def visitPrintStmt(self, ctx):
        value = self.visit(ctx.expr())
        self.output.append(str(value))

    def visitInt(self, ctx):
        return int(ctx.INT().getText())

    def visitFloat(self, ctx):
        return float(ctx.FLOAT().getText())

    def visitString(self, ctx):
        return ctx.STRING().getText()[1:-1]  # strip quotes

    def visitVar(self, ctx):
        name = ctx.ID().getText()
        if name not in self.variables:
            raise NameError(f"Undefined variable: '{name}'")
        return self.variables[name]

    def visitAddSub(self, ctx):
        left  = self.visit(ctx.expr(0))
        right = self.visit(ctx.expr(1))
        return left + right if ctx.op.text == '+' else left - right

    def visitMulDiv(self, ctx):
        left  = self.visit(ctx.expr(0))
        right = self.visit(ctx.expr(1))
        if ctx.op.text == '/':
            if right == 0: raise ZeroDivisionError("Division by zero")
            return left / right
        return left * right

    def visitCompare(self, ctx):
        left, right = self.visit(ctx.expr(0)), self.visit(ctx.expr(1))
        ops = {'<': left < right, '>': left > right,
               '==': left == right, '!=': left != right}
        return ops[ctx.op.text]

    def visitIfStmt(self, ctx):
        if self.visit(ctx.expr()):
            for stmt in ctx.statement():
                self.visit(stmt)

    def visitWhileStmt(self, ctx):
        while self.visit(ctx.expr()):
            for stmt in ctx.statement():
                self.visit(stmt)

def run_code(source: str):
    """Run source code and return (output, error)"""
    try:
        input_stream = InputStream(source)
        lexer = BraKetLexer(input_stream)
        stream = CommonTokenStream(lexer)
        parser = BraKetParser(stream)
        tree = parser.program()

        interp = Interpreter()
        interp.visit(tree)
        return "\n".join(interp.output), None
    except Exception as e:
        return None, str(e)