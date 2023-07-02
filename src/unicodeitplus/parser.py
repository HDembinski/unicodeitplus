"""
Parser for simple LaTeX.

This parser supports only the simple subject of LaTeX that we typically use.
"""
from lark import Lark

grammar = r"""
start: (item | math)*

?atom: CHARACTER
    | COMMAND

?item: atom
    | WS_EXT+
    | group

CHARACTER: /[^%#&\{\}^_\\]/ | ESCAPED
ESCAPED: /\\\S/
group: "{" item* "}"
math: "$" item* "$"
SUBSCRIPT: "_"
SUPERSCRIPT: "^"
COMMAND: (("\\" WORD) | SUBSCRIPT | SUPERSCRIPT)
WS_EXT: WS | "~" | "\," | "\;" | "\:" | "\>"

%import common.WS
%import common.WORD
"""

def make_parser(transformer):
    return Lark(grammar, parser="lalr", transformer=transformer)
