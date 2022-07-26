# https://www.circuit-diagram.org/news/2019/04/circuit-netlists

class NetList:
    def __init__(self, net_list_file):
        self.net_list = []
        self.GetNetListFromFile(net_list_file)

    def GetNetListFromFile(self, file):
        with open(file, "r") as net_list_file:
            for line in net_list_file:
                if line[0] != "*":
                    split_line = line.split(" ")
                    split_line[3] = split_line[3][:-1]

                    self.net_list.append(split_line)

        return self.net_list

    def GetComponents(self):
        return [item[0] for item in self.net_list]

    def GetLeftNodes(self):
        return [int(item[1]) for item in self.net_list]

    def GetRightNodes(self):
        return [int(item[2]) for item in self.net_list]

    def GetValues(self):
        return [int(item[3]) for item in self.net_list]


if __name__ == "__main__":
    NetList = NetList("../testing/Circuit1.txt")
    print(NetList.GetComponents())
    print(NetList.GetLeftNodes())
