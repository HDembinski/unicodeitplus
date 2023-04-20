"""
Parser for simple LaTeX.

This parser supports only the simple subject of LaTeX that we typically use.
"""
from lark import Lark
from pathlib import Path

with open(Path(__file__).parent / "latex.g") as f:
    grammar = f.read()

parser = Lark(f.read(), parser="lalr")
