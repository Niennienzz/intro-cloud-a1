import os
import uuid
import datetime


class PicStore:

    root = 'pics'
    
    def __init__(self, filename, data):
        date = datetime.datetime.now().strftime('%Y-%m-%d')
        _id = uuid.uuid4().hex.upper()
        self.file_path = os.path.join(self.root, date, _id, filename)
        self.data = data

    def save(self):
        os.makedirs(os.path.dirname(self.file_path))
        try:
            with open(self.file_path, 'wb') as file:
                file.write(self.data)
        except IOError:
            return '', False
        return self.file_path, True
