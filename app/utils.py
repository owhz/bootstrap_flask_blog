from datetime import tzinfo, timedelta


class UTC(tzinfo):
    def __init__(self, offset=0):
        self._offset = offset

    def utcoffset(self, dt):
        return timedelta(hours=self._offset)

    def tzname(self):
        return 'UTC%s' % ('+%d' % self._offset) if self._offset > 0 else str(self._offset)

    def dst(self):
        return timedelta(self._offset)
