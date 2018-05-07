# -*- coding: utf-8 -*-
__author__ = "chenk"
from connect_to_mysql import Connect_mysql
import json

class Transfer_Data:
    """从A数据库筛选特定数据插入至指定数据库B中"""
    def __init__(self, size=2000):
        """Connect to mysql.
        table_dict is a dict. For example:
        {"table":{"smart_stock_search":{"hasWhere":True,"cols":{"CreateTime":">='2018-04-01' \
        and CreateTime<='2018-04-11'"},"orderby":"CreateTime asc", "limit":"100"}}}"""
        self.size = size
        self.table_dic = self.get_config()
        connect_mysql = Connect_mysql()
        mysql_config = connect_mysql.get_config("mysql_config.json")
        self.conn_from, self.cur_from = connect_mysql.conn_mysql(host=mysql_config["small_tools_ifs8"]["host"],
                                             port=mysql_config["small_tools_ifs8"]["port"],
                                             user=mysql_config["small_tools_ifs8"]["user"],
                                             password=mysql_config["small_tools_ifs8"]["password"],
                                             database=mysql_config["small_tools_ifs8"]["database"],
                                             charset=mysql_config["small_tools_ifs8"]["charset"])

        self.conn_target, self.cur_target = connect_mysql.conn_mysql(host=mysql_config["localhost_cf_test"]["host"],
                                             port=mysql_config["localhost_cf_test"]["port"],
                                             user=mysql_config["localhost_cf_test"]["user"],
                                             password=mysql_config["localhost_cf_test"]["password"],
                                             database=mysql_config["localhost_cf_test"]["database"],
                                             charset=mysql_config["localhost_cf_test"]["charset"])

    def get_sql_of_drop_and_create_table(self,table):
        """Get the sql of drop table and create table."""
        sql = """show create table {0}""".format(table)
        self.cur_from.execute(sql)
        create_table = self.cur_from.fetchone()
        sql = "drop table if EXISTS {0};\n".format(table) + create_table[1]

        return sql

    def query_data(self, table, table_info):
        """Query from database."""
        where_condition = ""
        if table_info.get("hasWhere") == "true":
            where_condition = "where "
            if table_info.get("cols"):
                for key,value in table_info["cols"].items():
                    where_condition += key+value+" and "
                where_condition = where_condition[:-4]
        if table_info.get("orderby"):
            where_condition += " order by " + table_info.get("orderby")
        if table_info.get("limit"):
            where_condition += " limit " + table_info.get("limit")
        condition = where_condition
        query_sql = """select * from {0} {1} ;""".format(table, condition)
        create_table = self.get_sql_of_drop_and_create_table(table)
        insert_sql = "insert into {0} values ".format(table)

        return create_table,query_sql,insert_sql

    def insert_data(self):
        """Insert Data which query from database to the target database"""
        # insert_sql
        for table,table_info in self.table_dic.items():
            if table_info["isPass"] == True:
                continue
            create_sql, query_sql,insert_sql = self.query_data(table,table_info)
            self.cur_target.execute(create_sql)
            self.cur_from.execute(query_sql)
            while True:
                data = self.cur_from.fetchmany(self.size)
                if data == ():
                    break
                temp_sql = ""
                # if table == "smart_stock_info":
                #     pass
                for each_value in data:
                    temp_sql = "{0}(".format(temp_sql)
                    for each_col in each_value:
                        # 如果查询表字段为NULL，查询返回为None,需处理成NULL
                        if each_col == None:
                            temp_sql = "{0}NULL,".format(temp_sql)
                        else:
                            temp_sql = "{0}'{1}',".format(temp_sql,each_col)
                    temp_sql = "{0}),".format(temp_sql[:-1])
                sql = insert_sql + temp_sql[:-1] + ";commit;"

                 # execute_sql
                print("Dealing table:{0}".format(table))
                self.query_data_to_insert_data(sql)

        self.__end()

    def query_data_to_insert_data(self,insert_sql):
        """Execute SQL."""
        try:
            self.cur_target.execute(insert_sql)
            self.conn_target.commit()
        except Exception as e:
            print(str(e))
            print("Insert Data SQL:", insert_sql)

    def __end(self):
        """Close Connection!"""
        self.cur_from.close()
        self.cur_target.close()
        self.conn_from.close()
        self.conn_target.close()

    def get_config(self, file_name="config.json"):
        """Get Configuration!"""
        with open(file_name, "r", encoding="utf-8") as f:
            config = json.load(f)
        return config

if __name__ == "__main__":
    transfer = Transfer_Data(size=3)
    transfer.insert_data()
