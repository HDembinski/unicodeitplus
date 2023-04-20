from unicodeitplus import replace
from tabulate import tabulate

LATEX = r"""
\alpha
\beta
\gamma
\Gamma
\infty
e^+
\mu^-
\exists
\in
\int
\sum
\partial
\slash{\partial}
\longrightarrow
\to
p\bar{p}
\mathrm{t}\bar{\mathrm{t}}
\mathcal{H}
\mathbb{R}
\underline{x}
\phone
\checkmark
\dot{x}
\ddot{x}
\vec{x}
A^6
m_0
\Im
\Re
\hbar
\perp
\parallel
\therefore
\because
\subset
\supset
p_T / \mathrm{GeV} c^{-1}
K^0_S
D^{\ast\ast} \to hhee
A \mathbf{x} \simeq \mathbf{b}
"""

table = {"LaTeX": [], "Unicode": []}
for latex in LATEX.split("\n"):
    if not latex or latex.isspace():
        continue
    table["LaTeX"].append(f"``{latex}``")
    table["Unicode"].append(f"``{replace(latex)}``")

print(tabulate(table, headers="keys", tablefmt="rst"))
