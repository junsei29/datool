class HistoryManager:
    def __init__(self):
        self.history = []

    def add_history(self, action, column_name, data=None):
        """履歴を追加する"""
        self.history.append((action, column_name, data))

    def undo_last_action(self, csv_manager):
        """最後の操作を元に戻す"""
        if not self.history:
            return "履歴がありません。"

        action, column_name, data = self.history.pop()
        if action == "add":
            csv_manager.remove_column(column_name)
        elif action == "remove":
            csv_manager.df[column_name] = data
        return f"{column_name} の操作を元に戻しました。"
