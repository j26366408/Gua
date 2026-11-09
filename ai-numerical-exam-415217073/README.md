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
git clone fortran-history.bundle restored-project
cd restored-project
git log --oneline
```

透過 GitHub API 同步程式碼與檔案，GitHub 同步提交有自己的 SHA；原始本地 SHA 存於 bundle 與 evidence/project.json。

## 網頁

`dist/index.html` 是自含式單一網頁，包含題目、過程、完整原始碼、驗證結果、下載版控歷史與互動評分。AI 自評為 100 分，正式成績依教師評定。
