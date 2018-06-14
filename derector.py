#coding:utf-8
import time
import logging

def elapse_time(func):
    def wrapper(*args):
        start = time.time()
        func(*args)
        end = time.time()
        print("elapse_time:", end-start)
    return wrapper

def insert_log(is_print=False):
    def deractor(func):
        def wrapper(*args):
            if is_print:
                print("Function {0} is running".format(func.__name__))
                logging.info("Function {0} is running".format(func.__name__))
            return func(*args)
        return wrapper
    return deractor

@elapse_time
def func_1(time_sleep,range_num):
    time.sleep(time_sleep)
    for i in range(range_num):
        if i < range_num:
            continue
    return 1


@insert_log(is_print=True)
@elapse_time
def func():
    print("I am func")

logging.basicConfig(filename="demo1.log",filemode="a",level="DEBUG")
func()

# func_1(1,200000)
# func_2()
# func_3()