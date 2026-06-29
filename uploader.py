from pathlib import Path

# -------------------------
# Patch options.py
# -------------------------
opt = Path("options.py")
s = opt.read_text(encoding="utf-8")

if "--github_autopush" not in s:
    insert = '''
    parser.add_argument('--github_autopush', type=int, default=0,
                        help="1 = auto git add/commit/push logs during training")

    parser.add_argument('--github_every', type=int, default=50,
                        help="auto-push every N rounds")

    parser.add_argument('--github_branch', type=str, default='pc5-h3-dirty',
                        help="GitHub branch to push to")

    parser.add_argument('--github_message_prefix', type=str, default='PC5 H3 dirty auto upload',
                        help="commit message prefix for auto GitHub upload")
'''
    s = s.replace("    args = parser.parse_args()", insert + "\n    args = parser.parse_args()")
    opt.write_text(s, encoding="utf-8")

# -------------------------
# Patch federated.py
# -------------------------
fed = Path("federated.py")
s = fed.read_text(encoding="utf-8")

if "import subprocess" not in s:
    s = s.replace("import random", "import random\nimport subprocess")

if "def github_autopush" not in s:
    marker = "class TeeLogger:"
    func = '''
def github_autopush(args, rnd, txt_log_path):
    """
    Auto-commit and push logs to GitHub every N rounds.
    This uploads output_logs and logs while the experiment is still running.
    """
    if not hasattr(args, "github_autopush") or args.github_autopush != 1:
        return
    if rnd % args.github_every != 0:
        return

    print("GITHUB_AUTOPUSH_START")
    print(f"round={rnd}")
    print(f"branch={args.github_branch}")
    print(f"txt_log_path={txt_log_path}")

    try:
        subprocess.run(["git", "add", "output_logs", "logs"], check=False)

        msg = f"{args.github_message_prefix} round {rnd}"
        commit_result = subprocess.run(["git", "commit", "-m", msg], check=False)

        subprocess.run(["git", "push", "origin", args.github_branch], check=False)

        print("GITHUB_AUTOPUSH_END")
    except Exception as e:
        print("GITHUB_AUTOPUSH_FAILED")
        print(str(e))


'''
    s = s.replace(marker, func + marker)

if "github_autopush(args, rnd, txt_log_path)" not in s:
    target = "                print(\"POISON_FRACTION_SENSITIVITY_METRICS_NOTE: compare Poison Acc, Val_Acc, and labels_changed across pf=0.05,0.10,0.25,0.50.\")\n                txt_log_file.flush()\n"
    replacement = target + "\n        github_autopush(args, rnd, txt_log_path)\n"
    if target in s:
        s = s.replace(target, replacement, 1)
    else:
        # fallback: add after every round flush
        s = s.replace("        txt_log_file.flush()\n", "        txt_log_file.flush()\n\n        github_autopush(args, rnd, txt_log_path)\n", 1)

fed.write_text(s, encoding="utf-8")

print("PATCH_DONE_PC5_AUTOPUSH")