#!/usr/bin/env python3
import argparse
import os
import glob


def show_dashboard(query=None):
    base_dir = os.path.dirname(os.path.abspath(__file__))
    md_files = sorted(glob.glob(os.path.join(base_dir, "*.md")))

    print("=== Memory Dashboard ===\n")

    for path in md_files:
        name = os.path.basename(path)
        print(f"[{name}]")
        with open(path) as f:
            lines = f.read().strip().splitlines()
        for line in lines[:5]:
            print(f"  {line}")
        if len(lines) > 5:
            print(f"  ... ({len(lines)} lines total)")
        print()

    if query:
        print(f"Search: {query}\n")
        query_lower = query.lower()
        found_any = False
        for path in md_files:
            with open(path) as f:
                file_lines = f.readlines()
            matches = [l.rstrip() for l in file_lines if query_lower in l.lower()]
            if matches:
                found_any = True
                print(f"  [{os.path.basename(path)}]")
                for m in matches:
                    print(f"    {m}")
                print()
        if not found_any:
            print("  No matches found.")


def main():
    parser = argparse.ArgumentParser(description="Memory CLI")
    parser.add_argument(
        "--dashboard",
        nargs="?",
        const="",
        metavar="QUERY",
        help="Show dashboard; optionally search with QUERY",
    )
    args = parser.parse_args()

    if args.dashboard is not None:
        show_dashboard(args.dashboard if args.dashboard else None)
    else:
        parser.print_help()


if __name__ == "__main__":
    main()
