from .run_cli                 import run_cli
from rohdeschwarz.instruments import Vna
import sys


def main():
    run_cli(Vna)
    sys.exit(0)


if __name__ == "__main__":
    main()
