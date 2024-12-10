from tkinter import Tk, filedialog, messagebox, Button, Toplevel, Listbox, END
from csv_manager import CSVManager
from history_manager import HistoryManager

class GUI:
    def __init__(self, master):
        self.master = master
        self.master.title("CSV 加工ツール")

        self.csv_manager = CSVManager()
        self.history_manager = HistoryManager()

        # ボタン
        self.load_button = Button(master, text="CSVを開く", command=self.load_csv)
        self.load_button.pack()

        self.save_button = Button(master, text="CSVを保存", command=self.save_csv)
        self.save_button.pack()

        self.undo_button = Button(master, text="元に戻す (Ctrl+Z)", command=self.undo_last_action)
        self.undo_button.pack()

        self.history_button = Button(master, text="履歴を閲覧", command=self.view_history)
        self.history_button.pack()

    def load_csv(self):
        file_path = filedialog.askopenfilename(filetypes=[("CSV files", "*.csv")])
        if file_path:
            self.csv_manager.load_csv(file_path)
            messagebox.showinfo("情報", "CSVファイルを読み込みました。")

    def save_csv(self):
        file_path = filedialog.asksaveasfilename(defaultextension=".csv", filetypes=[("CSV files", "*.csv")])
        if file_path:
            self.csv_manager.save_csv(file_path)
            messagebox.showinfo("情報", "CSVファイルを保存しました。")

    def undo_last_action(self):
        message = self.history_manager.undo_last_action(self.csv_manager)
        messagebox.showinfo("元に戻す", message)

    def view_history(self):
        """履歴を閲覧"""
        history_window = Toplevel(self.master)
        history_window.title("操作履歴")

        listbox = Listbox(history_window)
        listbox.pack(fill="both", expand=True)

        for idx, (action, column_name, _) in enumerate(self.history_manager.history):
            listbox.insert(END, f"{idx + 1}: {action} - {column_name}")
