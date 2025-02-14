from tafel.core.reader import HokutoReader, Reader


class TestReader:
    def test_read_mpt(self):
        reader = Reader(ph=13.5, reference_potential=0.4, electrolyte_resistance=0.1)
        reader.read_mpt("tests/data/example.mpt")

        assert reader.electrode_surface_area == 0.45
        assert abs(reader.get_potential_shift() - 1.19785) < 1e-5

        logj, ircp = reader.get_tafel_plot()
        assert len(logj) == 327
        assert len(ircp) == 327

        print(reader.docs)
        assert reader.docs["Characteristic mass"] == "0.001 g"

    def test_read_hokuto(self):
        reader = HokutoReader()
        reader.read_csv("tests/data/example2.CSV")
        assert reader.electrode_surface_area == 1.0
        logj, ircp = reader.get_tafel_plot()

        assert len(reader['measurement']) == 3
        assert len(logj) == len(ircp)
