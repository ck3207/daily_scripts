# -*- coding: utf-8 -*-
import logging
import time

__author__ = "chenk"


class Pizza(object):
    radius = 422
    @classmethod
    def get_radius(cls):
        return cls.radius


def write_log(count, filename="test.log"):
    logging.basicConfig(level=logging.DEBUG,
                format='%(asctime)s %(filename)s[line:%(lineno)d] %(levelname)s %(message)s',
                datefmt='%a, %d %b %Y %H:%M:%S',
                filename=filename,
                filemode='w')
    num = 1
    while num < count:
        logging.info("Run %d times." % num)
        print("Run %d times." % num)
        num += 1
        time.sleep(1)

class IPorduct:
    """Define a interface of Product."""
    def __init__(self, company_type):
        self.__type = company_type
        self.__product_info = []

    def get_product_list(self):
        print("获取产品列表")

    def get_product_list_xy(self):
        print("获取xy的产品列表")

    def get_product_list_zt(self):
        print("获取zt的产品列表")

    def query_from_db(self, company_type):
        print("从数据库查询产品信息")

    def del_product_info(self):
        print("清空已查询的产品信息")

    product = property(get_product_list, query_from_db, del_product_info, "接口:产品列表")

if __name__ == "__main__":
    product = IPorduct("xy")
    product.product = ""
    product.product
# write_log(1000)
# print(Pizza.get_radius())
# print(Pizza().get_radius())
# print(Pizza.get_radius() is Pizza().get_radius())
# print("="*20)
# print(id(Pizza.get_radius))
# print(id(Pizza().get_radius))
# print(id(Pizza().get_radius))
# print(Pizza.get_radius is Pizza().get_radius)
# print(Pizza.get_radius == Pizza().get_radius)
# print("="*20)
# print(Pizza().get_radius is Pizza().get_radius)
# print(Pizza().get_radius == Pizza().get_radius)
