"""
Parser for simple LaTeX.

This parser supports only the simple subject of LaTeX that we typically use.
"""
from lark import Lark
from .transform import ToUnicode

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
COMMAND: (("\\" WORD WS*) | SUBSCRIPT | SUPERSCRIPT)
WS_EXT: WS | "~" | "\," | "\;" | "\:" | "\>"

%import common.WS
%import common.WORD
"""

parser = Lark(grammar, parser="lalr", transformer=ToUnicode())
