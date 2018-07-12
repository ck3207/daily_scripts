# coding:utf-8
import re
import random

def validate_the_input(entry="A1.COL1 + A2.COL2 / A3.COL1 + A4.COL4 / A5.COL5 = A3.COL3"):
    table_columns = list()
    reg_table_column = re.compile(r"\s*(\w+\.\w+)")
    reg_symbol = re.compile(r"[+,-,*,/,=]")
    i, j = 0, 1

    for table_column in reg_table_column.findall(entry):
        table_columns.insert(i, table_column)
        if table_column != "A3.COL3":
            values[table_column] = random.randint(100, 10000)
        i += 2
    for symbol in reg_symbol.findall(entry):
        table_columns.insert(j, symbol)
        j += 2
    return table_columns

def deal_opetator(columns_info):
    # table_columns_tmp = table_columns
    count = columns_info.count("*")+columns_info.count("/")
    while count:
        for operator in ["*", "/"]:
            try:
                index = columns_info.index(operator)
                left = columns_info.pop(index-1)
                middle = columns_info.pop(index-1)
                right = columns_info.pop(index-1)
                columns_info.insert(index-1, left+middle+right)
            except ValueError:
                pass
        count -= 1
    return columns_info

def cal(columns_info):
    equal_index = columns_info.index("=")

    # 获取待解字段及其位置
    for each in columns_info:
        if each == "+" or each == "-" or each == "=":
            continue
        elif "*" in each:
            for column_temp in each.split("*"):
                for column in column_temp.split("/"):
                    if column not in values:
                        target_index = columns_info.index(each)
                        target_column = column
                        break
        elif "/" in each:
            for column_temp in each.split("/"):
                for column in column_temp.split("*"):
                    if column not in values:
                        target_index = columns_info.index(each)
                        target_column = column
                        break
        else:
            if each not in values:
                target_index = columns_info.index(each)
                target_column = each
                break

    # 使未知变量在等式左边
    if equal_index < target_index:
        columns_info_temp = list()
        for each in columns_info[equal_index+1:]:
            columns_info_temp.append(each)
            if target_column in each:
                target_index = columns_info_temp.index(each)
        columns_info_temp.append("=")
        for each in columns_info[:equal_index]:
            columns_info_temp.append(each)
        equal_index = columns_info_temp.index("=")
    columns_info = columns_info_temp

    # 处理目标字段至最后
    add_column = False
    if equal_index > target_index:
        columns_info.insert(equal_index-1, columns_info.pop(target_index))
        # 目标字段诺到后面时，如果是第一个字段，需要在目标字段前加 “+”， 否则 将原目标字段前面的符号带过去
        if target_index > 1:
            columns_info.insert(equal_index-2, columns_info.pop(target_index-1))
        else:
            columns_info.insert(equal_index-1, "+")
            add_column = True

    value = 0
    # 待解字段在等号之前
    offset = 1
    if add_column == True:
        offset = 2
    if equal_index > target_index:
        plus_or_minus = 1
        # 计算等式右侧的值
        for each in columns_info[equal_index+offset:]:
            value_right = ""
            if each == "+":
                plus_or_minus = 1
                continue
            elif each == "-":
                plus_or_minus = -1
                continue
            elif ("*" in each and "/" not in each) or ("*" in each and "/" in each and each.index("*") < each.index("/")):
                temp_multiplication = each.split("*")
                for multiplication_column in temp_multiplication:
                    if "/" in multiplication_column:
                        temp_division = multiplication_column.split("/")
                        if isinstance(value_right, str):
                            value_right = values[temp_division[0]]
                        else:
                            value_right *= values[temp_division[0]]
                        for i in range(1, len(temp_division)):
                            value_right /= values[temp_division[i]]
                    else:
                        if isinstance(value_right, str):
                            value_right = values[temp_multiplication]
                        else:
                            value_right *= values[temp_multiplication]

            elif ("/" in each and "*" not in each) or ("/" in each and "*" in each and each.index("/") < each.index("*")):
                temp_division = each.split("/")
                for division_column in temp_division:
                    if "*" in division_column:
                        temp_multiplication = division_column.split("*")
                        if isinstance(value_right, str):
                            value_right = values[temp_multiplication[0]]
                        else:
                            value_right /= values[temp_multiplication[0]]
                        for i in range(1, len(temp_multiplication)):
                            value_right *= values[temp_multiplication[i]]
                    else:
                        if isinstance(value_right, str):
                            value_right = values[division_column]
                        else:
                            value_right /= values[division_column]

            else:
                value_right = values[each]
            value += value_right * plus_or_minus

        # 处理有待解字段的数据
        plus_or_minus = -1
        # 计算等式左边的值，并计算出等式左边中目标字段的值
        for each in columns_info[:equal_index]:
            value_left = ""
            if each == "+":
                plus_or_minus = -1
                continue
            elif each == "-":
                plus_or_minus = 1
                continue
            elif ("*" in each and "/" not in each) or ("*" in each and "/" in each and each.index("*") < each.index("/")):
                temp_multiplication = each.split("*")
                for multiplication_column in temp_multiplication:
                    if target_column in multiplication_column and multiplication_column != temp_multiplication[-1]:
                        temp_multiplication.remove(target_column)
                        temp_multiplication.append(target_column)
                        temp_multiplication.insert(0, 0)
                        continue
                    elif target_column in multiplication_column and multiplication_column == temp_multiplication[-1]:
                        """2048/16/8/4/2 = 2  --> a/b/c/d/e = 2"""
                        # value *= plus_or_minus
                        if "/" in multiplication_column:
                            temp_division = multiplication_column.split("/")
                            temp_index = len(temp_division) - 1
                            for i in range(0, len(temp_division)):
                                if temp_division[i] == target_column:
                                    temp_index = i
                                    continue
                                elif temp_index == 0:
                                    value *= values[temp_division[i]]
                                else:
                                    value = values[temp_division[0]] / (value * values[temp_division[i]])
                            print("Out0:", str(value))
                            return
                        else:
                            print("Out1:", str(value / value_left))
                            return
                    else:
                        # 此场景不可能出现目标字段
                        if "/" in multiplication_column:
                            temp_division = multiplication_column.split("/")
                            if isinstance(value_left, str):
                                value_left = values[temp_division[0]]
                            else:
                                value_left *= values[temp_division[0]]
                            for i in range(1, len(temp_division)):
                                value_left /= values[temp_division[i]]
                        else:
                            if isinstance(value_left, str):
                                value_left = values[multiplication_column]
                            else:
                                value_left *= values[multiplication_column]

            elif ("/" in each and "*" not in each) or ("/" in each and "*" in each and each.index("/") < each.index("*")):
                temp_division = each.split("/")
                for division_column in temp_division:
                    if target_column in division_column and division_column != temp_division[-1]:
                        temp_division.remove(target_column)
                        temp_division.append(target_column)
                        temp_division.insert(0, 0)
                        continue
                    elif target_column in division_column and division_column == temp_division[-1]:
                        """2048/16/8/4/2 = 2  --> a/b/c/d/e = 2"""
                        # value *= plus_or_minus
                        if "*" in division_column:
                            temp_multiplication = division_column.split("*")
                            for i in range(0, len(temp_multiplication)):
                                if temp_multiplication[i] == target_column:
                                    continue
                                else:
                                    value /= values[temp_multiplication[i]]
                            print("Out0:", str(value))
                            return
                        else:
                            print("Out1:", str(value * value_left))
                            return
                    else:
                        # 此场景不可能出现目标字段
                        if "*" in division_column:
                            temp_multiplication = division_column.split("/")
                            if isinstance(value_left, str):
                                value_left = values[temp_multiplication[0]]
                            else:
                                value_left /= values[temp_multiplication[0]]
                            for i in range(1, len(temp_multiplication)):
                                value_left /= values[temp_multiplication[i]]
                        else:
                            if isinstance(value_left, str):
                                value_left = values[division_column]
                            else:
                                value_left /= values[division_column]
            else:
                if each == target_column and each != columns_info[-1]:
                    columns_info.remove(target_column)
                    columns_info.insert(-1, target_column)
                    columns_info.insert(0, 0)
                    continue
                elif each == target_column and each == columns_info[-1]:
                    print("Out3:", str(value))
                else:
                    value_left = values[each]
            value += value_left * plus_or_minus
        print("Out3:", str(value))


if __name__ == "__main__":
    values = dict()
    table_columns = validate_the_input()

    print(table_columns)
    print(values)
    cal(deal_opetator(table_columns))