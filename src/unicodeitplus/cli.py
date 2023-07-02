"""Console script for unicodeitplus."""
import argparse
import sys
from unicodeitplus import UnicodeItPlus


def main() -> int:
    """Convert simple LaTeX into an unicode approximation to paste anywhere."""
    parser = argparse.ArgumentParser(description=main.__doc__)
    parser.add_argument("-r", "--preserve-roman", action="store_true", help="Do not italicize roman letters (A-Z a-z) in math")
    parser.add_argument("-w", "--preserve-math-whitespace", action="store_true", help="Preserve whitespace between math characters")
    parser.add_argument("-p", "--preamble", action="store", help="Override data file from a JSON file with custom commands")
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
