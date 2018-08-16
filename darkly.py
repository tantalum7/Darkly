
import twain
import time

class Darkly:

    @classmethod
    def get_scanner(cls):
        sm = twain.SourceManager(0)
        return Scanner(sm.OpenSource(sm.source_list[0].encode()))


class Scanner:

    def __init__(self, source: twain._Source):
        self.source = source
        self.index = 0

    def is_feeder_loaded(self):
        return bool(self.source.get_capability_current(twain.CAP_FEEDERLOADED)[1])

    def scan(self):
        self.source.RequestAcquire(0, 0)
        rv = self.source.XferImageNatively()
        if rv:
            (handle, count) = rv
            twain.DIBToBMFile(handle, 'image{}.bmp'.format(self.index))
            self.index += 1

        self.source.HideUI()

    def scan_all(self):

        while True:

            if self.is_feeder_loaded():
                self.scan()

            time.sleep(2)