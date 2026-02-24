import os
import json
from datetime import datetime

class CodeMemory:

    def __init__(self):
        self.file="code_memory.json"

        if not os.path.exists(self.file):
            with open(self.file,"w") as f:
                json.dump({},f)

    def save_code(self,name,code):

        with open(self.file) as f:
            data=json.load(f)

        data[name]={
            "code":code,
            "date":str(datetime.now())
        }

        with open(self.file,"w") as f:
            json.dump(data,f,indent=4)

    def get_code(self,name):

        with open(self.file) as f:
            data=json.load(f)

        return data.get(name)