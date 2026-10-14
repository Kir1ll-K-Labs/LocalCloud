import json
import ast

class ReceivedEvent:
    def __init__(self,address:str,event_data):
        self.address=address
        self.__event_data=ast.literal_eval(event_data)

    def __getattr__(self, item):
        if item=="event_data":
            return self.__event_data["event_data"]
        if item=="args":
            return self.__event_data.get("args",())
        elif item=="kwargs":
            return self.__event_data.get("kwargs",{})
        kwargs=self.__event_data.get("kwargs",{})
        if item in kwargs:
            return kwargs[item]
    def __getitem__(self, item):
        return self.__event_data["args"][item]
    def __len__(self):
        return len(self.__event_data.get("args",()))