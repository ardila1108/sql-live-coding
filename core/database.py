import glob
import pandas as pd


class Database:
    def __init__(self, name):
        self.path = f"data/{name}"
        self.file_dict = self._build_file_dict()

    def _build_file_dict(self):
        file_list = glob.glob(self.path + "/*.csv")
        return {
            file.split("/")[-1].replace(".csv", ""): pd.read_csv(file) for file in file_list
        }