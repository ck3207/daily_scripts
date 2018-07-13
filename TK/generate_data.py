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

    def generate_column_value(self, tables, entry_columns, db_type, num):

        for table in tables:
            result = self.get_cols(table=table, db_type=db_type)

            index = 0
            commit_num = 1000
            flag = False
            if result:
                while True:
                    insert_sql = ""
                    while commit_num:
                        insert_values = ""
                        for row_info in result:
                            column = row_info[0]
                            if len(row_info) > 3:
                                row_info = row_info[:2]
                            key = column
                            value = ""
                            # 字段已存在于字典项中，可直接取值
                            if key in self.all_columns_value and len(self.all_columns_value[key]) - 1 >= index:
                                value = self.all_columns_value.get(key)[index]
                            # 字段已存在于字典项中，但没有可取值
                            elif key in self.all_columns_value:
                                value = self._generate_column_value(row_info=row_info)
                                self.all_columns_value[key].append(value)
                            # 字段不存在于字典项中
                            else:
                                is_in_entry = False # 判断字段是否在表达式中的标志位
                                for entry_info, entry_column in entry_columns.items():
                                    # 字段在表达式中
                                    if column in entry_column:
                                        # 判断是否方程式只有一个未知数
                                        need_cal_column_num = 0
                                        for each in entry_column.split("||"):
                                            if self.all_columns_value[each.split(".")[1]] is None:
                                                need_cal_column_num += 1
                                            else:
                                                target_column = each.split(".")[1]
                                        # 方程中仅有一个未知变量
                                        if need_cal_column_num == 1:
                                            expression = ""
                                            entry_column = self.extract_to_table_point_column(entry_info)
                                            for each in entry_column:
                                                expression += each
                                            # 计算未知变量
                                            value = self.solve(entry_column=entry_column, expression=expression,
                                                               var=target_column)
                                            if target_column in self.all_columns_value:
                                                self.all_columns_value[target_column].append(value)
                                            else:
                                                self.all_columns_value[target_column] = [value]
                                            # 表达式未知字段与需要生成的字段不为同一字段
                                            if column != target_column:
                                                self.all_columns_value[key] = value
                                            # 表达式未知字段与需要生成的字段为同一字段
                                            else:
                                                is_in_entry = True
                                                break
                                        # 方程中有多个未知变量(暂不处理，有可能有别的表达式存在唯一变量)
                                        else:
                                            pass
                                    # 字段不在此表达式中
                                    else:
                                        pass
                                # 字段不在所有表达式中
                                if is_in_entry == False and isinstance(value, str):
                                    value = self._generate_column_value(row_info=row_info)
                                    self.all_columns_value[column] = [value]

                            insert_values += " '{0}',".format(value)
                        insert_values = "({0}),".format(insert_values[:-1])
                        insert_sql += "{0}".format(insert_values)
                        index += 1
                        commit_num -= 1
                        if commit_num == 0:
                            insert_sql = "insert into {0} values {1}".format(table, insert_sql[:-1])
                            commit_num = 1000
                            self.execute_sql(insert_sql)
                        if index >= num:
                            insert_sql = "insert into {0} values {1}".format(table, insert_sql[:-1])
                            self.execute_sql(insert_sql)
                            flag = True
                            break
                    if flag == True:
                        break

    def _generate_column_value(self, row_info):
        """According to the field type, it will generate a approciate value. Now it is support Mysql and Oracle."""
        col_name = row_info[0]
        if len(row_info) == 2:
            col_type_info = row_info[1]
            # index = int(col_type_info.rfind("("))  # 通过左右括号获取括号内的数据
            # 字段有无长度标识
            if "(" in col_type_info:
                parentheses_left = col_type_info.find("(")
                parentheses_right = col_type_info.rfind(")")
                length = int(col_type_info[parentheses_left+1: parentheses_right])
                col_type = col_type_info[:parentheses_left]
            else:
                length = 0
                col_type = col_type_info

            # 处理数值类型有符号与无符号
            if "unsigned" in col_type_info:
                is_unsigned = 1
            else:
                is_unsigned = 2

            # 数值类型根据有/无符号，变更输入数据的区间
            g = lambda x, y: -y - 1 if x == 2 else 0

            # 处理字段最大长度
            # g2 = lambda l, c: 10**7 - 1 if l >= len(c) + 6 else 10**(l+1) - 1
            random_range = 999999

            # MYSQL
            # 对于不同类型的字段，生成数据值的格式、内容等处理
            # char,varchar
            if "char" in col_type:
                if length - len(col_name) >= 6:
                    random_range = 10**(6+1) - 1
                    value = col_name + str(random.randint(0, random_range))
                else:
                    random_range = 10**length - 1
                    value = str(random.randint(0, random_range))
                return value
            elif col_type == "tinyint":
                # 编码为gbk时，每个字符最多占2个字节；编码为utf8时，每个字符最多占3个字节；此处以utf8编码占用空间计算，下同
                random_range = 127
                value = random.randint(g(is_unsigned, random_range), random_range)
                return value
            elif col_type == "smallint":
                random_range = 32767
                value = random.randint(g(is_unsigned, random_range), random_range)
                return value
            elif col_type == "mediumint":
                random_range = 8388607
                value = random.randint(g(is_unsigned, random_range), random_range)
                return value
            # int,integer,bigint
            elif "int" in col_type:
                random_range = 8388607
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

    def execute_sql(self, sql):
        try:
            self.cur.execute(sql)
            self.cur.execute("commit;")
        except Exception as e:
            print(str(e))

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
