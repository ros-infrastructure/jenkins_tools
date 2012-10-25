set -ex
/bin/echo "vvvvvvvvvvvvvvvvvvv  dispatch.sh vvvvvvvvvvvvvvvvvvvvvv"

# pass all arguments to the dispatcher on to the script we're running
SCRIPT_ARGS=""
for i in $*
  do 
  SCRIPT_ARGS=`echo $SCRIPT_ARGS $i`
done
echo "Arguments for script: " $SCRIPT_ARGS

#always ask for pbuilder to make sure we have the updated patched version
#sudo apt-get update  --> this is done in the Jenkins script, right before dispatch is called
sudo apt-get -y install pbuilder

#  get latest version of jenkins scripts
cd $WORKSPACE
if [ -e $WORKSPACE/run_debug_mode ] ; then
  /bin/echo "DEBUG  DEBUG DEBUG  DEBUG DEBUG  DEBUG DEBUG  DEBUG DEBUG  DEBUG DEBUG  DEBUG DEBUG  DEBUG "
  /bin/echo "DEBUG  DEBUG DEBUG  DEBUG DEBUG  DEBUG DEBUG  DEBUG DEBUG  DEBUG DEBUG  DEBUG DEBUG  DEBUG "
  /bin/echo "DEBUG  DEBUG DEBUG  DEBUG DEBUG  DEBUG DEBUG  DEBUG DEBUG  DEBUG DEBUG  DEBUG DEBUG  DEBUG "
  /bin/echo "DEBUG  DEBUG DEBUG  DEBUG DEBUG  DEBUG DEBUG  DEBUG DEBUG  DEBUG DEBUG  DEBUG DEBUG  DEBUG "
  /bin/echo "DEBUG  DEBUG DEBUG  DEBUG DEBUG  DEBUG DEBUG  DEBUG DEBUG  DEBUG DEBUG  DEBUG DEBUG  DEBUG "
  /bin/echo "DEBUG  DEBUG DEBUG  DEBUG DEBUG  DEBUG DEBUG  DEBUG DEBUG  DEBUG DEBUG  DEBUG DEBUG  DEBUG "
else
  if [ -d jenkins_scripts ] ; then
    cd jenkins_scripts
    git clean -dfx
    git reset --hard HEAD
    git pull
    cd ..
  else
    git clone http://github.com/ros-infrastructure/jenkins_scripts.git
  fi
  cd jenkins_scripts && git log -n 1
fi

cd $WORKSPACE
export > env
sudo mkdir -p /var/cache/pbuilder/ccache
sudo chmod a+w /var/cache/pbuilder/ccache

cat > pbuilder-env.sh <<EOF
#!/bin/bash -ex
/bin/echo "vvvvvvvvvvvvvvvvvvv  pbuilder-env.sh vvvvvvvvvvvvvvvvvvvvvv"
export CCACHE_DIR="/var/cache/pbuilder/ccache"
export PATH="/usr/lib/ccache:${PATH}"
export IMAGETYPE=$IMAGETYPE

export OS_NAME=$OS_NAME
export OS_PLATFORM=$OS_PLATFORM
export UBUNTU_DISTRO=$UBUNTU_DISTRO
export ARCH=$ARCH

export WORKSPACE=$WORKSPACE

if [ -d \$HOME/.ssh ]; then
  cp -a \$HOME/.ssh /root
  chown -R root.root /root/.ssh
fi
if [ -d \$HOME/.subversion ]; then
  cp -a \$HOME/.subversion /root
  chown -R root.root /root/.subversion
fi
cd $WORKSPACE
chmod 755 $WORKSPACE/jenkins_scripts/${SCRIPT}

echo "============================================================"
echo "==== Begin" $SCRIPT "script.    Ignore the output above ====="
echo "============================================================"

$WORKSPACE/jenkins_scripts/${SCRIPT} ${SCRIPT_ARGS}

echo "============================================================"
echo "==== End" $SCRIPT "script.    Ignore the output below ====="
echo "============================================================"

EOF

chmod 755 pbuilder-env.sh

TOP=$(cd `dirname $0` ; /bin/pwd)

#/usr/bin/env

tmpdir=`mktemp -d`
basetgz_filename=$tmpdir/basetgz
chroot_create.sh $IMAGETYPE $UBUNTU_DISTRO $ARCH $basetgz_filename
basetgz=`cat $basetgz_filename`
rm -rf $tmpdir







sudo pbuilder execute \
    --basetgz $basetgz \
    --bindmounts "/var/cache/pbuilder/ccache $WORKSPACE $HOME/.ssh" \
    --inputfile $WORKSPACE/jenkins_scripts/$SCRIPT \
    -- $WORKSPACE/pbuilder-env.sh $SCRIPT


/bin/echo "^^^^^^^^^^^^^^^^^^  dispatch.sh ^^^^^^^^^^^^^^^^^^^^"
