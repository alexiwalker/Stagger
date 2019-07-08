from lib import linear, core, stagger, visual
import os
import random
import inspect
__FNAME__ = lambda: inspect.stack()[1][3]

TEST_MESSAGE = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ1234567890 the quick brown fox Jumped over the lazy dog'

BASE_IMAGE = "images/test.png"


class Encode:

    @staticmethod
    def Linear():
        if not os.path.exists(BASE_IMAGE):
            core.noise_image(BASE_IMAGE, (1920, 1080))

        n = linear.Linear(BASE_IMAGE)
        px = n.encode_message(TEST_MESSAGE)

        assert px[0]
        assert linear.Linear(px[1]).extract_message() == TEST_MESSAGE

        print(f'linear.{__FNAME__()} OK')

    @staticmethod
    def Stagger():
        if not os.path.exists(BASE_IMAGE):
            core.noise_image(BASE_IMAGE, (1920, 1080))

        n = stagger.Stagger(BASE_IMAGE)
        px = n.encode_message(TEST_MESSAGE)

        assert px[0]
        assert stagger.Stagger(px[1]).extract_message() == TEST_MESSAGE

        print(f'stagger.{__FNAME__()} OK')

    def __init__(self):
        self.Linear()
        self.Stagger()


class Core:
    def __init__(self):
        self.int_to_bin()
        self.bitstream_to_8bit()

    @staticmethod
    def int_to_bin():
        a = 255  # 11111111
        b = 32  # 00100000
        c = 368  # 101110000

        a = core.int_to_bin(a)
        b = core.int_to_bin(b)
        c = core.int_to_bin(c)

        assert a == '11111111'
        assert b == '00100000'
        assert len(b) > 6
        assert c == '101110000'

        print(f'core.{__FNAME__()} OK')

    @staticmethod
    def bitstream_to_8bit():
        stream = ''
        for i in range(0, 20 * 8):
            stream += str(random.randint(0, 1))
        _8bit = core.bitstream_to_8bit(stream)

        for _byte in _8bit:
            assert len(_byte) == 8
            evar = False
            try:
                core.bin_to_int(_byte)
            except ValueError:
                evar = True

            assert not evar

        _stream = ''.join(_8bit)

        assert _stream == stream

        print(f'core.{__FNAME__()} OK')


if __name__ == '__main__':
    Encode()
    Core()
