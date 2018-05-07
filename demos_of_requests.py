# -*- coding: utf-8 -*-
__author__ = "chenk"

import requests,random,json


def add_operators(count = 30,token=""):
    """add operators"""
    f_access_token = open("access_token", "w")
    # f_operator_no = open("operator_no", "a")
    while count:
        operator_no = str(random.randint(100000,999999))
        name = operator_no
        password = "83cf8b609de60036a8277bd0e96135751bbc07eb234256d4b65b893360651bf2"
        telephone = "18200" + operator_no
        remark = "remark" + operator_no
        operator_add = {"operator_no":operator_no,"password":password, "operator_type":"1","branch_no":"1",\
                        "name":name,"telephone":telephone,"remark":remark,"access_token":token}
        r_session.post(url_prefix+"/manage-auth/operatorService/operatorAdd",data=operator_add,headers=headers)
        count -= 1
        f_access_token.write(operator_no + "," + operators_login(operator_no) + "\n")
    return

def operators_login(operator_no="88889"):
    login_argue = {"operator_no":operator_no, "password":"83cf8b609de60036a8277bd0e96135751bbc07eb234256d4b65b893360651bf2",
               "verify_code":"11113"}
    r = r_session.post(url_prefix + "/manage-auth/operatorService/operatorLogin", data=login_argue, headers=headers)
    access_token = r.json()["data"]["accessToken"]
    return access_token

type_dic = {"client_sex":{"0":"男","1":"女","2":"其他"},"age_period":{"0":"青少年","1":"中年","2":"中老年","3":"老年"}}
type_list = ["client_sex","age_period"]

headers = {"Host":"10.20.18.174","Cookie":"JSESSIONID=842C476D302D94366E2DC6A7C2DA3E84",
           "Content-Type":"application/x-www-form-urlencoded"}
url_prefix = "http://10.20.18.174"
r_session = requests.Session()
# add_operators(1000,"0f5808e595d6aeb40d6208209ab0b1819b2e4e6f8fee2a97b447327e64843a40")

access_token = "0f5808e595d6aeb40d6208209ab0b1819b2e4e6f8fee2a97b447327e64843a40"
field = random.choice(type_list)
value = random.randint(0,len(type_dic[field])-1)
desc = type_dic[field][str(value)]
group_name = field + "_" + desc + str(random.randint(100,999))

# add_group_argue = """group_name=aaa&group_condition=%7B%22type_attr%22%3A%5B%7B%22field%22%3A%22age_period%22%2C%22value%22%3A%221%22%2C%22operator%22%3A%224%22%2C%22desc%22%3A%22%E5%AE%A2%E6%88%B7%E5%B9%B4%E9%BE%84%E6%AE%B5%20%3D%E4%B8%AD%E5%B9%B4%22%7D%5D%2C%22type_fit%22%3A%5B%5D%2C%22type_done%22%3A%5B%5D%7D&access_token=dedc55ad1c723f2a28bc0b930494ce2e90964ff93b92cb2a7c243e553e984205"""
add_group_argue = {"group_name":"aaa","access_token":"dedc55ad1c723f2a28bc0b930494ce2e90964ff93b92cb2a7c243e553e984205",
"group_condition":""""{"type_attr":[{"field":"age_period","value":"1","operator":"4","desc":"客户年龄段 =中年"}],"type_fit":[],"type_done":[]}"""}

r = r_session.post(url_prefix+"/ifs-management/custom_user_group_add", data=add_group_argue, headers=headers)
print(r.json())
print("111|"+"\r"+"|111")