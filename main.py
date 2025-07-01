import tkinter as tk
from gui import ExcelUploaderGUI

def main():
    root = tk.Tk()
    app = ExcelUploaderGUI(root)
    root.mainloop()

if __name__ == "__main__":
    main()