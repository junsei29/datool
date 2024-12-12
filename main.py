import os
from sqlalchemy import create_engine
import pandas as pd
import sys

# 環境変数からデータベース接続文字列を取得
DATABASE_URL = os.getenv("DATABASE_URL")

# SQLAlchemyエンジンを作成
engine = create_engine(DATABASE_URL)

# データベース接続をテスト
try:
    with engine.connect() as connection:
        print("Successfully connected to the database!")
except Exception as e:
    print("Failed to connect to the database:", e)


# CLIモードでCSVを処理する関数
def process_csv(input_path, output_path, encoding="utf-8"):
    try:
        # CSVを読み込み
        df = pd.read_csv(input_path, encoding=encoding)
        print(f"CSVファイルを読み込みました: {input_path}")

        # 処理例: 最初の5行を表示
        print(df.head())

        # 処理結果を保存
        df.to_csv(output_path, index=False, encoding=encoding)
        print(f"処理済みCSVを保存しました: {output_path}")
    except Exception as e:
        print(f"エラーが発生しました: {e}")


if __name__ == "__main__":
    # Render環境であればCLIモードを実行
    if os.getenv("RENDER_ENV"):
        if len(sys.argv) < 3:
            print("使い方: python main.py <入力CSVパス> <出力CSVパス>")
        else:
            input_path = sys.argv[1]
            output_path = sys.argv[2]
            process_csv(input_path, output_path)
    else:
        # ローカル環境ではTkinterのGUIを有効にする
        try:
            from tkinter import Tk, filedialog, messagebox, Toplevel, Button, Frame, StringVar, OptionMenu, Label, Listbox, END
            from tkinter.ttk import Treeview
            from tkinter.simpledialog import askstring

            class CSVTool:
                def __init__(self, master):
                    self.master = master
                    self.master.title("CSV 加工ツール")

                    # ヘッダー用フレーム
                    header_frame = Frame(master)
                    header_frame.pack(fill="x")

                    # エンコード選択用のドロップダウンメニュー
                    self.encoding_var = StringVar(value="utf-8")
                    encoding_options = ["utf-8", "shift_jis", "euc-jp", "cp932"]
                    self.encoding_menu = OptionMenu(header_frame, self.encoding_var, *encoding_options)
                    self.encoding_menu.pack(side="left", padx=5, pady=5)

                    # CSV開くボタン
                    self.load_button = Button(header_frame, text="CSVを開く", command=self.load_file)
                    self.load_button.pack(side="left", padx=5, pady=5)

                    # 保存ボタン
                    self.save_button = Button(header_frame, text="CSVを保存", command=self.save_csv)
                    self.save_button.pack(side="left", padx=5, pady=5)

                    # 列削除用のドロップダウンとボタン
                    self.delete_column_var = StringVar(value="列を選択")
                    self.delete_column_menu = OptionMenu(header_frame, self.delete_column_var, [])
                    self.delete_column_menu.pack(side="left", padx=5, pady=5)
                    self.delete_column_button = Button(header_frame, text="列を削除", command=self.remove_column)
                    self.delete_column_button.pack(side="left", padx=5, pady=5)

                    # データ型変更ボタン
                    self.change_type_button = Button(header_frame, text="データ型を変更", command=self.change_type_dialog)
                    self.change_type_button.pack(side="left", padx=5, pady=5)

                    # 履歴表示ボタン
                    self.view_history_button = Button(header_frame, text="履歴を表示", command=self.view_history)
                    self.view_history_button.pack(side="left", padx=5, pady=5)

                    # データ情報表示ラベル
                    self.data_info_label = Label(master, text="列数: 0 | データ数: 0", anchor="w")
                    self.data_info_label.pack(fill="x", padx=5, pady=5)

                    # Treeviewウィジェット
                    self.tree = Treeview(master, columns=["#"] + ["dummy"], show="headings")
                    self.tree.heading("#", text="#")
                    self.tree.pack(expand=True, fill="both")

                    # データ型を表示するTreeview
                    self.type_tree = Treeview(master, columns=["Column", "Type"], show="headings")
                    self.type_tree.heading("Column", text="列名")
                    self.type_tree.heading("Type", text="データ型")
                    self.type_tree.pack(fill="x")

                    # データフレームと履歴を保持
                    self.df = None
                    self.history = []  # 履歴を保持するリスト

                    # ショートカット: Ctrl+Zで元に戻す
                    self.master.bind("<Control-z>", lambda event: self.undo_last_action())

                # 省略: 他のCSVToolメソッド

            root = Tk()
            app = CSVTool(root)
            root.mainloop()
        except Exception as e:
            print("GUIモードの初期化に失敗しました:", e)



#  import os
# from sqlalchemy import create_engine

# # 環境変数からデータベース接続文字列を取得
# DATABASE_URL = os.getenv("DATABASE_URL")

# # SQLAlchemyエンジンを作成
# engine = create_engine(DATABASE_URL)

# # データベース接続をテスト
# try:
#     with engine.connect() as connection:
#         print("Successfully connected to the database!")
# except Exception as e:
#     print("Failed to connect to the database:", e)


# import pandas as pd
# from tkinter import Tk, filedialog, messagebox, Toplevel, Button, Frame, StringVar, OptionMenu, Label, Listbox, END
# from tkinter.ttk import Treeview
# from tkinter.simpledialog import askstring

# class CSVTool:
#     def __init__(self, master):
#         self.master = master
#         self.master.title("CSV 加工ツール")

#         # ヘッダー用フレーム
#         header_frame = Frame(master)
#         header_frame.pack(fill="x")

#         # エンコード選択用のドロップダウンメニュー
#         self.encoding_var = StringVar(value="utf-8")
#         encoding_options = ["utf-8", "shift_jis", "euc-jp", "cp932"]
#         self.encoding_menu = OptionMenu(header_frame, self.encoding_var, *encoding_options)
#         self.encoding_menu.pack(side="left", padx=5, pady=5)

#         # CSV開くボタン
#         self.load_button = Button(header_frame, text="CSVを開く", command=self.load_file)
#         self.load_button.pack(side="left", padx=5, pady=5)

#         # 保存ボタン
#         self.save_button = Button(header_frame, text="CSVを保存", command=self.save_csv)
#         self.save_button.pack(side="left", padx=5, pady=5)

#         # 列削除用のドロップダウンとボタン
#         self.delete_column_var = StringVar(value="列を選択")
#         self.delete_column_menu = OptionMenu(header_frame, self.delete_column_var, [])
#         self.delete_column_menu.pack(side="left", padx=5, pady=5)
#         self.delete_column_button = Button(header_frame, text="列を削除", command=self.remove_column)
#         self.delete_column_button.pack(side="left", padx=5, pady=5)

#         # データ型変更ボタン
#         self.change_type_button = Button(header_frame, text="データ型を変更", command=self.change_type_dialog)
#         self.change_type_button.pack(side="left", padx=5, pady=5)

#         # 履歴表示ボタン
#         self.view_history_button = Button(header_frame, text="履歴を表示", command=self.view_history)
#         self.view_history_button.pack(side="left", padx=5, pady=5)

#         # データ情報表示ラベル
#         self.data_info_label = Label(master, text="列数: 0 | データ数: 0", anchor="w")
#         self.data_info_label.pack(fill="x", padx=5, pady=5)

#         # Treeviewウィジェット
#         self.tree = Treeview(master, columns=["#"] + ["dummy"], show="headings")
#         self.tree.heading("#", text="#")
#         self.tree.pack(expand=True, fill="both")

#         # データ型を表示するTreeview
#         self.type_tree = Treeview(master, columns=["Column", "Type"], show="headings")
#         self.type_tree.heading("Column", text="列名")
#         self.type_tree.heading("Type", text="データ型")
#         self.type_tree.pack(fill="x")

#         # データフレームと履歴を保持
#         self.df = None
#         self.history = []  # 履歴を保持するリスト

#         # ショートカット: Ctrl+Zで元に戻す
#         self.master.bind("<Control-z>", lambda event: self.undo_last_action())

#     def load_file(self):
#         """CSVまたはExcelファイルを読み込む"""
#         file_path = filedialog.askopenfilename(filetypes=[("CSV/Excel files", "*.csv;*.xlsx;*.xls")])
#         if file_path:
#             encoding = self.encoding_var.get()
#             try:
#                 if file_path.endswith(('.xls', '.xlsx')):
#                     self.df = pd.read_excel(file_path)
#                 else:
#                     self.df = pd.read_csv(file_path, encoding=encoding)
#                 self.update_treeview()
#                 self.update_data_info()
#                 self.update_column_dropdown()
#                 messagebox.showinfo("情報", f"ファイルを読み込みました: {file_path}\nエンコード: {encoding}")
#             except Exception as e:
#                 messagebox.showerror("エラー", f"ファイルの読み込みに失敗しました: {e}")

#     def update_treeview(self):
#         """Treeviewをデータフレームの内容で更新"""
#         if self.df is not None:
#             self.tree.delete(*self.tree.get_children())
#             columns = ["#"] + list(self.df.columns)  # 行番号列を追加
#             self.tree["columns"] = columns
#             self.tree["show"] = "headings"

#             for col in columns:
#                 self.tree.heading(col, text=col)

#             for i, row in enumerate(self.df.itertuples(index=False), start=1):  # 行番号を追加
#                 self.tree.insert("", "end", values=(i, *row))

#             self.update_type_tree()

#     def update_type_tree(self):
#         """データ型Treeviewを更新"""
#         self.type_tree.delete(*self.type_tree.get_children())
#         if self.df is not None:
#             for col in self.df.columns:
#                 self.type_tree.insert("", "end", values=(col, self.df[col].dtype))

#     def update_data_info(self):
#         """データ情報ラベルを更新"""
#         if self.df is not None:
#             num_columns = len(self.df.columns)
#             num_rows = len(self.df)
#             self.data_info_label.config(text=f"列数: {num_columns} | データ数: {num_rows}")

#     def update_column_dropdown(self):
#         """列削除用ドロップダウンメニューを更新"""
#         if self.df is not None:
#             self.delete_column_menu["menu"].delete(0, "end")  # 既存の選択肢をクリア
#             for col in self.df.columns:
#                 self.delete_column_menu["menu"].add_command(
#                     label=col, command=lambda value=col: self.delete_column_var.set(value)
#                 )

#     def remove_column(self):
#         """選択された列を削除"""
#         if self.df is None:
#             messagebox.showerror("エラー", "ファイルを読み込んでください。")
#             return

#         column_name = self.delete_column_var.get()
#         if column_name not in self.df.columns:
#             messagebox.showerror("エラー", f"列 '{column_name}' は存在しません。")
#             return

#         self.history.append(("remove", column_name, self.df[column_name].copy()))
#         self.df = self.df.drop(columns=[column_name])
#         self.update_treeview()
#         self.update_data_info()
#         self.update_column_dropdown()
#         messagebox.showinfo("情報", f"列 '{column_name}' を削除しました。")

#     def change_type_dialog(self):
#         """データ型変更ダイアログを開く"""
#         if self.df is None:
#             messagebox.showerror("エラー", "データ型を変更する前にファイルを読み込んでください。")
#             return

#         selected_items = self.type_tree.selection()
#         if not selected_items:
#             messagebox.showerror("エラー", "データ型を変更する列を選択してください。")
#             return

#         selected_item = selected_items[0]
#         column_name = self.type_tree.item(selected_item, "values")[0]

#         new_type = askstring("データ型変更", f"'{column_name}' の新しいデータ型を入力してください (例: int, float, str)")
#         if not new_type:
#             messagebox.showinfo("情報", "型変更がキャンセルされました。")
#             return

#         try:
#             self.change_column_type(column_name, new_type)
#             self.update_type_tree()
#         except Exception as e:
#             messagebox.showerror("エラー", f"データ型の変更に失敗しました: {e}")

#     def change_column_type(self, column_name, new_type):
#         """列のデータ型を変更"""
#         if column_name in self.df.columns:
#             old_data = self.df[column_name].copy()
#             self.history.append(("type_change", column_name, old_data))
#             try:
#                 self.df[column_name] = self.df[column_name].astype(new_type)
#                 self.update_treeview()
#                 messagebox.showinfo("情報", f"列 '{column_name}' のデータ型を '{new_type}' に変更しました。")
#             except Exception as e:
#                 messagebox.showerror("エラー", f"データ型の変更に失敗しました: {e}")

#     def undo_last_action(self):
#         """最後の操作を元に戻す"""
#         if not self.history:
#             messagebox.showinfo("情報", "元に戻す操作がありません。")
#             return

#         action, column_name, data = self.history.pop()
#         if action == "remove":
#             self.df[column_name] = data
#         elif action == "type_change":
#             self.df[column_name] = data

#         self.update_treeview()
#         self.update_type_tree()
#         self.update_data_info()
#         messagebox.showinfo("情報", f"'{column_name}' に対する操作を元に戻しました。")

#     def view_history(self):
#         """履歴を表示"""
#         if not self.history:
#             messagebox.showinfo("情報", "履歴がありません。")
#             return

#         history_window = Toplevel(self.master)
#         history_window.title("操作履歴")

#         listbox = Listbox(history_window, selectmode="single")
#         listbox.pack(fill="both", expand=True)

#         for idx, (action, column_name, _) in enumerate(self.history):
#             action_str = {"add": "追加", "remove": "削除", "type_change": "型変更"}.get(action, action)
#             listbox.insert(END, f"{idx + 1}: {action_str} - {column_name}")

#         def restore_action():
#             """選択した履歴を復元"""
#             selected_idx = listbox.curselection()
#             if not selected_idx:
#                 messagebox.showerror("エラー", "復元する履歴を選択してください。")
#                 return

#             idx = selected_idx[0]
#             action, column_name, data = self.history.pop(idx)

#             if action == "remove":
#                 self.df[column_name] = data
#             elif action == "type_change":
#                 self.df[column_name] = data

#             self.update_treeview()
#             self.update_type_tree()
#             self.update_data_info()
#             listbox.delete(idx)
#             messagebox.showinfo("情報", f"操作 '{action}' が復元されました。")

#         restore_button = Button(history_window, text="復元する", command=restore_action)
#         restore_button.pack()

#     def save_csv(self):
#         """加工済みCSVを保存"""
#         if self.df is not None:
#             file_path = filedialog.asksaveasfilename(defaultextension=".csv", filetypes=[("CSV files", "*.csv")])
#             if file_path:
#                 self.df.to_csv(file_path, index=False)
#                 messagebox.showinfo("情報", f"加工済みファイルを保存しました: {file_path}")
#         else:
#             messagebox.showerror("エラー", "まずCSVファイルを読み込んでください。")


# if __name__ == "__main__":
#     root = Tk()
#     app = CSVTool(root)
#     root.mainloop()
