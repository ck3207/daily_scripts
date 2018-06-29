import re
import random

def validate_the_input(entry="A1.COL1 + A2.COL2 * A3.COL1= A3.COL3"):
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

def cal(columns_info):
    value = 0
    for each in columns_info:
        if each == "+":
            pass

        if each in ["+", "-", "*", "/", "="]:
            print(each)

def demo(columns_info):
    for each in columns_info:
        if each not in ["+", "-", "*", "/", "="]:
            value = values[each]
        elif each == "+":
            pass

values = dict()
table_columns = validate_the_input()
print(table_columns)
print(values)
# cal(table_columns)