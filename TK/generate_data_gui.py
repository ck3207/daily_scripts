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
        # print(v)
        global conn,cur
        if db_type == "mysql":
            try:
                conn = pymysql.connect(host=self.host,port=self.port,user=self.username,\
                                                    password=self.password,database=self.database,charset=self.charset)
                cur = conn.cursor()
                print("Connect to mysql successfully!")
                self.get_all_tables()
            except Exception as e:
                print("Connect to mysql Error!")
                print(str(e))
        self.get_all_tables()
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
            Checkbutton(master, text=table_name, width=10*columnspan, anchor=W, padx=10,pady=5)\
                .grid(row=row+5, column=column*columnspan, columnspan=columnspan)
            table_num += 1

master = Tk()
master.minsize(800,300)
master.maxsize(800,800)
master.title("数据生成工具")
# frame = Frame(master,width=100,height=30)
Label(master, padx=10, pady=5, text="数据库地址：", width=10).grid(row=0,sticky=W)
Label(master, padx=10, pady=5, text="用  户  名:", width=10).grid(row=1,sticky=W)
Label(master, padx=10, pady=5, text="密      码:", width=10).grid(row=2,sticky=W)

e1 = Entry(master,width=80)
e2 = Entry(master,width=80)
e3 = Entry(master,width=80,show="*")

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
DB_TYPE = [("mysql",0), ("oracle",1)]
for db,num in DB_TYPE:
    Radiobutton(master, text=db,variable=v,value=num,width=10).grid(row=3,column=num,sticky=W)
    print(v)

b3 = Button(master, text="OK", command=lambda:connect_to_sql.connect_db("mysql"), height=5, width=10)\
    .grid(row=0,column=8,rowspan=3,columnspan=1,sticky=W,padx=10,pady=5)
b4 = Button(master, text="QUIT", command=lambda :connect_to_sql.disconnect(flag=True),width=10,padx=10,pady=5)\
    .grid(row=3,column=8,sticky=W)

Label(master,text="选择表",width=20, font=("宋体",18)).grid(row=4, column=2, columnspan=2)

mainloop()