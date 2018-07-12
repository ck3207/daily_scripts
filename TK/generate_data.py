# -*- coding: utf-8 -*-
__author__ = "chenk"
import random
import datetime
import time
import re

class Generate_Data:
    def __init__(self, cur):
        self.cur = cur
        self.all_columns_value = dict()

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

    def extract_to_table_point_column(self, entry="A1.COL1 + A2.COL2 / A3.COL1 + A4.COL4 / A5.COL5 = A3.COL3"):
        table_columns = list()
        reg_table_column = re.compile(r"\s*(\w+\.\w+)")
        reg_symbol = re.compile(r"[+,-,*,/,=]")
        i, j = 0, 1

        for table_column in reg_table_column.findall(entry):
            table_columns.insert(i, table_column.split(".")[1])
            i += 2
        for symbol in reg_symbol.findall(entry):
            table_columns.insert(j, symbol)
            j += 2
        return table_columns

    def solve(self, entry_column, expression, var):
        var_dict = {var: 1j}
        expression = expression.replace("=", "-(") + ")"
        for column in entry_column:
            globals[column] = self.all_columns_value[column]
        value = eval(expression, globals=var_dict)
        return -value.real/value.imag

    def generate_column_value(self, tables, entry_info, entry_columns, db_type, num):
        index = num
        if db_type == "mysql":
            pass
        elif db_type == "oracle":
            pass

        for table in tables:
            result = self.get_cols(table=table, db_type=db_type)
            insert_columns = ""
            insert_values = ""
            if result:
                while index:
                    break
                for row_info in result:
                    column = row_info[0]
                    key = column
                    if key in self.all_columns_value and len(self.all_columns_value[key]) - 1 >= index:
                        value = self.all_columns_value.get(key)[index]
                    elif key in self.all_columns_value:
                        value = self._generate_column_value(row_info=row_info)
                        self.all_columns_value[key].append(value)
                    else:
                        is_in_entry = False
                        for entry_column in entry_columns.values():
                            if column in entry_column:
                                is_in_entry = True
                                # 判断是否方程式只有一个未知数
                                need_cal_column_num = 0
                                for each in entry_column.split("||"):
                                    if self.all_columns_value[each.split(".")[1]] is None:
                                        need_cal_column_num += 1
                                    else:
                                        target_column = each.split(".")[1]
                                if need_cal_column_num == 1:
                                    expression = ""
                                    entry_column = self.extract_to_table_point_column(entry_info)
                                    for each in entry_column:
                                        expression += each
                                    value = self.solve(entry_column=entry_column, expression=expression,
                                                       var=target_column)
                                    if target_column in self.all_columns_value:
                                        self.all_columns_value[target_column].append(value)
                                    else:
                                        self.all_columns_value[target_column] = [value]

                            else:
                                self.get_column_value(row_info=row_info, table=table, column=column, index="")

                        if is_in_entry == False:
                            value = self._generate_column_value(row_info=row_info)
                            self.all_columns_value[column] = [value]

                        value = self._generate_column_value(row_info=row_info)
                        self.all_columns_value[key] = [value]

                    return self.get_column_value()

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

    def get_column_value(self, row_info, table, column, index):
        # 若字段数据已经生成，直接取值, 否则，调用生成数据方法
        key = table + "." + column
        key = column
        if key in self.all_columns_value and len(self.all_columns_value[key]) > index+1:
            value = self.all_columns_value.get(key)[index]
        elif key in self.all_columns_value:
            value = self._generate_column_value(row_info=row_info)
            self.all_columns_value[key].append(value)
        else:
            value = self._generate_column_value(row_info=row_info)
            self.all_columns_value[key] = [value]

        return value

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
