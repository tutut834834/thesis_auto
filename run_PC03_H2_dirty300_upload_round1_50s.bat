@echo off
echo ============================================================
echo PC03 H2 DIRTY 300 - UPLOAD ROUND 1 AND EVERY 50 ROUNDS
echo ============================================================

cd /d C:\Users\akiel\Downloads\thesis_auto_PC3

echo Starting monitor uploader in second window...
start "PC03 ROUND UPLOAD MONITOR" cmd /c python monitor_upload_PC03_H2_rounds.py

echo Starting experiment...
cd /d C:\Users\akiel\Downloads\all\all\Thesis_Experiments_Final_33-main\project_5_scenario2_lowpoison_stealth\src_code

python -u federated.py --data=fmnist --device=cpu --local_ep=2 --bs=256 --num_agents=10 --rounds=300 --snap=1 --num_corrupt=1 --poison_frac=0.5 --class_per_agent=10 --base_class=5 --target_class=7 --clean_label=0 --verify_stealth_data=1 --verify_poisoning=1 --seed=3

echo Experiment finished. Doing final push...
cd /d C:\Users\akiel\Downloads\thesis_auto_PC3

mkdir output_logs\PC03_H2_stealth_dirty300 2>nul

copy /Y "C:\Users\akiel\Downloads\all\all\Thesis_Experiments_Final_33-main\project_5_scenario2_lowpoison_stealth\src_code\output_logs\*.txt" "C:\Users\akiel\Downloads\thesis_auto_PC3\output_logs\PC03_H2_stealth_dirty300\"

echo PC03 final upload at %date% %time% > output_logs\PC03_H2_stealth_dirty300\PC03_FINAL_UPLOAD_DONE.txt

git pull
git add output_logs\PC03_H2_stealth_dirty300\*.txt
git commit -m "PC03 final H2 dirty 300 txt upload"
git push

echo DONE.
pause