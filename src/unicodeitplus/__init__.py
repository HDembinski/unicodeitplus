"""Top-level package for unicodeitplus."""
from importlib.metadata import version
from .parser import parser
from .transform import transform

__version__ = version("unicodeitplus")


def replace(s):
    tree = parser.parse(s)
    return transform(tree)
