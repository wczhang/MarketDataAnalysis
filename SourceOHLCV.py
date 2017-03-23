import urllib.request


class SourceOHLCV():
    """Class interfaces between Yahoo finance and a local data file.

    This class writes 5 minute data to a local .csv file.
    It updates the file without overlapping previous data and
    without writing redundant data. It can also reads from the
    local file.
    """

    def __init__(self, s):
        """Class constructor sets up attributes.

        Instance keeps track of the url where it sources data for its ticker,
        the name of the local file to where it writes.

        :param s: the stock ticker associated with an instance of this class
        :type s:  str
        """
        self._source = 'http://chartapi.finance.yahoo.com/instrument/1.0/' + s
        self._source += '/chartdata;type=quote;range=10d/csv'
        self._outFile = s + '.csv'

    def _pull(self):
        """Pull most recent data from Yahoo finance source url."""
        dataLines = []
        try:
            dataLines = urllib.request.urlopen(
                self._source).read().decode().split('\n')
        except Exception as e:
            print(str(e))
        return dataLines  # list

    def _parse(self, dl):
        """Parses new Yahoo finance OHLCV data from the raw data."""
        parsed = []
        recentDate = self._getMostRecentDate()

        for line in dl:
            splitLine = line.split(',')
            try:
                date = float(splitLine[0])
                if date > recentDate:
                    parsed += [line]
            except Exception as e:
                pass
        return parsed  # list

    def _getMostRecentDate(self):
        """Returns most-recent Unix timestamp recorded in a local data file."""
        date = 0
        try:
            file = open(self._outFile, 'r')
            file.seek(0, 2)
            file.seek(file.tell() - 70)
            lastLine = file.read().split('\n')[-2]
            date = int(lastLine.split(',')[0])
        except Exception as e:
            pass
        return date  # int

    def _appendLine(self, l):
        """Appends the passed line to the local data file."""
        file = open(self._outFile, 'a')
        file.write(l + '\n')
        file.close()

    def update(self):
        """Adds new OHLCV data to a local data file."""
        for line in self._parse(self._pull()):
            self._appendLine(line)

    def getRecent(self, n=1):
        """Reads lines from a local data file.

        The local data file is associated with a class instance
        and a stock ticker. It contains chronological OHLCV data.

        :param n: the number of lines to read
        :type n:  int
        :returns: data lines from file at self._outFile
        :rtype:   list of str

        .. warning:: n must be greater than or equal to zero
        .. todo:: write this function
        """
        pass
