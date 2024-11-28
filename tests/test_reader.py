from tafel.core.reader import Reader


class TestReader:
    def test_read_mpt(self):
        reader = Reader()
        reader.read_mpt("tests/data/example.mpt")
