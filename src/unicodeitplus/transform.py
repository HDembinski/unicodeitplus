"""Tools to transform LaTeX tree into unicode."""
from . import _make_data  # noqa, imported for side-effects
from .data import COMMANDS
from lark import Transformer as TransformerBase, Token
from typing import List, Any, Union

HAS_ARG = {
    r"_",
    r"^",
    r"\grave",
    r"\acute",
    r"\hat",
    r"\tilde",
    r"\bar",
    r"\overline",
    r"\breve",
    r"\dot",
    r"\ddot",
    r"\slash",
    r"\mathcal",
    r"\mathbf",
    r"\mathbb",
    r"\mathring",
    r"\mathrm",
    r"\check",
    r"\utilde",
    r"\underbar",
    r"\underline",
    r"\not",
    r"\lvec",
    r"\vec",
    r"\LVec",
    r"\vec",
    r"\dddot",
    r"\ddddot",
    r"\overleftrightarrow",
    r"\underleftarrow",
    r"\underrightarrow",
    r"\text",
    r"\left",
    r"\right",
    r"\big",
    r"\Big",
    r"\Bigg",
    r"\sqrt",
}

IGNORE_AS_FALLBACK = {
    r"\text",
    r"\mathbf",
    r"\mathrm",
    r"\left",
    r"\right",
    r"\big",
    r"\Big",
    r"\Bigg",
}

ESCAPED = {
    r"\}": "}",
    r"\{": "{",
    "\\\\": "\\",
}


class Transformer(TransformerBase):  # type:ignore
    """Convert Tree to Unicode."""

    def start(self, ch: List[Any]) -> str:
        """Handle start token."""
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
        """Handle character token."""
        return ch.value  # type:ignore

    def COMMAND(self, ch: Token) -> str:
        """Handle command token."""
        return ch.value.strip()  # type:ignore

    def math(self, ch: List[Any]) -> str:
        """Handle math token."""
        return _convert_math(ch)

    def group(self, ch: List[Any]) -> List[Any]:
        """Handle group token."""
        return ch

    def WS(self, ch: Token) -> str:
        """Handle whitespace token."""
        return ch.value  # type:ignore


def _convert_math(items: List[Any]) -> str:
    r: List[Union[str, List[Any]]] = []
    stack: List[str] = []

    def visitor(
        r: List[Union[str, List[Any]]], stack: List[str], items: List[Any]
    ) -> None:
        pop = -1
        for x in items:
            if pop >= 0:
                pop -= 1
            if isinstance(x, str):
                if x in HAS_ARG:
                    if x == r"\sqrt":
                        r.append(r"\sqrt")
                        stack.append(r"\overline")
                    else:
                        stack.append(x)
                    pop = 1
                elif not x.isspace() or (stack and stack[-1] == r"\text"):
                    r.append(stack.copy() + [x])
            elif isinstance(x, list):
                visitor(r, stack, x)
            else:
                assert False  # should never happen
            if pop == 0:
                stack.pop()

    visitor(r, stack, items)

    for i, x in enumerate(r):
        r[i] = _handle_cmds(x)  # type:ignore

    return "".join(str(x) for x in r)


def _handle_cmds(items: List[str]) -> str:
    # - x can be a character or a command, like \alpha
    # - cmd_stack contains stack with commands, may be empty
    # - to transform ^{\alpha} or \text{x} correctly, we first try to
    #   convert innermost command and x as a unit
    # - commands are treated independently only if previous step fails
    *cmd_stack, x = items
    if cmd_stack:
        innermost = True
        for cmd in reversed(cmd_stack):
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
