# text.py
# Prints and saves the full content of src_code folders.
# Use:
#   python text.py
# or:
#   python text.py C:\path\to\folder
#
# Output:
#   FULL_SRC_CODE_DUMP.txt

import os
import sys
from datetime import datetime

# File types we want to collect
ALLOWED_EXTENSIONS = {
    ".py", ".txt", ".md", ".sh", ".bat", ".slurm", ".json", ".yaml", ".yml",
    ".cfg", ".ini", ".tex"
}

# Folders we skip because they are huge/useless for code comparison
SKIP_DIRS = {
    "__pycache__", ".git", ".idea", ".vscode",
    "logs", "output_logs", "runs", "data", "datasets",
    "results", "checkpoints", "models_saved",
    "venv", ".venv", "env", "node_modules"
}

# Files we skip
SKIP_FILES = {
    "FULL_SRC_CODE_DUMP.txt"
}


def should_skip_dir(dirname):
    return dirname in SKIP_DIRS


def should_read_file(filename):
    if filename in SKIP_FILES:
        return False
    _, ext = os.path.splitext(filename)
    return ext.lower() in ALLOWED_EXTENSIONS


def safe_read(path):
    encodings = ["utf-8", "utf-8-sig", "latin-1", "cp1252"]
    for enc in encodings:
        try:
            with open(path, "r", encoding=enc) as f:
                return f.read()
        except UnicodeDecodeError:
            continue
        except Exception as e:
            return f"[ERROR READING FILE: {e}]"
    return "[ERROR: Could not decode file]"


def collect_files(root):
    collected = []

    for current_dir, dirs, files in os.walk(root):
        dirs[:] = [d for d in dirs if not should_skip_dir(d)]

        for file in sorted(files):
            if should_read_file(file):
                full_path = os.path.join(current_dir, file)
                collected.append(full_path)

    return sorted(collected)


def main():
    if len(sys.argv) > 1:
        root = sys.argv[1]
    else:
        root = os.getcwd()

    root = os.path.abspath(root)
    out_path = os.path.join(root, "FULL_SRC_CODE_DUMP.txt")

    files = collect_files(root)

    header = f"""
============================================================
FULL SRC CODE DUMP
Created: {datetime.now().strftime("%Y-%m-%d %H:%M:%S")}
Root folder: {root}
Number of files: {len(files)}
============================================================
"""

    print(header)

    with open(out_path, "w", encoding="utf-8") as out:
        out.write(header)

        for idx, path in enumerate(files, start=1):
            rel = os.path.relpath(path, root)
            content = safe_read(path)

            block_header = f"""

============================================================
FILE {idx}/{len(files)}
PATH: {rel}
FULL PATH: {path}
============================================================

"""
            print(block_header)
            print(content)

            out.write(block_header)
            out.write(content)
            out.write("\n\n")

    print("\n============================================================")
    print("DONE")
    print(f"Saved full dump to: {out_path}")
    print("============================================================")


if __name__ == "__main__":
    main()