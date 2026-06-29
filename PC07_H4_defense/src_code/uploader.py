import os
import time
import subprocess
from datetime import datetime

# ===== SETTINGS =====
REPO_DIR = r"H:\thesis_auto"
SOURCE_DIR = r"C:\Users\akiel\Downloads\all\all\Thesis_Experiments_Final_33-main\project_7_scenario4_defense_comparison"
TARGET_DIR = r"H:\thesis_auto\PC07_H4_defense"
SECONDS = 50
PC_NAME = "PC07"
COMMIT_NAME = "PC07 auto H4 defense upload"

def run(cmd, cwd=REPO_DIR):
    print(f"\n>>> {cmd}")
    result = subprocess.run(
        cmd,
        cwd=cwd,
        shell=True,
        text=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT
    )
    print(result.stdout)
    return result.stdout

def copy_project():
    os.makedirs(TARGET_DIR, exist_ok=True)
    cmd = f'xcopy /E /I /Y "{SOURCE_DIR}" "{TARGET_DIR}"'
    run(cmd)

def git_upload():
    now = datetime.now().strftime("%Y%m%d_%H%M%S")
    marker = os.path.join(REPO_DIR, f"{PC_NAME}_last_auto_upload.txt")

    with open(marker, "w", encoding="utf-8") as f:
        f.write(f"{PC_NAME} auto upload at {now}\n")

    run("git pull")
    copy_project()
    run(f"git add PC07_H4_defense {PC_NAME}_last_auto_upload.txt")
    out = run(f'git commit -m "{COMMIT_NAME} {now}"')

    if "nothing to commit" in out.lower():
        print("Nothing new to commit.")
    else:
        run("git push")

print("=== AUTO GITHUB UPLOADER STARTED ===")
print(f"Repo: {REPO_DIR}")
print(f"Source: {SOURCE_DIR}")
print(f"Target: {TARGET_DIR}")
print(f"Every {SECONDS} seconds")

while True:
    try:
        git_upload()
    except Exception as e:
        print("ERROR:", e)

    print(f"\nSleeping {SECONDS} seconds...\n")
    time.sleep(SECONDS)