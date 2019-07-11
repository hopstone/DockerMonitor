# -*- coding: utf-8 -*-
# @Time    : 2018/8/22 下午10:03
# @Author  : Zhixin Piao 
# @Email   : piaozhx@shanghaitech.edu.cn

import sys
import os

sys.path.append(os.path.abspath('./'))

from multiprocessing import Pool
import json
import pymysql
import time

from config import DB_HOST, DB_NAME, DB_PASSWOED, DB_USERNAME
from handler.base_handler import STANDARD_NODE_LIST


# NODE_LIST = ['ws62', 'ws63', 'ws64', 'ws65', 'rtx01', 'rtx02']
NODE_LIST = ['node47', 'node48']
NODE_ID_LIST = [4, 5]
# NODE_LIST = ['ws62']


def get_useful_gpu_msg(node_name, node_id):
    conn = pymysql.connect(DB_HOST, DB_USERNAME, DB_PASSWOED, DB_NAME, )
    cursor = conn.cursor()
    while True:
        gpu_msg = os.popen('''ssh %s '/root/anaconda3/bin/python /root/svip_tools/get_gpu_msg.py' ''' % node_name).read().strip()
        cursor.execute("UPDATE docker.svip_gpu SET node_gpu_msg = '%s' WHERE node_id=%d" % (gpu_msg, node_id))

        try:
            conn.commit()
            print('%s OK' % node_name)
        except:
            conn.rollback()
            print('rollback')


def main():
    # get_useful_gpu_msg(4)

    p = Pool(len(NODE_LIST))
    args_list = [(node_name, node_id) for node_name, node_id in zip(NODE_LIST, NODE_ID_LIST)]
    p.starmap(get_useful_gpu_msg, args_list)
    p.close()


if __name__ == '__main__':
    main()
