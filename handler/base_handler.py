# -*- coding: utf-8 -*-
# @Time    : 2018/8/12 下午8:36
# @Author  : Zhixin Piao 
# @Email   : piaozhx@shanghaitech.edu.cn

import tornado.web
import os
from utils import utils

STANDARD_NODE_LIST = list(range(0, 35 + 1))


class BaseHandler(tornado.web.RequestHandler):
    def get_current_user(self):
        return self.get_secure_cookie("user")

    @property
    def db(self):
        return self.application.db

    def get_node_list_by_str_nodes(self, nodes):
        try:
            node_list = eval('[%s]' % nodes)
        except:
            return None

        if not isinstance(node_list, list) or len(node_list) == 0:
            return None

        for node_id in node_list:
            if node_id not in STANDARD_NODE_LIST:
                return None
        return node_list

    @classmethod
    def get_website_ip(self):
        return '10.15.89.41'

    @classmethod
    def create_container_on_remote(self, node_name, docker_type, cname, container_port, advisor):
        container_name = '%s-%s' % (cname, node_name)
        addition_str = utils.ContainerAdditionStr(node_name, advisor, cname).get_additional_str()

        memory_size = os.popen('''ssh %s  free -h | head -n 2 | tail -n 1 | awk -F' ' '{print $2}' ''' % node_name).read().strip()
        memory_unit = memory_size[-1]
        memory_size = int(memory_size[:-1])
        shm_size = memory_size // 2
        shm_size = str(shm_size) + memory_unit

        os.system("ssh %s "
                  "%s run "
                  "--name %s "
                  "--network=host "
                  "-v /p300/docker/%s:/p300 "
                  "-v /p300/datasets:/datasets:ro "
                  "-v /public/docker/%s/bin:/bin "
                  "-v /public/docker/%s/etc:/etc "
                  "-v /public/docker/%s/lib:/lib "
                  "-v /public/docker/%s/lib64:/lib64 "
                  "-v /public/docker/%s/opt:/opt "
                  "-v /public/docker/%s/root:/root "
                  "-v /public/docker/%s/sbin:/sbin "
                  "-v /public/docker/%s/usr:/usr "
                  # "--privileged=true "
                  # "--volume /run/dbus/system_bus_socket:/run/dbus/system_bus_socket:ro "
                  # "--restart unless-stopped "
                  "--add-host %s:127.0.0.1 "
                  "--add-host node01:10.10.10.101 "
                  "--add-host node02:10.10.10.102 "
                  "--add-host node03:10.10.10.103 "
                  "--add-host node04:10.10.10.104 "
                  "--add-host node05:10.10.10.105 "
                  "--add-host node06:10.10.10.106 "
                  "--add-host node07:10.10.10.107 "
                  "--add-host node08:10.10.10.108 "
                  "--add-host node09:10.10.10.109 "
                  "--add-host node10:10.10.10.110 "
                  "--add-host node11:10.10.10.111 "
                  "--add-host node12:10.10.10.112 "
                  "--add-host node13:10.10.10.113 "
                  "--add-host node14:10.10.10.114 "
                  "--add-host node15:10.10.10.115 "
                  "--add-host node16:10.10.10.116 "
                  "--add-host node17:10.10.10.117 "
                  "--add-host node18:10.10.10.118 "
                  "--add-host node19:10.10.10.119 "
                  "--add-host node20:10.10.10.120 "
                  "--add-host node21:10.10.10.121 "
                  "--add-host node22:10.10.10.122 "
                  "--add-host node23:10.10.10.123 "
                  "--add-host node24:10.10.10.124 "
                  "--add-host node25:10.10.10.125 "
                  "--add-host node26:10.10.10.126 "
                  "--add-host node27:10.10.10.127 "
                  "--add-host node28:10.10.10.128 "
                  "--add-host node29:10.10.10.129 "
                  "--add-host node30:10.10.10.130 "
                  "--add-host node31:10.10.10.131 "
                  "--add-host node32:10.10.10.132 "
                  "--add-host node33:10.10.10.133 "
                  "--add-host node34:10.10.10.134 "
                  "--add-host node35:10.10.10.135 "
                  "--add-host admin:10.10.10.100 "
                  "--shm-size=%s "
                  "%s "
                  "-h %s "
                  "-d "
                  "deepo_plus "
                  "/usr/sbin/sshd -p %d -D" % (
                      node_name, docker_type, container_name, cname, cname, cname, cname, cname, cname, cname, cname, cname, container_name, shm_size,
                      addition_str,
                      container_name, container_port))
        print("create container on %s successful!" % node_name)

    @classmethod
    def rm_container_on_remote(self, node_name, username):
        container_name = '%s-%s' % (username, node_name)

        os.system('ssh %s "docker stop %s && docker rm %s"' % (node_name, container_name, container_name))
        print('close', container_name, 'done')
