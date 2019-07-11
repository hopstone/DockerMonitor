# -*- coding: utf-8 -*-
# @Time    : 2019-05-20 23:47
# @Author  : Zhixin Piao 
# @Email   : piaozhx@shanghaitech.edu.cn


from db.db_manager import DatabaseManager
import time
from tqdm import tqdm


def main():
    db = DatabaseManager()
    cursor = db.get_cursor()
    # time_condition = " AND query_time >= '%s' AND query_time <= '%s'"
    # DELETE FROM gpu_old WHERE DATE_FORMAT(query_time, '%s') <> 0 ORDER BY query_time LIMIT 1;

    for i in tqdm(range(16000)):
        cursor.execute("DELETE FROM gpu_old WHERE DATE_FORMAT(query_time, '%s') <> 0 LIMIT 10000")
        db.commit()


if __name__ == '__main__':
    main()
