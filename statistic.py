# -*- coding: utf-8 -*-
# @Time    : 2019-04-20 19:15
# @Author  : Zhixin Piao 
# @Email   : piaozhx@shanghaitech.edu.cn

from db.db_manager import DatabaseManager
import time
import json
import xlsxwriter


def get_date_list():
    return ['2019-03-04', '2019-03-05', '2019-03-06', '2019-03-07', '2019-03-08', '2019-03-09', '2019-03-10', '2019-03-11', '2019-03-12', '2019-03-13',
            '2019-03-14', '2019-03-15', '2019-03-16', '2019-03-17', '2019-03-18', '2019-03-19', '2019-03-20', '2019-03-21', '2019-03-22', '2019-03-23',
            '2019-03-24', '2019-03-25', '2019-03-26', '2019-03-27', '2019-03-28', '2019-03-29', '2019-03-30', '2019-03-31', '2019-04-01', '2019-04-02',
            '2019-04-03', '2019-04-04']




def get_one_node_gpu_usage_info(db, node_id, start_date, end_date):
    cursor = db.get_cursor()
    # time_condition = " AND query_time >= '%s' AND query_time <= '%s'"

    cursor.execute("SELECT * FROM gpu "
                   "WHERE node_id = " + str(node_id) +
                   # " AND query_time >= DATE_SUB(CURDATE(), INTERVAL 1 DAY)"
                   # " AND query_time >= DATE_SUB(CURDATE(), INTERVAL 1 DAY)"
                   " AND query_time >= '%s' "
                   " AND query_time < '%s' "
                   # "AND DATE_FORMAT(query_time, '%i') % 15 = 0 "\
                   " AND DATE_FORMAT(query_time, '%%s') = 0 " % (start_date, end_date)
                   )
    res_list = cursor.fetchall()

    res_num = len(res_list)
    print(res_num)
    if res_num == 0:
        if node_id in [13, 14, 26]:
            gpu_num = 8
        else:
            gpu_num = 4
        return [{'avg_gpu_utils': 0, 'avg_mem_used': 0, 'user_dict': {}} for _ in range(gpu_num)]

    gpu_num = len(json.loads(res_list[0][1])['gpus'])
    gpu_stat_list = [{'avg_gpu_utils': 0, 'avg_mem_used': 0, 'user_dict': {}} for _ in range(gpu_num)]

    for res in res_list:
        gpu_info_list = json.loads(res[1])['gpus']

        for idx, gpu_info in enumerate(gpu_info_list):
            gpu_id = gpu_info['index']
            gpu_utils = gpu_info['utilization.gpu']
            gpu_mem_used = gpu_info['memory.used']
            gpu_mem_total = gpu_info['memory.total']

            # gpu_stat_list[idx]['avg_gpu_utils'] += gpu_utils
            gpu_stat_list[idx]['avg_mem_used'] += gpu_mem_used

            if len(gpu_info['processes']) > 0:
                gpu_stat_list[idx]['avg_gpu_utils'] += 1

            for p_info in gpu_info['processes']:
                uname = p_info['username']
                if uname.find('-') != -1:
                    uname = uname[:uname.find('-')]

                if uname not in gpu_stat_list[idx]['user_dict']:
                    gpu_stat_list[idx]['user_dict'][uname] = 1
                else:
                    gpu_stat_list[idx]['user_dict'][uname] += 1

    for idx in range(gpu_num):
        gpu_stat_list[idx]['avg_gpu_utils'] /= res_num
        gpu_stat_list[idx]['avg_mem_used'] /= res_num

    return gpu_stat_list


def main():
    db = DatabaseManager()

    start_time = time.time()
    stat_node_id = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24, 27, 28, 29, 30, 31, 32, 33, 34, 35]
    # stat_node_id = [1]
    date_list = get_date_list()

    wb = xlsxwriter.Workbook('gpu_stat.xlsx')
    gpu_utils_sheet = wb.add_worksheet('gpu_utils')
    user_num_sheet = wb.add_worksheet('user_num')

    """
    sheet title
    """
    gpu_utils_sheet.write(0, 0, 'node')
    gpu_utils_sheet.write(0, 1, 'gpu_id')
    for i in range(len(date_list) - 1):
        gpu_utils_sheet.write(0, 2 + i, date_list[i])

    user_num_sheet.write(0, 0, 'node')
    for i in range(len(date_list) - 1):
        user_num_sheet.write(0, 1 + i, date_list[i])

    """
    sheet content
    """
    for i in range(len(date_list) - 1):
        cluster_gpu_stat_list = []

        row_cursor = 1
        for node_idx, node_id in enumerate(stat_node_id):
            print('-' * 30, node_id, '-', date_list[i], '-', date_list[i + 1], '-' * 30)
            gpu_stat_list = get_one_node_gpu_usage_info(db, node_id, date_list[i], date_list[i + 1])
            cluster_gpu_stat_list.append(gpu_stat_list)
            print(gpu_stat_list)

            node_user_dict = {}
            for gpu_id, gpu_stat in enumerate(gpu_stat_list):
                # gpu utils sheet
                gpu_utils_sheet.write(row_cursor + gpu_id, 0, node_id)
                gpu_utils_sheet.write(row_cursor + gpu_id, 1, gpu_id)
                gpu_utils_sheet.write(row_cursor + gpu_id, 2 + i, gpu_stat['avg_gpu_utils'])

                # user num sheet
                gpu_user_dict = gpu_stat['user_dict']
                for user_name, user_count in gpu_user_dict.items():
                    if user_name not in node_user_dict:
                        node_user_dict[user_name] = user_count
                    else:
                        node_user_dict[user_name] += user_count

            row_cursor += len(gpu_stat_list)
            user_num_sheet.write(1 + node_idx, 0, node_id)
            user_num_sheet.write(1 + node_idx, 1 + i, len(node_user_dict))

    wb.close()

        # cluster_user_dict = {}
        # for gpu_stat_list in cluster_gpu_stat_list:
        #     for gpu_stat in gpu_stat_list:
        #         gpu_user_dict = gpu_stat['user_dict']
        #
        #         for user_name, user_count in gpu_user_dict.items():
        #             if user_name not in cluster_user_dict:
        #                 cluster_user_dict[user_name] = user_count
        #             else:
        #                 cluster_user_dict[user_name] += user_count

        # print(len(cluster_user_dict))
        # print(sorted(list(cluster_user_dict.items()), key=lambda x: x[1], reverse=True))


if __name__ == '__main__':
    main()
