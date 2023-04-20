"""Top-level package for unicodeitplus."""
try:
    from importlib.metadata import version

    __version__ = version("unicodeitplus")
except Exception:
    pass

from .parser import parser

__all__ = ["replace", "parse"]


def parse(s: str) -> str:
    """Parse simple LaTeX code and replace it by an unicode approximation."""
    return parser.parse(s)  # type:ignore


def replace(s: str) -> str:
    """Replace simple LaTeX code by unicode approximation."""
    return parse(f"${s}$")
