"""Generate examples for README.rst."""
from unicodeitplus import replace
from tabulate import tabulate

LATEX = r"""
\alpha \beta \gamma \Gamma \Im \Re \hbar
e^+ \mu^- \slash{\partial}
\exists \in \int \sum \partial \infty
\perp \parallel \therefore \because \subset \supset
\to \longrightarrow
p\bar{p} \mathrm{t}\bar{\mathrm{t}}
\mathcal{H} \mathbb{R}
\phone \checkmark
\underline{x} \dot{x} \ddot{x} \vec{x}
A^6 m_0
1.2 \times 10^{23}
$p_T / \mathrm{GeV} c^{-1}$
K^0_S
$D^{\ast\ast} \to hhee$
$A \cdot \mathbf{x} \simeq \mathbf{b}$
"""

table = {"LaTeX": [], "Unicode": []}
for latex in LATEX.split("\n"):
    if not latex or latex.isspace():
        continue
    table["LaTeX"].append(f"``{latex.strip('$')}``")
    if latex.startswith("$"):
        s = replace(latex.strip("$"))
    else:
        s = " ".join(replace(x) for x in latex.split())
    table["Unicode"].append(f"``{s}``")

print(tabulate(table, headers="keys", tablefmt="rst"))
