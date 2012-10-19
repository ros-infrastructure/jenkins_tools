#!/usr/bin/env python

from setuptools import setup, find_packages

setup(
    name='jenkins_tools',
    version='0.2.0',
    packages=find_packages(exclude=['test']),
    package_data={
        'jenkins_tools.generators.debian':
            ['jenkins_tools/generators/debian/templates/*.em']
    },
    install_requires=[
        'empy >= 3.1',
        'PyYAML >= 3.10',
        'jenkins >= 0.2',
        'argparse >= 1.2.1',
        'rosdep >= 0.10.3',
        'catkin-pkg >= 0.1.2',
        'distribute >= 0.6.24'
    ],
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
    license='BSD',
    test_suite='test',
    entry_points={
        'console_scripts': [
            'git-jenkins_tools-run_jenkins_now = jenkins_tools.commands.config:main',
            'git-jenkins_tools-run_jenkins_periodic-upstream = jenkins_tools.commands.import_upstream:main',
            'git-jenkins_tools-run_jenkins_vcs = jenkins_tools.commands.branch:main',
            'git-jenkins_tools-run_local = jenkins_tools.commands.patch.patch_main:main'
        ]
    }
)
