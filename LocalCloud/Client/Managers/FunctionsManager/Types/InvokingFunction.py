class InvokingFunction:
    def __init__(self, address: str, function_data=None, function_name: str = ""):
        self.address = address
        self.function_name = function_name
        self.function_data = function_data