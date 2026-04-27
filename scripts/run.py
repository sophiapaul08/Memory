#!/usr/bin/env python3
"""Script runner: python scripts/run.py <script> [args...]"""
import sys
import runpy

if len(sys.argv) < 2:
    print("Usage: run.py <script> [args...]")
    sys.exit(1)

script = sys.argv[1]
sys.argv = sys.argv[1:]
runpy.run_path(script, run_name="__main__")
