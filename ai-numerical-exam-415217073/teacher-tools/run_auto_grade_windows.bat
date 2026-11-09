@echo off
chcp 65001 >nul
cd /d "%~dp0"
where py >nul 2>nul
if not errorlevel 1 (
  py -3 auto_grade.py --project . --output auto-assessment.json
) else (
  python auto_grade.py --project . --output auto-assessment.json
)
echo 報告為 auto-assessment.json，可匯入網頁重新評分。
pause
