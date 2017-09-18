#! /bin/bash
export TERM=xterm
RED=$(tput setaf 1)
GREEN=$(tput setaf 2)
YELLOW=$(tput setaf 3)
NORMAL=$(tput op)

create_virtual_bridge="brctl addbr virbr0"
$create_virtual_bridge
echo -e "${GREEN}'Successful : Create virtual bridge '${NORMAL}"

qemu_image_install="qemu-img create -f qcow2 ./baseimage.qcow 8G"
$create_virtual_bridge
echo -e "${GREEN}'Successful : Create qemu image '${NORMAL}"
