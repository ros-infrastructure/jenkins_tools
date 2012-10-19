#!/usr/bin/env python

from setuptools import setup, find_packages

setup(
    name='jenkins_tools',
    version='0.0.2',
    packages=['jenkins_tools'],
    package_dir = {'jenkins_tools':'src/jenkins_tools'},
    scripts = ['scripts/run_chroot_jenkins_now',
               'scripts/run_chroot_jenkins_periodic',
               'scripts/run_chroot_jenkins_vcs',
               'scripts/run_chroot_local',
               'scripts/chroot_create.sh',
               'scripts/chroot_update.sh',
               'scripts/chroot_dispatch.sh'],
    install_requires=[
        'empy >= 3.1',
        'PyYAML >= 3.10',
        'jenkins >= 0.2',
        'argparse >= 1.2.1',
        'rosdep >= 0.10.3',
        'rospkg >= 1.0.6',
        'catkin-pkg >= 0.1.2',
        'distribute >= 0.6.24'],
    author='Wim Meeussen',
    author_email='wim@hidof.com',
    maintainer='Wim Meeussen',
    maintainer_email='wim@hidof.com',
    url='http://www.ros.org/wiki/jenkins_tools',
    download_url='http://pr.willowgarage.com/downloads/jenkins_tools/',
    keywords=['ROS'],
    classifiers=['Programming Language :: Python',
                 'License :: OSI Approved :: BSD License'],
    description="A tool for running scripts in a chroot environment on Jenkins or locally",
    long_description="""
A tool for running scripts in a chroot environment on Jenkins or locally""",
    license='BSD'
)
