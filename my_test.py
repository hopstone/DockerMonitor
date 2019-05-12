# -*- coding: utf-8 -*-
# @Time    : 2018/8/11 下午5:05
# @Author  : Zhixin Piao 
# @Email   : piaozhx@shanghaitech.edu.cn


import os
import xlrd
import xlsxwriter


def main():
    # open the file for reading
    wbRD = xlrd.open_workbook('gpu_stat.xlsx')
    sheets = wbRD.sheets()

    wb = xlsxwriter.Workbook('gpu_stat.xlsx')

    for sheet in sheets: # write data from old file
        newSheet = wb.add_worksheet(sheet.name)
        for row in range(sheet.nrows):
            for col in range(sheet.ncols):
                newSheet.write(row, col, sheet.cell(row, col).value)

    for row in range(10, 20): # write NEW data
        for col in range(20):
            newSheet.write(row, col, "test ({}, {})".format(row, col))

    wb.close() # THIS writes



if __name__ == '__main__':
    main()
