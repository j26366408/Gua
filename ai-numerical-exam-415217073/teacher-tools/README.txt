江文樺 415217073 AI數值方法：老師操作包

一、直接操作評分系統（免安裝）
雙擊 scoring.html，以瀏覽器開啟。
選擇前四題達標或未達標，按「計算得分」。
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
grade.py：Python 終端機評分程式，可執行 python grade.py。
fortran-history.bundle：本地端原版與逐行註解版完整版本歷史。
evidence/：原版、註解版編譯與三次隨機測試結果。

網頁上的即時加總示範以 JavaScript 在瀏覽器運算；真正的 Fortran 執行紀錄另外標示。
