#! /bin/bash
export TERM=xterm
RED=$(tput setaf 1)
GREEN=$(tput setaf 2)
YELLOW=$(tput setaf 3)
NORMAL=$(tput op)

bridge_name='default'
#create virtual bridge
virsh net-define $bridge_name'.xml'
vursg net-start $bridge_name

#create qemu image
qemu_image_install="qemu-img create -f qcow2 ./baseimage.qcow2 8G"
$qemu_image_install
echo -e "${GREEN}'Successful : Create qemu image '${NORMAL}"

#create kvm-image from ubuntu archive
virt-install \
  --name base-image \
  --ram 1024 \
  --disk path=./baseimage.qcow2 \
  --vcpus 1 \
  --os-type linux \
  --graphics none \
  --console pty,target_type=serial \
  --location 'http://kr.archive.ubuntu.com/ubuntu/dists/xenial/main/installer-amd64' \
  --extra-args 'console=ttyS0,115200n8 serial'

#shutdown base-image
virsh shutdown base-image

#mount guest's disk and enable a service
guestmount -d base-image -i /mnt
ln -s /mnt/lib/systemd/system/getty@.service /mnt/etc/systemd/system/getty.target.wants/getty@ttyS0.service
umount /mnt
