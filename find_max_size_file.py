# -*- coding: utf-8 -*-
__author__ = "chenk"

import os,sys
from os.path import join, getsize

try:
    path = sys.argv[1]
    top_N = sys.argv[2]
except:
    path = os.getcwd()
    path = "D:\\"
    top_N = 10

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

exclusive_dir = ["iSeeRobotAdvisor","LightInvesting2","VM INSTALL","VIPSTU"]
rank_list = list()
rank_dic = dict()
for dirpath, dirnames, filenames in os.walk(top=path):
    for each in exclusive_dir:
        if each in dirnames:
            dirnames.remove(each)
    # size = sum([getsize(join(dirpath, name)) for name in filenames])
    for name in filenames:
        file = join(dirpath,name)
        size = getsize(file)
        rank_list,removed_size = rank(rank_list=rank_list,size=size,length=top_N)
        if removed_size:
            try:
                rank_dic[size] = file
                rank_dic.pop(removed_size)
            except:
                pass

for key,value in sorted(rank_dic.items(),key=lambda d:d[0],reverse=True):
    print(value, humanble_size(key))
