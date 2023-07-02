"""Console script for unicodeitplus."""
import argparse
import sys
from unicodeitplus import UnicodeItPlus


def main() -> int:
    """Convert simple LaTeX into an unicode approximation to paste anywhere."""
    parser = argparse.ArgumentParser(description=main.__doc__)
    parser.add_argument("ARG", nargs="+", help="some LaTeX code")
    args = parser.parse_args()
    options_dict = vars(args)
    sargs = " ".join(args.ARG)
    parser = UnicodeItPlus(options_dict)
    if "$" not in sargs:
        s = parser.replace(sargs)
    else:
        s = parser.parse(sargs)
    sys.stdout.write(s + "\n")
    return 0


if __name__ == "__main__":
    sys.exit(main())  # pragma: no cover
