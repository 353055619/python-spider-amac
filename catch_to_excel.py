'''
Description: 将缓存数据写入excel
Version: 1.0
Author: 魏苏航
email: godw2017@163.com
'''

import pickle

import xlwt

import config


def cache_to_excel(cache_path: str, excel_path: str):
    """
    读取缓存数据，存入excel中
    :param cache_path: 缓存数据路径
    :param excel_path: excel存储路径
    """
    print("Saving to excel...")

    with open(cache_path, "rb+") as f:
        datalist = pickle.load(f, encoding="gbk")

    workbook = xlwt.Workbook(encoding="utf-8")
    sheet = workbook.add_sheet("基金数据")
    sheet.write(0, 0, "基金管理人全称(中文)")
    sheet.write(0, 1, "登记时间")
    sheet.write(0, 2, "是否为符合提供投资建议条件的第三方机构")
    sheet.write(0, 3, "管理规模区间 ")
    for index, item in enumerate(datalist):
        row = index + 1
        sheet.write(row, 0, item["name"])
        sheet.write(row, 1, item["registerDate"])
        sheet.write(row, 2, item["ok"])
        sheet.write(row, 3, item["scale"])
    workbook.save(excel_path)


if __name__ == '__main__':
    cache_to_excel(config.CATCH_PATH, config.EXCEL_PATH)
