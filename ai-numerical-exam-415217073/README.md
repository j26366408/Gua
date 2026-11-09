# AI數值方法：1 到 N 的 Fortran 加總測驗

姓名：江文樺；學號：415217073；日期：2026-11-09。

## 執行

```sh
mkdir -p build
gfortran -std=f2008 -Wall -Wextra -Werror -fcheck=all -O2 src/sum_to_n.f90 -o build/sum_to_n
echo 10 | ./build/sum_to_n
python3 verify.py
python3 grade.py
```

N 的範圍為 1 到 10,000,000；使用 64 位元整數與迴圈加總。
`evidence/` 保存實際執行紀錄。重跑 verify.py 會重新抽樣並更新 random-tests.json；提交頁面保留測驗當次紀錄。

## 本地原始 Git 歷史

`fortran-history.bundle` 保留本地端原版及逐行註解版兩次認錄，原版先編譯與驗證再提交，註解版重新編譯驗證後再提交。

```sh
git clone --branch main fortran-history.bundle restored-project
cd restored-project
git log --oneline
```

透過 GitHub API 同步程式碼與檔案，GitHub 同步提交有自己的 SHA；原始本地 SHA 存於 bundle 與 evidence/project.json。

## 網頁

`dist/index.html` 是自含式單一網頁，包含題目、過程、完整原始碼、驗證結果、下載版控歷史與互動評分。AI 自評為 100 分，正式成績依教師評定。


## 老師操作

網頁上方「老師操作區」新增 N 輸入、即時計算、三組隨機試算、評分入口與程式包下載。網頁試算以 JavaScript 執行；真正 Fortran 的執行紀錄仍在第一、二題。

`teacher-tools/` 含免安裝的 scoring.html，以及需 gfortran 的 Windows / macOS / Linux 編譯執行腳本。`dist/teacher-tools.zip` 為整包下載。


## 第五題：自動判定版

`auto_grade.py` 會真正編譯並執行 Fortran、隨機測試三組、從 bundle 還原兩版重新編譯、檢查每行註解與 Git 父子關係，再向公開 GitHub 下載檔案核對。

```sh
python3 auto_grade.py --project . --output auto-assessment.json
```

`assessment.js` 與網頁接受各題實際數據及 JSON 紀錄，由程式決定達標狀態；不用人先選達標。網頁可比對輸入及連線查 GitHub，真正重新編譯請執行 Python 評分器。`teacher-tools/scoring.html` 是可離線開啟的獨立評分頁（GitHub 即時核對仍需要網路）。
