# -*- coding: utf-8 -*-
__author__ = "chenk"

a_list = [1,22,33,11,21,22,100]
a_set = {1,22,33,11,21,24,100}
a_tuple = (1,22,33,11,21,24,100)
b = {"a":"A","g":"G","c":"C","v":"V","d":"V"}
c = [(97,"a"),(97,"y"),(97,"i"),(97,"b"),(97,"w"),(10,"10"),(100,"100")]

print(sorted(a_list))
print(sorted(a_set))
print(sorted(a_tuple))
print(sorted(b.items(),key=lambda kv:kv[0], reverse=False))
print(sorted(b.items(),key=lambda kv:kv[0], reverse=True))
print(sorted(b.items(),key=lambda kv:kv[1], reverse=False))
print(sorted(b.items(),key=lambda kv:(kv[1],kv[0]), reverse=False))
print(sorted(c,key=lambda l:l[0], reverse=False))
print(sorted(c,key=lambda l:(l[0],l[1]), reverse=False))

x = 10.123456789
print(int(2*x)/2+int(2*x)%2)
def round_off(num, decimals_length):
    temp_1 = num * 10 ** (decimals_length + 1) / 10
    temp_2 = num * 10 ** (decimals_length + 1) % 10
    if temp_2 >= 5:
        return temp_1
