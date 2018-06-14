# -*- coding: utf-8 -*-
__author__ = "chenk"
import re
import pymysql

from tkinter import *

class Connect_to_sql:
    def __init__(self):
        url = e1.get()
        self.host = re.search("//(.+?):", url).group(1)
        try:
            self.port = int(re.search(":(\d+)", url).group(1))
        except AttributeError:
            self.port = 80
        self.charset = re.search("charset=(.+)", url).group(1).replace("-","")
        self.database = re.search(":\d*/(.+?)\?", url[8:]).group(1)
        self.username = e2.get()
        self.password = e3.get()

    def connect_db(self,db_type="mysql"):
        self.disconnect()
        # print(v.get())
        global conn,cur
        if DB_TYPE[v.get()] == "mysql":
            try:
                conn = pymysql.connect(host=self.host,port=self.port,user=self.username,\
                                                    password=self.password,database=self.database,charset=self.charset)
                cur = conn.cursor()
                print("Connect to mysql successfully!")
                
                self.get_all_tables()
            except Exception as e:
                print("Connect to mysql Error!")
                print(str(e))
        elif DB_TYPE[v.get()] == "oracle":
            pass
        return conn, cur

    def disconnect(self, flag=False):
        if conn !=0 and cur != 0:
            cur.close()
            conn.close()
            print("Connection break!")
        if flag == True:
            master.destroy()

    def get_all_tables(self):
        cur.execute("show tables")
        v = IntVar()
        table_name = StringVar()
        table_num = 0
        columnspan = 3
        for table in cur.fetchall():
            table_name = table
            row = table_num // 3
            column = table_num % 3
            Checkbutton(master, text=table_name, padx=10,pady=5)\
                .grid(row=row+5, column=column*columnspan, columnspan=columnspan, sticky=W)
            table_num += 1

    def get_value(self):
        print(v.get())
        return v.get()

master = Tk()
# master.minsize(800,300)
# master.maxsize(800,800)
master.title("数据生成工具")
Label(master, padx=10, pady=5, text="数据库地址：").grid(row=0,sticky=W)
Label(master, padx=10, pady=5, text="用  户  名:").grid(row=1,sticky=W)
Label(master, padx=10, pady=5, text="密      码:").grid(row=2,sticky=W)

e1 = Entry(master, width=80)
e2 = Entry(master, width=80)
e3 = Entry(master, width=80, show="*")

# Typesetting
e1.grid(row=0,column=1,columnspan=8,padx=10,pady=5,sticky=W)
e2.grid(row=1,column=1,columnspan=8,padx=10,pady=5,sticky=W)
e3.grid(row=2,column=1,columnspan=8,padx=10,pady=5,sticky=W)

# example
e1.insert(0,"http://127.0.0.1:3306/cf_test?charset=utf-8")
e2.insert(0,"root")
e3.insert(0,"123456")

connect_to_sql = Connect_to_sql()
conn,cur = 0,0

v = IntVar()
DB_TYPE = {0:"mysql", 1:"oracle"}
for key,value in DB_TYPE.items():
    Radiobutton(master, text=value,variable=v,value=key).grid(row=3,column=key,sticky=W)

b3 = Button(master, text="OK", command=lambda:connect_to_sql.connect_db("mysql"), width=10, height=5)\
    .grid(row=0,column=9,rowspan=3,sticky=W,padx=10,pady=5)
b4 = Button(master, text="QUIT", command=lambda :connect_to_sql.disconnect(flag=True), width=10)\
    .grid(row=3,column=9,sticky=W,padx=10,pady=5)

Label(master,text="配置表关系", font=("宋体",16)).grid(row=4, column=0, columnspan=2, sticky=W,padx=10,pady=5)

mainloop()