# -*- coding: utf-8 -*-
__author__ = "chenk"

from rediscluster import StrictRedisCluster
import sys

def redis_cluster():
    redis_nodes =  [{'host': '10.20.18.170', 'port': 6380},
                    {'host': '10.20.18.170', 'port': 6381},
                    {'host': '10.20.18.170', 'port': 6382},
                    {'host': '10.20.18.170', 'port': 6383},
                    {'host': '10.20.18.170', 'port': 6384},
                    {'host': '10.20.18.170', 'port': 6385}
                   ]
    redis_nodes =  [{'host': '10.20.37.224', 'port': 7111},
                    {'host': '10.20.37.224', 'port': 7112},
                    {'host': '10.20.37.225', 'port': 7113},
                    {'host': '10.20.37.225', 'port': 7114},
                    {'host': '10.20.37.226', 'port': 7115},
                    {'host': '10.20.37.226', 'port': 7116}
                   ]
    try:
        # redisconn = StrictRedisCluster(startup_nodes=redis_nodes, password="abc")
        redisconn = StrictRedisCluster(startup_nodes=redis_nodes, password="")
    except Exception as e:
        print("Connect Error!")
        print(str(e))
        sys.exit(1)

    return redisconn
    # redisconn.set('name','admin')
    # redisconn.set('age',18)
    # print("name is: ", redisconn.get('name'))
    # print("age  is: ", redisconn.get('age'))

redis = redis_cluster()
# fund_account_list = [30003590,30003592,30003593,30003594,30003595,30003596,30003598,30003599]
# # fund_account_list = [30,2,12,10]
#
# i = 1
# value = ""
# is_break = 0
# max_fund_account = sorted(fund_account_list,reverse=True)[0]
# while max_fund_account:
#     for fund_account in fund_account_list:
#         if fund_account == i:
#             value += "1"
#             is_break = 1
#             break
#     if is_break == 0:
#         value += "0"
#
#     i += 1
#     is_break = 0
#     max_fund_account -= 1

# redis.set("{ifs.management.base.service.redisclusterservice.bitmap}.auth.18511",value)
redis.set("{foo", "foo")
print(redis.get("foo"))
print("Done")