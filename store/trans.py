import asyncio
import uuid
import datetime
from os import path
from store.s3 import PicS3Store
from wand.image import Image
from const.const import Constants


class PicTrans:
    """PicTrans generates image transformations and save to disk.

        Attributes:
            origin_path (str): The filepath to the original image file.
            pic_stores (dict of PicS3Store): PicStore for each transformation.
    """

    def __init__(self, data):
        """Init.

        The init method takes the input image data and converts it into JPEG format.
        Then the method generates a relative filepath as origin_path.
        The origin_path has a format of {yyyy-mm-dd}/{uuid}/original.jpg

        Args:
            data (bytes): The original image data.
        """
        # compose file path
        date = datetime.datetime.now().strftime('%Y-%m-%d')
        _id = uuid.uuid4().hex.upper()
        self.origin_path = path.join(date, _id, Constants.ORIGIN)

        # ensure jpeg image
        with Image(blob=data) as original:
            with original.convert('jpeg') as converted:
                self.data = converted.make_blob()

        # set original picture storage
        self.pic_stores = {self.origin_path: PicS3Store(self.origin_path, self.data)}

    def trans(self):
        """Make transformations.

        This method takes the original image data and makes four transformations in memory.
        One of the transformations is a thumbnail of the original image.
        Each transformation is run in a separate coroutine.
        """
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        loop.run_until_complete(asyncio.gather(
            self.make_thumbnail(),
            self.make_trans1(),
            self.make_trans2(),
            self.make_trans3(),
        ))
        loop.close()

    async def make_thumbnail(self):
        """Coroutine that makes thumbnail.
        """
        thum_path = path.join(path.dirname(self.origin_path), Constants.THUMB)
        with Image(blob=self.data) as image:
            with image.clone() as img:
                img.crop(width=500, height=500, gravity='center')
                self.pic_stores[thum_path] = PicS3Store(thum_path, img.make_blob())

    async def make_trans1(self):
        """Coroutine that makes transformation #1.
        """
        trans1_path = path.join(path.dirname(self.origin_path), Constants.TRANS_1)
        with Image(blob=self.data) as image:
            with image.clone() as img:
                img.flop()
                self.pic_stores[trans1_path] = PicS3Store(trans1_path, img.make_blob())

    async def make_trans2(self):
        """Coroutine that makes transformation #2.
        """
        trans2_path = path.join(path.dirname(self.origin_path), Constants.TRANS_2)
        with Image(blob=self.data) as image:
            with image.clone() as img:
                img.evaluate(operator='leftshift', value=1, channel='red')
                self.pic_stores[trans2_path] = PicS3Store(trans2_path, img.make_blob())

    async def make_trans3(self):
        """Coroutine that makes transformation #3.
        """
        trans3_path = path.join(path.dirname(self.origin_path), Constants.TRANS_3)
        with Image(blob=self.data) as image:
            with image.clone() as img:
                frequency = 3
                phase_shift = -90
                amplitude = 0.2
                bias = 0.7
                img.function('sinusoid', [frequency, phase_shift, amplitude, bias])
                self.pic_stores[trans3_path] = PicS3Store(trans3_path, img.make_blob())

    def save(self):
        """Save files.

        This method saves the original image as well as its four transformations on disk.
        It does so by calling the underlying PicS3Store.save() for each image.
        Each save is run in a separate coroutine.

        Returns:
            (str): The original path of image.
        """
        funcs = []
        for key, store in self.pic_stores.items():
            funcs.append(store.save)
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        loop.run_until_complete(asyncio.gather(
            funcs[0](),
            funcs[1](),
            funcs[2](),
            funcs[3](),
            funcs[4](),
        ))
        loop.close()

    def trans_save(self):
        """Transform and save.

        This method combines trans() and save().
        It makes four transformations in memory and save them on disk.

        Returns:
            (str): The filepath of the original image saved.
        """
        self.trans()
        self.save()
        return self.origin_path
