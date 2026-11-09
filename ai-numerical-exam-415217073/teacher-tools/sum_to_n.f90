program sum_to_n ! 宣告主程式名稱
  use iso_fortran_env, only: int64, error_unit ! 使用 64 位元整數與標準錯誤輸出
  implicit none ! 禁止未宣告變數
  integer(int64) :: n, i, total ! 宣告上限、迴圈變數與加總結果
  integer :: ios ! 宣告輸入狀態碼
  print '(A)', 'Enter N (1..10000000):' ! 提示可接受的整數範圍
  read (*, *, iostat=ios) n ! 讀入 N 並記錄讀取狀態
  if (ios /= 0) then ! 判斷輸入是否失敗
    write (error_unit, '(A)') 'ERROR: input must be an integer.' ! 輸出非整數輸入的錯誤訊息
    stop 1 ! 以非零狀態結束程式
  end if ! 結束輸入失敗判斷
  if (n < 1_int64 .or. n > 10000000_int64) then ! 檢查 N 是否超出範圍
    write (error_unit, '(A)') 'ERROR: N must be in 1..10000000.' ! 輸出範圍錯誤訊息
    stop 1 ! 以非零狀態結束程式
  end if ! 結束範圍檢查
  total = 0_int64 ! 將累加結果初始化為零
  do i = 1_int64, n ! 從 1 迴圈到 N，預設每次加 1
    total = total + i ! 把本次整數加入總和
  end do ! 結束加總迴圈
  print '(A,I0,A,I0)', 'N = ', n, ', SUM = ', total ! 印出 N 與總和，I0 不保留多餘空白
end program sum_to_n ! 結束主程式
