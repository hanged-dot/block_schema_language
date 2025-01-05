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
    
    def to_string(self):
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

    def to_string(self):
        s = ""
        for begin, end in self.content.keys["edge"]:
            s+= f"{begin} -> {end} [{self.content.to_string()}]; \n"
        return s
