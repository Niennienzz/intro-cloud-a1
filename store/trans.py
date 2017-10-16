import uuid
import datetime
from os import path
from store.pic import PicStore
from wand.image import Image
from const.const import Constants


class PicTrans:

    def __init__(self, data):
        # compose file path
        date = datetime.datetime.now().strftime('%Y-%m-%d')
        _id = uuid.uuid4().hex.upper()
        self.origin_path = path.join(date, _id, Constants.ORIGIN)

        # ensure jpeg image
        with Image(blob=data) as original:
            with original.convert('jpeg') as converted:
                self.data = converted.make_blob()

        # set original picture storage
        self.pic_stores = [PicStore(self.origin_path, self.data)]

    def trans(self):
        # make thumbnail
        thum_path = path.join(path.dirname(self.origin_path), Constants.THUMB)
        with Image(blob=self.data) as image:
            with image.clone() as img:
                img.transform(resize='x200>')
                self.pic_stores.append(PicStore(thum_path, img.make_blob()))

        # make trans1
        trans1_path = path.join(path.dirname(self.origin_path), Constants.TRANS_1)
        with Image(blob=self.data) as image:
            with image.clone() as img:
                img.flop()
                self.pic_stores.append(PicStore(trans1_path, img.make_blob()))

        # make trans2
        trans2_path = path.join(path.dirname(self.origin_path), Constants.TRANS_2)
        with Image(blob=self.data) as image:
            with image.clone() as img:
                img.evaluate(operator='leftshift', value=1, channel='red')
                self.pic_stores.append(PicStore(trans2_path, img.make_blob()))

        # make trans3
        trans3_path = path.join(path.dirname(self.origin_path), Constants.TRANS_3)
        with Image(blob=self.data) as image:
            with image.clone() as img:
                frequency = 3
                phase_shift = -90
                amplitude = 0.2
                bias = 0.7
                img.function('sinusoid', [frequency, phase_shift, amplitude, bias])
                self.pic_stores.append(PicStore(trans3_path, img.make_blob()))

    def save(self):
        result = []
        for store in self.pic_stores:
            filepath, ok = store.save()
            if ok:
                result.append(filepath)
            else:
                result.append('')
        return result

    def trans_save(self):
        self.trans()
        (origin, thum, tran1, tran2, tran3) = self.save()
        return origin
