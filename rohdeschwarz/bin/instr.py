from .run_cli                 import run_cli
from rohdeschwarz.instruments import Instrument
import sys


def main():
    run_cli(Instrument)
    sys.exit(0)


if __name__ == "__main__":
    main()
