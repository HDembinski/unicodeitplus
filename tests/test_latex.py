import pytest
from unicodeitplus import replace

LATEX_TEST_CASES = {
    r"foo?!-1+2. \}  \\ ": r"foo?!-1+2. } \\ ",
    r"$\left(\mathbf{\alpha + 1}^2_x y\right)$ bar": "(𝛂+𝟏²ₓ𝑦) bar",
    r"$\beta^{12}$ $\bar p {}^foo$ $\bar \mathrm{t}$ ": "𝛽¹² 𝑝̄ᶠ𝑜𝑜 t̄ ",
    r"$D^{\ast\ast} \to hhee$": "𝐷**→ℎℎ𝑒𝑒",
    r"$\mathbf{xyz + 1}$": "𝐱𝐲𝐳+𝟏",
    r"$\sqrt {1Aas\alpha}$": "√1̅𝐴̅𝑎̅𝑠̅𝛼̅",
    r"$\vec{x} b^2 \vec\alpha\overline\alpha K^0_S p_\text{T} \text T$": "𝑥⃗𝑏²𝛼⃗𝛼̅𝐾⁰ₛ𝑝ₜT",
    r"$\sqrt{abcd}$": "√𝑎̅𝑏̅𝑐̅𝑑̅",
    r"$p_T / \text{GeV}c^{-1}$": "𝑝ₜ/GeV𝑐⁻¹",
    (
        r"Search for resonant $ \mathrm{t}\overline{\mathrm{t}} $"
        r" production in proton-proton collisions at $ \sqrt{s}=13 $ TeV"
    ): "Search for resonant tt̅ production in proton-proton collisions at √𝑠̅=13 TeV",
}


@pytest.mark.parameterize("latex,expected", LATEX_TEST_CASES.items())
def test_test_strings(latex, expected):
    assert replace(latex) == expected
