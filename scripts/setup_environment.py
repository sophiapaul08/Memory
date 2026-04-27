#!/usr/bin/env python3
"""Set up the Memory project environment."""
import subprocess
import sys


def main():
    print("Setting up Memory environment...")

    result = subprocess.run(
        [sys.executable, "-m", "pip", "install", "--upgrade", "pip"],
        capture_output=True,
        text=True,
    )
    if result.returncode == 0:
        print("pip up to date.")
    else:
        print(f"pip upgrade warning: {result.stderr.strip()}")

    print("Environment ready.")


if __name__ == "__main__":
    main()
