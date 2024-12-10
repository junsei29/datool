import pandas as pd

class CSVManager:
    def __init__(self):
        self.df = None

    def load_csv(self, file_path):
        """CSVファイルを読み込む"""
        self.df = pd.read_csv(file_path)
        return self.df

    def save_csv(self, file_path):
        """CSVファイルを保存する"""
        if self.df is not None:
            self.df.to_csv(file_path, index=False)

    def add_column(self, column_name, default_value=0):
        """列を追加する"""
        if self.df is not None:
            self.df[column_name] = default_value

    def remove_column(self, column_name):
        """列を削除する"""
        if self.df is not None and column_name in self.df.columns:
            deleted_data = self.df[column_name].copy()
            self.df = self.df.drop(columns=[column_name])
            return deleted_data
