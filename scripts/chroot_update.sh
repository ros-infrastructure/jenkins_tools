#!/bin/sh -ex

/bin/echo "vvvvvvvvvvvvvvvvvvv  update_chroot.sh vvvvvvvvvvvvvvvvvvvvvv"
/bin/echo $*
id

apt-get install -y python-setuptools ccache wget curl curl-ssl sudo git-buildpackage dput python-yaml python-pip python-support python-setuptools

case $1 in
    fat)
        apt-get install -y wget git-core mercurial subversion \
            ccache lsb-release ccache cmake libopenmpi-dev \
            libboost-dev libboost-all-dev python-all \
            gccxml python-empy python-yaml python-nose python-mock python-minimock \
            python-numpy \
            python-wxgtk2.8 \
            openssl sudo liblog4cxx10-dev libgtest-dev libbz2-dev \
            libhdf5-openmpi-dev octave3.2 libtbb-dev libtbb2 \
	    debhelper python-argparse
        ;;
esac

mkdir -p $HOME

git config --global user.name  "Willow Garage Package Ranch Bot"
git config --global user.email "pkgranchbot@willowgarage.com"

/bin/echo "^^^^^^^^^^^^^^^^^^  update_chroot.sh ^^^^^^^^^^^^^^^^^^^^"
