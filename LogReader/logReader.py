# -*- coding: utf-8 -*-
import os
import time

__author__ = "chenk"


class LogReader:
    """日志读取器"""
    def __init__(self, logs):
        self.__logs = logs
        self.__readers = {}

    def get_file_obj(self, file_path):
        """传入文件路径，若文件存在，返回文件读取对象与文件读取位置(默认为0)"""
        if os.path.exists(file_path):
            f = open(file=file_path, mode="r", encoding="utf-8")
            self.__readers[file_path] = f
            self.read_lines_from_tail(file_path)

    def seek_to_end(self, func):
        def wrapper(obj):
            self.__readers[obj] = obj.seek(0, 2)
            func(obj)
        return wrapper

    def read_lines_from_tail(self, file_path, num=20):
        """从尾部开始获取最后N行数据"""
        is_enough = False
        self.__pre_print(file_path)
        while True:
            lines = next(self.read_lines(file_path))
            if len(lines) < num and not is_enough:
                return self.tail_log(lines[-num:])
            else:
                is_enough = True
                temp = lines[:]
                if self.__readers[file_path].seek(0, 1) == self.__readers[file_path].seek(0, 2):
                    if len(lines) < num:
                        lines = temp + lines
                    return self.tail_log(lines[-num:])

    def read_lines(self, file_path, num=1000):
        """读取N行数据，默认读取1000行"""
        lines = []
        while num:
            line = self.__readers[file_path].readline()
            if line == "":
                break
            lines.append(line)
            num -= 1
        yield lines

    def skip_read(self, obj, line_num=20):
        logs = obj.readlines()
        for line in logs[len(logs)-line_num:]:
            print(line, end="")

    def output(self, file_path):
        """从文件流读取数据"""
        seek_value = self.__readers[file_path].seek(0, 1)
        if seek_value == self.__readers[file_path].seek(0, 2):
            return
        else:
            self.__readers[file_path].seek(seek_value, 0)
        self.__pre_print(file_path)
        print(self.__readers[file_path].read())

    def tail_log(self, line_list):
        for line in line_list:
            print(line, end="")

    def __pre_print(self, file_path):
        print("\n"*2, "="*15, file_path, "="*15, "\n")

    def __close(self):
        for value in self.__readers.values():
            value.close()

    def start(self):
        for file_path in self.__logs:
            self.get_file_obj(file_path)
        while True:
            for file_path in self.__readers.keys():
                self.output(file_path)
                time.sleep(0.1)
