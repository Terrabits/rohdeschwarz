from .segment import Segment


class Segments(object):


    # constructor

    def __init__(self, vna, channel_index):
        super(Segments, self).__init__()
        self._vna     = vna
        self._channel = vna.channel(channel_index)


    # channel

    @property
    def channel(self):
        return self._channel.index


    # count

    @property
    def count(self):
        scpi      = ':SENS{0}:SEGM:COUN?'
        scpi      = scpi.format(self.channel)
        count_str = self._vna.query(scpi)
        return int(count_str)


    @count.setter
    def count(self, count):
        # is count valid?
        if count < 0:
            raise ValueError('segments.count must be greater than zero')

        # no segments?
        if not count:
            self.delete_all()
            return

        # get segment count
        old_count = self.count

        # remove segments?
        if old_count > count:
            for i in range(old_count, count, -1):
                self.delete(i)

        # add segments?
        if old_count < count:
            for i in range(old_count + 1, count + 1):
                self.add(i)


    # segments

    def add(self, index=None):
        # append segment to end?
        if index is None:
            index = self.count + 1

        scpi = ':SENS{0}:SEGM{1}:ADD'
        scpi = scpi.format(self.channel, index)
        self._vna.write(scpi)


    def delete(self, index):
        # negative index?
        if index < 0:
            index += self.count

        # delete
        scpi = ':SENS{0}:SEGM{1}:DEL'
        scpi = scpi.format(self.channel, index)
        self._vna.write(scpi)


    def delete_all(self):
        scpi = ':SENS{0}:SEGM:DEL:ALL'
        scpi = scpi.format(self.channel)
        self._vna.write(scpi)


    def at(self, index):
        # negative index?
        if index < 0:
            index += self.count

        # get
        return Segment(self._vna, self.channel, index)


    # operators

    def __getitem__(self, index):
        # negative index?
        if index < 0:
            index += self.count

        # get
        return self.at(index + 1)


    def __len__(self):
        return self.count


    def __iter__(self):
        for i in range(self.count):
            yield self.at(i + 1)
