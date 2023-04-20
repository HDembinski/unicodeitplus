=============
unicodeitplus
=============

.. image:: https://img.shields.io/pypi/v/unicodeitplus.svg
        :target: https://pypi.python.org/pypi/unicodeitplus

Convert simple LaTeX into an unicode approximation.

This package is a more complete LaTeX to Unicode converter than `unicodeit <https://github.com/svenkreiss/unicodeit/>`_. Like unicodeit, it is largely based on ``unimathsymbols.txt`` from Günter Milde, which is maps LaTeX macros to Unicode symbols.

Examples
--------

===================================  =========
LaTeX                                Unicode
===================================  =========
``\alpha``                           𝛼
``\beta``                            𝛽
``\gamma``                           𝛾
``\Gamma``                           𝛤
``\infty``                           ∞
``e^+``                              𝑒⁺
``\mu^-``                            𝜇⁻
``\exists``                          ∃
``\in``                              ∈
``\int``                             ∫
``\sum``                             ∑
``\partial``                         ∂
``\to``                              →
``p\bar{p}``                         𝑝𝑝̄
``\mathrm{t}\bar{\mathrm{t}}``       tt̄
``\mathcal{H}``                      ℋ
``\mathbb{R}``                       ℝ
``\slash{\partial}``                 ∂̸
``\underline{x}``                    𝑥̲
``\sqrt{12}``                        √1̅2̅
``\phone``                           ☎
``\checkmark``                       ✓
``\dot{x}``                          𝑥̇
``\ddot{x}``                         𝑥̈
``\vec{x}``                          𝑥⃗
``A^6``                              𝐴⁶
``m_0``                              𝑚₀
``\Im``                              ℑ
``\Re``                              ℜ
``\hbar``                            ℏ
``\perp``                            ⟂
``\parallel``                        ∥
``\therefore``                       ∴
``\because``                         ∵
``\subset``                          ⊂
``\supset``                          ⊃
``p_T / \mathrm{GeV}c^{-1}``         𝑝ₜ/GeV𝑐⁻¹
===================================  =========
