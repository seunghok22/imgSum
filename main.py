import tkinter as tk
import tkinter.font as tkFont
from gui import ImageOrderApp

if __name__ == "__main__":
    root = tk.Tk()
    app = ImageOrderApp(root)
    default_font = tkFont.nametofont("TkDefaultFont")
    default_font.configure(size=12)
    root.mainloop()