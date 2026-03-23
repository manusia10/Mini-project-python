import tkinter as tk
from tkinter import ttk, messagebox

from main1 import ACCENT, CARD, TEXT

LOG_FILE = "done_log.txt"

# colors
BG = "#f0f0f0"
PANEL = "#d6d6d6"
FONT_H = ("Arial", 18)
FONT_M = ("Arial", 12)
FONT_S = ("Arial", 10)
class main_app(tk.Tk):
  def __init__(self):
    super().__init__()
    self.title("TO DO LIST")
    self.geometry("600x700")
    self.iconbitmap("img/logo.ico")
    self.resizable(False, False)
    self.configure(bg=BG)
    self.tasks: list[dict] = []
    self._build_ui()

  def _build_ui(self):
    # Header
    header = tk.Frame(self, bg=BG, pady=20)
    header.pack(fill="x")
    tk.Label(header, text="TO DO LIST", font=FONT_H, bg=BG).pack()
    tk.Label(header, text="Enter the tasks to be done.", font=FONT_S, bg=BG).pack()

    # Input
    input_frame = tk.Frame(self, bg=PANEL,padx=20, pady=10)
    input_frame.pack(fill="x", padx=20)

    self.entry_var = tk.StringVar()
    entry = tk.Entry(input_frame, textvariable=self.entry_var,
      font=FONT_M, bg=CARD, fg=TEXT,
      insertbackground=ACCENT, relief="flat",
      bd=0, highlightthickness=2,
      highlightcolor=ACCENT,
      highlightbackground=CARD)

if __name__ == "__main__":
  app = main_app()
  app.mainloop()