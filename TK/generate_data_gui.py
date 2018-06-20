# -*- coding: utf-8 -*-
__author__ = "chenk"
import re
from tkinter import *
import json

# import cx_Oracle
import pymysql


class Connect_to_sql:
    def __init__(self):
        self.host = ""
        self.port = ""
        self.username = ""
        self.password = ""
        self.database = ""
        self.charset = ""
        self.tables = list()

    # def get_url(self):
    #     url = e1.get()
    #     self.host = re.search("//(.+?):", url).group(1)
    #     try:
    #         self.port = int(re.search(":(\d+)", url).group(1))
    #     except AttributeError:
    #         self.port = 80
    #     self.charset = re.search("charset=(.+)", url).group(1).replace("-","")
    #     self.database = re.search(":\d*/(.+?)\?", url[8:]).group(1)
    #     self.username = e2.get()
    #     self.password = e3.get()

    def connect_db(self,conn_name):
        self.disconnect()
        self.host = f_json[conn_name]["host"]
        self.port = f_json[conn_name]["port"]
        self.username = f_json[conn_name]["user"]
        self.password = f_json[conn_name]["password"]
        self.database = f_json[conn_name]["database"]
        self.charset = f_json[conn_name]["charset"]
        db_type = f_json[conn_name]["db_type"]
        global conn,cur
        if db_type == "mysql":
            try:
                conn = pymysql.connect(host=self.host,port=self.port,user=self.username,\
                                                    password=self.password,database=self.database,charset=self.charset)
                cur = conn.cursor()
                print("Connect to mysql successfully!")
            except Exception as e:
                print("Connect to mysql Error!")
                print(str(e))
        elif db_type == "oracle":
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

        return self.get_all_tables(db_type=db_type)

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
        for table in cur.fetchall():
            self.tables.append(table[0])
        return self.tables

    def create_new_page(self):
        top = Toplevel(master)
        top.state("zoomed")
        return top


class Display:
    def __init__(self):
        master.state("zoomed")

    def get_configure_page(self):
        top = Toplevel(master, relief=SUNKEN)
        top.title("数据库配置")
        # new window on the top layer
        top.resizable(0,0)
        top.attributes("-toolwindow", 1)
        top.wm_attributes("-topmost", 1)
        # top.grid()
        self.center_window(top, 500, 400)
        b = Button(top, text="选择配置", command=lambda: self.get_db_configure(top, b))
        b.grid(padx=200, pady=5, ipadx=20,ipady=20)

    def table_select_page(self, top, conn_name):
        """"""
        top.withdraw()
        tables = connect_to_sql.connect_db(conn_name=conn_name)
        v = IntVar()
        v = 0
        table_num = 0
        width = master.winfo_width()
        height = master.winfo_height()
        # print(width, height)
        rows = height // 50
        columns = width // 300
        for table in tables:
            table_name = table
            row = table_num % rows
            column = table_num // rows
            if column > columns:
                pass
                # print(tables[:])
                # Button(master,text="下一页").grid(padx=200, pady=5, ipadx=20, ipady=20, row=rows+1, column=columns)
                # table_num -= row*(columns-1)
                # Checkbutton(master, width=25, text=table_name, variable=v, padx=10, pady=5, anchor=W).\
                #     grid(padx=20, pady=5, row=row, column=column-columns-1, sticky=W)
            else:
                Checkbutton(master, width=25, text=table_name, variable=v, padx=10, pady=5, anchor=W).\
                    grid(padx=20, pady=5, row=row, column=column, sticky=W)

            table_num += 1
            v += 1
        Button(master,text="下一步",command=self.set_logic_configure_page)\
            .grid(padx=200, pady=5, ipadx=20, ipady=20, row=rows+1, column=columns)


    def set_logic_configure_page(self):
        master.children()
        Label(master, text="逻辑规则", anchor=W).grid(padx=20, pady=5, ipadx=20, ipady=20,row=0,column=2, sticky=W)
        Label(master, text="常量设置", anchor=W).grid(padx=20, pady=5, ipadx=20, ipady=20,row=0,column=12, sticky=W)

    def get_db_configure(self, top, Button_obj):
        global f_json
        with open("db_config.json", "r") as f:
            f_json = json.load(f)
        sb = Scrollbar(top)
        sb.grid(row=7, rowspan=20, sticky=E+N+S)
        # 联动设置,当Listbox 视野发生变化时，执行yscrollcommand=sb.set通知到Scrobar
        v = StringVar
        l = Listbox(top, width=67, height=17, selectmode=BROWSE, yscrollcommand=sb.set, listvariable=v)
        l.bind('<Double-Button-1>', func=self.handlerAdaptor(self.handler, lb=l, top=top))
        for name in f_json:
            name = "连接名：{0}, 地址：{1}".format(name,f_json[name]["host"])
            l.insert(END,name)
        l.grid(row=7,rowspan=20, columnspan=10, padx=5, pady=2, sticky=N+S+W)
        # 联动设置,用户操作滚动条时，执行l.yview方法通知Listbox
        sb.config(command=l.yview)
        Button_obj.config(state=DISABLED)

    def handler(self, event, top, lb):
        """事件处理函数"""
        global db_type
        content = lb.get(lb.curselection())
        name = content.split(", 地址")[0][4:]
        # print(name)
        self.table_select_page(top, name)

    def handlerAdaptor(self,fun, **kwds):
        """事件处理函数的适配器，相当于中介，那个event是从那里来的呢，我也纳闷，这也许就是python的伟大之处吧"""
        return lambda event, fun=fun, kwds=kwds: fun(event, **kwds)

    def center_window(self, master, w, h):
        # 获取屏幕 宽、高
        ws = master.winfo_screenwidth()
        hs = master.winfo_screenheight()
        # 计算 x, y 位置
        x = (ws / 2) - (w / 2)
        y = (hs / 2) - (h / 2)
        master.geometry('%dx%d+%d+%d' % (w, h, x, y))
        # master.deiconify()

f_json = ""
conn,cur = 0,0
master = Tk()
master.title("数据生成工具")
connect_to_sql = Connect_to_sql()
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