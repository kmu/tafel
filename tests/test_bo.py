import shutil
from pathlib import Path
from unittest import TestCase

from tafel.core.bo import BayesianOptimizer
from tafel.core.reader import Reader


class TestBO(TestCase):
    def test_perform_bayesian_optimization(self):
        reader = Reader()
        reader.read_mpt("tests/data/example.mpt")
        x = reader.get_log_j()
        y = reader.get_ir_corrected_potential()
        bo = BayesianOptimizer(10, 0.5, 2, 1, [], Path("test_output"))
        bo.fit(x, y)

    def tearDown(self):
        shutil.rmtree("test_output")
