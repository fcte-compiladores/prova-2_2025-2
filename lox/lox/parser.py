from pathlib import Path
import os
import lark
from .token import Token, TokenType
from .ast import Assign, Binary, Expr, ExprStmt, Identifier, Literal, LogicAnd, LogicOr, Return, Unary, Call
from .ast import Block, If, Print, Stmt, Program, Var, Function,  While

BASE = Path(__file__).parent / "grammar.lark"
SOURCE = BASE.read_text()
GRAMMAR = lark.Lark(SOURCE, parser="lalr", start=["program", "expression"])

type Input = str

DEBUG_PARSER = os.environ.get("DEBUG_PARSER", "0") == "1"


@lark.v_args(inline=True)
class LoxTransformer(lark.Transformer):
    #
    # Terminais
    #
    def STRING(self, token: lark.Token):
        return Literal(token[1:-1])

    def NUMBER(self, token: lark.Token):
        return Literal(float(token))

    def LITERAL(self, token: lark.Token):
        if token == "true":
            return Literal(True)
        if token == "false":
            return Literal(False)
        if token == "nil":
            return Literal(None)

    def IDENTIFIER(self, token: lark.Token):
        return Identifier(str(token))

    #
    # Expr
    #
    def binary(self, left: Expr, op: lark.Token, right: Expr):
        return Binary(left, lox_token(op), right)

    def unary(self, op: lark.Token, right: Expr):
        return Unary(lox_token(op), right)

    def logic_and(self, left: Expr, right: Expr):
        return LogicAnd(left, right)

    def logic_or(self, left: Expr, right: Expr):
        return LogicOr(left, right)

    def call(self, callee: Expr, args=None):
        return Call(callee, args or [])

    def assignment(self, left: Identifier, right: Expr | None = None):
        return Assign(left.name, right or Literal(None))

    @lark.v_args(inline=False)
    def arguments(self, children: list[Expr]):
        return children

    #
    # Stmt
    #
    @lark.v_args(inline=False)
    def program(self, children):
        return Program(children)

    def expr_stmt(self, expr: Expr):
        return ExprStmt(expr)

    def print_stmt(self, expression):
        return Print(expression)

    def var_decl(self, identifier: Identifier, initializer=None):
        if initializer is None:
            initializer = Literal(None)
        return Var(identifier.name, initializer)

    @lark.v_args(inline=False)
    def block(self, children: list[Stmt]):
        return Block(children)

    def if_stmt(self, cond, then, else_=None):
        if else_ is None:
            else_ = Block([])  # lox: else {}
        return If(cond, then, else_)

    def while_stmt(self, cond: Expr, body: Stmt):
        return While(cond, body)

    def for_stmt(self, init: Expr | Var | None, cond: Expr | None, incr: Expr | None, body: Stmt):
        if incr is not None:
            body = Block([body, ExprStmt(incr)])
        body = While(cond or Literal(True), body)
        if isinstance(init, Var):
            body = Block([init, body])
        elif init:
            body = Block([ExprStmt(init), body])
        return body

    def for_init(self, init: Expr | Var | None = None):
        return init

    def for_condition(self, cond: Expr | None = None):
        return cond

    def for_increment(self, incr: Expr | None = None):
        return incr

    def function(self, identifier: Identifier, parameters: list[str], block: Block):
        return Function(identifier.name, parameters, block.body)

    def return_stmt(self, value: Expr | None = None):
        return Return(value)

    @lark.v_args(inline=False)
    def parameters(self, children: list[Identifier]):
        return [identifier.name for identifier in children]


def parse(src: str, debug: bool = DEBUG_PARSER) -> Stmt:
    tree = GRAMMAR.parse(src, start="program")
    transformer = LoxTransformer()
    ast = transformer.transform(tree)
    if debug:
        print("-" * 40)
        if hasattr(ast, "pretty"):
            print(ast.pretty())
        else:
            import rich

            rich.print(ast)
        print("-" * 40)
    return ast


TOKEN_TYPES = {
    "!": TokenType.BANG,
    "+": TokenType.PLUS,
    "-": TokenType.MINUS,
    "*": TokenType.STAR,
    "/": TokenType.SLASH,
    ">": TokenType.GREATER,
    "<": TokenType.LESS,
    ">=": TokenType.GREATER_EQUAL,
    "<=": TokenType.LESS_EQUAL,
    "==": TokenType.EQUAL_EQUAL,
    "!=": TokenType.BANG_EQUAL,
}


def lox_token(token: lark.Token) -> Token:
    type = TOKEN_TYPES[token]
    return Token(type, str(token), token.line)
