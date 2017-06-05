#!/usr/bin/env python

import docker

c = docker.Client(base_url='unix://var/run/docker.sock',version='1.22',timeout=10)
ex = c.exec_create(container='37d91ab772d3',cmd='mkdir /data0')
print c.exec_inspect(ex)
ls=c.exec_start(exec_id=ex["Id"],tty=True)
