from pathlib import Path
import sys

PROJECT_DIR = Path(__file__).parent / '..'
PROJECT_DIR = PROJECT_DIR.resolve()

sys.path.insert(0, str(PROJECT_DIR))
