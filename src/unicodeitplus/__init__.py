"""Top-level package for unicodeitplus."""
from importlib.metadata import version
from .parser import parser
from .transform import transform

__version__ = version("unicodeitplus")
__all__ = ["replace"]


def replace(s: str) -> str:
    """
    Replace simple LaTeX code by unicode approximation.
    """
    tree = parser.parse(s)
    return transform(tree)
