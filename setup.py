#!/usr/bin/env python

from setuptools import setup, find_packages

setup(
    name='jenkins_tools',
    version='0.0.50',
    packages=['jenkins_tools'],
    package_dir = {'jenkins_tools':'src/jenkins_tools'},
    scripts = ['scripts/run_chroot_jenkins_now',
               'scripts/run_chroot_jenkins_periodic',
               'scripts/run_chroot_jenkins_vcs',
               'scripts/run_chroot_local',
               'scripts/delete_jenkins',
               'scripts/generate_jenkins_devel',
               'scripts/generate_jenkins_doc',
               'scripts/generate_jenkins_prerelease',
               'scripts/chroot_create.sh',
               'scripts/chroot_update.sh',
               'scripts/chroot_dispatch.sh'],
    install_requires=['empy', 'PyYAML', 'jenkins', 'argparse', 'rosdep', 'rospkg', 'catkin-pkg', 'distribute'],
    package_data = {'jenkins_tools': ['resources/templates/*']},
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
