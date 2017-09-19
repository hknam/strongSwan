#! /bin/bash
export TERM=xterm
RED=$(tput setaf 1)
GREEN=$(tput setaf 2)
YELLOW=$(tput setaf 3)
NORMAL=$(tput op)

number_of_clones=$1

for ((count=1;count<=number_of_clones;count++)); do
  echo "$count"
done
