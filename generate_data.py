# -*- coding: utf-8 -*-
__author__ = "chenk"
from connect_to_mysql import Connect_mysql
import random,datetime,time

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

                 # 处理数值类型有符号与无符号
                 if "unsigned" in col_type_info:
                     is_unsigned = 1
                 else:
                     is_unsigned = 2

                 # 处理无长度字段 eg:date
                 if index == -1:
                     col_type = col_type_info
                 else:
                     col_type = col_type_info[:index]

                 # 数值类型根据有/无符号，变更输入数据的区间
                 g = lambda x, y: -y - 1 if x == 2 else 0

                 # 处理字段长度
                 random_range = 999999

                 # char,varchar
                 if "char" in col_type:
                     insert_sql = "{0}'{1}',".format(insert_sql, col_name + str(random.randint(0, random_range)))
                 elif col_type == "tinyint":
                     # 编码为gbk时，每个字符最多占2个字节；编码为utf8时，每个字符最多占3个字节；此处以utf8编码占用空间计算，下同
                     random_range = 255//(3*1*is_unsigned)
                     insert_sql = (insert_sql + "%d,") % random.randint(g(is_unsigned,random_range), random_range)
                 elif col_type == "smallint":
                     random_range = 65535//(3*2*is_unsigned)    # 除考虑编码外，每个数字占用2个字节
                     insert_sql = (insert_sql + "%d,") % random.randint(g(is_unsigned,random_range), random_range)
                 elif col_type == "mediumint":
                     random_range = 65535//(3*2*is_unsigned)    # 除考虑编码外，每个数字占用2个字节
                     insert_sql = (insert_sql + "%d,") % random.randint(g(is_unsigned,random_range), random_range)
                 # int,integer,bigint
                 elif "int" in col_type:
                     insert_sql = (insert_sql + "%d,") % random.randint(g(is_unsigned,random_range), random_range)
                 elif col_type in ["decimal", "double", "numeric", "real","float"]:
                     insert_sql = (insert_sql + "%f,") % random.uniform(g(is_unsigned,random_range), random_range)
                 elif col_type == "date":
                     insert_sql = "{0}'{1}',".format(insert_sql, get_date(random.randint(-300, 0)))
                 elif col_type == "time":
                     insert_sql = "{0}'{1}',".format(insert_sql, get_time())
                 # timestamp,datetime
                 elif "time" in col_type:
                     insert_sql = "{0}'{1}',".format(insert_sql, get_date(random.randint(-300, 0)) + " " + get_time())
                 elif col_type == "year":
                     insert_sql = "{0}'{1}',".format(insert_sql, str(random.randint(1901, 2155)))

             sql_value += "({0}),".format(insert_sql[:-1])
             commit_num -= 1

         sql += "insert into {0} values {1};".format(table, sql_value[:-1])
         try:
             cur.execute(sql)
             conn.commit()
             print("Insert into {0} successfully!".format(table))
         except:
             print("SQL ERROR:{0}".format(sql))
         commit_times -= 1

def get_date(num=0):
    """获取今日日期"""
    if num == 0:
        return datetime.date.today().strftime("%Y%m%d")
    else:
        return (datetime.date.today() + datetime.timedelta(days=num)).strftime("%Y-%m-%d")

def get_time():
    """获取今日日期"""
    return time.strftime("%H:%M:%S")


if __name__ == "__main__":
    connect_mysql = Connect_mysql()
    mysql_config = connect_mysql.get_config("mysql_config.json")
    conn, cur = connect_mysql.conn_mysql(host=mysql_config["localhost_cf_test"]["host"],
                                         port=mysql_config["localhost_cf_test"]["port"], \
                                         user=mysql_config["localhost_cf_test"]["user"],
                                         password=mysql_config["localhost_cf_test"]["password"], \
                                         database=mysql_config["localhost_cf_test"]["database"],
                                         charset=mysql_config["localhost_cf_test"]["charset"])

    # tables = ["all_securate_test","businflag_test"]
    tables = ["smart_organization_forecast_copy","investor","test"]
    for table in tables:
        cols = get_cols(table)
        generate_data_for_mysqldb(columns=cols,commit_num=10,commit_times=3)

