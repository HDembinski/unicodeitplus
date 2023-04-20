"""Console script for unicodeitplus."""
import argparse
import sys
from unicodeitplus import replace


def main() -> int:
    """Console script for unicodeitplus."""
    parser = argparse.ArgumentParser()
    parser.add_argument("_", nargs="*")
    args = parser.parse_args()
    print(" ".join(replace(arg) for arg in args._))
    return 0


if __name__ == "__main__":
    sys.exit(main())  # pragma: no cover
