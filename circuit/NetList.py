# https://www.circuit-diagram.org/news/2019/04/circuit-netlists
from components.ComponentType import ComponentType


class NetList:
    def __init__(self):
        self.net_list = []

    def LoadFile(self, file):
        self.net_list = []

        with open(file, "r") as net_list_file:
            for line in net_list_file:
                if line[0] != "*":
                    split_line = line.split(" ")

                    if split_line[3][-1] == "\n":
                        split_line[3] = split_line[3][:-1]

                    self.net_list.append(split_line)

        return self

    def GetComponentsAndIDs(self):
        return [item[0] for item in self.net_list]

    def GetLeftNodes(self):
        return [item[1] for item in self.net_list]

    def GetRightNodes(self):
        return [item[2]for item in self.net_list]

    def GetValues(self):
        return [int(item[3]) for item in self.net_list]

    def GetComponentsDetails(self):
        components_details = []

        components_and_ids = self.GetComponentsAndIDs()
        left_nodes = self.GetLeftNodes()
        right_nodes = self.GetRightNodes()
        values = self.GetValues()

        for index in range(len(components_and_ids)):
            component_details = {
                'id': int(components_and_ids[index][1:]),
                'left_node': left_nodes[index],
                'right_node': right_nodes[index],
                'component_type': ComponentType(components_and_ids[index][0]),
                'value': values[index]
            }

            components_details.append(component_details)

        return components_details

