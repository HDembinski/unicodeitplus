=============
unicodeitplus
=============

.. image:: https://img.shields.io/pypi/v/unicodeitplus.svg
        :target: https://pypi.python.org/pypi/unicodeitplus

Convert simple LaTeX into an unicode approximation and paste it anywhere.

This package provides a more complete LaTeX to Unicode converter than `unicodeit <https://github.com/svenkreiss/unicodeit/>`_. ``unicodeitplus`` uses a better parser (generated from EBNF with the fantastic `Lark library <https://github.com/lark-parser/lark>`_) than ``unicodeit``, which handles some code on which ``unicodeit`` fails, and allows one to parse a mix of text and math code, like::

    $p_T$ / GeV $c^{-1}$

I want to eventually merge this project into ``unicodeit``, discussions with the maintainer of ``unicodeit`` are ongoing.

LaTeX to Unicode: How does this even work?
------------------------------------------
Unicode contains many subscript and superscript characters. It also contains font variations of characters of both latin and greek characters, including italic, boldface, bold italic, and more. It contains a lot of special mathematical characters and diacritical marks, which we use to approximate LaTeX renderings using just unicode characters.

Like ``unicodeit``, ``unicodeitplus`` is largely based on ``unimathsymbols.txt`` from Günter Milde, which provides the mapping between LaTeX macros and Unicode symbols.

Caveats
-------
- Only a subset of all LaTeX code can be converted to Unicode. Some Unicode characters simply don't exist. For example, subscript characters exist only for a subset of all lowercase latin characters, there are no subscript characters for uppercase latin characters, and all subscript or superscript characters are in roman font (upright).
- Some code is rendered the best best approximation, for example, ``p_T`` as ``𝑝ₜ``, assuming that a reasonable approximation is preferred over a failed conversion.
- Your font needs to contain glyphs for the Unicode characters, otherwise you will typically see a little box with the unicode character index.
- The visually best results seem to be obtained with monospace fonts.

Examples
--------

=======================================================  =================
LaTeX                                                    Unicode
=======================================================  =================
``\alpha \beta \gamma \Gamma \Im \Re \hbar``             ``𝛼 𝛽 𝛾 𝛤 ℑ ℜ ℏ``
``e^+ \mu^- \slash{\partial}``                           ``𝑒⁺ 𝜇⁻ ∂̸``
``\exists \in \int \sum \partial \infty``                ``∃ ∈ ∫ ∑ ∂ ∞``
``\perp \parallel \therefore \because \subset \supset``  ``⟂ ∥ ∴ ∵ ⊂ ⊃``
``\to \longrightarrow``                                  ``→ ⟶``
``p\bar{p} \mathrm{t}\bar{\mathrm{t}}``                  ``𝑝𝑝̄ tt̄``
``\mathcal{H} \mathbb{R}``                               ``ℋ ℝ``
``\phone \checkmark``                                    ``☎ ✓``
``\underline{x} \dot{x} \ddot{x} \vec{x}``               ``𝑥̲ 𝑥̇ 𝑥̈ 𝑥⃗``
``A^6 m_0``                                              ``𝐴⁶ 𝑚₀``
``1.2 \times 10^{23}``                                   ``1.2 × 10²³``
``p_T / \mathrm{GeV} c^{-1}``                            ``𝑝ₜ/GeV𝑐⁻¹``
``K^0_S``                                                ``𝐾⁰ₛ``
``D^{\ast\ast} \to hhee``                                ``𝐷**→ℎℎ𝑒𝑒``
``A \cdot \mathbf{x} \simeq \mathbf{b}``                 ``𝐴⋅𝐱≃𝐛``
=======================================================  =================
