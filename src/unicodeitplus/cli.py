"""Console script for unicodeitplus."""
import argparse
import sys
from unicodeitplus import replace, parse


def main() -> int:
    """Convert simple LaTeX into an unicode approximation to paste anywhere."""
    parser = argparse.ArgumentParser(description=main.__doc__)
    parser.add_argument("ARG", nargs="+", help="some LaTeX code")
    args = parser.parse_args()
    sargs = " ".join(args._)
    if "$" not in sargs:
        s = replace(sargs)
    else:
        s = parse(sargs)
    print(s)
    return 0


if __name__ == "__main__":
    sys.exit(main())  # pragma: no cover
