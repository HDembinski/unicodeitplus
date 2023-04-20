from pathlib import Path
from typing import Dict


def _generate_sub_and_super_scripts() -> Dict[str, str]:
    import string

    # Wikipedia: https://en.wikipedia.org/wiki/Unicode_subscripts_and_superscripts

    cmds = {}

    greek_latex = (
        r"\alpha",
        r"\beta",
        r"\gamma",
        r"\delta",
        r"\epsilon",
        r"\zeta",
        r"\eta",
        r"\theta",
        r"\iota",
        r"\kappa",
        r"\lambda",
        r"\mu",
        r"\nu",
        r"\xi",
        "o",
        r"\pi",
        r"\rho",
        r"\sigma",
        r"\tau",
        r"\upsilon",
        r"\phi",
        r"\chi",
        r"\psi",
        r"\omega",
    )

    superscript_numbers = "⁰¹²³⁴⁵⁶⁷⁸⁹"
    for i, ch in enumerate(superscript_numbers):
        cmds[f"^{{{i}}}"] = ch

    subscript_numbers = "₀₁₂₃₄₅₆₇₈₉"
    for i, ch in enumerate(subscript_numbers):
        cmds[f"_{{{i}}}"] = ch

    superscript_lowercase = "ᵃᵇᶜᵈᵉᶠᵍʰⁱʲᵏˡᵐⁿᵒᵖ𐞥ʳˢᵗᵘᵛʷˣʸᶻ"
    superscript_uppercase = "ᴬᴮꟲᴰᴱꟳᴳᴴᴵᴶᴷᴸᴹᴺᴼᴾꟴᴿ ᵀᵁⱽᵂ   "
    for latex, ch in zip(
        string.ascii_letters, superscript_lowercase + superscript_uppercase
    ):
        if ch != " ":
            cmds[f"^{{{latex}}}"] = ch

    subscript_lowercase = "ₐ   ₑ  ₕᵢⱼₖₗₘₙₒₚ ᵣₛₜᵤᵥ ₓ  "
    for latex, ch in zip(string.ascii_letters, subscript_lowercase * 2):
        if ch != " ":
            cmds[f"_{{{latex}}}"] = ch

    superscript_lowercase_greek = " ᵝᵞᵟᵋ  ᶿᶥ          ᶹᵠᵡ  "
    subscript_lowercase_greek = " ᵦᵧ             ᵨ   ᵩᵪ  "
    for latex, sup, sub in zip(
        greek_latex, superscript_lowercase_greek, subscript_lowercase_greek
    ):
        if sup != " ":
            cmds[f"^{{{latex}}}"] = sup
        if sub != " ":
            cmds[f"_{{{latex}}}"] = sub

    return cmds


def _generate_from_unimathsymbols_txt() -> Dict[str, str]:
    d = Path(__file__).parent
    fn = None
    while d.parent is not None:
        d = d.parent
        if (d / "extern").exists():
            fn = d / "extern" / "unimathsymbols.txt"
            break
    assert fn is not None

    # Symbols extracted from extern/unimathsymbols.txt, which is under Copyright 2011 by
    # Günter Milde and licensed under the LaTeX Project Public License (LPPL)
    def match(comments: str) -> str:
        matches = [
            ("PLUS", "+"),
            ("MINUS", "-"),
            ("EQUALS", "="),
            ("LEFT PARENTHESIS", "("),
            ("RIGHT PARENTHESIS", ")"),
        ]
        for match, latex in matches:
            if match in comments:
                return latex
        assert False, f"unmatched: {comments}"  # nosec, never arrive here

    cmds = {}
    with open(fn) as f:
        for line in f:
            if line.startswith("#"):
                continue
            items = line.split("^")
            _, ch, latex, latex2, clas, category, requirements, comments = items
            comments = comments[:-1]
            if latex:
                if len(ch) > 1:
                    cmds[latex] = ch[1]
                else:
                    cmds[latex] = ch
            elif latex2:
                cmds[latex2] = ch
            elif comments.startswith("SUPERSCRIPT"):
                latex = f"^{{{match(comments)}}}"
                cmds[latex] = ch
            elif comments.startswith("SUBSCRIPT"):
                latex = f"_{{{match(comments)}}}"
                cmds[latex] = ch
            else:
                pass

    return cmds


def _corrections_and_enhancements() -> Dict[str, str]:
    cmds = {}
    cmds[r"^{\ast}"] = "*"
    cmds["h"] = "ℎ"
    cmds[r"\partial"] = "∂"
    cmds[r"\slash"] = "\u0338"
    cmds[r"\phone"] = "☎"
    cmds[r"\thinspace"] = "\u2009"
    return cmds


def _aliases(cmds: Dict[str, str]) -> None:
    alias = {
        r"\rightarrow": r"\to",
        r"\hslash": r"\hbar",
        r"\thinspace": r"\,",
    }
    for old, new in alias.items():
        cmds[new] = cmds[old]


def generate_data() -> str:
    """Generate source code for Python module with database of known LaTeX commands."""
    cmds = _generate_sub_and_super_scripts()
    cmds.update(_generate_from_unimathsymbols_txt())
    cmds.update(_corrections_and_enhancements())
    _aliases(cmds)

    chunks = [
        """\"\"\"
Symbols extracted from extern/unimathsymbols.txt.

extern/unimathsymbols.txt is under Copyright 2011 by Günter Milde and licensed under the
LaTeX Project Public License (LPPL).

As a Derived Work, this file is licensed under LaTeX Project Public License (LPPL).
\"\"\"

COMMANDS = {
"""
    ]
    for key in sorted(cmds):
        val = cmds[key]
        chunks.append(f"    {key!r}: {val!r},\n".replace("'", '"'))
    chunks.append("}\n")

    return "".join(chunks)


if __name__ == "__main__":
    print(generate_data())
else:
    fn_data = Path(__file__).parent / "data.py"
    if fn_data.stat().st_mtime < Path(__file__).stat().st_mtime:
        with open(fn_data, "w") as f:
            f.write(generate_data())
