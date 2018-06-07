# -*- coding: utf-8 -*-
__author__ = "chenk"

import os
import datetime
import shutil
import re

from connect_to_mysql import Connect_mysql


def del_csv_file(path="file"):
    flag = ["_1.csv","_2.csv","_3.csv"]
    for file in os.listdir(path):
        for each in flag:
            if each in file:
                os.remove(path+os.path.sep+file)
    return

def which_csv(path="file"):
    """Select the csv file whose suffix is .csv"""
    csv_file = list()
    for file in os.listdir(path):
        if file not in except_csv_files:
            if ".csv" in file:
                file_path = "file/{0}".format(file)
                new_file_path = "file/{0}".format(file.split(".")[0])
                shutil.copy(file_path, new_file_path + "_1.csv")
                shutil.copy(file_path, new_file_path + "_2.csv")
                shutil.copy(file_path, new_file_path + "_3.csv")
                csv_file.append(file.split(".")[0])
    return csv_file

def get_date(date, num=90):
    """获取今日日期"""
    if len(date) == 8:
        year = int(date[:4])
        month = int(date[4:6])
        day = int(date[6:])
        try:
            target_date = (datetime.date(year, month, day) + datetime.timedelta(days=num)).strftime("%Y%m%d")
        except ValueError:
            return False

        if target_date in trading_day:
            return target_date
        else:
            return get_date(date,num+1)
    else:
        raise Exception("There is a wrong date {0}".format(date))

def get_all_trading_dates_of_a_certain_year(year="2017"):
    """获取指定年份的所有交易日"""
    all_trading_dates = list()
    sql = "SELECT DISTINCT init_date from exchangedate ed WHERE ed.exchange_type = 1 \
AND ed.init_date > '{0}0101' AND ed.init_date <= '{0}1231' ORDER BY init_date ASC".format(year)

    cur.execute(sql)
    for each in cur.fetchall():
        all_trading_dates.append(str(each[0]))
    return all_trading_dates

def file_deal(file):
    print("Deal file {0}...".format(file))
    try:
        with open(file="file/{0}.csv".format(file), mode="a",encoding="gbk") as f_origin:
            for i in range(1,4):
                if i == 1:
                    num = 90
                elif i == 2:
                    num = 180
                elif num == 3:
                    num = 270
                flag = 0
                with open(file="file/{0}.csv".format(file+"_"+str(i)), mode="r",encoding="gbk") as f:
                    reg = re.compile("(2017\d{4})")
                    for line in f.readlines():
                        for each_date in re.findall(reg,line):
                            target_date = get_date(each_date,num)
                            if target_date:
                                line = line.replace(each_date,target_date)
                            else:
                                continue
                        if flag == 1:
                            f_origin.write(line)
                        flag = 1
        print("Deal file {0} Successfully.".format(file))
    except UnicodeDecodeError as e:
        print("Deal file {0} Error.".format(file))
        print(str(e))

connect_mysql = Connect_mysql()
mysql_config = connect_mysql.get_config("mysql_config.json")
conn, cur = connect_mysql.conn_mysql(host=mysql_config["localhost_huaan"]["host"], port=mysql_config["localhost_huaan"]["port"],\
                         user=mysql_config["localhost_huaan"]["user"], password=mysql_config["localhost_huaan"]["password"], \
                        database=mysql_config["localhost_huaan"]["database"], charset=mysql_config["localhost_huaan"]["charset"])

trading_day_2017 = get_all_trading_dates_of_a_certain_year(year="2017")
trading_day_2018 = get_all_trading_dates_of_a_certain_year(year="2018")
trading_day = trading_day_2017+trading_day_2018

except_csv_files = ["his_asset.csv","his_assetdebit.csv","clientinfo.csv","his_datafund.csv","his_datastock.csv"]
del_csv_file()
for file in which_csv():
    file_deal(file)

cur.close()
conn.close()