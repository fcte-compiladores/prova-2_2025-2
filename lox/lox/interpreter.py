from functools import singledispatch

from .ast import (
    Assign,
    Binary,
    Block,
    Call,
    Expr,
    ExprStmt,
    Function,
    Grouping,
    Identifier,
    If,
    Literal,
    LogicAnd,
    LogicOr,
    Print,
    Program,
    Return,
    Stmt,
    Unary,
    Value,
    Var,
    While,
)
from .env import Env
from .runtime import LoxCallable, LoxFunction
from .token import Token, TokenType


class LoxReturn(Exception):
    def __init__(self, value: Value):
        self.value = value


@singledispatch
def eval(expr: Expr, ctx: Env) -> Value:
    raise TypeError(f"[eval] tipo não suportado: {type(expr)}")


@singledispatch
def exec(expr: Stmt, ctx: Env) -> Value:
    raise TypeError(f"[exec] tipo não suportado: {type(expr)}")


@eval.register
def _(expr: Literal, ctx: Env):
    return expr.value


@eval.register
def _(expr: Grouping, ctx: Env):
    return eval(expr.expression, ctx)


@eval.register
def _(expr: Unary, ctx: Env):
    right = eval(expr.right, ctx)
    match expr.operator.type:
        case TokenType.MINUS:
            if isinstance(right, float):
                return -right
            raise RuntimeError(f"operação inválida: -{right}")
        case TokenType.BANG:
            return not truthy(right)
        case token:
            raise RuntimeError(f"operação unária inválida {token}")


@eval.register
def _(expr: Binary, ctx: Env):
    left = eval(expr.left, ctx)
    right = eval(expr.right, ctx)

    match expr.operator.type:
        # Operações matemáticas
        case TokenType.PLUS:
            if isinstance(left, float) and isinstance(right, float):
                return left + right
            elif isinstance(left, str) and isinstance(right, str):
                return left + right
            raise RuntimeError(f"operação inválida: {left} + {right}")
        case TokenType.MINUS:
            assure_floats(left, right, expr.operator)
            return left - right  # type: ignore
        case TokenType.STAR:
            assure_floats(left, right, expr.operator)
            return left * right  # type: ignore
        case TokenType.SLASH:
            assure_floats(left, right, expr.operator)
            return left / right  # type: ignore

        # Comparações
        case TokenType.EQUAL_EQUAL:
            if type(left) != type(right):  # noqa
                return False
            return left == right
        case TokenType.BANG_EQUAL:
            if type(left) != type(right):  # noqa
                return True
            return left != right
        case TokenType.GREATER_EQUAL:
            assure_floats(left, right, expr.operator)
            return left >= right  # type: ignore
        case TokenType.GREATER:
            assure_floats(left, right, expr.operator)
            return left > right  # type: ignore
        case TokenType.LESS:
            assure_floats(left, right, expr.operator)
            return left < right  # type: ignore
        case TokenType.LESS_EQUAL:
            assure_floats(left, right, expr.operator)
            return left <= right  # type: ignore

        case token:
            raise RuntimeError(f"operação binaria inválida {token}")


def assure_floats(x, y, op: Token):
    if not isinstance(x, float) and not isinstance(y, float):
        raise RuntimeError(f"operação inválida: {op.lexeme}")


@eval.register
def _(expr: LogicAnd, ctx: Env):
    left = eval(expr.left, ctx)
    right = eval(expr.right, ctx)
    if not truthy(left):
        return left
    return right


@eval.register
def _(expr: LogicOr, ctx: Env):
    left = eval(expr.left, ctx)
    right = eval(expr.right, ctx)
    if truthy(left):
        return left
    return right


@eval.register
def _(expr: Identifier, ctx: Env):
    try:
        return ctx[expr.name]
    except KeyError:
        raise RuntimeError(f"variável não existe: {expr.name}")


@eval.register
def _(expr: Assign, ctx: Env) -> Value:
    value = eval(expr.right, ctx)
    ctx[expr.name] = value
    return value


@eval.register
def _(expr: Call, ctx: Env) -> Value:
    callee = eval(expr.callee, ctx)
    args = [eval(arg, ctx) for arg in expr.args]
    if not isinstance(callee, LoxCallable):
        raise RuntimeError(f"{callee} não é uma função.")
    if len(args) != callee.n_args():
        raise RuntimeError(f"{callee}: número errado de argumentos.")
    return callee.call(ctx, args)


#
# Implementações de exec
#
@exec.register
def _(cmd: Program, ctx: Env):
    for stmt in cmd.body:
        exec(stmt, ctx)


@exec.register
def _(cmd: Print, ctx: Env):
    print(eval(cmd.right, ctx))


@exec.register
def _(cmd: ExprStmt, ctx: Env):
    eval(cmd.expr, ctx)


@exec.register
def _(cmd: Var, ctx: Env):
    value = eval(cmd.right, ctx)
    ctx.define(cmd.name, value)


@exec.register
def _(cmd: Block, ctx: Env):
    child_ctx = Env(ctx)
    for stmt in cmd.body:
        exec(stmt, child_ctx)


@exec.register
def _(cmd: If, ctx: Env):
    if truthy(eval(cmd.cond, ctx)):
        exec(cmd.then_body, ctx)
    else:
        exec(cmd.else_body, ctx)


@exec.register
def _(cmd: While, ctx: Env):
    while truthy(eval(cmd.cond, ctx)):
        exec(cmd.body, ctx)


@exec.register
def _(cmd: Function, ctx: Env):
    function = LoxFunction(cmd, ctx)
    ctx.define(cmd.name, function)


@exec.register
def _(cmd: Return, ctx: Env):
    if cmd.value is not None:
        value = eval(cmd.value, ctx)
    else:
        value = None
    raise LoxReturn(value)


def truthy(obj) -> bool:
    if obj is False or obj is None:
        return False
    return True
