#!/bin/sh -ex

/bin/echo "vvvvvvvvvvvvvvvvvvv  update_chroot.sh vvvvvvvvvvvvvvvvvvvvvv"

apt-get update
apt-get install -y \
    python-setuptools ccache wget curl curl-ssl sudo git-buildpackage dput python-yaml python-pip python-support \
    git-core mercurial subversion python-all gccxml python-empy python-nose python-mock python-minimock lsb-release \
    python-numpy python-wxgtk2.8 python-argparse python-networkx graphviz python-sphinx doxygen python-epydoc cmake pkg-config openssh-client


mkdir -p $HOME
/bin/echo "^^^^^^^^^^^^^^^^^^  update_chroot.sh ^^^^^^^^^^^^^^^^^^^^"
