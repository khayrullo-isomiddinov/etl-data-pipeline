from pathlib import Path
import sqlite3
import tkinter as tk
from tkinter import ttk, scrolledtext

def show_database_gui():
    DB_PATH = Path(__file__).resolve().parents[1] / "databases" / "db_labels.db"
    
    try:
        con = sqlite3.connect(DB_PATH)
        cur = con.cursor()
        
        root = tk.Tk()
        root.title("Database Viewer")
        root.geometry("1000x700")
        
        notebook = ttk.Notebook(root)
        notebook.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        tables = cur.execute("SELECT name FROM sqlite_master WHERE type='table';").fetchall()
        
        for table_name, in tables:
            frame = ttk.Frame(notebook)
            notebook.add(frame, text=table_name)
            
            tree_frame = ttk.Frame(frame)
            tree_frame.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
            
            tree = ttk.Treeview(tree_frame)
            
            v_scroll = ttk.Scrollbar(tree_frame, orient=tk.VERTICAL, command=tree.yview)
            h_scroll = ttk.Scrollbar(tree_frame, orient=tk.HORIZONTAL, command=tree.xview)
            tree.configure(yscrollcommand=v_scroll.set, xscrollcommand=h_scroll.set)
            
            tree.grid(row=0, column=0, sticky='nsew')
            v_scroll.grid(row=0, column=1, sticky='ns')
            h_scroll.grid(row=1, column=0, sticky='ew')
            
            tree_frame.grid_rowconfigure(0, weight=1)
            tree_frame.grid_columnconfigure(0, weight=1)
            
            cur.execute(f"PRAGMA table_info({table_name});")
            columns = [col[1] for col in cur.fetchall()]
            
            tree['columns'] = columns
            tree.column('#0', width=0, stretch=tk.NO) 
            tree.heading('#0', text='')
            
            for col in columns:
                tree.column(col, anchor=tk.W, width=120)
                tree.heading(col, text=col, anchor=tk.W)
            
            data = cur.execute(f"SELECT * FROM {table_name};").fetchall()
            
            for i, row in enumerate(data):
                tree.insert('', tk.END, values=row, iid=i)
            
            count_label = ttk.Label(frame, text=f"Total rows: {len(data)}")
            count_label.pack(pady=5)
        
        con.close()
        
        status_bar = ttk.Label(root, text=f"Database: {DB_PATH.name} | Tables: {len(tables)}", relief=tk.SUNKEN, anchor=tk.W)
        status_bar.pack(side=tk.BOTTOM, fill=tk.X)
        
        root.mainloop()
        
    except Exception as e:
        error_root = tk.Tk()
        error_root.title("Error")
        error_text = scrolledtext.ScrolledText(error_root, width=80, height=10)
        error_text.pack(padx=10, pady=10)
        error_text.insert(tk.END, f"Error accessing database:\n{str(e)}")
        error_text.config(state=tk.DISABLED)
        error_root.mainloop()

if __name__ == "__main__":
    show_database_gui()