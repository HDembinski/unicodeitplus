"""Tools to transform LaTeX tree into unicode."""
from .data import COMMANDS
from lark import Tree, Token
from typing import Optional, List, Union
from dataclasses import dataclass


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


@dataclass
class State:
    """Current state of the transform function."""

    math: bool
    group: bool
    command: List[str]


def transform(ch: Union[Token, Tree], state: Optional[State] = None) -> str:
    """Transform Lark Tree into unicode string."""
    if state is None:
        state = State(False, False, [])

    if isinstance(ch, Tree):
        r = []
        if ch.data == "math":
            state.math = True
        if ch.data == "group":
            state.group = True
        for x in ch.children:
            r.append(transform(x, state))
        if ch.data == "math":
            state.math = False
        if ch.data == "group":
            state.group = False
            if state.command:
                state.command.clear()
        return "".join(r)

    if ch.type == "CHARACTER":
        x = ESCAPED.get(ch.value, ch.value)
        return _handle_cmd(state, x)
    if ch.type == "WS":
        return "" if state.math else " "
    if ch.type == "COMMAND":
        x = ch.value.strip()
        if x in HAS_ARG:
            if x == r"\sqrt":
                state.command.append(r"\overline")
                return COMMANDS[r"\sqrt"]
            state.command.append(x)
            return ""
        return _handle_cmd(state, x)
    # never arrive here
    assert False, f"unknown token {ch}"  # nosec


def _handle_cmd(state: State, x: str) -> str:
    # - x can be a character or a command, like \alpha
    # - state.command contains stack with commands, may be empty
    # - to transform ^{\alpha} or \text{x} correctly, we first try to
    #   convert innermost command and x as a unit
    # - they are treated independently only if previous step fails
    cmd_stack = state.command.copy()
    if state.math:
        cmd = cmd_stack[-1] if cmd_stack else ""
        latex = f"{cmd}{{{x}}}"
        if cmd and latex in COMMANDS:
            x = COMMANDS[latex]
            cmd_stack.pop()
        elif x.startswith(r"\\"):
            x = COMMANDS.get(x, x)
        elif cmd in (r"\text", r"\mathrm"):
            cmd_stack.pop()
        else:
            x = COMMANDS.get(x, x)
        for cmd in reversed(cmd_stack):
            if cmd in COMMANDS:
                # must be some unicode modifier, e.g. \dot, \vec
                assert cmd in HAS_ARG  # nosec
                x += COMMANDS[cmd]
            else:
                latex = f"{cmd}{{{x}}}"
                if latex in COMMANDS:
                    x = COMMANDS[latex]
                elif cmd not in IGNORE_AS_FALLBACK:
                    x = latex
    else:
        for cmd in reversed(state.command):
            x = f"{cmd}{{{x}}}"
    if state.command and not state.group:
        state.command.pop()
    return x
