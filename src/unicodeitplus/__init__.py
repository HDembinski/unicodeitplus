"""Top-level package for unicodeitplus."""
from importlib.metadata import version
from .parser import parser
from .transform import transform
from pathlib import Path

__version__ = version("unicodeitplus")
__all__ = ["replace"]

_cdir = Path(__file__).parent
_make_data = _cdir / "_make_data.py"
if _make_data.stat().st_mtime > (_cdir / "data.py").stat().st_mtime:
    from importlib import import_module

    import_module("unicodeitplus._make_data").write_data()


def parse(s: str) -> str:
    """
    Parse simple LaTeX code and replace it by an unicode approximation.
    """
    tree = parser.parse(s)
    return transform(tree)


def replace(s: str) -> str:
    """
    Replace simple LaTeX code by unicode approximation.
    """
    return parse(f"${s}$")
