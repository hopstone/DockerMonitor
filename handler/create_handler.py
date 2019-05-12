# -*- coding: utf-8 -*-
# @Time    : 2018/8/11 下午9:59
# @Author  : Zhixin Piao 
# @Email   : piaozhx@shanghaitech.edu.cn

from handler.base_handler import BaseHandler
import os
import json


class CreateHandler(BaseHandler):
    def post(self):
        """
        code 101: blank input!
        code 102: name exists
        code 200: everything is ok
        :return:
        """
        cname = self.get_argument('cname')
        chs_name = self.get_argument('chs_name')
        email = self.get_argument('email')
        advisor = self.get_argument('advisor')
        ret_data = {'code': '', 'log': ''}
        self.log = ''

        if cname == '' or chs_name == '' or email == '' or advisor == '':
            ret_data['code'] = 101
            self.write(ret_data)
            return

        uid = self.db.get_uid_by_username(cname)
        if uid != None:
            ret_data['code'] = 102
            self.write(ret_data)
            return

        uid = self.db.try_to_add_user(cname)

        container_port = uid + 21000
        each_user_port_num = 10
        port_range_str = '%d-%d' % (30000 + each_user_port_num * (uid - 1000), 30000 + each_user_port_num * (uid - 1000 + 1) - 1)
        self.create_user_docker_dir(cname, container_port, port_range_str, advisor)
        self.db.add_user(cname, container_port, port_range_str, email, chs_name, advisor)
        self.db.add_user_permission(uid, [0], 'yes', '', '', '')

        ret_data['code'] = 200
        ret_data['log'] = self.log
        self.write(ret_data)

    def create_user_docker_dir(self, cname, container_port, port_range_str, advisor):
        self.log += 'Creating user docker dir...\n'

        user_dir = '/public/docker/%s' % cname
        if os.path.exists(user_dir):
            print(user_dir, 'exist!!!!')
            self.log += "User docker dir exists!!!, just change user's permission\n"
            return False
        else:
            prepare_root_path = '/public/docker/prepare_baseline-1'
            prepare_dirname_list = sorted(os.listdir(prepare_root_path))

            print('Creating user docker dir...')
            if len(prepare_dirname_list) == 0:
                os.system("cp -r /public/docker/baseline-1 %s" % user_dir)
            else:
                prepare_dir = '%s/%s' % (prepare_root_path, prepare_dirname_list[0])
                print("mv %s %s" % (prepare_dir, user_dir))
                os.system("mv %s %s" % (prepare_dir, user_dir))

            # build ssh-key
            os.system('''cat /dev/zero | ssh-keygen -q -N "" -f /public/docker/%s/root/.ssh/id_rsa''' % cname)
            os.system("cat /public/docker/%s/root/.ssh/id_rsa.pub >> /public/docker/%s/root/.ssh/authorized_keys" % (cname, cname))
            os.system('sed -i "s/user_port/%d/g" /public/docker/%s/root/.ssh/config' % (container_port, cname))
            os.system('sed -i "s/user_port_range/%s/g" /public/docker/%s/etc/motd' % (port_range_str, cname))
            print('Done.')
            self.log += "user docker dir has been created successfully!\n"

            print('Creating user admin container...')
            self.log += 'Creating user admin container...\n'

            self.create_container_on_remote('admin', 'docker', cname, container_port, advisor)
            print('Done.')
            self.log += 'Done.\n'

            return True
