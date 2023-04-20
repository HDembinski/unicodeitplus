"""Tools to transform LaTeX tree into unicode."""
from . import _make_data  # noqa, imported for side-effects
from .data import COMMANDS, HAS_ARG
from lark import Transformer, Token
from typing import List, Any


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

ESCAPED = {
    r"\}": "}",
    r"\{": "{",
    r"\_": "_",
    r"\^": "^",
    "\\\\": "\\",
}


class ToUnicode(Transformer):  # type:ignore
    """Convert Tree to Unicode."""

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
                    x = ESCAPED.get(x, x)
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
        return ch.value  # type:ignore

    WS = CHARACTER

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
                        if not x.isspace() or (stack and stack[-1] == r"\text"):
                            r.append(stack.copy() + [x])
                    else:
                        assert False  # should never happen
                    stack[:] = initial_stack

        r: List[List[str]] = []
        visitor(r, [], items)
        return "".join(_handle_cmds(x[:-1], x[-1]) for x in r)


def _handle_cmds(cmds: List[str], x: str) -> str:
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
            if latex in COMMANDS:
                x = COMMANDS[latex]
            elif cmd in (r"\text", r"\mathrm"):
                pass
            else:
                if innermost:
                    x = COMMANDS.get(x, x)
                if cmd in COMMANDS:
                    # must be some unicode modifier, e.g. \dot, \vec
                    assert cmd in HAS_ARG  # nosec
                    x += COMMANDS[cmd]
                elif cmd not in IGNORE_AS_FALLBACK:
                    x = latex
            innermost = False
    else:
        x = COMMANDS.get(x, x)
    return x
