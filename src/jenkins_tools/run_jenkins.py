#!/usr/bin/env python

import datetime
import jenkins
import os
import pkg_resources
import yaml

JENKINS_SERVER = 'http://jenkins.ros.org/'


def build_job(jenkins_instance, job_name, parameters=None):
    #return jenkins_instance.build_job(job_name)
    # replicate internal implementation of Jenkins.build_job()
    import urllib2
    if not jenkins_instance.job_exists(job_name):
        raise jenkins.JenkinsException('no such job[%s]' % (job_name))
    # pass parameters to create a POST request instead of GET
    return jenkins_instance.jenkins_open(urllib2.Request(jenkins_instance.build_job_url(job_name, parameters), 'foo=bar'))


def _get_jenkins_conf():
    jenkins_conf = pkg_resources.resource_string('jenkins_tools', 'resources/templates/jenkins_conf.yaml')
    return yaml.load(jenkins_conf)


def _update_jenkins_job(jenkins_instance, jenkins_conf, ubuntu_distro, arch, job_name, email, script, script_args, user_name, custom_params=None, parameters=None, matrix=None, priority=None, timeout=None):
    job_xml = pkg_resources.resource_string('jenkins_tools', 'resources/templates/jenkins_template.xml')

    params = {}
    params['PROJECT'] = 'project'
    params['MATRIX'] = ''

    params['ARCH'] = arch
    params['EMAIL'] = email
    params['UBUNTU_DISTRO'] = ubuntu_distro

    params['TIME'] = str(datetime.datetime.now())
    params['USERNAME'] = user_name
    params['HOSTNAME'] = os.uname()[1]
    params['PARAMETERS'] = ''

    params['SCRIPT'] = script
    params['SCRIPT_ARGS'] = ' '.join(script_args)
    params['NODE'] = params['SCRIPT']

    params['TRIGGER'] = jenkins_conf['triggers']['none']
    params['VCS'] = jenkins_conf['vcs']['none']

    params['PRIORITY'] = str(priority) if priority else '100'  # 100 minutes is the default priority

    params['TIMEOUT'] = jenkins_conf['timeout']['absolute'].replace('@(MINUTES)', str(timeout)) if timeout else ''

    if parameters:
        params['PARAMETERS'] = jenkins_conf['parameters']['block'].replace('@(PARAMS)', ' '.join([jenkins_conf['parameters']['param'].replace('@(PARAM)', p) for p in parameters[0].keys()]))

    if matrix:
        axis = ''
        for axis_name, axis_values in matrix.iteritems():
            axis += jenkins_conf['matrix']['axis'].replace('@(NAME)', axis_name).replace('@(VALUES)', ' '.join([jenkins_conf['matrix']['value'].replace('@(VALUE)', v) for v in axis_values]))
        params['MATRIX'] = jenkins_conf['matrix']['block'].replace('@(AXIS)', axis)
        params['MATRIX'] = params['MATRIX'].replace('@(NODE)', params['NODE'])
        params['PROJECT'] = 'matrix-project'

    for k, v in custom_params.iteritems():
        params[k] = v

    # replace @(xxx) in template file
    for key, value in params.iteritems():
        job_xml = job_xml.replace("@(%s)" % key, value)

    # (re-)configure job
    if jenkins_instance.job_exists(job_name):
        jenkins_instance.reconfig_job(job_name, job_xml)
        print "Reconfigured job %s" % job_name
    else:
        jenkins_instance.create_job(job_name, job_xml)
        print "Created job %s" % job_name


# configure a job and trigger a build
def run_jenkins_now(jenkins_instance, ubuntu_distro, arch, job_name, email, script, script_args, user_name, parameters=None, matrix=None, additional_publishers=''):
    jc = _get_jenkins_conf()
    params = {}
    params['EMAIL_COMMITTER'] = 'false'
    params['ADDITIONAL_PUBLISHERS'] = additional_publishers
    _update_jenkins_job(jenkins_instance, jc, ubuntu_distro, arch, job_name, email, script, script_args, user_name, custom_params=params, parameters=parameters, matrix=matrix)
    # build all jobs
    if not parameters or len(parameters) == 0:
        build_job(jenkins_instance, job_name)
    else:
        for p in parameters:
            build_job(jenkins_instance, job_name, p)
    print "Started job %s" % job_name


# configure a job with periodic trigger
def run_jenkins_periodic(jenkins_instance, ubuntu_distro, arch, job_name, email, period, script, script_args, user_name, matrix=None, priority=None, timeout=None, additional_publishers=''):
    jc = _get_jenkins_conf()
    params = {}
    params['EMAIL_COMMITTER'] = 'false'
    params['TRIGGER'] = jc['triggers']['periodic'][period]
    params['ADDITIONAL_PUBLISHERS'] = additional_publishers
    _update_jenkins_job(jenkins_instance, jc, ubuntu_distro, arch, job_name, email, script, script_args, user_name, params, matrix=matrix, priority=priority, timeout=timeout)


# configure a job with vcs trigger
def run_jenkins_vcs(jenkins_instance, ubuntu_distro, arch, job_name, email, vcs, uri, branch, script, script_args, user_name, matrix=None, priority=None, timeout=None):
    jc = _get_jenkins_conf()
    params = {}
    params['EMAIL_COMMITTER'] = 'true'
    params['TRIGGER'] = jc['triggers']['vcs']
    params['VCS'] = jc['vcs'][vcs].replace('@(URI)', uri).replace('@(BRANCH)', branch)
    _update_jenkins_job(jenkins_instance, jc, ubuntu_distro, arch, job_name, email, script, script_args, user_name, params, matrix=matrix, priority=priority, timeout=timeout)
