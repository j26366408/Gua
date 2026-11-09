#!/bin/sh
set -eu
cd "$(dirname "$0")"
if ! command -v gfortran >/dev/null 2>&1; then
  printf '%s\n' '需要先安裝 GNU Fortran (gfortran)。'
  exit 1
fi
mkdir -p build
gfortran -std=f2008 -Wall -Wextra -Werror -fcheck=all -O2 sum_to_n.f90 -o build/sum_to_n
while true; do
  ./build/sum_to_n || true
  printf '%s' 'Run again? (y/n): '
  read -r again || exit 0
  case "$again" in y|Y) ;; *) exit 0 ;; esac
done
