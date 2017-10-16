#! /bin/bash
export TERM=xterm
RED=$(tput setaf 1)
GREEN=$(tput setaf 2)
YELLOW=$(tput setaf 3)
NORMAL=$(tput op)

bridge_name='default'
#create virtual bridge
virsh net-define $bridge_name'.xml'
virsh net-start $bridge_name

package_update="apt-get update"
package_install="apt-get install -y "

#$package_update
echo -e "${GREEN}'Successful : Update package sources'${NORMAL}"

#install softwares
install_package_list='bridge-utils qemu-kvm virt-manager libvirt-bin libguestfs-tools virtinst haveged'
$package_install$install_package_list
echo -e "${GREEN}'Successful : Install packages from custom repo '${NORMAL}"

#create image folder
mkdir -p ../images

#create qemu image
qemu_image_install="qemu-img create -f qcow2 ../images/baseimage.qcow2 8G"
$qemu_image_install
echo -e "${GREEN}'Successful : Create qemu image '${NORMAL}"

echo "#######################################################################"
echo "# Important step"
echo "# After install ubuntu-server, base-image should be off, using ctrl+]"
echo "# And execute commands as below"
echo "#######################################################################"

echo "mount guest's disk and enable a service"
echo "guestmount -d base-image -i /mnt"
echo "ln -s /mnt/lib/systemd/system/getty@.service /mnt/etc/systemd/system/getty.target.wants/getty@ttyS0.service"
echo "umount /mnt"

sleep 5

#create kvm-image from ubuntu archive
virt-install \
  --name base-image \
  --ram 1024 \
  --disk path=../images/baseimage.qcow2 \
  --vcpus 1 \
  --os-type linux \
  --graphics none \
  --console pty,target_type=serial \
  --location 'http://kr.archive.ubuntu.com/ubuntu/dists/xenial/main/installer-amd64' \
  --extra-args 'console=ttyS0,115200n8'

pidof virt-install | cut -d' ' -f1
if [ $? -eq 0 ]; then
    echo -e "${GREEN}'Successful : Install ubuntu-server base image from repository '${NORMAL}"
else
    echo -e "${RED}'Fail : Install ubuntu-server base image from repository '${NORMAL}"
fi

#shutdown base-image
virsh shutdown base-image
echo -e "${GREEN}'Successful : Shutdown base-image '${NORMAL}"



#echo -e "${GREEN}'Successful : mount guest's disk and enable a service '${NORMAL}"
