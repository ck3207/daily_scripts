# -*- coding: utf-8 -*-
__author__ = "chenk"

import os,sys
from os.path import join, getsize


def humanble_size(size):
    """For Readding Easy!"""
    if size > 1024: # Kb
        size /= 1024
        if size > 1024:  # Mb
            size /= 1024
            if size > 1024: # Gb
                size /= 1024
                return str(round(size,2))+"Gb"
            else:
                return str(round(size,2)) + "Mb"
        else:
            return str(round(size,2))+"Kb"

    else:
        return str(round(size,2))+"bytes"

def rank(rank_list,size,length=3):
    """Return rank_list and size,if size is False then rank_list is not updated, 
    others are updated. Size will be returned which was removed."""
    is_update = False
    if length < 3:
        length = 3
    if not len(rank_list):
        for i in range(length):
            rank_list.append(i)

    for i in range(length):
        each = rank_list[length-1-i]
        if size >= each:
            continue
        # 排除入参size是最小的情况
        elif each != rank_list[-1]:
            rank_list.insert(rank_list.index(each)+1,size)
            size = rank_list.pop(-1)
            return rank_list,size
        # 处理入参size是最小的情况
        else:
            return rank_list,is_update

    # 处理入参size是最大的情况
    rank_list.insert(0,size)
    size = rank_list.pop(-1)
    return rank_list,size

if __name__ == "__main__":
    try:
        path = sys.argv[1]
        top_N = sys.argv[2]
    except:
        path = os.getcwd()
        path = "D:\\"
        top_N = 10

    exclusive_dir = ["iSeeRobotAdvisor","LightInvesting2","VM INSTALL","VIPSTU"]
    rank_list = list()
    rank_dic = dict()

    # topdown=True 则可更改dirnames列表(删除或者分割列表)，walk方法紧会递归进入仍在dirnames列表中的目录；
    # topdown=False 则无论对dirnames列表如何处理，递归子目录会重新生成，不会改变
    for dirpath, dirnames, filenames in os.walk(top=path,topdown=True):
        for each in exclusive_dir:
            if each in dirnames:
                dirnames.remove(each)
        for name in filenames:
            file = join(dirpath,name)   # 合并成绝对路径
            try:
                size = getsize(file)    # 获取文件大小（单位：byte 字节）
            except:
                continue
            rank_list,removed_size = rank(rank_list=rank_list,size=size,length=int(top_N))
            if removed_size:
                try:
                    rank_dic[size] = file
                    rank_dic.pop(removed_size)
                except:
                    pass

    # 按照字典的key 进行排序
    for key,value in sorted(rank_dic.items(),key=lambda d:d[0],reverse=True):
<<<<<<< HEAD
<<<<<<< HEAD
<<<<<<< HEAD
        print(value, humanble_size(key))
=======
        print(value.replace("//","\\"), humanble_size(key))
>>>>>>> bf1d6521452718089e453e51f4e7909361dbab89
=======
        print(value.replace("//","\\"), humanble_size(key))
>>>>>>> bf1d6521452718089e453e51f4e7909361dbab89
=======
        print(value.replace("//","\\"), humanble_size(key))
>>>>>>> b0fdffd83922f86a16c764544f27038b0bffc487

# More details you can Browse Blog
# http://blog.csdn.net/ck3207/article/details/79392505