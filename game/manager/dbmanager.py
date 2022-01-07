from game.helpers.dataframe import read_csv
from pathlib import Path

# TODO: remove this class (deprecated)
class DbManager:
    def __init__(self, gui):
        self.game = gui
        data_path = Path(r"data/external")
        self.dfs = {}

        for dir in self.game.m_res.resource_dirs:
            for pth in (dir / data_path).glob("*.csv"):
                self.dfs[pth.stem] = read_csv(pth, index_col=0)

        data_path = Path(r"data")

        for dir in self.game.m_res.resource_dirs:
            for pth in (dir / data_path).glob("*.csv"):
                self.dfs[pth.stem] = read_csv(pth, index_col=0)

    def get_characteristic(self, id):
        return self.dfs["characteristics"].loc[id, "name"]

    def get_nature(self):
        return self.dfs["natures"].sample()
