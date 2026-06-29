import os
import time
import subprocess
from datetime import datetime

# ============================================================
# AUTO GITHUB UPLOADER FOR PC07 / HYPOTHESIS 4 DEFENSE RUN
# Copies the whole project into H:\thesis_auto\PC07_H4_defense
# and pushes to GitHub every 50 seconds.
# ============================================================

REPO_DIR = r"H:\thesis_auto"

SOURCE_DIR = (
    r"C:\Users\akiel\Downloads\all\all"
    r"\Thesis_Experiments_Final_33-main"
    r"\project_7_scenario4_defense_comparison"
)

TARGET_FOLDER_NAME = "PC07_H4_defense"
TARGET_DIR = os.path.join(REPO_DIR, TARGET_FOLDER_NAME)

SECONDS = 50
PC_NAME = "PC07"
COMMIT_PREFIX = "PC07 auto H4 defense upload"


def run(cmd, cwd=REPO_DIR, allow_fail=False):
    print("\n>>>", cmd)
    result = subprocess.run(
        cmd,
        cwd=cwd,
        shell=True,
        text=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
    )
    print(result.stdout)

    if result.returncode != 0 and not allow_fail:
        print(f"WARNING: command returned code {result.returncode}")

    return result.stdout, result.returncode


def check_paths():
    if not os.path.isdir(REPO_DIR):
        raise RuntimeError(f"Repo folder not found: {REPO_DIR}")

    if not os.path.isdir(SOURCE_DIR):
        raise RuntimeError(f"Source folder not found: {SOURCE_DIR}")

    os.makedirs(TARGET_DIR, exist_ok=True)


def copy_project_with_robocopy():
    """
    Robocopy does not ask the annoying xcopy F/D question.
    Exit codes 0-7 are normal/success-ish for robocopy.
    """
    cmd = (
        f'robocopy "{SOURCE_DIR}" "{TARGET_DIR}" '
        f'/E /NFL /NDL /NJH /NJS /NP /R:1 /W:1'
    )

    out, code = run(cmd, cwd=REPO_DIR, allow_fail=True)

    if code <= 7:
        print(f"ROBOCOPY OK, exit code {code}")
    else:
        print(f"ROBOCOPY PROBLEM, exit code {code}")

    return out, code


def write_marker_file():
    now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    marker_path = os.path.join(REPO_DIR, f"{PC_NAME}_last_auto_upload.txt")

    with open(marker_path, "w", encoding="utf-8") as f:
        f.write(f"{PC_NAME} last auto upload: {now}\n")
        f.write(f"Source: {SOURCE_DIR}\n")
        f.write(f"Target: {TARGET_DIR}\n")

    return marker_path


def git_upload_once():
    now_commit = datetime.now().strftime("%Y%m%d_%H%M%S")

    print("\n============================================================")
    print(f"AUTO UPLOAD ITERATION: {now_commit}")
    print("============================================================")

    check_paths()

    run("git pull", cwd=REPO_DIR, allow_fail=True)

    copy_project_with_robocopy()

    marker_path = write_marker_file()
    marker_name = os.path.basename(marker_path)

    run(f'git add "{TARGET_FOLDER_NAME}" "{marker_name}"', cwd=REPO_DIR, allow_fail=True)

    commit_msg = f"{COMMIT_PREFIX} {now_commit}"
    out, code = run(f'git commit -m "{commit_msg}"', cwd=REPO_DIR, allow_fail=True)

    lower = out.lower()

    if "nothing to commit" in lower or "working tree clean" in lower:
        print("Nothing new to commit. Logs may not have changed yet.")
        return

    run("git push", cwd=REPO_DIR, allow_fail=True)


def main():
    print("=== AUTO GITHUB UPLOADER STARTED ===")
    print(f"Repo:   {REPO_DIR}")
    print(f"Source: {SOURCE_DIR}")
    print(f"Target: {TARGET_DIR}")
    print(f"Every:  {SECONDS} seconds")
    print("Stop with CTRL + C")

    while True:
        try:
            git_upload_once()
        except KeyboardInterrupt:
            print("\nStopped by user.")
            break
        except Exception as e:
            print("\nERROR:", repr(e))

        print(f"\nSleeping {SECONDS} seconds...\n")
        time.sleep(SECONDS)


if __name__ == "__main__":
    main()