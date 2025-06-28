import tkinter as tk
from tkinter import simpledialog

class DualInputDialog(simpledialog.Dialog):
    def body(self, master):
        tk.Label(master, text="제품 이미지의 배치위치(1 입력시 1번 고정이미지의 다음에 배치)\n유동이미지의 수는 1, 2, 3형식으로 입력하세요.", justify='left').grid(row=0, column=0, columnspan=2, sticky='w', pady=(0,10))
        tk.Label(master, text="위치:").grid(row=1)
        tk.Label(master, text="수량:").grid(row=2)

        self.position = tk.Entry(master)
        self.num = tk.Entry(master)

        self.position.grid(row=1, column=1)
        self.num.grid(row=2, column=1)
        return self.position  # 포커스

    def apply(self):
        num_list = [int(x.strip()) for x in self.num.get().split(", ") if x.strip()]
        self.result = {
            "position": self.position.get(),
            "num": num_list
        }
