import os

class PicStore():

    root = 'pics'
    
    # TODO: Make file structure nice.
    def __init__(self, path, data):
        self.origin = os.path.join(self.root, '123', path)
        self.suffix_thumb = os.path.join(self.root, '123', 'thumb' + path)
        self.suffix_trans1 = os.path.join(self.root, '123', 'trans1' + path)
        self.suffix_trans2 = os.path.join(self.root, '123', 'trans2' + path)
        self.suffix_trans3 = os.path.join(self.root, '123', 'trans3' + path)
        self.data = data

    def trans_save(self):
        os.makedirs(os.path.join(self.root, '123'))
        file = open(self.origin, 'wb')
        file.write(self.data)
        file.close()

        file = open(self.suffix_thumb, 'wb')
        file.write(self.data)
        file.close()

        return self.origin, self.suffix_thumb