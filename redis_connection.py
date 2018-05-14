# -*- coding: utf-8 -*-
__author__ = "chenk"

import redis
from rediscluster import StrictRedisCluster
import sys

class Connect_Reids:
    def __init__(self,nodes=[{"host":"127.0.0.1","port":6379}],password=None,db=None):
        """redis连接初始化配置：
        nodes = [{'host':'10.20.18.xxx','port':6380},
                        {'host':'10.20.xxx.xxx','port':6381},
                        {'host':'10.20.xxx.xxx','port':6382},
                        {'host':'10.20.xxx.xxx','port':6383},
                        {'host':'10.20.xxx.xxx','port':6384},
                        {'host':'10.20.xxx.xxx','port':6385}
                       ]
        """
        self.redis_nodes = nodes
        self.redis_password = password
        self.db = db

    def redis_cluster(self):
        """reids 集群连接"""
        try:
            redis_conn = StrictRedisCluster(startup_nodes=self.redis_nodes,password=self.redis_password)
        except Exception as e:
            print("Connect Reids_Cluster Error!")
            print(str(e))
            sys.exit(1)

        return redis_conn

    def redis_single(self,redis_node):
        """redis 单点连接"""
        try:
            redis_conn = redis.Redis(host=redis_node["host"], port=redis_node["port"], \
                                     db=redis_node["db"], password=redis_node["password"])
        except Exception as e:
            print("Connect Reids_Single Error")
            print(str(e))
            sys.exit(1)

        return redis_conn

    def connect_redis(self):
        """根据配置连接redis单点/reids集群"""
        if len(self.redis_nodes) == 1:
            return self.redis_single(self.redis_nodes[0])
        else:
            return self.redis_cluster()

    # redisconn.set('name','admin')
    # redisconn.set('age',18)
    # print("name is: ", redisconn.get('name'))
    # print("age  is: ", redisconn.get('age'))


nodes = [{'host':'10.20.18.xxx','port':6380},
                {'host':'10.20.18.xxx','port':6381},
                {'host':'10.20.18.xxx','port':6382},
                {'host':'10.20.18.xxx','port':6383},
                {'host':'10.20.18.xxx','port':6384},
                {'host':'10.20.18.xxx','port':6385}
           ]

connect_redis = Connect_Reids(nodes=nodes,password="abc")
r = connect_redis.connect_redis()
fund_account_list = [30003590,30003592,30003593,30003594,30003595,30003596,30003598,30003599]
# fund_account_list = [30,2,12,10]

i = 1
value = ""
is_break = 0
max_fund_account = sorted(fund_account_list,reverse=True)[0]
while max_fund_account:
    for fund_account in fund_account_list:
        if fund_account == i:
            value += "1"
            is_break = 1
            break
    if is_break == 0:
        value += "0"

    i += 1
    is_break = 0
    max_fund_account -= 1

r.set("{ifs.management.base.service.redisclusterservice.bitmap}.auth.18511",value)
print("Done")