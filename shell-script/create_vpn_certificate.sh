#! /bin/bash
export TERM=xterm
RED=$(tput setaf 1)
GREEN=$(tput setaf 2)
YELLOW=$(tput setaf 3)
NORMAL=$(tput op)

server_ip='192.168.122.2'

#speed up the key generation using haveged
systemctl enable haveged
systemctl start haveged
