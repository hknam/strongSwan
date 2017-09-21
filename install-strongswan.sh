#! /bin/bash
export TERM=xterm
RED=$(tput setaf 1)
GREEN=$(tput setaf 2)
YELLOW=$(tput setaf 3)
NORMAL=$(tput op)

package_install="apt-get install -y "
package_update="apt-get update"
wget_install="wget "
uncompress_tar="tar xvf "
move_folder='cd '

#package update
$package_update
echo -e "${GREEN}'Successful : Update package sources'${NORMAL}"

#install softwares
install_package_list='wget make gcc libgmp3-dev build-essential bridge-utils qemu libvirt-bin libguestfs-tools virtinst haveged'
$package_install$install_package_list
echo -e "${GREEN}'Successful : Install packages from custom repo '${NORMAL}"

#strongSwan source code download
strongswan_url='https://download.strongswan.org/strongswan-5.6.0.tar.bz2'
$wget_install$strongswan_url
echo -e "${GREEN}'Successful : Install strongSwan source file from '$strongswan_url${NORMAL}"

#unpack the strongSwan source code
strongswan_source_file=${strongswan_url:32}
echo $strongswan_source_file
$uncompress_tar$strongswan_source_file
echo -e "${GREEN}'Successful : Unpack the tar file '${NORMAL}"

#move strongSwan directory
target_strongswan_dir=${strongswan_source_file:0:16}
cd $target_strongswan_dir
strongswan_dir=$PWD

#configure
configure=$strongswan_dir$'/configure --prefix=/usr --sysconfdir=/etc'
$configure
echo -e "${GREEN}'Successful : Configure strongSwan using options '${NORMAL}"

#make
make
echo -e "${GREEN}'Successful : Build the strongSwan source '${NORMAL}"

#install strongSwan
make install
echo -e "${GREEN}'Successful : Install the strongSwan '${NORMAL}"
