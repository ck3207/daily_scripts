import pickle
import os
import time

# import numpy as np

class Label_Verify:
    """Some methods point to verify labels of big data."""
    def __init__(self):
        # return the main data and the change ratio
        self.change_ratio = []
        # only return the ratio
        self.change_ratio_only = []
        # data may be abnormal
        self.abnormal_ratio = []
        # data of reading from a file
        self.data = []

    def read_data(self, file_path=os.getcwd(), filename="test.txt"):
        full_path = file_path + os.sep + filename
        with open(full_path, "r") as f:
            while True:
                f_read = f.readline()
                if f_read == "":
                    break
                elif f_read.strip() == "":
                    continue
                else:
                    self.data.append(tuple(f_read.replace("\n", "").split("\t")))

        return self.data

    def cal_change_ratio(self, data):
        """data = [(fund_account, init_date, value),]
        Attention: The value must be the last element. 
        If not, the function will make mistake. """

        for i, info in enumerate(data):
            if i+1 < len(data):
                try:
                    # cal change ratio
                    if not (isinstance(info, list) or isinstance(info, tuple)):
                        change_ratio = (float(data[i+1]) - float(info))/float(info)
                        info = [""]
                    else:
                        change_ratio = (float(data[i+1][-1]) - float(info[-1]))/float(info[-1])
                except ZeroDivisionError:
                    continue

                except Exception as e:
                    print(str(e))
                    continue
                self.change_ratio_only.append(change_ratio)
                # middle data
                piece = []
                for each in info:
                    piece.append(each)
                # only change the last value, and save the other information
                piece.append(change_ratio)
                self.change_ratio.append(tuple(piece))

        return self.change_ratio, self.change_ratio_only

    def get_top_change_ratio(self, top_num=3):
        """Get a certain num data that may be abnormal data."""
        temp_change_ratio = self.change_ratio_only[:]
        for i in range(top_num):
            try:
                top = max(temp_change_ratio)
            except ValueError:
                continue
            self.abnormal_ratio.append(top)
            temp_change_ratio.remove(top)

        return self.abnormal_ratio

    def location_abnormal_data_info(self):
        """From self.abnormal_ratio to find the matched data of  self.change_ratio, 
        then return."""
        # data, may be abnormal
        abnormal_data_info = []
        for ratio in self.abnormal_ratio:
            index = self.change_ratio_only.index(ratio)
            abnormal_data_info.append(self.change_ratio[index])

        return abnormal_data_info

    def dump_to_file(self, data, filename="filename"):
        """Save Data."""
        target_file = open("{0}.pkl".format(filename), "wb")
        pickle.dump(data, target_file)
        target_file.close()
        return

    def load_file(self, filename="filename"):
        """Load Data"""
        target_file = open("{0}.pkl".format(filename), "rb")
        load_data = pickle.load(target_file)
        target_file.close()
        return load_data

    def _print(self):
        print(self.change_ratio_only)
        # for each in self.change_ratio:
            # print(each)
        # print(np.max(self.change_ratio))

    def generate_demo_date(self):
        import random
        fund_account = "10000001"
        no = 10000000
        num = 20000000
        with open("test.txt", "w") as f:
            while num:
                ratio = random.uniform(-1, 1)
                f.write("{0}\t{1}\t{2}\n".format(fund_account, no, ratio))
                no += 1
                num -= 1

        return


if __name__ == "__main__":
    label_verify = Label_Verify()
    before = time.time()
    label_verify.generate_demo_date()
    print(time.time() - before)
    before = time.time()
    change_ratio, change_ratio_only = label_verify.cal_change_ratio(label_verify.read_data())
    label_verify.get_top_change_ratio(top_num=100)
    abnormal_data_info = label_verify.location_abnormal_data_info()
    print(time.time() - before)
    for each in abnormal_data_info:
        print(each)
    # label_verify.cal_change_ratio(data=[1, 1.223, 1.23434, 2.111, 2.333, 4.1221, 5.1212])
    # label_verify.get_top_change_ratio(top_num=3)
    # label_verify._print()
    # print(np.max([(100, 0.12), (101, 0.11), (102, 0.33)]))
    # label_verify.read_data()