import numpy as np
import pickle

class Label_Verify:
    """Some methods point to verify labels of big data."""
    def __init__(self):
        self.change_ratio = []
        self.change_ratio_only = []
        self.abnormal_data = []

    def read_data(self):
        pass

    def cal_change_ratio(self, data):
        """data = [(fund_account, init_date, value)]
        Attention: The value must be the last element. 
        If not, the function will make mistake. """

        for i, info in enumerate(data):
            if i+1 < len(data):
                # cal change ratio
                if not isinstance(info, list):
                    change_ratio = (data[i+1] - info)/info
                    info = [""]
                else:
                    change_ratio = (data[i+1][-1] - info[-1])/info[-1]
                self.change_ratio_only.append(change_ratio)
                piece = []
                for each in info[:-1]:
                    piece.append(each)
                # only change the last value, and save the other information
                piece.append(change_ratio)
                self.change_ratio.append(tuple(piece))

    def get_top_change_ratio(self, top_num=3):
        """Get a certain num data that may be abnormal data."""
        temp_change_ratio = self.change_ratio_only[:]
        for i in range(top_num):
            top = max(temp_change_ratio)
            self.abnormal_data.append(top)
            temp_change_ratio.remove(top)

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

if __name__ == "__main__":
    label_verify = Label_Verify()
    label_verify.cal_change_ratio(data=[1, 1.223, 1.23434, 2.111, 2.333, 4.1221, 5.1212])
    label_verify.get_top_change_ratio(top_num=3)
    label_verify._print()
    print(np.max([(100, 0.12), (101, 0.11), (102, 0.33)]))