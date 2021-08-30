class ResponseBody:
    def __init__(self, data, message:str, status_code:int):
        self.data = data
        self.message = message
        self.status_code = status_code