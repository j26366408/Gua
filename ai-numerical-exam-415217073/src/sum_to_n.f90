program sum_to_n
  use iso_fortran_env, only: int64, error_unit
  implicit none
  integer(int64) :: n, i, total
  integer :: ios
  print '(A)', 'Enter N (1..10000000):'
  read (*, *, iostat=ios) n
  if (ios /= 0) then
    write (error_unit, '(A)') 'ERROR: input must be an integer.'
    stop 1
  end if
  if (n < 1_int64 .or. n > 10000000_int64) then
    write (error_unit, '(A)') 'ERROR: N must be in 1..10000000.'
    stop 1
  end if
  total = 0_int64
  do i = 1_int64, n
    total = total + i
  end do
  print '(A,I0,A,I0)', 'N = ', n, ', SUM = ', total
end program sum_to_n
