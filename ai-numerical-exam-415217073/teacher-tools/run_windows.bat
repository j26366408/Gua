@echo off
chcp 65001 >nul
setlocal
cd /d "%~dp0"
where gfortran >nul 2>nul
if errorlevel 1 (
  echo 找不到 gfortran。請在已安裝 GNU Fortran 的電腦執行本檔。
  echo 程式碼是 sum_to_n.f90；網頁評分可直接開啟 scoring.html。
  pause
  exit /b 1
)
if not exist build mkdir build
gfortran -std=f2008 -Wall -Wextra -Werror -fcheck=all -O2 sum_to_n.f90 -o build\sum_to_n.exe
if errorlevel 1 (
  echo 編譯失敗，請參考上方訊息。
  pause
  exit /b 1
)
:again
build\sum_to_n.exe
choice /c YN /m "再次輸入 N？ Y=是 N=結束"
if errorlevel 2 exit /b
if errorlevel 1 goto again
