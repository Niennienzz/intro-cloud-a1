import os


class PicStore:

    root = 'pics'
    
    def __init__(self, filename, data):
        self.file_path = os.path.join(self.root, filename)
        self.data = data

    def save(self):
        if not os.path.exists(os.path.dirname(self.file_path)):
            os.makedirs(os.path.dirname(self.file_path))
        try:
            with open(self.file_path, 'wb') as file:
                file.write(self.data)
        except IOError:
            return '', False
        return self.file_path, True
