江文樺 415217073 AI數值方法：老師操作包

一、直接操作評分系統（免安裝）
雙擊 scoring.html，以瀏覽器開啟。
輸入前四題的實際結果，按「檢查輸入並自動評分」。
每題達標給 20 分；第五題系統自身通過檢查時給 20 分。

二、執行真正的 Fortran 程式（需先安裝 gfortran）
Windows：解壓縮全部檔案，雙擊 run_windows.bat。
macOS/Linux：於資料夾終端機執行 sh run_macos_linux.sh。
腳本會先編譯 sum_to_n.f90，成功後接受您輸入 N 並輸出總和。
可重複輸入不同 N。範圍為 1 到 10,000,000。
如果電腦未安裝 gfortran，腳本會明確提示，請使用課程已配置的 Fortran 環境。

手動編譯方式：
mkdir build
gfortran -std=f2008 -Wall -Wextra -Werror -fcheck=all -O2 sum_to_n.f90 -o build/sum_to_n

三、其他檔案
auto_grade.py：真正執行編譯與測試的自動評分程式。
fortran-history.bundle：本地端原版與逐行註解版完整版本歷史。
evidence/：原版、註解版編譯與三次隨機測試結果。

網頁上的即時加總示範以 JavaScript 在瀏覽器運算；真正的 Fortran 執行紀錄另外標示。

四、真正自動評分（新版第五題）
需要 Python 3.9 以上、Git、gfortran，以及可連線 GitHub 的網路。
Windows：雙擊 run_auto_grade_windows.bat。
macOS/Linux：執行 sh run_auto_grade_macos_linux.sh。
也可手動執行 python auto_grade.py --project . --output auto-assessment.json。
系統會實際編譯及執行 Fortran、重新隨機驗算三組、還原 Git bundle 檢查原版與註解版，並下載 GitHub 檔案核對內容。
輸出的 auto-assessment.json 可匯入 scoring.html。網頁會重新判定各題，不會直接相信 JSON 裡的總分。
若缺少工具或網路暫時無法存取，會標為 unverified（待驗證）。
網頁本身只能依輸入紀錄比對與連線查 GitHub；重新實際執行 Fortran 必須使用上述 Python 評分程式。
