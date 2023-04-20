from unicodeitplus.cli import main
import sys


def test_cli(capsys):
    sys.argv = ["prog", "foo $x^3$", "bar"]
    assert main() == 0
    out, err = capsys.readouterr()
    assert out == "foo 𝑥³ bar\n"
    assert err == ""
