import tkinter as tk

def animate():
    print("[TEST] animate called")
    root.after(1000, animate)

root = tk.Tk()
root.after(1000, animate)
root.mainloop()
