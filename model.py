import datetime

class Message():
    def __init__(self , text: str, author:str, created: datetime ):
        self.text : str = text
        self.author : str = author
        self.created : datetime = created
        self.group = 'Group'


    def as_json(self):
        return {"author": self.author, 'text': self.text, 'time': self.created }


class Group():
    def __init__(self, messages:list):
        self.messages: list = messages 

    def as_json(self):
        return [message for message in self.messages]
    


