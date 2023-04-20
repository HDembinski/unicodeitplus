=============
unicodeitplus
=============

.. image:: https://img.shields.io/pypi/v/unicodeitplus.svg
        :target: https://pypi.python.org/pypi/unicodeitplus

Convert simple LaTeX into an unicode approximation.

This package provides a more complete LaTeX to Unicode converter than `unicodeit <https://github.com/svenkreiss/unicodeit/>`_. Like unicodeit, it is largely based on ``unimathsymbols.txt`` from Günter Milde, which is maps LaTeX macros to Unicode symbols.

unicodeitplus uses a better parser (generated from EBNF with the fantastic `Lark library <https://github.com/lark-parser/lark>`_), which fixes a few bugs in unicodeit and also allows one to parse a mix of text and math code, like ``$p_T$ / GeV $c^{-1}$``.

Examples
--------

==================================  =============
LaTeX                               Unicode
==================================  =============
``\alpha``                          ``𝛼``
``\beta``                           ``𝛽``
``\gamma``                          ``𝛾``
``\Gamma``                          ``𝛤``
``\infty``                          ``∞``
``e^+``                             ``𝑒⁺``
``\mu^-``                           ``𝜇⁻``
``\exists``                         ``∃``
``\in``                             ``∈``
``\int``                            ``∫``
``\sum``                            ``∑``
``\partial``                        ``∂``
``\slash{\partial}``                ``∂̸``
``\longrightarrow``                 ``⟶``
``\to``                             ``→``
``p\bar{p}``                        ``𝑝𝑝̄``
``\mathrm{t}\bar{\mathrm{t}}``      ``tt̄``
``\mathcal{H}``                     ``ℋ``
``\mathbb{R}``                      ``ℝ``
``\underline{x}``                   ``𝑥̲``
``\phone``                          ``☎``
``\checkmark``                      ``✓``
``\dot{x}``                         ``𝑥̇``
``\ddot{x}``                        ``𝑥̈``
``\vec{x}``                         ``𝑥⃗``
``A^6``                             ``𝐴⁶``
``m_0``                             ``𝑚₀``
``\Im``                             ``ℑ``
``\Re``                             ``ℜ``
``\hbar``                           ``ℏ``
``\perp``                           ``⟂``
``\parallel``                       ``∥``
``\therefore``                      ``∴``
``\because``                        ``∵``
``\subset``                         ``⊂``
``\supset``                         ``⊃``
``p_T / \mathrm{GeV} c^{-1}``       ``𝑝ₜ/GeV𝑐⁻¹``
``K^0_S``                           ``𝐾⁰ₛ``
``D^{\ast\ast} \to hhee``           ``𝐷**→ℎℎ𝑒𝑒``
``A \mathbf{x} \simeq \mathbf{b}``  ``𝐴𝐱≃𝐛``
==================================  =============
