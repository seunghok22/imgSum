import tkinter as tk
from tkinter import filedialog
import os
from PIL import Image, ImageTk

from popup import DualInputDialog
from img import save_combined_images
from scroll import ScrollableFrame

class ImageOrderApp:
    def __init__(self, root):
        self.root = root
        self.static_images = []
        self.flex_images = []
        self.static_thumbs = []
        self.flex_thumbs = []
        self.selected_static_idx = None
        self.selected_flex_idx = None

        self.position = 0
        self.num = 0

        # 중앙 배치를 위한 중간 프레임
        center_frame = tk.Frame(root)
        center_frame.pack(expand=True)  # 중앙에 배치

        # 고정이미지 스크롤 프레임 (가로 500)
        static_labelframe = tk.LabelFrame(center_frame, text="고정이미지 목록")
        static_labelframe.pack(padx=10, pady=5)
        self.static_scroll = ScrollableFrame(static_labelframe, width=600, height=250)
        self.static_scroll.pack()

        # 유동이미지 스크롤 프레임 (가로 500)
        flex_labelframe = tk.LabelFrame(center_frame, text="유동이미지 목록")
        flex_labelframe.pack(padx=10, pady=5)
        self.flex_scroll = ScrollableFrame(flex_labelframe, width=600, height=250)
        self.flex_scroll.pack()

        btn_frame = tk.Frame(root)
        btn_frame.pack()
        tk.Button(btn_frame, text="up", command=self.move_up).pack(side=tk.LEFT, padx=(5,0))
        tk.Button(btn_frame, text="down", command=self.move_down).pack(side=tk.LEFT)
        tk.Button(btn_frame, text="고정이미지 추가", command=self.add_statics).pack(side=tk.LEFT, padx=(5,30), pady=10)
        tk.Button(btn_frame, text="up", command=self.move_up_flex).pack(side=tk.LEFT)
        tk.Button(btn_frame, text="down", command=self.move_down_flex).pack(side=tk.LEFT)
        tk.Button(btn_frame, text="유동이미지 추가", command=self.add_flexs).pack(side=tk.LEFT, padx=(5,30))
        tk.Button(btn_frame, text="저장", command=self.save_images).pack(side=tk.LEFT, padx=(0,5))

        self.refresh_static_frame()
        self.refresh_flex_frame()

    def refresh_static_frame(self):
        for widget in self.static_scroll.inner_frame.winfo_children():
            widget.destroy()
        self.static_thumbs.clear()
        for idx, (img, fname) in enumerate(self.static_images):
            thumb = img.copy()
            thumb.thumbnail((40, 40))
            tk_img = ImageTk.PhotoImage(thumb)
            self.static_thumbs.append(tk_img)
            row = tk.Frame(self.static_scroll.inner_frame)
            row.pack(anchor='w', pady=2)
            bg = "#aeeeee" if self.selected_static_idx == idx else None
            row.config(bg=bg)
            def on_row_click(event, index=idx):
                self.selected_static_idx = index
                self.refresh_static_frame()
            row.bind("<Button-1>", on_row_click)
            img_label = tk.Label(row, image=tk_img, bg=bg)
            img_label.pack(side=tk.LEFT)
            img_label.bind("<Button-1>", on_row_click)
            txt_label = tk.Label(row, text=f"{idx+1}. {fname}", bg=bg)
            txt_label.pack(side=tk.LEFT, padx=5)
            txt_label.bind("<Button-1>", on_row_click)

    def refresh_flex_frame(self):
        for widget in self.flex_scroll.inner_frame.winfo_children():
            widget.destroy()
        self.flex_thumbs.clear()
        for idx, (img, fname) in enumerate(self.flex_images):
            thumb = img.copy()
            thumb.thumbnail((40, 40))
            tk_img = ImageTk.PhotoImage(thumb)
            self.flex_thumbs.append(tk_img)
            row = tk.Frame(self.flex_scroll.inner_frame)
            row.pack(anchor='w', pady=2)
            bg = "#aeeeee" if self.selected_flex_idx == idx else None
            row.config(bg=bg)
            def on_row_click(event, index=idx):
                self.selected_flex_idx = index
                self.refresh_flex_frame()
            row.bind("<Button-1>", on_row_click)
            img_label = tk.Label(row, image=tk_img, bg=bg)
            img_label.pack(side=tk.LEFT)
            img_label.bind("<Button-1>", on_row_click)
            txt_label = tk.Label(row, text=f"{idx+1}. {fname}", bg=bg)
            txt_label.pack(side=tk.LEFT, padx=5)
            txt_label.bind("<Button-1>", on_row_click)

    def add_statics(self):
        files = filedialog.askopenfilenames(
            filetypes=[("Image files", "*.png;*.jpg;*.jpeg;*.bmp;*.gif")]
        )
        for f in files:
            img = Image.open(f)
            self.static_images.append((img, os.path.basename(f)))
        self.refresh_static_frame()

    def add_flexs(self):
        files = filedialog.askopenfilenames(
            filetypes=[("Image files", "*.png;*.jpg;*.jpeg;*.bmp;*.gif")]
        )
        for f in files:
            img = Image.open(f)
            self.flex_images.append((img, os.path.basename(f)))
        self.refresh_flex_frame()

    def move_up(self):
        idx = self.selected_static_idx
        if idx is not None and idx > 0:
            self.static_images[idx-1], self.static_images[idx] = self.static_images[idx], self.static_images[idx-1]
            self.selected_static_idx -= 1
            self.refresh_static_frame()

    def move_down(self):
        idx = self.selected_static_idx
        if idx is not None and idx < len(self.static_images)-1:
            self.static_images[idx+1], self.static_images[idx] = self.static_images[idx], self.static_images[idx+1]
            self.selected_static_idx += 1
            self.refresh_static_frame()

    def move_up_flex(self):
        idx = self.selected_flex_idx
        if idx is not None and idx > 0:
            self.flex_images[idx-1], self.flex_images[idx] = self.flex_images[idx], self.flex_images[idx-1]
            self.selected_flex_idx -= 1
            self.refresh_flex_frame()

    def move_down_flex(self):
        idx = self.selected_flex_idx
        if idx is not None and idx < len(self.flex_images)-1:
            self.flex_images[idx+1], self.flex_images[idx] = self.flex_images[idx], self.flex_images[idx+1]
            self.selected_flex_idx += 1
            self.refresh_flex_frame()

    def save_images(self):
        dialog = DualInputDialog(self.root, title="이미지 순서와 갯수")
        self.position = int(dialog.result['position'])
        self.num = dialog.result['num']
        save_combined_images(self.static_images, self.flex_images, self.position, self.num)

