from utils import check_if_nodes


TYPE_DICT={
    "operation": "rectangle",
    "condition": "diamond",
    "input/output": "parallelogram",
    "start/stop": "ellipse"
}

class Block:
    def __init__(self, name, content):
        self.name = name
        self.content = content
    
    def to_string(self, nodes_list):
        return f"{self.name} [{self.content.to_string()}]; \n"


class Content:
    def __init__(self):
        self.keys = {}

    def add(self, key, val):
        self.keys[key] = val
        return self
    
    def to_string(self):
        return (",").join([f"{key} = {value} " for key,value in self.keys.items() if key != "edge" ])
    
class Line:
    def __init__(self, name, content):
        self.name = name 
        self.content = content

    def to_string(self, node_list):
        s = ""
        for begin, end in self.content.keys["edge"]:
            if check_if_nodes(begin, end, node_list): 
                s+= f"{begin} -> {end} [{self.content.to_string()}]; \n"
            else:
                break
        return s
