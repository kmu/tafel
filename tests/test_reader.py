from tafel.core.reader import Reader


class TestReader:
    def test_read_mpt(self):
        reader = Reader(
            ph=13.5, ag_agcl_3m_nacl_v_vs_nhe=0.4, electrolyte_resistance=0.1
        )
        reader.read_mpt("tests/data/example.mpt")

        assert reader.electrode_surface_area == 0.046
        assert abs(reader.get_potential_shift() - 1.19785) < 1e-5
