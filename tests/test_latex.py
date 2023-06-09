import pytest
from unicodeitplus import parse, replace

REPLACE_TEST_CASES = {
    r"\infty": "∞",
    r"e^+": "𝑒⁺",
    r"\mu^-": "𝜇⁻",
    r"\int\sum\partial": "∫∑∂",
    r"\to": "→",
    r"p\bar{p}": "𝑝𝑝̄",
    r"\mathrm{p}\bar{\mathrm{p}}": "pp̄",
    r"p_\text{T} \text T": "𝑝ₜT",
    r"\mathcal{H}": "ℋ",
    r"\mathbb{R}": "ℝ",
    r"\slash{\partial}": "∂̸",
    r"\underline{x}": "𝑥̲",
    r"\phone": "☎",
    r"\checkmark": "✓",
    r"\dot{x}": "𝑥̇",
    r"\ddot{x}": "𝑥̈",
    r"A^6": "𝐴⁶",
    r"m_0": "𝑚₀",
    r"\Im": "ℑ",
    r"\Re": "ℜ",
    r"\hbar": "ℏ",
    r"\gamma": "𝛾",
    r"\Gamma": "𝛤",
    r"\perp": "⟂",
    r"\parallel": "∥",
    r"\therefore": "∴",
    r"\because": "∵",
    r"\subset": "⊂",
    r"\supset": "⊃",
}


@pytest.mark.parametrize("latex", REPLACE_TEST_CASES)
def test_replace(latex):
    expected = REPLACE_TEST_CASES[latex]
    got = replace(latex)
    assert expected == got


PARSE_TEST_CASES = {
    r"foo?!-1+2.;'\" \}  \\ $bar$": "foo?!-1+2.;'\" } \\ 𝑏𝑎𝑟",
    r"$\left(\mathbf{\alpha + 1}^2_x y\right)$ bar": "(𝛂+𝟏²ₓ𝑦) bar",
    r"$\beta^{12}$ $\bar p {}^foo$ $\bar \mathrm{t}$ ": "𝛽¹² 𝑝̄ᶠ𝑜𝑜 t̄ ",
    r"$D^{\ast\ast} \to hhee$": "𝐷**→ℎℎ𝑒𝑒",
    r"$\mathbf{xyz + 1}$": "𝐱𝐲𝐳+𝟏",
    r"$\sqrt {1Aas\alpha}$": "√1̅𝐴̅𝑎̅𝑠̅𝛼̅",
    r"$\vec{x} b^2 \vec\alpha\overline\alpha K^0_S p_\text{T} \text T$": "𝑥⃗𝑏²𝛼⃗𝛼̅𝐾⁰ₛ𝑝ₜT",
    r"$\sqrt{abcd}$": "√𝑎̅𝑏̅𝑐̅𝑑̅",
    r"$p_T / \text{GeV}c^{-1}$": "𝑝ₜ/GeV𝑐⁻¹",
    (
        r"Search for $ \mathrm{t}\overline{\mathrm{t}} $"
        r" in collisions at $ \sqrt{s}=13 $~TeV"
    ): "Search for tt̅ in collisions at √𝑠̅=13\xa0TeV",
    r"$\overline {\mathrm{a} b}$ foo": "a̅𝑏̅ foo",
    "{abc{d{e}}a}   {}": "{abc{d{e}}a} {}",
    r"foo\;bar\~": "foo\u2004bar~",
}


@pytest.mark.parametrize("latex", PARSE_TEST_CASES)
def test_parse(latex):
    expected = PARSE_TEST_CASES[latex]
    got = parse(latex)
    assert expected == got
