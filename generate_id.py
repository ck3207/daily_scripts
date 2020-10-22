class Generate:
    def __init__(self, filename):
        self.filename = filename
        self.f = ""

    def open_file(self):
        self.f = open(file=self.filename, mode="w")

        return self.f

    def generate_id(self, start_id, num):
        for i in range(start_id, start_id+num):
            self.f.write(str(i) + "\n")

    def close_file(self):
        self.f.close()


generate = Generate(filename="ids.txt")
generate.open_file()
generate.generate_id(1000000, 5000000)

