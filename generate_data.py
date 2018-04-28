# -*- coding: utf-8 -*-
__author__ = "chenk"
from connect_to_mysql import Connect_mysql
import random,datetime

def get_cols(table):
     """通用造数据函数"""
     sql = "desc " + table
     cur.execute(sql)
     result = cur.fetchall()

     return result

def generate_data_for_mysqldb(columns,commit_num,commit_times):
     """通用造数据函数
     columns 是表的所有字段元祖，
     commit_num 是每次插入数据库的数量，
     commit_times*commit_num是插入的总数据量"""
     commit_num_temp = commit_num
     while commit_times:
         sql = ""   # 被执行的sql
         sql_value = "" # 数据组集
         commit_num = commit_num_temp
         while commit_num:
             insert_sql = ""    # 单组数据
             for col in columns:
                 col_name = col[0]
                 col_type_info = col[1]
                 index = int(col_type_info.rfind("("))

                 # if col_name == "status":
                 #     pass
                 # 处理无长度字段 eg:date
                 if index == -1:
                     col_type = col_type_info
                     col_length = 1
                 else:
                     col_type = col_type_info[:index]

                 # 处理浮点型字段 eg: decidecimal(19,2)
                 try:
                     col_length = int(col_type_info[index + 1:-1])
                 except:
                     col_length = 1

                 # 处理字段长度
                 if col_length >= 20:
                     random_range = 2 ** 20 - 1
                 else:
                     max_add_length = 2 ** col_length - len(col_name) - 1
                     if max_add_length < 6:
                         col_name = ""
                         max_add_length = col_length
                     else:
                         max_add_length = 6
                     random_range = 2 ** max_add_length - 1

                 if col_type in ["varchar"]:
                     insert_sql = "{0}'{1}',".format(insert_sql, col_name + str(random.randint(0, random_range)))
                 elif "int" in col_type:
                     insert_sql = (insert_sql + "%d,") % random.randint(0, random_range)
                 elif col_type in ["decimal", "double", "numeric", "real"]:
                     insert_sql = (insert_sql + "%f,") % random.uniform(0, random_range)
                 elif col_type == "date":
                     insert_sql = "{0}'{1}',".format(insert_sql, get_date(random.randint(-100, 0)))
                 elif col_type == "timestamp":
                     pass

             sql_value += "({0}),".format(insert_sql[:-1])
             commit_num -= 1

         sql += "insert into {0} values {1};".format(table, sql_value[:-1])
         cur.execute(sql)
         conn.commit()
         commit_times -= 1

def get_date(num=0):
    """获取今日日期"""
    if num == 0:
        return datetime.date.today().strftime("%Y%m%d")
    else:
        return (datetime.date.today() + datetime.timedelta(days=num)).strftime("%Y%m%d")

connect_mysql = Connect_mysql()
mysql_config = connect_mysql.get_config("mysql_config.json")
conn, cur = connect_mysql.conn_mysql(host=mysql_config["localhost_cf_test"]["host"], port=mysql_config["localhost_cf_test"]["port"],\
                         user=mysql_config["localhost_cf_test"]["user"], password=mysql_config["localhost_cf_test"]["password"], \
                        database=mysql_config["localhost_cf_test"]["database"], charset=mysql_config["localhost_cf_test"]["charset"])

if __name__ == "__main__":
    # tables = ["all_securate_test","businflag_test"]
    tables = ["his_datastock_test"]
    for table in tables:
        cols = get_cols(table)
        generate_data_for_mysqldb(columns=cols,commit_num=10,commit_times=3)

