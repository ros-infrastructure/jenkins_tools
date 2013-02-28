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


def build_job(jenkins_instance, job_name, parameters=None):
    #return jenkins_instance.build_job(job_name)
    # replicate internal implementation of Jenkins.build_job()
    import urllib2
    if not jenkins_instance.job_exists(job_name):
        raise jenkins.JenkinsException('no such job[%s]' % (job_name))
    # pass parameters to create a POST request instead of GET
    return jenkins_instance.jenkins_open(urllib2.Request(jenkins_instance.build_job_url(job_name, parameters), 'foo=bar'))


# Schedule a set of jobs in Jenkins
def run_jenkins_now(jenkins_instance, ubuntu_distro, arch, job_name, email, script, script_args, user_name, parameters=None, matrix=None):

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
    params['MATRIX'] = ''
    params['PROJECT'] = 'project'
    if parameters and len(parameters) > 0:
        params['PARAMETERS'] = jc['parameters']['block'].replace('@(PARAMS)', ' '.join([jc['parameters']['param'].replace('@(PARAM)', p) for p in parameters[0].keys()]))
    if matrix:
        axis = ''
        for axis_name, axis_values in matrix.iteritems():
            axis += jc['matrix']['axis'].replace('@(NAME)', axis_name).replace('@(VALUES)', ' '.join([ jc['matrix']['value'].replace('@(VALUE)', v) for v in axis_values]))
        params['MATRIX'] = jc['matrix']['block'].replace('@(AXIS)', axis)
        params['MATRIX'] = params['MATRIX'].replace('@(NODE)', params['NODE'])
        params['PROJECT'] = 'matrix-project'

    # replace @(xxx) in template file
    for key, value in params.iteritems():
        job_xml = job_xml.replace("@(%s)"%key, value)


    # schedule a new job
    if jenkins_instance.job_exists(job_name):
        jenkins_instance.reconfig_job(job_name, job_xml)
        print "Reconfigured job %s"%job_name
    else:
        jenkins_instance.create_job(job_name, job_xml)
        print "Created job %s"%job_name

    # build all jobs
    if not parameters or len(parameters) == 0:
        build_job(jenkins_instance, job_name)
    else:
        for p in parameters:
            build_job(jenkins_instance, job_name, p)
    print "Started job %s"%job_name





# Schedule a set of jobs in Jenkins
def run_jenkins_periodic(jenkins_instance, ubuntu_distro, arch, job_name, email,
                         period, script, script_args, user_name, matrix=None):

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
    params['MATRIX'] = ''
    params['PROJECT'] = 'project'
    params['MATRIX'] = ''
    if matrix:
        axis = ''
        for axis_name, axis_values in matrix.iteritems():
            axis += jc['matrix']['axis'].replace('@(NAME)', axis_name).replace('@(VALUES)', ' '.join([ jc['matrix']['value'].replace('@(VALUE)', v) for v in axis_values]))
        params['MATRIX'] = jc['matrix']['block'].replace('@(AXIS)', axis)
        params['MATRIX'] = params['MATRIX'].replace('@(NODE)', params['NODE'])
        params['PROJECT'] = 'matrix-project'

    # replace @(xxx) in template file
    for key, value in params.iteritems():
        job_xml = job_xml.replace("@(%s)"%key, value)

    # schedule a new job
    if jenkins_instance.job_exists(job_name):
        jenkins_instance.reconfig_job(job_name, job_xml)
        print "Reconfigured job %s"%job_name
    else:
        jenkins_instance.create_job(job_name, job_xml)
        print "Created job %s"%job_name




# Schedule a set of jobs in Jenkins
def run_jenkins_vcs(jenkins_instance,
                    ubuntu_distro, arch, job_name, email, vcs, uri, branch,
                    script, script_args, user_name, matrix=None):

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
    params['MATRIX'] = ''
    params['PROJECT'] = 'project'
    params['MATRIX'] = ''
    if matrix:
        axis = ''
        for axis_name, axis_values in matrix.iteritems():
            axis += jc['matrix']['axis'].replace('@(NAME)', axis_name).replace('@(VALUES)', ' '.join([ jc['matrix']['value'].replace('@(VALUE)', v) for v in axis_values]))
        params['MATRIX'] = jc['matrix']['block'].replace('@(AXIS)', axis)
        params['MATRIX'] = params['MATRIX'].replace('@(NODE)', params['NODE'])
        params['PROJECT'] = 'matrix-project'

    # replace @(xxx) in template file
    for key, value in params.iteritems():
        job_xml = job_xml.replace("@(%s)"%key, value)

    # schedule a new job
    if jenkins_instance.job_exists(job_name):
        jenkins_instance.reconfig_job(job_name, job_xml)
        print "Reconfigured job %s"%job_name
    else:
        jenkins_instance.create_job(job_name, job_xml)
        print "Created job %s"%job_name



