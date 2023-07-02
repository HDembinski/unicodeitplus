"""Tools to transform LaTeX tree into unicode."""
from . import _make_data  # noqa, imported for side-effects
from .data import COMMANDS, HAS_ARG
from lark import Transformer, Token
from typing import List, Any
from string import ascii_letters


IGNORE_AS_FALLBACK = {
    r"\text",
    r"\mathbb",
    r"\mathrm",
    r"\mathbf",
    r"\mathsf",
    r"\mathsfbf",
    r"\mathsfbfit",
    r"\mathsfit",
    r"\mathtt",
    r"\left",
    r"\right",
    r"\big",
    r"\Big",
    r"\Bigg",
}

# ESCAPED = {
#     "\\\\": "\\",
#     r"\}": "}",
#     r"\{": "{",
#     r"\_": "_",
#     r"\^": "^",
#     r"\~": "~",
# }

WHITESPACE = {
    # unbreakable space
    "~": "\u00A0",
    # thinspace ~0.17em
    r"\,": "\u2009",
    # medspace ~0.22em
    r"\:": "\u2005",
    r"\>": "\u2005",
    # thickspace ~0.28em
    r"\;": "\u2004",
}


class ToUnicode(Transformer):  # type:ignore
    """Convert Tree to Unicode."""

    def __init__(self, options = None):
        options = options if options else dict()
        self.preserve_roman = options.get("preserve_roman", False)
        self.preserve_math_whitespace = options.get("preserve_math_whitespace", False)
        
        self.commands = COMMANDS

        if self.preserve_roman:
            self.commands.update({ x: x for x in ascii_letters })

    def start(self, ch: List[Any]) -> str:
        """
        Return final unicode.

        The start token is handled last, because the transformer
        starts from the leafs. So when we arrive here, everything
        else is already transformed into strings. We only need
        to handle escaped characters correctly and recursively
        unparse groups.
        """
        r: List[str] = []

        def visitor(r: List[str], ch: List[Any]) -> None:
            for x in ch:
                if isinstance(x, str):
                    r.append(x)
                elif isinstance(x, list):
                    r.append("{")
                    visitor(r, x)
                    r.append("}")
                else:
                    assert False  # this should never happen

        visitor(r, ch)
        return "".join(r)

    def CHARACTER(self, ch: Token) -> str:
        """
        Handle character token.

        This is either a single charactor or an escaped character sequence.
        """
        if ch.value.startswith("\\"):
            return ch.value[1:]  # type:ignore
        return ch.value  # type:ignore

    def WS_EXT(self, ch: Token) -> str:
        """
        Handle whitespace.
        """
        return WHITESPACE.get(ch.value, " ")

    def COMMAND(self, ch: Token) -> str:
        """
        Handle command token.

        We need to strip the whitespace which may be there.
        """
        return ch.value.strip()  # type:ignore

    def group(self, items: List[Any]) -> List[Any]:
        """
        Handle group token.

        Nothing to do, we just the children as a list.
        """
        return items

    def math(self, items: List[Any]) -> str:
        """
        Handle math token.

        Here the actual magic happens. The challenge is to treat macros which accept an
        argument correctly, while respecting the grouping. A command which accepts an
        argument acts on the next character or group. Groups can be nested, so we need
        to handle this with recursion.

        First, a recursive visitor with a command stack converts nested macros and
        groups into a list of flat lists of commands which end in a leaf (a charactor or
        command that accepts no argument).

        Then, we convert each list of commands with the function _handle_cmds into
        unicode. See comments in that function for details.
        """

        is_space = lambda x: isinstance(x, str) and x.isspace()

        if not self.preserve_math_whitespace:
            items = [x for x in items if not is_space(x)]
        def visitor(
            r: List[List[str]],
            stack: List[str],
            items: List[Any],
        ) -> None:
            initial_stack = stack.copy()
            for x in items:
                if isinstance(x, str) and x in HAS_ARG:
                    if x == r"\sqrt":
                        r.append(stack.copy() + [r"\sqrt"])
                        stack.append(r"\overline")
                    else:
                        stack.append(x)
                else:
                    if isinstance(x, list):
                        visitor(r, stack, x)
                    elif isinstance(x, str):
                        r.append(stack.copy() + [x])
                    else:
                        assert False  # should never happen
                    if not is_space(x):
                        stack[:] = initial_stack

        r: List[List[str]] = []
        visitor(r, [], items)
        return "".join(self._handle_cmds(x[:-1], x[-1]) for x in r)


    def _handle_cmds(self, cmds: List[str], x: str) -> str:
        # - x can be character or command, like \alpha
        # - cmds contains commands to apply, may be empty
        # - to transform ^{\alpha} or \text{x} correctly,
        #   we first try to convert innermost command and x
        #   as unit; if this fails we treat commands sequentially
        # - other commands in cmds must be modifiers like \dot or
        #   \vec that are converted into diacritical characters
        # - if we cannot convert, we return unconverted LaTeX
        if cmds:
            innermost = True
            for cmd in reversed(cmds):
                latex = f"{cmd}{{{x}}}"
                if latex in self.commands:
                    x = self.commands[latex]
                elif cmd in (r"\text", r"\mathrm"):
                    pass
                else:
                    if innermost:
                        x = self.commands.get(x, x)
                    if cmd in self.commands:
                        # must be some unicode modifier, e.g. \dot, \vec
                        assert cmd in HAS_ARG  # nosec
                        x += self.commands[cmd]
                    elif cmd not in IGNORE_AS_FALLBACK:
                        x = latex
                innermost = False
        else:
            x = self.commands.get(x, x)
        return x
