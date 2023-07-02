"""Top-level package for unicodeitplus."""
try:
    from importlib.metadata import version

    __version__ = version("unicodeitplus")
except Exception:
    pass

from .parser import make_parser
from .transform import ToUnicode

__all__ = ["UnicodeItPlus"]


def parse(s: str) -> str:
    """Parse simple LaTeX code and replace it by an unicode approximation."""
    return parser.parse(s)  # type:ignore


def replace(s: str) -> str:
    """Replace simple LaTeX code by unicode approximation."""
    return parse(f"${s}$")

class UnicodeItPlus():
    def __init__(self, options = None):
        transformer = ToUnicode(options)
        self.parser = make_parser(transformer)
    
    def parse(self, s: str) -> str:
        """Parse simple LaTeX code and replace it by an unicode approximation."""
        return self.parser.parse(s)

    def replace(self, s: str) -> str:
        """Replace simple LaTeX code by unicode approximation."""
        return self.parser.parse(f"${s}$")
