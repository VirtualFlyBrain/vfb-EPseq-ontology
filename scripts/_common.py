"""Shared CLI bits: put src/ on the path (scripts run without installing the package)."""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))
