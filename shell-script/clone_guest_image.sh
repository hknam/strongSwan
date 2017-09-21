#! /bin/bash
export TERM=xterm
RED=$(tput setaf 1)
GREEN=$(tput setaf 2)
YELLOW=$(tput setaf 3)
NORMAL=$(tput op)

number_of_clones=$1

#shutdown base-image
virsh shutdown base-image

#mount guest's disk and enable a service
guestmount -d base-image -i /mnt
ln -s /mnt/lib/systemd/system/getty@.service /mnt/etc/systemd/system/getty.target.wants/getty@ttyS0.service
umount /mnt


for ((count=1;count<=number_of_clones;count++)); do
  echo "$count"
done
