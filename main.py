# main.py
from main_gui import StockPredictionApp
import tkinter as tk

if __name__ == "__main__":
    root = tk.Tk()
    app = StockPredictionApp(root)
    root.mainloop()
