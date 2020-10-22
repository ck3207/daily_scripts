import datetime
import time
import random

class IntervalDate:
    """获取两个随机的日期， begin_date，end_date 提供给账户分析自定义区间接口使用"""
    def __init__(self):
        self.current_date = time.strftime("%Y%m%d", time.localtime())

    def get_random_num(self, small_num, big_num):
        """返回一个基于small_num与big_num的整数"""
        if isinstance(small_num, int) and isinstance(big_num, int):
            return random.randint(small_num, big_num)
        return "Argue small_num and big_num should be integer."

    def get_date(self, init_date="", date_diff=0):
        """产生一个随机日期， 该日期为区间结束日期end_date"""
        if init_date == "":
            init_date = self.current_date
        if date_diff == 0:
            date_diff = self.get_random_num(-100, 0)

        if len(init_date) == 8:
            year = int(init_date[:4])
            month = int(init_date[4:6])
            day = int(init_date[6:])
            target_date = (datetime.date(year, month, day) + datetime.timedelta(days=date_diff)).strftime("%Y%m%d")
        else:
            return "init_date must be format yyyyMMdd"
        return target_date

    def get_interval_date(self, init_date="", date_diff=0):
        """返回一组日期， 开始日期begin_date, 结束日期end_date, 两个日期相差时间大于等于7天；"""
        if init_date == "":
            init_date = self.current_date
        begin_date, end_date = "", ""
        end_date = self.get_date()
        begin_date = self.get_date(init_date=begin_date, date_diff=random.randint(-200, -7))

        return begin_date, end_date

    def generate_hundreds_of_date(self, date_num):
        if date_num > 0 and isinstance(date_num, int):
            with open(file="interval_date.txt", mode="w", encoding="utf-8") as f:
                while date_num:
                    begin_date, end_date = self.get_interval_date()
                    f.write(begin_date + "," + end_date + "\n")
                    date_num -= 1
        else:
            return "Argue date_num must be integer."
        return


if __name__ == "__main__":
    interval_date = IntervalDate()
    interval_date.generate_hundreds_of_date(date_num=100)
