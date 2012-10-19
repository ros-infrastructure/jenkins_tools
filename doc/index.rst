Jenkins_Tools -- 0.2.0
==============

.. Links

.. _catkin: https://github.com/ros-infrastructure/jenkins_tools

How do I install jenkins_tools?
-----------------------

On Ubuntu the recommend method is to use apt::

    $ sudo apt-get install python-jenkins-tools

On other systems you can install jenkins_tools via pypi::

    $ sudo pip install -U jenkins-tools

Note: pip will not notify you of updates, so check often if you use pip

How do I release something with jenkins_tools?
---------------------------------------

It depends on your use case:

.. toctree::
    :maxdepth: 1

    tutorials/jenkins_tools_setup
    tutorials/catkin_release
    tutorials/non_catkin
    tutorials/notify_build_farm

.. toctree::
    :hidden:

    glossary
