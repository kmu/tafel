from pathlib import Path

import numpy as np
import pandas as pd


class Reader:
    def __init__(
        self,
        ph: float = 13,
        reference_potential: float = 0.210,
        electrolyte_resistance: float = 0.05,
    ) -> None:
        self.ph = ph
        self.reference_potential = reference_potential
        self.electrolyte_resistance = electrolyte_resistance

    def read_mpt(self, path: str) -> None:
        with Path(path).open() as f:
            contents = f.read()

        header_line = contents.split("Nb header lines : ")[1].split("\n")[0]
        header_lines = int(header_line)

        self.df = pd.read_csv(path, skiprows=header_lines - 1, sep="\t")

        contents = contents.split("Electrode surface area : ")[1].split(" cm2")[0]
        self.electrode_surface_area = float(contents)

    def get_potential_shift(self) -> float:
        return self.ph * 0.0591 + self.reference_potential

    def get_log_j(self) -> np.ndarray:
        j = self.get_j()
        return np.log10(j / 1000)  # Convert to A/cm2

    def get_decent_data(self) -> pd.DataFrame:
        mask = self.df["<I>/mA"] > 0
        return self.df.loc[mask, :].copy()

    def get_j(self, cycle_number: int = -1) -> pd.Series:
        sdf = self.get_decent_data()
        sdf = sdf[sdf["cycle number"] == cycle_number] if cycle_number >= 0 else sdf
        return sdf["<I>/mA"] / self.electrode_surface_area  # mA/cm2

    def get_tafel_plot(self) -> tuple:
        logj = self.get_log_j()
        ircp = self.get_ir_corrected_potential()

        return logj, ircp

    def get_ir_corrected_potential(self) -> np.ndarray:
        potential_shift = self.get_potential_shift()
        sdf = self.get_decent_data()
        self.E_vs_RHE_V = sdf["Ewe/V"] + potential_shift

        ia = sdf["<I>/mA"] / 1000
        self.iR = ia * self.electrolyte_resistance

        return self.E_vs_RHE_V - self.iR

    def get_xy(self) -> tuple[np.ndarray, np.ndarray]:
        return self.get_log_j(), self.get_ir_corrected_potential()
