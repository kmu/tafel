from unittest import TestCase

from tafel.core.bo import perform_bayesian_optimization
from tafel.core.reader import Reader


class TestBO(TestCase):
    def test_perform_bayesian_optimization(self):
        reader = Reader()
        reader.read_mpt("tests/data/example.mpt")
        x = reader.get_log_j()
        y = reader.get_ir_corrected_potential()
        perform_bayesian_optimization(x, y, 10, 0.5, 2, 1, [])
