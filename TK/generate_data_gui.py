# -*- coding: utf-8 -*-
__author__ = "chenk"
import re
import pymysql
from tkinter import *

import cx_Oracle

class Connect_to_sql:
    def __init__(self):
        self.host = ""
        self.port = ""
        self.username = ""
        self.database = ""
        self.charset = ""
        self.tables = list()

    def get_url(self):
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
        self.get_url()
        global conn,cur
        if DB_TYPE[v.get()] == "mysql":
            try:
                conn = pymysql.connect(host=self.host,port=self.port,user=self.username,\
                                                    password=self.password,database=self.database,charset=self.charset)
                cur = conn.cursor()
                print("Connect to mysql successfully!")
            except Exception as e:
                print("Connect to mysql Error!")
                print(str(e))
        elif DB_TYPE[v.get()] == "oracle":
            """username/password@host:port/database"""
            try:
                url = "{0}/{1}@{2}:{3}/{4}".format(self.username,self.password,self.host,self.port,self.database)
                # print(url)
                conn = cx_Oracle.connect(url)
                cur = conn.cursor()
                print("Connect to oracle successfully!")
            except Exception as e:
                print("Connect to mysql Error!")
                print(str(e))

        self.get_all_tables(db_type=DB_TYPE[v.get()])

        return conn, cur

    def disconnect(self, flag=False):
        if conn !=0 and cur != 0:
            cur.close()
            conn.close()
            print("Connection break!")
        if flag == True:
            master.destroy()

    def get_all_tables(self, db_type):
        if db_type == "mysql":
            sql = "show tables"
        elif db_type == "oracle":
            sql = "select table_name from user_tables"
        cur.execute(sql)
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
            self.tables.append(table[0])

    def get_value(self):
        print(v.get())
        return v.get()

class Display:
    def __init__(self):
        master.state("zoomed")
        Label(master,text="hello")

    def get_configure_page(self):
        top = Toplevel(master,relief=SUNKEN)
        top.title("数据库配置")
        top.geometry("500x400")
        top.grid()
        self.center_window(top, 500, 400)
        Button(top,text="选择配置", command=lambda:self.get_db_configure(top),pady=10).grid()
        # Label(master, text="数据库配置", padx=10, pady=5, width=10, height=5, font="宋体,18")\
        #     .grid(row=0,rowspan=2,column=0,columnspan=2)
        # Button(master, text="选择配置", padx=10, pady=5, font="宋体,18", \
        #        width=10,height=5, command=self.get_db_configure,bg="grey").grid(row=2,column=2)

    def table_select_page(self):
        """"""
        Label(master,text="数据库配置", padx=10,pady=5,font="宋体,18", width=100,height=60)

    def get_logic_configure_page(self):
        pass

    def get_db_configure(self,master):
        l = Listbox(master,setgrid=False,selectmode=BROWSE)
        for item in ["a","b","c"]:
            l.insert(END,item)
            l.grid()

    def center_window(self,master,w, h):
        # 获取屏幕 宽、高
        ws = master.winfo_screenwidth()
        hs = master.winfo_screenheight()
        # 计算 x, y 位置
        x = (ws / 2) - (w / 2)
        y = (hs / 2) - (h / 2)
        master.geometry('%dx%d+%d+%d' % (w, h, x, y))

master = Tk()
# master.minsize(800,300)
# master.maxsize(1366,768)
master.title("数据生成工具")
display = Display()
display.get_configure_page()

# master.state("zoomed")
# Label(master, padx=10, pady=5, text="数据库地址：").grid(row=0,sticky=W)
# Label(master, padx=10, pady=5, text="用  户  名:").grid(row=1,sticky=W)
# Label(master, padx=10, pady=5, text="密      码:").grid(row=2,sticky=W)
#
# e1 = Entry(master, width=80)
# e2 = Entry(master, width=80)
# e3 = Entry(master, width=80, show="*")
#
# # Typesetting
# e1.grid(row=0,column=1,columnspan=8,padx=10,pady=5,sticky=W)
# e2.grid(row=1,column=1,columnspan=8,padx=10,pady=5,sticky=W)
# e3.grid(row=2,column=1,columnspan=8,padx=10,pady=5,sticky=W)
#
# # example
# e1.insert(0,"http://127.0.0.1:3306/cf_test?charset=utf-8")
# e2.insert(0,"root")
# e3.insert(0,"123456")
# Label(master, width=150, height=35).grid(row=3,rowspan=30,column=0,columnspan=30)
#
# connect_to_sql = Connect_to_sql()
# conn,cur = 0,0
#
# v = IntVar()
# DB_TYPE = {0:"mysql", 1:"oracle"}
# for key,value in DB_TYPE.items():
#     Radiobutton(master, text=value,variable=v,value=key).grid(row=3,column=key,sticky=W)
#
# b3 = Button(master, text="OK", command=lambda:connect_to_sql.connect_db("mysql"), width=10, height=5)\
#     .grid(row=0,column=9,rowspan=3,sticky=W,padx=10,pady=5)
# b4 = Button(master, text="QUIT", command=lambda :connect_to_sql.disconnect(flag=True), width=10)\
#     .grid(row=3,column=9,sticky=W,padx=10,pady=5)
#
# Label(master,text="配置表关系", font=("宋体",16)).grid(row=4, column=0, columnspan=2, sticky=W,padx=10,pady=5)

mainloop()