# -*- coding: utf-8 -*-
__author__ = "chenk"

tax_dic = {1500:3,4500:10,9000:20,35000:25,55000:30,80000:35}
fare_dic = {"health_insurance":65,"social_security":256,"provident_fund":12,"tax_threshold":3500,"other":21}

salary = 12205
max_tax = 45
tax_fare = 0

provident_fund = lambda x:x*fare_dic["provident_fund"]*0.01 if x*fare_dic["provident_fund"]*0.01 < 4654 else 4654
salary_reduce = provident_fund(salary) + fare_dic["social_security"] + fare_dic["health_insurance"] + fare_dic["other"]
salary_temp = salary - salary_reduce - fare_dic["tax_threshold"]
for key,value in sorted(tax_dic.items(), key = lambda x:x[0], reverse=False):
    if salary_temp < key:
        tax_fare += salary_temp*value*0.01
        print("tax_fare:%.2f,salary:%.2f" % (tax_fare, salary-tax_fare-salary_reduce))
        salary_temp = 0
        break
    else:
        tax_fare += key*value*0.01
    salary_temp -= key

if salary_temp > 0:
    tax_fare += salary_temp*max_tax*0.01
    print("tax_fare:%.2f,salary:%.2f" % (tax_fare, salary-tax_fare-salary_reduce))