import os
import re
import time
import shutil
import subprocess
from pathlib import Path
from datetime import datetime

EXP_LOG_DIR = Path(r"C:\Users\akiel\Downloads\all\all\Thesis_Experiments_Final_33-main\project_5_scenario2_lowpoison_stealth\src_code\output_logs")
REPO_DIR = Path(r"C:\Users\akiel\Downloads\thesis_auto_PC3")
DEST_DIR = REPO_DIR / "output_logs" / "PC03_H2_stealth_dirty300"

UPLOAD_ROUNDS = {1, 50, 100, 150, 200, 250, 300}
uploaded = set()

DEST_DIR.mkdir(parents=True, exist_ok=True)

def run(cmd):
    print("RUN:", cmd)
    subprocess.run(cmd, cwd=str(REPO_DIR), shell=True)

def copy_txt_logs():
    DEST_DIR.mkdir(parents=True, exist_ok=True)
    for src in EXP_LOG_DIR.glob("*.txt"):
        dst = DEST_DIR / src.name
        try:
            shutil.copy2(src, dst)
        except PermissionError:
            # log may be open; try again later
            pass

def find_max_round():
    max_round = 0
    for path in EXP_LOG_DIR.glob("*.txt"):
        try:
            text = path.read_text(encoding="utf-8", errors="ignore")
        except Exception:
            continue
        rounds = re.findall(r"\|\s*Round:\s*(\d+)\s*\|", text)
        for r in rounds:
            max_round = max(max_round, int(r))
    return max_round

def upload(reason):
    copy_txt_logs()
    proof = DEST_DIR / "PC03_UPLOAD_PROOF.txt"
    proof.write_text(f"{reason}\nUploaded at {datetime.now()}\n", encoding="utf-8")

    run("git pull")
    run(r"git add output_logs\PC03_H2_stealth_dirty300\*.txt")
    run(f'git commit -m "PC03 H2 txt upload {reason}"')
    run("git push")

print("PC03 monitor started. Uploading at rounds:", sorted(UPLOAD_ROUNDS))

while True:
    r = find_max_round()
    print("Current detected round:", r)

    if r in UPLOAD_ROUNDS and r not in uploaded:
        uploaded.add(r)
        upload(f"round_{r}")

    if r >= 300:
        upload("final_round_300")
        print("Monitor finished.")
        break

    time.sleep(60)