
def find_redis_slots(filename="redis_slots.txt"):
    first = 0
    slots_list = []
    with open(file=filename, mode="r") as f:
        while True:
            line = f.readline().replace("\n", "")
            if line == "":
                break
            else:
                all_slots = line.split(" ")
                first_init, last_init = all_slots[0].split("-")
                first_init = int(first_init)
                last_init = int(last_init)
                for each in all_slots[1:]:
                    try:
                        first, last = each.split("-")
                    except Exception as e:
                        first = last = each
                    first = int(first)
                    last = int(last)
                    while first > last_init + 1:
                        last_init += 1
                        slots_list.append(last_init)
                    last_init = last



    return slots_list


if __name__ == "__main__":
    print(find_redis_slots())


