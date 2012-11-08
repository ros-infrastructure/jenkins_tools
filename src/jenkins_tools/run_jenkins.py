#!/usr/bin/env python

import sys
import jenkins
import urllib
import yaml
import datetime
import os
import pkg_resources
from rospkg import environment



JENKINS_SERVER = 'http://jenkins.willowgarage.com:8080/'


# Schedule a set of jobs in Jenkins
def run_jenkins_now(jenkins_instance, ubuntu_distro, arch, name, email, script, script_args, user_name, parameters=None):

    job_xml = pkg_resources.resource_string('jenkins_tools', 'resources/templates/jenkins_template.xml')
    jenkins_conf = pkg_resources.resource_string('jenkins_tools', 'resources/templates/jenkins_conf.yaml')
    jc = yaml.load(jenkins_conf)

    # get arguments
    params = {}
    params['UBUNTU_DISTRO'] = ubuntu_distro
    params['ARCH'] = arch
    params['EMAIL'] = email
    params['EMAIL_COMMITTER'] = 'false'
    params['SCRIPT'] = script
    params['NODE'] = params['SCRIPT']
    params['SCRIPT_ARGS'] = ' '.join(script_args)
    params['TRIGGER'] = jc['triggers']['none']
    params['VCS'] = jc['vcs']['none']
    params['TIME'] = str(datetime.datetime.now())
    params['USERNAME'] = user_name
    params['HOSTNAME'] = os.uname()[1]
    params['PARAMETERS'] = ''
    if parameters and len(parameters) > 0:
        params['PARAMETERS'] = jc['params'].replace('@(PARAMS)', ' '.join([jc['add_param'].replace('@(PARAM)', p) for p in parameters[0].keys()]))

    # replace @(xxx) in template file
    for key, value in params.iteritems():
        job_xml = job_xml.replace("@(%s)"%key, value)

    # schedule a new job
    job_name = "%s-%s"%(params['SCRIPT'], name)
    if jenkins_instance.job_exists(job_name):
        jenkins_instance.reconfig_job(job_name, job_xml)
        print "Reconfigured job %s"%job_name
    else:
        jenkins_instance.create_job(job_name, job_xml)
        print "Created job %s"%job_name

    # build all jobs
    if not param_values:
        jenkins_instance.build_job(job_name)
        print "Started job %s"%job_name
    else:
        for p in param_values:
            jenkins_instance.build_job(job_name, p)
            print "Started job %s with parameters %s"%(job_name, str(p))

    print "When the job finishes, you will receive an email at %s"%params['EMAIL']
    return job_name





# Schedule a set of jobs in Jenkins
def run_jenkins_periodic(jenkins_instance, ubuntu_distro, arch, name, email,
                         period, script, script_args, user_name):

    job_xml = pkg_resources.resource_string('jenkins_tools', 'resources/templates/jenkins_template.xml')
    jenkins_conf = pkg_resources.resource_string('jenkins_tools', 'resources/templates/jenkins_conf.yaml')
    jc = yaml.load(jenkins_conf)

    # get arguments
    params = {}
    params['UBUNTU_DISTRO'] = ubuntu_distro
    params['ARCH'] = arch
    params['EMAIL'] = email
    params['EMAIL_COMMITTER'] = 'false'
    params['TRIGGER'] = jc['triggers']['periodic'][period]
    params['SCRIPT'] = script
    params['NODE'] = params['SCRIPT']
    params['SCRIPT_ARGS'] = ' '.join(script_args)
    params['VCS'] = jc['vcs']['none']
    params['TIME'] = str(datetime.datetime.now())
    params['USERNAME'] = user_name
    params['HOSTNAME'] = os.uname()[1]
    params['PARAMETERS'] = ''

    # replace @(xxx) in template file
    for key, value in params.iteritems():
        job_xml = job_xml.replace("@(%s)"%key, value)

    # schedule a new job
    job_name = "%s-%s-%s-%s"%(params['SCRIPT'], name, params['UBUNTU_DISTRO'], params['ARCH'])
    if jenkins_instance.job_exists(job_name):
        jenkins_instance.reconfig_job(job_name, job_xml)
        print "Reconfigured job %s"%job_name
    else:
        jenkins_instance.create_job(job_name, job_xml)
        print "Created job %s"%job_name
    return job_name




# Schedule a set of jobs in Jenkins
def run_jenkins_vcs(jenkins_instance,
                    ubuntu_distro, arch, name, email, vcs, uri, branch,
                    script, script_args, user_name):

    job_xml = pkg_resources.resource_string('jenkins_tools', 'resources/templates/jenkins_template.xml')
    jenkins_conf = pkg_resources.resource_string('jenkins_tools', 'resources/templates/jenkins_conf.yaml')
    jc = yaml.load(jenkins_conf)

    # get arguments
    params = {}
    params['UBUNTU_DISTRO'] = ubuntu_distro
    params['ARCH'] = arch
    params['EMAIL'] = email
    params['EMAIL_COMMITTER'] = 'true'
    params['TRIGGER'] = jc['triggers']['vcs']
    params['VCS'] = jc['vcs'][vcs].replace('@(URI)', uri).replace('@(BRANCH)', branch)
    params['SCRIPT'] = script
    params['NODE'] = params['SCRIPT']
    params['TIME'] = str(datetime.datetime.now())
    params['SCRIPT_ARGS'] = ' '.join(script_args)
    params['USERNAME'] = user_name
    params['HOSTNAME'] = os.uname()[1]
    params['PARAMETERS'] = ''

    # replace @(xxx) in template file
    for key, value in params.iteritems():
        job_xml = job_xml.replace("@(%s)"%key, value)

    # schedule a new job
    job_name = "%s-%s-%s-%s"%(params['SCRIPT'], name, params['UBUNTU_DISTRO'], params['ARCH'])
    if jenkins_instance.job_exists(job_name):
        jenkins_instance.reconfig_job(job_name, job_xml)
        print "Reconfigured job %s"%job_name
    else:
        jenkins_instance.create_job(job_name, job_xml)
        print "Created job %s"%job_name
    return job_name



