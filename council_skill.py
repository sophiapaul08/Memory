#!/usr/bin/env python3
"""Council skill: answers questions by searching memory files for relevant context."""
import sys
import os
import glob


def load_memory(base_dir):
    memories = {}
    for path in sorted(glob.glob(os.path.join(base_dir, "*.md"))):
        with open(path) as f:
            memories[os.path.basename(path)] = f.read()
    return memories


def search_memory(memories, query):
    terms = [t.lower() for t in query.split() if len(t) > 2]
    if not terms:
        terms = [query.lower()]
    results = []
    for name, content in memories.items():
        lines = content.splitlines()
        matches = [
            line.strip()
            for line in lines
            if line.strip() and any(t in line.lower() for t in terms)
        ]
        if matches:
            results.append((name, matches))
    return results


def council(question):
    base_dir = os.path.dirname(os.path.abspath(__file__))
    memories = load_memory(base_dir)

    print(f"Question: {question}\n")
    print("=== Council Response ===\n")

    results = search_memory(memories, question)

    if results:
        print("Relevant knowledge found:\n")
        for name, matches in results:
            print(f"  [{name}]")
            for m in matches:
                print(f"    - {m}")
            print()
    else:
        print("No direct matches found in memory files.\n")
        print("Available knowledge bases:")
        for name in memories:
            first_line = memories[name].splitlines()[0] if memories[name] else "(empty)"
            print(f"  [{name}] {first_line}")
        print()

    print("Tip: Add more .md files to the Memory directory to expand the knowledge base.")


def main():
    if len(sys.argv) < 2:
        print("Usage: council_skill.py <question>")
        sys.exit(1)
    question = " ".join(sys.argv[1:])
    council(question)


if __name__ == "__main__":
    main()
