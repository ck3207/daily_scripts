# -*- coding: utf-8 -*-
__author__ = "chenk"
import random
import datetime
import time
import re

class Generate_Data:
    def __init__(self, cur):
        self.cur = cur

    def get_cols(self, table, db_type):
        """获取表字段名、字段类型"""
        if db_type == "mysql":
         sql = "desc " + table
        elif db_type == "oracle":
         sql = "select column_name,data_type,data_length from user_tab_columns where Table_Name='{0}'".format(table)
        else:
         return
        self.cur.execute(sql)
        result = self.cur.fetchall()

        return result

    def generate_column_value(self, column_relation, table, db_type, index):
        if db_type == "mysql":
            pass
        elif db_type == "oracle":
            pass
        result = self.get_cols(table=table, db_type=db_type)
        if result:
            for row_info in result:
                column = row_info[0]
                return self.get_column_value(column_relation, row_info, table, column, index)

    def _generate_column_value(self, row_info):
        """According to the field type, it will generate a approciate value. Now it is support Mysql and Oracle."""
        col_name = row_info[0]
        if len(row_info) == 2:
            col_type_info = row_info[1]
            index = int(col_type_info.rfind("("))  # 通过左右括号获取括号内的数据

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

            # MYSQL
            # 对于不同类型的字段，生成数据值的格式、内容等处理
            # char,varchar
            if "char" in col_type:
                col_length = int(col_type_info[index + 1:-1])  # 获取字段允许长度
                if len(col_name) > (col_length - 6):
                    if col_length < 6:
                        value = str(random.randint(0, 9 * 10 ** col_length))
                    else:
                        value = str(random.randint(0, random_range))
                else:
                    value = col_name + str(random.randint(0, random_range))
                return value
            elif col_type == "tinyint":
                # 编码为gbk时，每个字符最多占2个字节；编码为utf8时，每个字符最多占3个字节；此处以utf8编码占用空间计算，下同
                random_range = 255 // (3 * 1 * is_unsigned)
                value = random.randint(g(is_unsigned, random_range), random_range)
                return value
            elif col_type == "smallint":
                random_range = 65535 // (3 * 2 * is_unsigned)  # 除考虑编码外，每个数字占用2个字节
                value = random.randint(g(is_unsigned, random_range), random_range)
                return value
            elif col_type == "mediumint":
                random_range = 65535 // (3 * 2 * is_unsigned)  # 除考虑编码外，每个数字占用2个字节
                value = random.randint(g(is_unsigned, random_range), random_range)
                return value
            # int,integer,bigint
            elif "int" in col_type:
                value = random.randint(g(is_unsigned, random_range), random_range)
                return value
            elif col_type in ["decimal", "double", "numeric", "real", "float"]:
                value = random.uniform(g(is_unsigned, random_range), random_range)
                return value
            elif col_type == "date":
                value = get_date(random.randint(-300, 0))
                return value
            elif col_type == "time":
                value = get_time()
                return value
            # timestamp,datetime
            elif "time" in col_type:
                value = get_date(random.randint(-300, 0)) + " " + get_time()
                return value
            elif col_type == "year":
                value = str(random.randint(1901, 2155))
                return value
        elif len(row_info) == 3:
            col_type = row_info[1]
            col_length = row_info[2]
            # ORACLE
            print("Oracle")

    def get_column_value(self, column_relation, row_info, table, column, index):
        """column_relation = {0:{"l0":["table1", "+table2"], "l1":["table2"]}}"""
        operator = {"+":"-", "-":"+", "*":"/", "/":"*"}
        # 若字段数据已经生成，直接取值
        for key in column_relation.keys():
            if isinstance(key, str) and column in key:
                if len(column_relation[key]) < index + 1:
                    continue
                else:
                    return column_relation.get(key)[index]

        target_column = {"target_column": ["column", "l0", ]}
        ignore = list()
        for key in column_relation.keys():
            if isinstance(key, int):
                i = 0
                if "l0" in column_relation[key]:
                    lr = "l"
                else:
                    lr = "r"
                for left in column_relation[key][lr+"0"]:
                    for each in ["+", "-", "*", "/"]:
                        left = left.replace(each, "")
                    if len(column_relation[left]) < index + 1:
                        i += 1
                        target_column["target_column"] = [left, lr+"0"]
                for right in column_relation[key][lr+"1"]:
                    for each in ["+", "-", "*", "/"]:
                        right = right.replace(each, "")
                    if len(column_relation[right]) < index + 1:
                        i += 1
                        target_column["target_column"] = [right, lr+"1"]
                if i == 1:
                    value = 0
                    j = 0
                    if lr == "l" and target_column["target_column"][2] == (lr + "0"):
                        reg = re.compile(r"([+,-,*,/])")
                        for each in column_relation[key][lr+"1"]:
                            col_info = column_relation[key][lr + "1"][j - 1]
                            symbol = reg.match(col_info).group(1)
                            table_column = col_info.replace(symbol, "").strip()
                            if "*" in each:
                                value += column_relation[table_column] * column_relation[each.replace("*", "")]
                            elif "/" in each:
                                value += column_relation[key][lr + "1"][j-1] / column_relation[key][lr+"1"][j]
                            elif "+" in each:
                                value += column_relation[each.replace("+", "")]
                            elif "-" in each:
                                pass
                            else:
                                value += column_relation[each]
                            j += 1
                    else:
                        pass
                    return

        # 字段
        if column_relation.get(table+"."+column) is None:
            return self._generate_column_value(row_info=row_info)
        elif column_relation.get(table+"."+column) == []:
            value = self._generate_column_value(row_info=row_info)
            column_relation.get(table + "." + column).append(value)
            return value
        else:
            return column_relation.get(table+"."+column)[index]

    def deal_operator(self, operator):
        if operator == "+":
            pass


    def generate_data_for_mysqldb(self, columns, commit_num, commit_times):
         """通用造数据函数
         columns 是表的所有字段元祖，
         commit_num 是每次插入数据库的数量，
         commit_times*commit_num是插入的总数据量"""
         global linkfield
         commit_num_temp = commit_num
         linkfield_index = 0
         while commit_times:
             sql = ""   # 被执行的sql
             sql_value = "" # 数据组集
             commit_num = commit_num_temp
             while commit_num:
                 insert_sql = ""    # 单组数据
                 for col in columns:
                     col_name = col[0]
                     col_type_info = col[1]
                     index = int(col_type_info.rfind("("))  # 通过左右括号获取括号内的数据

                     # linkfield["pass_colunm"] 中的字段是一个标识，可判断防止获取linkfield中产生的数据
                     if linkfield.get(col_name):
                         if not (table+col_name) in linkfield["pass_colunm"]:
                            insert_sql = "{0}'{1}',".format(insert_sql, linkfield[col_name][linkfield_index])
                            linkfield_index += 1
                            continue

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

                     # 对于不同类型的字段，生成数据值的格式、内容等处理
                     # char,varchar
                     if "char" in col_type:
                         col_length = int(col_type_info[index + 1:-1])  # 获取字段允许长度
                         if len(col_name) > (col_length-6):
                             if col_length < 6:
                                value = str(random.randint(0, 9*10**col_length))
                             else:
                                 value = str(random.randint(0, random_range))
                         else:
                             value = col_name + str(random.randint(0, random_range))
                         insert_sql = "{0}'{1}',".format(insert_sql, value)
                     elif col_type == "tinyint":
                         # 编码为gbk时，每个字符最多占2个字节；编码为utf8时，每个字符最多占3个字节；此处以utf8编码占用空间计算，下同
                         random_range = 255//(3*1*is_unsigned)
                         value = random.randint(g(is_unsigned,random_range), random_range)
                         insert_sql = (insert_sql + "%d,") % value
                     elif col_type == "smallint":
                         random_range = 65535//(3*2*is_unsigned)    # 除考虑编码外，每个数字占用2个字节
                         value = random.randint(g(is_unsigned,random_range), random_range)
                         insert_sql = (insert_sql + "%d,") % value
                     elif col_type == "mediumint":
                         random_range = 65535//(3*2*is_unsigned)    # 除考虑编码外，每个数字占用2个字节
                         value = random.randint(g(is_unsigned,random_range), random_range)
                         insert_sql = (insert_sql + "%d,") % value
                     # int,integer,bigint
                     elif "int" in col_type:
                         value = random.randint(g(is_unsigned,random_range), random_range)
                         insert_sql = (insert_sql + "%d,") % value
                     elif col_type in ["decimal", "double", "numeric", "real","float"]:
                         value = random.uniform(g(is_unsigned,random_range), random_range)
                         insert_sql = (insert_sql + "%f,") % value
                     elif col_type == "date":
                         value = get_date(random.randint(-300, 0))
                         insert_sql = "{0}'{1}',".format(insert_sql, value)
                     elif col_type == "time":
                         value = get_time()
                         insert_sql = "{0}'{1}',".format(insert_sql, value)
                     # timestamp,datetime
                     elif "time" in col_type:
                         value = get_date(random.randint(-300, 0)) + " " + get_time()
                         insert_sql = "{0}'{1}',".format(insert_sql, value)
                     elif col_type == "year":
                         value = str(random.randint(1901, 2155))
                         insert_sql = "{0}'{1}',".format(insert_sql, value)

                     # 判断字段是否在配置 linkfield_judge中，若是，则需存储数据值
                     if col_name in linkfield_judge.keys():
                         if not linkfield.get(col_name):
                             linkfield[col_name] = list()
                         linkfield[col_name].append(value)

                         # 处理同一张表中多个字段值相同的情况
                         for k, w in linkfield_judge.items():
                             if k != col_name and w == linkfield_judge[col_name]:
                                 if not linkfield.get(k):
                                     linkfield[k] = list()
                                 linkfield[k].append(value)
                                 # 对于正常生成数据的字段，放在过滤字段列表中，以作标识
                                 if not table+col_name in linkfield["pass_colunm"]:
                                    linkfield["pass_colunm"].append(table+col_name)

                 sql_value += "({0}),".format(insert_sql[:-1])
                 commit_num -= 1

             sql += "insert into {0} values {1};".format(table, sql_value[:-1])

             # 执行拼接的SQL
             try:
                 self.cur.execute(sql)
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
    generate_data = Generate_Data()
    tables = ["portrait_all","portrait_fund"]   # 配置需要插入数据的表名
    # 配置各表关联字段的关系,值相同的键为关联字段 eg: linkfield_judge = {"fund_account":0,"client_id":0, "client_name":1}
    # 下述配置的意思为 配置的表中若有fund_account 与 client_id,各表中字段fund_accout、client_id都做关联；
    # 各表的client_name值都会关联。
    linkfield_judge = {"fund_account":0,"client_name":0}
    # 例如：linkfield: {'pass_colunm':['portrait_allfund_account'],'client_name':['fund_account91', 'fund_account01'}
    linkfield = {"pass_colunm":[]}  # 存储关联字段的值

    for table in tables:
        # print("linkfield:",linkfield)
        cols = generate_data.get_cols(table)    # 获取表字段
        generate_data.generate_data_for_mysqldb(columns=cols,commit_num=10,commit_times=5)  # 生成数据
