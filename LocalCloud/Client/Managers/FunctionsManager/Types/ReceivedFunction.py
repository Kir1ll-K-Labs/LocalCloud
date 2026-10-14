import ast
class ReceivedFunction:
    def __init__(self, address: str, function_data):
        self.address = address
        self.__function_data = ast.literal_eval(function_data)

    def __getattr__(self, item):
        if item == "args":
            return self.__function_data.get("args", ())
        elif item == "kwargs":
            return self.__function_data.get("kwargs", {})
        kwargs = self.__function_data.get("kwargs", {})
        if item in kwargs:
            return kwargs[item]

    def __getitem__(self, item):
        return self.__function_data["args"][item]

    def __len__(self):
        return len(self.__function_data.get("args", ()))