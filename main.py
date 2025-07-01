import os
import sys
from core import run_app


# Add the project root directory to sys.path
project_root = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, project_root)


if __name__ == "__main__":
    run_app()
