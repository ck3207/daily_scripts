# -*- coding: utf-8 -*-
__author__ = "chenk"

from connect_to_mysql import Connect_mysql

class Transfer_Data:
    """从A数据库筛选特定数据插入至指定数据库B中"""
    def __init__(self, table_dict=dict()):
        """Connect to mysql"""
        self.table_dic = table_dict
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

    def query_data(self, table_info=dict()):
        """Query from database."""
        where_condition = ""
        for table,info in table_info.items():
            if info.get("hasWhere") == True:
                where_condition = "where "
                if info.get("cols"):
                    for key,value in info["cols"].items():
                        where_condition += key+value+" and "
                    where_condition = where_condition[:-4]
            if info.get("orderby"):
                where_condition += " order by " + info.get("orderby")
            if info.get("limit"):
                where_condition += " limit " + info.get("limit")
        condition = where_condition
        query_sql = """select * from {0} {1} ;""".format(table, condition)
        create_table = self.get_sql_of_drop_and_create_table(table)
        insert_sql = "insert into {0} values ".format(table)
        return create_table,query_sql,insert_sql

    def insert_data(self):
        """Insert Data which query from database to the target database"""
        for value in self.table_dic.values():
            create_sql, query_sql,insert_sql = self.query_data(value)
            self.cur_from.execute(query_sql)
            data = self.cur_from.fetchall()
            for each_value in data:
                insert_sql += "("
                for each_col in each_value:
                    insert_sql += "{0},".format(each_col)
                insert_sql += "{0}),".format(insert_sql[:-1])
            print(insert_sql)

        self.__end()

    def query_data_to_insert_data(self,data):
        """pass"""

    def __end(self):
        """Close Connection!"""
        self.cur_from.close()
        self.cur_target.close()
        self.conn_from.close()
        self.conn_target.close()

about_table = {"table":{"smart_stock_search":{"hasWhere":False,"cols":{"CreateTime":">=2018-04-01","CreateTime":"<=2018-04-11"},"orderby":"CreateTime asc", "limit":"100"}}}

transfer = Transfer_Data(about_table)
transfer.insert_data()

{"table":{"smart_stock_search":{"hasWhere":False,"cols":{"CreateTime":">=2018-04-01","CreateTime":"<=2018-04-11"}}}}