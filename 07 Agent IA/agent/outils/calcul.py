"""Outil de l'agent : calculatrice sûre (pas d'exécution de code arbitraire).

Usage : python outils/calcul.py "79 + 129 + 49"   ->  257
Fonctions : round, min, max, abs, sum([..]). Opérateurs : + - * / // % **"""
import ast
import operator as op
import sys

OPS = {ast.Add: op.add, ast.Sub: op.sub, ast.Mult: op.mul, ast.Div: op.truediv,
       ast.FloorDiv: op.floordiv, ast.Mod: op.mod, ast.Pow: op.pow, ast.USub: op.neg, ast.UAdd: op.pos}
FN = {"round": round, "min": min, "max": max, "abs": abs, "sum": sum}


def ev(n):
    if isinstance(n, ast.Expression):
        return ev(n.body)
    if isinstance(n, ast.Constant) and isinstance(n.value, (int, float)):
        return n.value
    if isinstance(n, ast.BinOp) and type(n.op) in OPS:
        return OPS[type(n.op)](ev(n.left), ev(n.right))
    if isinstance(n, ast.UnaryOp) and type(n.op) in OPS:
        return OPS[type(n.op)](ev(n.operand))
    if isinstance(n, (ast.List, ast.Tuple)):
        return [ev(x) for x in n.elts]
    if isinstance(n, ast.Call) and isinstance(n.func, ast.Name) and n.func.id in FN:
        return FN[n.func.id](*[ev(a) for a in n.args])
    raise ValueError("expression non autorisée")


if __name__ == "__main__":
    # décimales avec un point (12.99) ; la virgule sépare les éléments d'une liste
    expr = " ".join(sys.argv[1:]) if len(sys.argv) > 1 else ""
    expr = expr.replace("€", "").replace("%", "/100")
    try:
        r = ev(ast.parse(expr, mode="eval"))
        print(f"{expr} = {round(r, 4) if isinstance(r, float) else r}")
    except Exception as e:
        print(f"Erreur de calcul : {e}")
