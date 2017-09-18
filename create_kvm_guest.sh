#! /bin/bash
export TERM=xterm
RED=$(tput setaf 1)
GREEN=$(tput setaf 2)
YELLOW=$(tput setaf 3)
NORMAL=$(tput op)

create_virtual_bridge="brctl addbr virbr0"
$create_virtual_bridge
echo -e "${GREEN}'Successful : Create virtual bridge '${NORMAL}"

qemu_image_install="qemu-img create -f qcow2 ./baseimage.qcow2 8G"
$qemu_image_install
echo -e "${GREEN}'Successful : Create qemu image '${NORMAL}"

create_base_image="virt-install \
                  --name base-image \
                  --ram 1024 \
                  --disk path=./baseimage.qcow2 \
                  --os-type linux \
                  --graphics none \
                  --console pty,target_type=serial \
                  --cdrom './ubuntu-16.04.3-server-amd64.iso' \
                  --extra-args 'console=ttyS0,115200n8 serial'
"
$create_base_image
