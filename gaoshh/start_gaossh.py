# -*- coding: utf-8 -*-
# @Time    : 2019-07-11 23:37
# @Author  : Zhixin Piao 
# @Email   : piaozhx@shanghaitech.edu.cn

import sys

sys.path.append('./')

import os
from db.db_manager import DatabaseManager
from handler.base_handler import BaseHandler
from tqdm import tqdm
import pathlib


class ContainerAdditionStr:

    def __init__(self, node_name, advisor, cname):
        self.node_name = node_name
        self.advisor = advisor
        self.group_mapping = {
            '何旭明': 'plus_group',
            '高盛华': 'svip_group'
        }
        self.username = cname

    def get_node_addition_str(self):
        addition_str = ""

        '''
        public
        '''
        if self.node_name == 'node40':
            addition_str += " -v /new_disk1:/new_disk1 "
            addition_str += " -v /new_disk2:/new_disk2 "
            addition_str += " -v /ssd:/ssd "
            addition_str += " -v /home:/old_home "
        if self.node_name == 'node42':
            addition_str += " -v /new_disk1:/new_disk1 "
            addition_str += " -v /new_disk2:/new_disk2 "
            addition_str += " -v /ssd:/ssd "
            addition_str += " -v /home:/old_home "
        if self.node_name == 'node43':
            addition_str += " -v /new_disk1:/new_disk1 "
            addition_str += " -v /new_disk2:/new_disk2 "
            addition_str += " -v /ssd:/ssd "
            addition_str += " -v /home:/old_home "
        if self.node_name == 'node44':
            addition_str += " -v /new_disk1:/new_disk1 "
            addition_str += " -v /new_disk2:/new_disk2 "
            addition_str += " -v /ssd:/ssd "
            addition_str += " -v /home:/old_home "

        if self.node_name == 'node47':
            addition_str += " -v /public:/public "
        if self.node_name == 'node48':
            addition_str += " -v /public:/public "

        return addition_str

    def get_advisor_addition_str(self):
        addition_str = ""
        return addition_str

    def get_user_addition_str(self):
        addition_str = ""
        return addition_str

    def get_additional_str(self):
        str = self.get_node_addition_str() + self.get_advisor_addition_str() + self.get_user_addition_str()
        print(str)
        return str


def rm_container_on_remote(node_name, username):
    container_name = '%s-%s' % (username, node_name)

    os.system('ssh %s "docker stop %s && docker rm %s"' % (node_name, container_name, container_name))
    print('close', container_name, 'done')


def create_container_on_remote(node_name, docker_type, cname, container_port, advisor):
    container_name = '%s-%s' % (cname, node_name)
    addition_str = ContainerAdditionStr(node_name, advisor, cname).get_additional_str()

    memory_size = os.popen('''ssh %s  free -h | head -n 2 | tail -n 1 | awk -F' ' '{print $2}' ''' % node_name).read().strip()
    memory_unit = memory_size[-1]
    memory_size = int(memory_size[:-1])
    shm_size = memory_size // 2
    shm_size = str(shm_size) + memory_unit

    os.system("ssh %s "
              "%s run "
              "--name %s "
              "--network=host "
              "-v /AI_public/docker/%s/bin:/bin "
              "-v /AI_public/docker/%s/etc:/etc "
              "-v /AI_public/docker/%s/lib:/lib "
              "-v /AI_public/docker/%s/lib64:/lib64 "
              "-v /AI_public/docker/%s/opt:/opt "
              "-v /AI_public/docker/%s/root:/root "
              "-v /AI_public/docker/%s/sbin:/sbin "
              "-v /AI_public/docker/%s/usr:/usr "
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
              "--add-host node36:10.10.10.136 "
              "--add-host node37:10.10.10.137 "
              "--add-host node38:10.10.10.138 "
              "--add-host node39:10.10.10.139 "
              "--add-host node40:10.10.10.140 "
              "--add-host node41:10.10.10.141 "
              "--add-host node42:10.10.10.142 "
              "--add-host node43:10.10.10.143 "
              "--add-host node44:10.10.10.144 "
              "--add-host node45:10.10.10.145 "
              "--add-host node46:10.10.10.146 "
              "--add-host node47:10.10.10.147 "
              "--add-host node48:10.10.10.148 "
              "--add-host admin:10.10.10.100 "
              "--shm-size=%s "
              "%s "
              "-h %s "
              "-d "
              "deepo_plus "
              "/usr/sbin/sshd -p %d -D" % (
                  node_name, docker_type, container_name, cname, cname, cname, cname, cname, cname, cname, cname, container_name, shm_size,
                  addition_str, container_name, container_port))
    print("create container on %s successful!" % node_name)


def main():
    db = DatabaseManager()
    user_info_list = db.get_all_user_info()
    # permission_list = ['node40', 'node41', 'node42', 'node43', 'node44', 'node45', 'node46', 'node47', 'node48']
    permission_list = ['node40', 'node41', 'node42', 'node43', 'node44', 'node46']
    # permission_list = ['node48']

    """
    gaossh permission
    """
    for user_info in tqdm(user_info_list):
        username = user_info['username']
        cname = username
        container_port = user_info['container_port']
        advisor = user_info['advisor']

        if advisor not in ['高盛华']:
            continue

        if cname not in ['liandz']:
            continue

        for node_name in permission_list:
            docker_type = 'docker' if node_name == 'admin' else 'nvidia-docker'

            rm_container_on_remote(node_name, cname)
            create_container_on_remote(node_name, docker_type, cname, container_port, advisor)

            print("create %s-%s successfully." % (cname, node_name))

        os.system("cp gaoshh/gaossh_node.txt gaoshh/tmp.txt")
        os.system('sed -i "s/user_port/%d/g" gaoshh/tmp.txt' % (container_port))
        os.system('cat gaoshh/tmp.txt >>  /public/docker/%s/root/.ssh/config' % (cname))
        os.system("rm gaoshh/tmp.txt")

    return

    """
    AI Cluster permission    
    """
    for user_info in tqdm(user_info_list):
        username = user_info['username']
        cname = username
        container_port = user_info['container_port']
        advisor = user_info['advisor']

        if cname not in ['piaozx']:
            continue

        for permission_detail in user_info['permission']:
            node_name = permission_detail['name']
            docker_type = 'docker' if node_name == 'admin' else 'nvidia-docker'

            if node_name != 'node01':
                continue

            BaseHandler.rm_container_on_remote(node_name, cname)
            BaseHandler.create_container_on_remote(node_name, docker_type, cname, container_port, advisor)

            print("create %s-%s successfully." % (cname, node_name))


if __name__ == '__main__':
    main()
