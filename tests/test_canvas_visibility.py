import tkinter as tk

class TestApp:
    def __init__(self, root):
        self.root = root
        self.canvas = tk.Canvas(root, bg='skyblue', highlightthickness=0)
        self.canvas.pack(fill='both', expand=True)

        self.canvas.create_oval(100, 100, 120, 120, fill='white', outline='')

        print("[CANVAS TEST] Canvas created and packed.")
        self.root.after(1000, self.print_canvas_info)

    def print_canvas_info(self):
        print("[CANVAS INFO]")
        print("  - width:", self.canvas.winfo_width())
        print("  - height:", self.canvas.winfo_height())
        print("  - viewable:", self.canvas.winfo_viewable())
        print("  - mapped:", self.canvas.winfo_ismapped())

root = tk.Tk()
root.geometry("400x300")
app = TestApp(root)
root.mainloop()
