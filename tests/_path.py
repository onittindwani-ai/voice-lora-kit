"""Make the tools folder importable from the tests."""
import sys
from pathlib import Path

TOOLS = Path(__file__).resolve().parent.parent / "tools"
ROOT = TOOLS.parent
if str(TOOLS) not in sys.path:
    sys.path.insert(0, str(TOOLS))
