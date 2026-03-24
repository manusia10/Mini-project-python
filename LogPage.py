#LOGPAGE 

import tkinter as tk
import os
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

  #use this size only
  def __init__(self):
    super().__init__()
    self.withdraw()
    self.title("Logs Page")
    self.geometry("600x700")
    self.iconbitmap("img/logo.ico")
    self.resizable(False, False)
    self.configure(bg=BG)
    self.tasks: list[dict] = []
    #button
    self.btn = tk.Frame(self, bg=BG)
    self.btn.pack(fill="x", pady=10, padx=8,side="bottom") 
    self._build_ui()
    self.gobackBTN() #สำหรับย้อนกลับไปหน้า Main
    self.deiconify()


  def _build_ui(self):
    window = tk.Frame(self, bg=BG, pady=20)
    window.pack(fill="both", expand=True, side="top")
    
    title_label = tk.Label(window, text="FOR SUCCESS", font=FONT_H, bg=BG)
    title_label.pack()
    title_label = tk.Label(window, text="Congratulations! You completed your To-Do List!\n", font=FONT_S, bg=BG)
    title_label.pack()
    
    frame = tk.Frame(window, bg=BG, padx=12, pady=0)
    frame.pack(fill="both", expand=True) #fill= "both"ให้ frame ขยายทั้งเเนวตั้งเเนวนอน"
    
    txt = tk.Text(frame, font=FONT_S, bg=PANEL, fg="black",relief="flat", bd=0, wrap="word", state="disabled", height=20)
    txt.pack(side="left", fill="both", expand=True)

    #scrollbar 
    sb = ttk.Scrollbar(frame, orient="vertical", command=txt.yview)
    sb.pack(side="right", fill="y") #ยึดไว้ด้านขวา
    txt.configure(yscrollcommand=sb.set) #เชื่อมกันระหว่างการเลื่อน

    #เช็คว่า Logfile มีจริงไหม
    if os.path.exists(LOG_FILE):
      #มีไฟล์ ให้เปิดไฟล์เเบบอ่าน
      with open(LOG_FILE, encoding="utf-8") as f:
        content = f.read()
    else:
      content = "(No log yet. Mark tasks as done to start logging.)"

    txt.configure(state="normal");
    txt.insert("1.0", content)
    txt.configure(state="disabled")
    print("Welcome to log")


    #Start: buttonLog
  def gobackBTN(self):
    tk.Button(self.btn, text="Go back to main", 
                  bg=CARD, fg=TEXT, relief="flat",
                  activebackground="#1a4a7a", activeforeground=TEXT,
                  cursor="hand2", padx=10, pady=4,
                  command=self.goBack).pack(side="right")
                  #command send to def view_log
#End: buttonLog
    
  def goBack(self):
    print("Welcome back to main")




if __name__ == "__main__":
  app = main_app()
  app.mainloop()