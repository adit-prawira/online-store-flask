class ResponseBody:
    def __init__(self, data, message:str, status:int):
        self.data = data
        self.message = message
        self.status = status