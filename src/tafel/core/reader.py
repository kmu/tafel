from pathlib import Path

import pandas as pd


class Reader:
    def read_mpt(self: "Reader", path: str) -> None:
        with Path(path).open() as f:
            contents = f.read()

        header_line = contents.split("Nb header lines : ")[1].split("\n")[0]
        header_lines = int(header_line)

        self.df = pd.read_csv(path, skiprows=header_lines - 1, sep="\t")

        contents = contents.split("Electrode surface area : ")[1].split(" cm2")[0]
        self.electrode_surface_area = float(contents)
