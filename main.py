import tkinter as tk
from tkinter import ttk, messagebox
import datetime
import os

LOG_FILE = "done_log.txt"

# colors
BG = "#f0f0f0"
PANEL = "#d6d6d6"
ACCENT = "#53e15f"
ACCENT2 = "#357ABD"
CARD = "#ffffff"
TEXT = "#333333"
CROSS = "#ff0000"
DONE_CLR = "#53e15f"
SUBTEXT = "#747272"
FONT_H = ("Arial", 18)
FONT_M = ("Arial", 12)
FONT_S = ("Arial", 10)
FONT_BTN = ("Arial", 10, "bold")

def log_add(task_text: str):
        now = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        with open(LOG_FILE, "a", encoding="utf-8") as f:
            f.write(f"{now}  ADD          {task_text}\n")

def log_del(task_text: str):
        now = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        with open(LOG_FILE, "a", encoding="utf-8") as f:
            f.write(f"{now}  DELETE       {task_text}\n")

def log_done(task_text: str):
        now = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        with open(LOG_FILE, "a", encoding="utf-8") as f:
            f.write(f"{now}  DONE         {task_text}\n")

def log_del_done(task_text: str):
        now = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        with open(LOG_FILE, "a", encoding="utf-8") as f:
            f.write(f"{now}  REMOVE DONE  {task_text}\n")

class main_app(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("TO DO LIST")
        self.geometry("600x700")
        self.iconbitmap("img/logo.ico")
        self.resizable(False, False)
        self.configure(bg=BG)
        self.tasks: list[dict] = []
        self._build_frames()

    def _build_frames(self):
        self.frames = {}
        self.frames["home"] = home_page(self)
        self.frames["log"]  = log_viewer(self)
        self.show_frame("home")

    def show_frame(self, name: str):
        for frame in self.frames.values():
            frame.pack_forget()
        self.frames[name].pack(fill="both", expand=True)
    
class home_page(tk.Frame):
    def __init__(self, master):
        super().__init__(master, bg=BG)
        self.master_app = master
        self.build_ui()

    def build_ui(self):
        # Header
        header = tk.Frame(self, bg=BG, pady=20)
        header.pack(fill="x")
        tk.Label(header, text="TO DO LIST", font=FONT_H, bg=BG).pack()
        tk.Label(header, text="Enter the tasks to be done.", font=FONT_S, bg=BG).pack()

        # Input
        input_frame = tk.Frame(self, bg=BG, padx=20, pady=10)
        input_frame.pack(fill="x", padx=20)

        self.entry_var = tk.StringVar()
        entry = tk.Entry(input_frame, textvariable=self.entry_var,
                        font=FONT_M, bg=CARD, fg=TEXT,
                        relief="flat", bd=0, highlightthickness=2,
                        highlightbackground=CARD)
        entry.pack(side="left", fill="x", expand=True, ipady=8, padx=(0, 10))
        entry.bind("<Return>", lambda e: self.add_task())

        btn_add = tk.Button(input_frame, text="+ ADD", font=FONT_BTN,
                            bg=ACCENT, fg="white", relief="flat",
                            activebackground="#36c740", activeforeground="white",
                            cursor="hand2", padx=14, pady=6,
                            command=self.add_task)
        btn_add.pack(side="left")

        # Filter Tabs
        tab_frame = tk.Frame(self, bg=BG, pady=8)
        tab_frame.pack(fill="x", padx=20)
        self.filter_var = tk.StringVar(value="all")
        for label, val in [("ALL", "all"), ("PENDING", "pending"), ("DONE", "done")]:
            rb = tk.Radiobutton(tab_frame, text=label, variable=self.filter_var,
                                value=val, command=self.refresh_list,
                                font=FONT_S, bg=BG, fg=SUBTEXT,
                                selectcolor=BG, activebackground=BG,
                                indicatoron=False, relief="flat",
                                padx=12, pady=4,
                                cursor="hand2")
            rb.pack(side="left", padx=2)

        # Task List
        list_outer = tk.Frame(self, bg=BG)
        list_outer.pack(fill="both", expand=True, padx=20, pady=(0, 20))

        self.canvas = tk.Canvas(list_outer, bg=BG, highlightthickness=0)
        self.canvas.pack(side="left", fill="both", expand=True)

        scrollbar = ttk.Scrollbar(list_outer, orient="vertical", command=self.canvas.yview)
        scrollbar.pack(side="right", fill="y")
        self.canvas.configure(yscrollcommand=scrollbar.set)
        self.canvas.bind("<Configure>", lambda e: self.canvas.configure(scrollregion=self.canvas.bbox("all")))
        self.canvas.bind_all("<MouseWheel>", self. _on_mousewheel)

        self.list_frame = tk.Frame(self.canvas, bg=BG)
        self.canvas.create_window((0, 0), window=self.list_frame, anchor="nw")

        # Bottom bar
        bot = tk.Frame(self, bg=PANEL, padx=16, pady=10)
        bot.pack(fill="x", padx=20, pady=(0, 16))

        self.status_lbl = tk.Label(bot, text="0 tasks", font=FONT_S,
                                  bg=PANEL, fg=SUBTEXT)
        self.status_lbl.pack(side="left")

        self.btn_remove_done = tk.Button(bot, text="REMOVE DONE", font=FONT_BTN,
                                        bg=CARD, fg=TEXT, relief="flat",
                                        cursor="hand2", padx=10, pady=4,
                                        command=self.remove_done)

        self.btn_view_log = tk.Button(bot, text="VIEW LOG", font=FONT_BTN,
                                     bg=CARD, fg=TEXT, relief="flat",
                                     cursor="hand2", padx=10, pady=4,
                                     command=self.view_log)
        self.btn_view_log.pack(side="right")

        self.refresh_list()

    # check scroll
    def _on_mousewheel(self, event):
        if self.list_frame.winfo_height() > self.canvas.winfo_height():
            self.canvas.yview_scroll(int(-1 * (event.delta / 120)), "units")

    def add_task(self):
        text = self.entry_var.get().strip()
        if not text:
            messagebox.showwarning("Empty Task", "Please enter a task first.")
            return
        log_add(text)
        self.master_app.tasks.append({"text": text, "done": False})
        self.entry_var.set("")
        self.refresh_list()

    def toggle_done(self, idx: int):
        task = self.master_app.tasks[idx]
        task["done"] = not task["done"]
        if task["done"]:
            log_done(task["text"])
        self.refresh_list()

    def remove_task(self, idx: int):
        task = self.master_app.tasks[idx]
        log_del(task["text"])
        self.master_app.tasks.pop(idx)
        self.refresh_list()

    def remove_done(self):
        before = len(self.master_app.tasks)
        done_tasks = [t for t in self.master_app.tasks if t["done"]]
        self.master_app.tasks = [t for t in self.master_app.tasks if not t["done"]]
        removed = before - len(self.master_app.tasks)
        for t in done_tasks:
            log_del_done(t["text"])

        self.refresh_list()
    
        if removed > 0:
            messagebox.showinfo("Removed", f"Removed {removed} completed task(s).")
        else:
            messagebox.showinfo("Nothing to Remove", "No completed tasks found.")

    # task card
    def _task_card(self, orig_idx: int, task: dict, row: int):
        is_done = task["done"]
        card_bg  = "#ffffff" if is_done else CARD
        strike   = "overstrike" if is_done else ""

        card = tk.Frame(self.list_frame, bg=card_bg,
                        pady=10, padx=12, cursor="arrow")
        card.pack(fill="x", padx=0, pady=4)

        # Checkbox-style toggle button
        chk_sym  = "✓" if is_done else "○"
        chk_fg   = DONE_CLR if is_done else SUBTEXT
        chk_btn  = tk.Button(card, text=chk_sym, font=("Courier New", 14, "bold"),
                            bg=card_bg, fg=chk_fg, relief="flat", bd=0,
                            activebackground=card_bg, activeforeground=card_bg,
                            cursor="hand2", width=2,
                            command=lambda idx=orig_idx: self.toggle_done(idx))
        chk_btn.pack(side="left", padx=(0, 8))

        # Task text
        lbl = tk.Label(card, text=task["text"],
                      font=("Courier New", 12, strike),
                      bg=card_bg, fg=TEXT,
                      anchor="w", justify="left",
                      wraplength=440)
        lbl.pack(side="left", fill="x", expand=True)

        # Remove button
        del_btn = tk.Button(card, text="✕", font=("Courier New", 11, "bold"),
                            bg=card_bg, fg=CROSS, relief="flat", bd=0,
                            activebackground=card_bg, activeforeground=CROSS,
                            cursor="hand2",
                            command=lambda idx=orig_idx: self.remove_task(idx))
        del_btn.pack(side="right", padx=(8, 0))

    def refresh_list(self):
        for w in self.list_frame.winfo_children():
            w.destroy()

        filt = self.filter_var.get()
        visible = [
            (i, t) for i, t in enumerate(self.master_app.tasks)
            if filt == "all"
            or (filt == "done" and t["done"])
            or (filt == "pending" and not t["done"])
        ]
        if not visible:
            tk.Label(self.list_frame, text="— no tasks here —",
                    font=FONT_S, bg=BG, fg=SUBTEXT,
                    pady=30).pack()
        else:
            for i, (orig_idx, task) in enumerate(visible):
                    self._task_card(orig_idx, task, i)

        total = len(self.master_app.tasks)
        done  = sum(1 for t in self.master_app.tasks if t["done"])
        self.status_lbl.config(text=f"{done}/{total} done")

        # refresh_list
        if self.filter_var.get() == "done":
            self.btn_remove_done.pack(side="right", padx=(0, 10))
        else:
            self.btn_remove_done.pack_forget()

        self.list_frame.update_idletasks()
        self.canvas.configure(scrollregion=self.canvas.bbox("all"))
      
    # method view_log
    def view_log(self):
        self.master_app.frames["log"].reload()
        self.master_app.show_frame("log")

# log_viewer
class log_viewer(tk.Frame):
    def __init__(self, master):
        super().__init__(master, bg=BG)
        self.master_app = master
        self._build_ui()

    def _build_ui(self):
        header = tk.Frame(self, bg=BG, pady=20)
        header.pack(fill="x")
        tk.Label(header, text="COMPLETED TASKS LOG", font=FONT_H, bg=BG).pack()
        tk.Label(header, text="A record of all completed tasks.", font=FONT_S, bg=BG).pack()

        frame = tk.Frame(self, bg=BG, padx=12, pady=0)
        frame.pack(fill="both", expand=True)

        txt = tk.Text(frame, font=FONT_S, bg=PANEL, fg="black",
                      relief="flat", bd=0, wrap="word",
                      state="disabled", height=20)
        txt.pack(side="left", fill="both", expand=True)

        sb = ttk.Scrollbar(frame, orient="vertical", command=txt.yview)
        sb.pack(side="right", fill="y")
        txt.configure(yscrollcommand=sb.set)

        if os.path.exists(LOG_FILE):
            with open(LOG_FILE, encoding="utf-8") as f:
                content = f.read()
        else:
            content = "No log yet. Mark tasks as done to start logging."

        txt.configure(state="normal")
        txt.insert("1.0", content)
        txt.configure(state="disabled")

        tk.Button(self, text="BACK", font=FONT_BTN,
                  bg=CARD, fg=TEXT, relief="flat",
                  cursor="hand2", padx=10, pady=4,
                  command=lambda: self.master_app.show_frame("home")).pack(side="right", pady=20, padx=(0, 30))
            
    # reload
    def reload(self):
        for w in self.winfo_children():
            w.destroy()
        self._build_ui()

if __name__ == "__main__":
  app = main_app()
  app.mainloop()