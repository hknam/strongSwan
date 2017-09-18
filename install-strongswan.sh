#! /bin/bash
export TERM=xterm
RED=$(tput setaf 1)
GREEN=$(tput setaf 2)
YELLOW=$(tput setaf 3)
NORMAL=$(tput op)

package_install="apt-get install -y libguestfs-tools"
package_update="apt-get update"
wget_install="wget "
uncompress_tar="tar xvf "
move_folder='cd '

$package_update
echo -e "${GREEN}'Successful : Update package sources'${NORMAL}"

install_package_list='wget make gcc libgmp3-dev build-essential bridge-utils qemu libvirt-bin libguestfs-tools'
$package_install$install_package_list
echo -e "${GREEN}'Successful : Install packages from custom repo '${NORMAL}"

strongswan_url='https://download.strongswan.org/strongswan-5.6.0.tar.bz2'
$wget_install$strongswan_url
echo -e "${GREEN}'Successful : Install strongSwan source file from '$strongswan_url${NORMAL}"

strongswan_source_file=${strongswan_url:32}
echo $strongswan_source_file
$uncompress_tar$strongswan_source_file
echo -e "${GREEN}'Successful : Unpack the tar file '${NORMAL}"


target_strongswan_dir=${strongswan_source_file:0:16}
cd $target_strongswan_dir
strongswan_dir=$PWD

configure=$strongswan_dir$'/configure --prefix=/usr --sysconfdir=/etc'
$configure
echo -e "${GREEN}'Successful : Configure strongSwan using options '${NORMAL}"

make
echo -e "${GREEN}'Successful : Build the strongSwan source '${NORMAL}"

make install
echo -e "${GREEN}'Successful : Install the strongSwan '${NORMAL}"
