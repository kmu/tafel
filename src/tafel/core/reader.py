import re
from io import StringIO
from pathlib import Path
from typing import Any

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

        lines = contents.splitlines()
        metadata = {}

        for _, line in enumerate(lines):
            if line.startswith("mode"):
                break
            if ":" in line:
                key, value = line.split(":", 1)
                metadata[key.strip()] = value.strip()

        self.docs = metadata

        header_line = metadata.get("Nb header lines", "0")
        header_lines = int(header_line)

        self.df = pd.read_csv(path, skiprows=header_lines - 1, sep="\t")

        electrode_surface_area = metadata.get("Electrode surface area", "0 cm2").split(" cm2")[0]
        self.electrode_surface_area = float(electrode_surface_area)

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


class HokutoReader(Reader):
    def get_number_of_measurements(self) -> int:
        return len(self.docs["measurements"])

    @staticmethod
    def txt_to_dict(txt: str) -> dict[str, Any]:
        sections = re.split(r"《(.*?)》\n", txt)[1:]

        # Parsing into a dictionary
        parsed_data = {}

        for i in range(0, len(sections), 2):
            section_name = sections[i].strip()
            section_content = sections[i + 1].strip().split("\n")

            if "測定データ" in section_name:
                # Handling measurement data separately
                data = pd.read_csv(StringIO("\n".join(section_content)), sep=",", header=None)
                data.columns = data.iloc[0]
                data = data.iloc[1:]
                parsed_data[section_name] = data
            else:
                # General key-value extraction
                section_dict = {}
                for line in section_content:
                    parts = [x.strip() for x in line.split(",") if x.strip()]
                    if len(parts) == 2:  # noqa: PLR2004
                        section_dict[parts[0]] = parts[1]
                    elif len(parts) > 2:  # noqa: PLR2004
                        section_dict[parts[0]] = parts[1:]  # Store as list if multiple values
                parsed_data[section_name] = section_dict

        return parsed_data

    def get_tafel_plots(self):
        for measurement in self.docs["measurements"]:
            self.df = measurement["測定データ"]
            self.df = self.df.query("種別 == 'アノード'")
            self.df = self.df.rename(columns={"3 電流I": "<I>/mA", "4 WE/CE": "Ewe/V"})
            self.df["<I>/mA"] = self.df["<I>/mA"].astype(float)
            self.df["Ewe/V"] = self.df["Ewe/V"].astype(float)

    def read_csv(self, path: str) -> None:
        measurements = []
        self.docs = {}

        with Path(path).open(encoding="shift-jis") as f:
            contents = f.read()

        chapters = contents.split("《測定フェイズヘッダ》")

        for i, chapter in enumerate(chapters):
            if i == 0:
                self.docs["metadata"] = self.txt_to_dict(chapter)
            else:
                _docs = self.txt_to_dict("《測定フェイズヘッダ》" + chapter)
                measurements.append(_docs)

        self.docs["measurements"] = measurements
        # Splitting the sections

        self.df = self.docs["measurements"][-1]["測定データ"]
        # self.df = self.df.query("種別 == 'アノード'")
        self.df = self.df.query("種別 == 'カソード'")
        self.df = self.df.rename(columns={"3 電流I": "<I>/mA", "4 WE/CE": "Ewe/V"})
        self.df["<I>/mA"] = self.df["<I>/mA"].astype(float)
        self.df["Ewe/V"] = self.df["Ewe/V"].astype(float)

        area_info = self.docs["metadata"]["測定情報"]["面積"]
        if area_info[1] == "cm2":
            self.electrode_surface_area = float(area_info[0])
        else:
            msg = f"Unknown area unit: {area_info[1]}"
            raise ValueError(msg)
