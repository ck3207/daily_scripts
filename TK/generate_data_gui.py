# -*- coding: utf-8 -*-
__author__ = "chenk"
import re
from tkinter import *
from tkinter import ttk
from tkinter import messagebox
import json
import  generate_data

import cx_Oracle
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

    def connect_db(self,conn_name, top):
        # self.disconnect()
        self.host = f_json[conn_name]["host"]
        self.port = f_json[conn_name]["port"]
        self.username = f_json[conn_name]["user"]
        self.password = f_json[conn_name]["password"]
        self.database = f_json[conn_name]["database"]
        self.charset = f_json[conn_name]["charset"]
        db_type = f_json[conn_name]["db_type"]
        global conn, cur
        if db_type == "mysql":
            try:
                conn = pymysql.connect(host=self.host, port=self.port, user=self.username,\
                                                    password=self.password, database=self.database, charset=self.charset)
                cur = conn.cursor()
                print("Connect to mysql successfully!")
            except Exception as e:
                messagebox.showerror(title="数据库连接错误", message=str(e), parent=top, icon="error")
                return

        elif db_type == "oracle":
            """username/password@host:port/database"""
            try:
                url = "{0}/{1}@{2}:{3}/{4}".format(self.username, self.password, self.host, self.port, self.database)
                # print(url)
                conn = cx_Oracle.connect(url)
                cur = conn.cursor()
                print("Connect to oracle successfully!")
            except Exception as e:
                messagebox.showerror(title="数据库连接错误", message=str(e), parent=top, icon="error")
                return

        return self.get_all_tables(db_type=db_type)

    def disconnect(self):
        """Disconnect database and release resource. If flag is true, the program will be shutdown. """
        cur.close()
        conn.close()
        master.destroy()

    def get_all_tables(self, db_type):
        """This Function will return the tables in the current database. Now its only positive to Mysql and Oralce."""
        if db_type == "mysql":
            sql = "show tables"
        elif db_type == "oracle":
            sql = "select table_name from user_tables"
        cur.execute(sql)
        for table in cur.fetchall():
            self.tables.append(table[0])
        return self.tables

class Display:
    def __init__(self):
        # 获取屏幕 宽、高
        self.ws = master.winfo_screenwidth()
        self.hs = master.winfo_screenheight()
        self.hs -= 50
        master.maxsize(self.ws,self.hs) # 设置最大屏幕尺寸
        master.protocol("WM_DELETE_WINDOW", connect_to_sql.disconnect)    # 点击关闭按钮，退出程序
        # master.minsize(self.ws,self.hs)
        master.resizable(0, 0)
        master.state("zoomed")  # 窗口最大化
        self.examples = ["例如：A.col1 + A.col2 = A.col3", "例如：A.col1 + B.col2 = A.col3"]
        self.logic_set_row_left = 0 # 逻辑规则
        self.logic_set_row_right = 0    # 常量设置
        self.entry = ""
        self.checked_tables = list()    # 选中表
        self.all_tables = list()
        self.vs = list()    # Checkbutton
        self.svs = list()   # Entry

    def get_configure_page(self):
        top = Toplevel(master, relief=SUNKEN)
        top.title("数据库配置")
        top.protocol("WM_DELETE_WINDOW", master.quit)   # 点击右上角关闭按钮，即退出程序
        # new window on the top layer
        top.resizable(0,0)  # 大小不可变
        top.attributes("-toolwindow", 1)
        top.wm_attributes("-topmost", 1)
        top.grid()
        self.center_window(top, 500, 400)
        b = Button(top, text="选择配置", command=lambda: self.get_db_configure(top, b))
        b.grid(padx=200, pady=5, ipadx=20,ipady=20)

    def table_select_page(self, top, conn_name):
        """"""
        self.all_tables = connect_to_sql.connect_db(conn_name=conn_name, top=top)
        if self.all_tables:
            top.withdraw()
        # 粗略估计 最大行数、列数
        rows = self.hs // 45
        columns = self.ws // 250
        # 分页处理
        pages = len(self.all_tables) // (rows*columns)
        if len(self.all_tables) % (rows*columns) == 0:
            pass
        else:
            pages += 1

        tab_control = ttk.Notebook(master)
        for page in range(pages):
            tab = ttk.Frame(tab_control)  # Add a tab
            tab_control.add(tab, text='第{0}页'.format(str(page)))  # Make second tab visible
            tab_control.grid(row=0, column=0, padx=10, pady=5, ipadx=10, ipady=5)
            table_num = 0
            page += 1
            # 仅获取当前页需展示的表
            for table in self.all_tables[(page-1)*rows*columns:page*rows*columns]:
                """
                设置一个IntVar 并把该对象存放在self.vs列表中，在选择完毕后，
                轮循self.vs表中的对象，获取其值来判断是否被选中
                """
                vv = IntVar()
                row = table_num % rows
                column = table_num // rows
                t = ttk.Checkbutton(tab, width=25, text=table, variable=vv, onvalue=1, offvalue=0)
                self.vs.append({table: vv})
                t.grid(padx=20, pady=5, row=row, column=column, sticky=W)
                table_num += 1

        next = Button(master,text="下一步",command=lambda: self.set_logic_configure_page(tab_control, next))
        next.grid(padx=20, pady=20, ipadx=20, ipady=20, row=rows+1)

    def get_select_tables(self):
        for cb in self.vs:
            for key,value in cb.items():
                value = value.get()
                if value == 1:
                    print(key, value)
                    self.checked_tables.append(key)
        return

    def set_logic_configure_page(self, tab, b):
        frame = Frame(master)
        frame.grid()
        self.get_select_tables()
        tab.destroy()
        b.destroy()
        Button(frame, text="+", command=lambda: self.add_logic_entry(frame, flag=True), width=5)\
            .grid(row=self.logic_set_row_left,column=0, padx=10, pady=10, ipadx=10, ipady=10, sticky=E)
        Label(frame, text="逻辑规则", width=10)\
            .grid(row=self.logic_set_row_left, column=1, padx=10, pady=10, ipadx=10, ipady=10, sticky=E)
        Button(frame, text="+", command=lambda: self.add_logic_entry(frame, flag=False), width=5)\
            .grid(row=self.logic_set_row_right, column=80, padx=20, pady=10, ipadx=10, ipady=10)
        Label(frame, text="常量设置", width=10)\
            .grid(row=self.logic_set_row_right, column=81, padx=20, pady=10, ipadx=10, ipady=10)
        Button(frame, text="提交", command=lambda: self.get_logic_setting(frame), width=5)\
            .grid(row=self.logic_set_row_left, column=161, padx=10, pady=10, ipadx=10, ipady=10, sticky=E)


    def add_logic_entry(self, frame, flag=False):
        sv = StringVar()
        yview = None
        if not isinstance(self.entry, str):
            print(self.entry.get())

        # 条件个数做了限制
        if (self.logic_set_row_left > self.hs//40 and flag == True) \
                or (self.logic_set_row_right > self.hs//40 and flag == False):
            messagebox.showwarning(title="Warning", \
                                   message="每项规则最多能设置{}个条件".format(int(self.hs//40)), icon="warning")
            return
        if flag:
            self.svs.append(["left", self.logic_set_row_left, sv])
            self.logic_set_row_left += 1
            self.entry = Entry(frame, textvariable=sv, width=80, yscrollcommand=yview)
            self.entry.delete(0, END)
            self.entry.grid(row=self.logic_set_row_left, pady=5, column=0, columnspan=80, padx=20)
        else:
            self.svs.append(["right", self.logic_set_row_right, sv])
            self.logic_set_row_right += 1
            self.entry = Entry(frame, textvariable=sv, width=80, yscrollcommand=yview)
            self.entry.delete(0, END)
            self.entry.grid(row=self.logic_set_row_right, column=80, columnspan=80, pady=5, padx=20)
        self.entry.focus()

    def get_logic_setting(self, frame):
        # frame = Frame(master)
        # frame.grid()
        for each in self.svs:
            print(each[0], each[1], each[2].get())
            flag, error = self.validate_the_input(each[2].get())
            if not flag:
                messagebox.showerror(title="设置错误", message=error, icon="error", parent=frame)

    def validate_the_input(self, entry="A1.COL1 + A2.COL2 = A3.COL3"):
        """Extrat entry ==> A1.COL1||A2.COL2||A3.COL3, then split by || \
        and judge each table.column whethor it is validate or not. """
        operator = ["+", "-", "*", "/", "="]
        entry.strip().replace(" ", "")
        for each in operator:
            entry_temp = ""
            if each in entry:
                for split in entry.split(each):
                    entry_temp += split.strip() + "||"
                entry = entry_temp[:-2]
            operator.remove(each)
        for each in entry.split("||"):
            if each.strip() == "":
                entry.remove(each)
            else:
                try:
                    table = each.split(".")[0]
                    if table not in self.checked_tables:
                        if table not in self.all_tables:
                            return 0, "Table[{0}] is not found!".format(table)
                        else:
                            self.checked_tables.append(table)
                            print(each, " passed!")
                except IndexError:
                    # messagebox.showerror(title="数据库连接错误", message=str(e), parent=top)
                    print("Input is not valid, column should be Tables.Column!")
                    return 0, "Input is not valid, column should be Tables.Column!"
        return 1, None

    def get_db_configure(self, top, Button_obj):
        global f_json
        with open("db_config.json", "r") as f:
            f_json = json.load(f)
        sb = Scrollbar(top)
        sb.grid(row=7, rowspan=20, sticky=E+N+S)
        # 联动设置,当Listbox 视野发生变化时，执行yscrollcommand=sb.set通知到Scrobar
        v = StringVar
        l = Listbox(top, width=67, height=17, selectmode=SINGLE, yscrollcommand=sb.set, listvariable=v)
        l.bind('<Double-Button-1>', func=self.handlerAdaptor(self.handler, lb=l, top=top))
        for name in f_json:
            name = "连接名：{0}, 地址：{1}".format(name,f_json[name]["host"])
            l.insert(END, name)
        l.grid(row=7, rowspan=20, columnspan=10, padx=5, pady=2, sticky=N+S+W)
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
        # 计算 x, y 位置
        x = (self.ws / 2) - (w / 2)
        y = (self.hs / 2) - (h / 2)
        master.geometry('%dx%d+%d+%d' % (w, h, x, y))
        # master.deiconify()

    def warning_message(self):
        pass

class Extract_Columns_Relations:
    def __init__(self):
        pass

    def extract_relations(self):
        pass

if __name__ == "__main__":
    f_json = ""
    conn, cur = 0, 0
    master = Tk()
    master.title("数据生成工具")
    connect_to_sql = Connect_to_sql()
    display = Display()
    display.get_configure_page()

    mainloop()