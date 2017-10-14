import os

# from wand.image import Image

class PicStore():

    root = 'pics'
    
    # TODO: Make file structure nice.
    def __init__(self, filename, data):
        self.origin = os.path.join(self.root, '123', filename)
        self.suffix_thumb = os.path.join(self.root, '123', 'thumb' + filename)
        self.suffix_trans1 = os.path.join(self.root, '123', 'trans1' + filename)
        self.suffix_trans2 = os.path.join(self.root, '123', 'trans2' + filename)
        self.suffix_trans3 = os.path.join(self.root, '123', 'trans3' + filename)
        self.data = data

    def save(self):
        os.makedirs(os.path.dirname(self.origin))
        try:
            with open(self.origin, 'wb') as file:
                file.write(self.data)
        except IOError:
            return False
        return True

    # def trans(self):
    #     with Image(blob=self.data) as original:
    #         with original.clone() as converted:
    #             converted.sample(50, 50)
    #             return converted

    def trans_save(self):
        # data = self.trans()
        ok = self.save()
        return self.origin, self.suffix_thumb
