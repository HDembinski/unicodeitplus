"""Generate src/unicodeitplus/parser.py."""
import subprocess as subp
import sys
from pathlib import Path

fn_latex_grammar = Path(__file__).parent / "latex.g"

out = subp.check_output(
    [sys.executable, "-m", "lark.tools.standalone", fn_latex_grammar]
)

sys.stdout.write(out.decode())
