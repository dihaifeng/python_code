#!/usr/bin/env python3

import jenkins,time
from django.conf import settings
import logging
import re
import xml.etree.cElementTree as ET
from common.models import ConfigDict


log = logging.getLogger('django')


def render_command(command, nexus_path):
    """
    为shell命令渲染变量值
    :param command: shell命令
    :param nexus_path: 所属的nexus files仓库组
    :return: 渲染后的command
    """
    configs = ConfigDict()
    url = configs['nexus.raw_url'] + nexus_path + '/$Tag_Version.tgz'
    command = command.replace('$release_url', url)
    return command


class Jenkins_API():

    def __init__(self,url,user,token):
        self.server = jenkins.Jenkins(url, username=user, password=token)
        self.prefix = "KUN__"
        self.build_xml_template = '''
  <project>
  <actions/>
  <description></description>
  <keepDependencies>false</keepDependencies>
  <properties>
    <jenkins.model.BuildDiscarderProperty>
      <strategy class="hudson.tasks.LogRotator">
        <daysToKeep>-1</daysToKeep>
        <numToKeep>5</numToKeep>
        <artifactDaysToKeep>-1</artifactDaysToKeep>
        <artifactNumToKeep>-1</artifactNumToKeep>
      </strategy>
    </jenkins.model.BuildDiscarderProperty>
    <hudson.model.ParametersDefinitionProperty>
      <parameterDefinitions>
        <net.uaznia.lukanus.hudson.plugins.gitparameter.GitParameterDefinition plugin="git-parameter@0.9.0">
          <name>Tag_Version</name>
          <description></description>
          <uuid>5d264244-f330-422d-8760-f36dce753e34</uuid>
          <type>PT_BRANCH_TAG</type>
          <branch></branch>
          <tagFilter>*</tagFilter>
          <branchFilter>.*</branchFilter>
          <sortMode>NONE</sortMode>
          <defaultValue></defaultValue>
          <selectedValue>NONE</selectedValue>
          <quickFilterEnabled>false</quickFilterEnabled>
        </net.uaznia.lukanus.hudson.plugins.gitparameter.GitParameterDefinition>
      </parameterDefinitions>
    </hudson.model.ParametersDefinitionProperty>
  </properties>
  <scm class="hudson.plugins.git.GitSCM" plugin="git@3.6.4">
    <configVersion>2</configVersion>
    <userRemoteConfigs>
      <hudson.plugins.git.UserRemoteConfig>
        <url></url>
        <credentialsId>weiboad_common-privatekey</credentialsId>
      </hudson.plugins.git.UserRemoteConfig>
    </userRemoteConfigs>
    <branches>
      <hudson.plugins.git.BranchSpec>
        <name>$Tag_Version</name>
      </hudson.plugins.git.BranchSpec>
    </branches>
    <doGenerateSubmoduleConfigurations>false</doGenerateSubmoduleConfigurations>
    <submoduleCfg class="list"/>
    <extensions>
      <hudson.plugins.git.extensions.impl.CloneOption>
        <shallow>true</shallow>
        <noTags>false</noTags>
        <reference></reference>
        <depth>1</depth>
        <honorRefspec>false</honorRefspec>
      </hudson.plugins.git.extensions.impl.CloneOption>
    </extensions>
  </scm>
  <assignedNode></assignedNode>
  <canRoam>false</canRoam>
  <disabled>false</disabled>
  <blockBuildWhenDownstreamBuilding>false</blockBuildWhenDownstreamBuilding>
  <blockBuildWhenUpstreamBuilding>false</blockBuildWhenUpstreamBuilding>
  <triggers/>
  <concurrentBuild>false</concurrentBuild>
  <builders>
    <hudson.tasks.Shell>
      <command>
      </command>
    </hudson.tasks.Shell>
  </builders>
  <publishers/>
  <buildWrappers>
    <hudson.plugins.ws__cleanup.PreBuildCleanup plugin="ws-cleanup@0.34">
      <deleteDirs>false</deleteDirs>
      <cleanupParameter></cleanupParameter>
      <externalDelete></externalDelete>
    </hudson.plugins.ws__cleanup.PreBuildCleanup>
  </buildWrappers>
  </project>
  '''

    def exist_job(self,job_name):
        return self.server.get_job_name(job_name) is not None


    def create_job(self,pro_obj):
        job_name = self.generate_jenkins_name(pro_obj)
        detail = pro_obj.detail
        git_path = pro_obj.git_path
        label = pro_obj.label
        build_command = pro_obj.build_command

        log.info('Create or reconfig Jenkins Project [%s].', job_name)
        if self.exist_job(job_name):
            build_xml = self.modify_config(job_name, detail,git_path, label, render_command(build_command, pro_obj.nexus_path))
            self.server.reconfig_job(job_name,build_xml)
        else:
            build_xml = self.modify_config(job_name, detail,git_path, label, render_command(build_command, pro_obj.nexus_path), exist=False)
            self.server.create_job(job_name,build_xml)

    def modify_config(self, job_name, detail, git_path, label, build_command, exist=True):
        """
        如果jenkins已有项目，下载项目的xml配置，只修改git、detail、Build、构建节点label相关信息并生成xml返回
        :param job_name: jenkin项目名称
        :param detail: 描述
        :param git_path: git地址ssh
        :param label: jenkins构建节点的label
        :param build_command: 构建脚本
        :param exist: 是否jenkins项目已存在，默认已存在
        :return:
        """
        if exist:
            config_xml = self.server.get_job_config(job_name)
        else:
            config_xml = self.build_xml`_template
        log.info("Reconfig jenkins job [%s] with [desc: %s git: %s buildcommand: %s]", job_name, detail,git_path, build_command)
        config_root = ET.fromstring(config_xml)
        config_root.find('description').text = detail
        config_root.find('builders').find('hudson.tasks.Shell').find('command').text = build_command
        config_root.find('scm').find('userRemoteConfigs').find('hudson.plugins.git.UserRemoteConfig').find('url').text = git_path
        config_root.find('assignedNode').text = label
        return ET.tostring(config_root, encoding="utf-8").decode("utf-8")

    def delete_job(self,obj):
        job_name = obj.jenkins_name
        if self.exist_job(job_name):
            self.server.delete_job(job_name)

    def generate_jenkins_name(self, obj):
        """
        生成jenkins项目的名称。以"KUN__"开头并连接项目的名称
        :param obj:
        :return:
        """
        if not obj.jenkins_name:
            obj.jenkins_name = self.prefix + obj.name
            obj.save()
        return obj.jenkins_name

    def create_build(self, obj, tag):
        """
        执行jenkins项目构建
        :param obj:
        :param tag:
        :return:
        """
        job_name = self.generate_jenkins_name(obj)
        print(job_name, tag)
        build_param = {'Tag_Version':tag}
        if not self.exist_job(job_name):
            self.create_job(obj)
        job_info = self.server.get_job_info(job_name)
        current_id = job_info['nextBuildNumber']
        self.server.build_job(job_name,build_param)
        parent_url = job_info['url'] + str(current_id) + '/'
        localtime = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
        build_result = {
            "build_id": current_id,
            "tag": tag,
            "status": 3,
            "build_time": localtime,
            "jenkins_build_url": parent_url,
            # "pro_id": obj.id
            }
        return build_result

    def get_tags(self):
        """
        遍历每个jenkins的节点配置，解析出所有的标签list
        :return:
        """
        reg = re.compile('<label>(.*)</label>')
        tags = set()
        for node in self.server.get_nodes():
            print(node)
            try:
                config = self.server.get_node_config(node['name'])
                labels = reg.findall(config)
                if labels and labels[0]:
                    tags = tags | set(labels[0].split(' '))
            except jenkins.NotFoundException:
                pass
        return list(tags)



# Jenkins_U = ''
# Jenkins_T = ''
# Jenkins_URL = 'http://jenkinx.xxx.xxx.com/'
# ja = Jenkins_API(Jenkins_URL, Jenkins_U, Jenkins_T)
# print(ja.get_tags())
# j = jenkins.Jenkins(Jenkins_URL, username=xxxxxx, password=xxxxxxxxx)
# print(j.get_whoami())

# # print(j.get_all_jobs())
# print(j.build_job('Farmer-ng', parameters={"param1": "1.0.2"}))
# # queue_info = j.get_queue_info()
# # print(queue_info)
# # i = queue_info[0].get('id')
# # print(i)
# print("============================")

# print(j.get_build_info('Farmer-ng', 31))
# j.get_build_console_output('Farmer-ng', 35)
