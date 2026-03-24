import tkinter as tk
from tkinter import ttk, messagebox
import datetime
import os

LOG_FILE = "done_log.txt"

# ─── Color Palette ───────────────────────────────────────────────
BG        = "#DEDEE0"
PANEL     = "#6A00FF"
CARD      = "#63666A"
ACCENT    = "#30D303"
ACCENT2   = "#F5A623"
TEXT      = "#EAEAEA"
SUBTEXT   = "#8892A4"
DONE_CLR  = "#2ECC71"
FONT_H    = ("Courier New", 18, "bold")
FONT_M    = ("Courier New", 12)
FONT_S    = ("Courier New", 10)
FONT_BTN  = ("Courier New", 11, "bold")


# ─── Utility ─────────────────────────────────────────────────────
def log_done(task_text: str):
    now = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    with open(LOG_FILE, "a", encoding="utf-8") as f:
        f.write(f"[{now}] ✓ {task_text}\n")


# ─── Main App ────────────────────────────────────────────────────
class TodoApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("✦ TO-DO LIST")
        self.geometry("600x700")
        self.resizable(False, False)
        self.configure(bg=BG)
        self.tasks: list[dict] = []   # {"text": str, "done": bool, "var": BooleanVar}
        self._build_ui()

    # ── UI Construction ──────────────────────────────────────────
    def _build_ui(self):
        # Header
        hdr = tk.Frame(self, bg=BG, pady=20)
        hdr.pack(fill="x")
        tk.Label(hdr, text="✦ TO-DO LIST", font=FONT_H,
                 bg=BG, fg=ACCENT).pack()
        tk.Label(hdr, text="track what matters", font=FONT_S,
                 bg=BG, fg=SUBTEXT).pack()

        # Input row
        inp_frame = tk.Frame(self, bg=PANEL, padx=16, pady=12)
        inp_frame.pack(fill="x", padx=20)

        self.entry_var = tk.StringVar()
        entry = tk.Entry(inp_frame, textvariable=self.entry_var,
                         font=FONT_M, bg=CARD, fg=TEXT,
                         insertbackground=ACCENT, relief="flat",
                         bd=0, highlightthickness=2,
                         highlightcolor=ACCENT,
                         highlightbackground=CARD)
        entry.pack(side="left", fill="x", expand=True, ipady=8, padx=(0, 10))
        entry.bind("<Return>", lambda e: self.add_task())

        btn_add = tk.Button(inp_frame, text="+ ADD", font=FONT_BTN,
                            bg=ACCENT, fg="white", relief="flat",
                            activebackground="#c73652", activeforeground="white",
                            cursor="hand2", padx=14, pady=6,
                            command=self.add_task)
        btn_add.pack(side="left")

        # Filter tabs
        tab_frame = tk.Frame(self, bg=BG, pady=8)
        tab_frame.pack(fill="x", padx=20)
        self.filter_var = tk.StringVar(value="all")
        for label, val in [("ALL", "all"), ("PENDING", "pending"), ("DONE", "done")]:
            rb = tk.Radiobutton(tab_frame, text=label, variable=self.filter_var,
                                value=val, command=self.refresh_list,
                                font=FONT_S, bg=BG, fg=SUBTEXT,
                                selectcolor=BG, activebackground=BG,
                                activeforeground=ACCENT,
                                indicatoron=False, relief="flat",
                                padx=12, pady=4,
                                cursor="hand2")
            rb.pack(side="left", padx=2)

        # Task list canvas (scrollable)
        list_outer = tk.Frame(self, bg=BG, padx=20)
        list_outer.pack(fill="both", expand=True, pady=(0, 10))

        self.canvas = tk.Canvas(list_outer, bg=BG, bd=0,
                                highlightthickness=0)
        self.canvas.pack(side="left", fill="both", expand=True)

        scrollbar = ttk.Scrollbar(list_outer, orient="vertical",
                                  command=self.canvas.yview)
        scrollbar.pack(side="right", fill="y")
        self.canvas.configure(yscrollcommand=scrollbar.set)
        self.canvas.bind("<Configure>",
                         lambda e: self.canvas.configure(
                             scrollregion=self.canvas.bbox("all")))
        self.canvas.bind_all("<MouseWheel>",
                             lambda e: self.canvas.yview_scroll(
                                 -1 * (e.delta // 120), "units"))

        self.list_frame = tk.Frame(self.canvas, bg=BG)
        self.canvas.create_window((0, 0), window=self.list_frame, anchor="nw")

        # Bottom bar
        bot = tk.Frame(self, bg=PANEL, padx=16, pady=10)
        bot.pack(fill="x", padx=20, pady=(0, 16))

        self.status_lbl = tk.Label(bot, text="0 tasks", font=FONT_S,
                                   bg=PANEL, fg=SUBTEXT)
        self.status_lbl.pack(side="left")

        tk.Button(bot, text="🗑 REMOVE DONE", font=FONT_BTN,
                  bg=CARD, fg=ACCENT2, relief="flat",
                  activebackground="#1a4a7a", activeforeground=ACCENT2,
                  cursor="hand2", padx=10, pady=4,
                  command=self.remove_done).pack(side="right", padx=(6, 0))

        tk.Button(bot, text="📋 VIEW LOG", font=FONT_BTN,
                  bg=CARD, fg=TEXT, relief="flat",
                  activebackground="#1a4a7a", activeforeground=TEXT,
                  cursor="hand2", padx=10, pady=4,
                  command=self.view_log).pack(side="right")

        self.refresh_list()

    # ── Task Operations ──────────────────────────────────────────
    def add_task(self):
        text = self.entry_var.get().strip()
        if not text:
            messagebox.showwarning("Empty Task", "Please enter a task first.")
            return
        self.tasks.append({"text": text, "done": False})
        self.entry_var.set("")
        self.refresh_list()

    def toggle_done(self, idx: int):
        task = self.tasks[idx]
        task["done"] = not task["done"]
        if task["done"]:
            log_done(task["text"])
        self.refresh_list()

    def remove_task(self, idx: int):
        self.tasks.pop(idx)
        self.refresh_list()

    def remove_done(self):
        before = len(self.tasks)
        self.tasks = [t for t in self.tasks if not t["done"]]
        removed = before - len(self.tasks)
        self.refresh_list()
        if removed:
            messagebox.showinfo("Removed", f"Removed {removed} completed task(s).")
        else:
            messagebox.showinfo("Nothing to Remove", "No completed tasks found.")

    # ── Refresh UI ───────────────────────────────────────────────
    def refresh_list(self):
        for w in self.list_frame.winfo_children():
            w.destroy()

        filt = self.filter_var.get()
        visible = [
            (i, t) for i, t in enumerate(self.tasks)
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

        total = len(self.tasks)
        done  = sum(1 for t in self.tasks if t["done"])
        self.status_lbl.config(
            text=f"{done}/{total} done"
        )

        self.list_frame.update_idletasks()
        self.canvas.configure(scrollregion=self.canvas.bbox("all"))

    def _task_card(self, orig_idx: int, task: dict, row: int):
        is_done = task["done"]
        card_bg  = "#0a2540" if is_done else CARD
        txt_fg   = DONE_CLR  if is_done else TEXT
        strike   = "overstrike" if is_done else ""

        card = tk.Frame(self.list_frame, bg=card_bg,
                        pady=10, padx=12, cursor="arrow")
        card.pack(fill="x", padx=0, pady=4)

        # Checkbox-style toggle button
        chk_sym  = "✓" if is_done else "○"
        chk_fg   = DONE_CLR if is_done else SUBTEXT
        chk_btn  = tk.Button(card, text=chk_sym, font=("Courier New", 14, "bold"),
                             bg=card_bg, fg=chk_fg, relief="flat", bd=0,
                             activebackground=card_bg, activeforeground=DONE_CLR,
                             cursor="hand2", width=2,
                             command=lambda idx=orig_idx: self.toggle_done(idx))
        chk_btn.pack(side="left", padx=(0, 8))

        # Task text
        lbl = tk.Label(card, text=task["text"],
                       font=("Courier New", 12, strike),
                       bg=card_bg, fg=txt_fg,
                       anchor="w", justify="left",
                       wraplength=440)
        lbl.pack(side="left", fill="x", expand=True)

        # Remove button
        del_btn = tk.Button(card, text="✕", font=("Courier New", 11, "bold"),
                            bg=card_bg, fg=ACCENT, relief="flat", bd=0,
                            activebackground=card_bg, activeforeground="#ff0000",
                            cursor="hand2",
                            command=lambda idx=orig_idx: self.remove_task(idx))
        del_btn.pack(side="right", padx=(8, 0))

    # ── Log Viewer ───────────────────────────────────────────────
    def view_log(self):
        win = tk.Toplevel(self)
        win.title("Done Log")
        win.geometry("560x420")
        win.configure(bg=BG)
        win.resizable(False, False)

        tk.Label(win, text="📋 COMPLETION LOG",
                 font=FONT_H, bg=BG, fg=ACCENT, pady=14).pack()

        frame = tk.Frame(win, bg=BG, padx=16, pady=0)
        frame.pack(fill="both", expand=True)

        txt = tk.Text(frame, font=FONT_S, bg=PANEL, fg=TEXT,
                      relief="flat", bd=0, wrap="word",
                      state="disabled")
        txt.pack(side="left", fill="both", expand=True)

        sb = ttk.Scrollbar(frame, orient="vertical", command=txt.yview)
        sb.pack(side="right", fill="y")
        txt.configure(yscrollcommand=sb.set)

        if os.path.exists(LOG_FILE):
            with open(LOG_FILE, encoding="utf-8") as f:
                content = f.read()
        else:
            content = "(No log yet. Mark tasks as done to start logging.)"

        txt.configure(state="normal")
        txt.insert("1.0", content)
        txt.configure(state="disabled")

        tk.Button(win, text="CLOSE", font=FONT_BTN,
                  bg=ACCENT, fg="white", relief="flat",
                  activebackground="#c73652", padx=16, pady=6,
                  cursor="hand2", command=win.destroy).pack(pady=12)


# ─── Run ─────────────────────────────────────────────────────────
if __name__ == "__main__":
    app = TodoApp()
    app.mainloop()