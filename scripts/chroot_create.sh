#!/bin/bash -ex

/bin/echo "vvvvvvvvvvvvvvvvvvv  create_chroot.sh vvvvvvvvvvvvvvvvvvvvvv"
IMAGETYPE=$1
IMAGVERSION=$2
DISTRO=$3
ARCH=$4
BASE=/var/cache/pbuilder/$IMAGETYPE.$DISTRO.$ARCH-$IMAGEVERSION
IMAGEFILE_FILENAME=$5

IMAGEFILE=$BASE.tgz
IMAGELOCK=$BASE.updatelock
IMAGESTAMPFILE=$BASE.version
ROOTDIR=$BASE/apt-conf-$IMAGVERSION
echo $IMAGEFILE > $IMAGEFILE_FILENAME

if [ ! -f $IMAGEFILE ] ; then
    sudo flock $IMAGELOCK -c "pbuilder --create --distribution $DISTRO --architecture $ARCH --basetgz $IMAGEFILE --debootstrapopts --variant=buildd --components \"main universe multiverse\" --othermirror \"deb http://us.archive.ubuntu.com/ubuntu/ $DISTRO-updates main restricted\" --debootstrapopts --keyring=/etc/apt/trusted.gpg"
fi

UPDATE=/usr/bin/chroot_update.sh

# get version stamp of image
if [ ! -f $IMAGESTAMPFILE ] ; then
    IMAGESTAMP=0
else
    IMAGESTAMP=$(cat $IMAGESTAMPFILE)
fi
/bin/echo "Image stamp is $IMAGESTAMP"

# get version stamp of chroot_update script
REPOSTAMP=$(apt-show-versions python-jenkins-tools  | awk '{for (i = 0; i < 10; i++)  if ( !match($i, " ") && match($i, "[0-9].[0-9]") ) print $i}')
/bin/echo "Repo stamp is $REPOSTAMP"


if [ $IMAGESTAMP != $REPOSTAMP ] ; then

    /bin/echo "chroot_update has been updated, so let's update the chroot tar"
    /bin/echo $REPOSTAMP > stamp.tmp
    sudo rm -f $IMAGESTAMPFILE
    sudo mv stamp.tmp $IMAGESTAMPFILE
    sudo flock $IMAGELOCK -c "pbuilder execute --basetgz $IMAGEFILE --save-after-exec -- $UPDATE $IMAGETYPE"
fi


/bin/echo "^^^^^^^^^^^^^^^^^^  create_chroot.sh ^^^^^^^^^^^^^^^^^^^^"
