import json
from datetime import datetime

class Message():
    def __init__(self, text: str, author: str, created: datetime, group: str):
        self.text = text
        self.author = author
        self.created = created
        self.group = group

    def as_json(self):
        return {
            "author": self.author,
            "text": self.text,
            "created": self.created.isoformat(),
            "group": self.group
        }
    
    @staticmethod
    def from_json(data):
        return Message(
            text=data['text'],
            author=data['author'],
            created=datetime.fromisoformat(data['created']),
            group=data['group']
        )


class Group():
    def __init__(self, name: str,  admin : str , messages: list = None):
        self.name = name
        self.admin = admin
        self.messages = messages if messages else []

    def as_json(self):
        return {
            "name": self.name,
            "admin": self.admin,
            "messages": [message.as_json() for message in self.messages]
        }

    @staticmethod
    def from_json(data):
        messages = [Message.from_json(msg) for msg in data['messages']]
        return Group(name=data['name'], admin=data['admin'], messages=messages)


class MessageBoard():
    def __init__(self, groups: list = None):
        self.groups = groups if groups else []

    def add_group(self, group: Group):
        self.groups.append(group)

    def save_to_file(self, filename: str):
        with open(filename, 'w') as f:
            json.dump([group.as_json() for group in self.groups], f, indent=4)

    @staticmethod
    def load_from_file(filename: str):
        with open(filename, 'r') as f:
            groups_data = json.load(f)
            groups = [Group.from_json(group_data) for group_data in groups_data]
            return MessageBoard(groups=groups)


# # Example usage
# new_message = Message('Hello', 'John', datetime.utcnow(), 'Group1')
# new_group = Group(name='Group1',admin='keree', messages=[new_message])
# board = MessageBoard(groups=[new_group])

# # Save to file
# board.save_to_file('message_board.json')

# # Load from file
# loaded_board = MessageBoard.load_from_file('message_board.json')
# add_message_to_group(loaded_board, 'Group1', Message('Another message', 'Alice', datetime.utcnow(), 'Group1'))

# print(loaded_board.groups[0].messages[1].text)  