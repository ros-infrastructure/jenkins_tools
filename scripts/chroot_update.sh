#!/bin/sh -ex
#stamp: 1351191507

/bin/echo "vvvvvvvvvvvvvvvvvvv  update_chroot.sh vvvvvvvvvvvvvvvvvvvvvv"

apt-get install -y \
    python-setuptools ccache wget curl curl-ssl sudo git-buildpackage dput python-yaml python-pip python-support \
    git-core mercurial subversion python-all gccxml python-empy python-nose python-mock python-minimock \
    python-numpy python-wxgtk2.8 python-argparse

mkdir -p $HOME
/bin/echo "^^^^^^^^^^^^^^^^^^  update_chroot.sh ^^^^^^^^^^^^^^^^^^^^"
