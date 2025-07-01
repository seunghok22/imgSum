import tkinter as tk
from tkinter import filedialog, messagebox
from readexcel import read_excel_file
from mkimgs import merge_file_lists, create_images_from_merge_list

class ExcelUploaderGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("엑셀 파일 업로드")
        self.root.geometry("1024x300")

        # 버튼 프레임
        button_frame = tk.Frame(root)
        button_frame.pack(pady=20)

        self.upload_btn = tk.Button(button_frame, text="엑셀 파일 업로드", command=self.upload_excel)
        self.upload_btn.pack(side=tk.LEFT, padx=20)

        self.output_btn = tk.Button(button_frame, text="출력 경로 선택", command=self.select_output_dir)
        self.output_btn.pack(side=tk.LEFT, padx=20)

        self.save_btn = tk.Button(button_frame, text="저장", command=self.save_images)
        self.save_btn.pack(side=tk.LEFT, padx=20)

        # 파일 라벨
        self.label = tk.Label(root, text="선택된 파일 없음", anchor='w', width=120)
        self.label.pack(padx=20, pady=(10, 5))

        # 출력 경로 라벨
        self.output_label = tk.Label(root, text="출력 경로가 선택되지 않았습니다", anchor='w', width=120)
        self.output_label.pack(padx=20, pady=(0, 10))

        # 이미지 개수 라벨
        self.count_label = tk.Label(root, text="고정이미지: 0개, 유동이미지 세트: 0개", anchor='w', width=120, fg='blue')
        self.count_label.pack(padx=20, pady=(10, 10))

        self.output_dir = None
        self.excel_loaded = False
        self.fixed_images = []
        self.moving_images = []

    def upload_excel(self):
        file_path = filedialog.askopenfilename(
            title="엑셀 파일 선택",
            filetypes=[("Excel files", "*.xlsx *.xls *.csv"), ("All files", "*.*")]
        )
        if file_path:
            self.label.config(text=f"선택된 파일: {file_path}")
            try:
                fixed_count, moving_count, fixed_images, moving_images = read_excel_file(file_path)
                self.fixed_images = fixed_images
                self.moving_images = moving_images
                self.count_label.config(
                    text=f"고정이미지: {fixed_count}개, 유동이미지 세트: {moving_count}개"
                )
                self.excel_loaded = True
            except Exception as e:
                self.count_label.config(
                    text=f"엑셀 파일을 읽는 중 오류 발생: {e}"
                )
                self.excel_loaded = False

    def select_output_dir(self):
        dir_path = filedialog.askdirectory(
            title="출력 폴더 선택"
        )
        if dir_path:
            self.output_dir = dir_path
            self.output_label.config(text=f"선택된 출력 경로: {dir_path}")

    def save_images(self):
        if not self.excel_loaded or not self.fixed_images or not self.moving_images:
            messagebox.showerror("오류", "엑셀 파일을 먼저 업로드하세요.")
            return
        if not self.output_dir:
            messagebox.showerror("오류", "출력 경로를 먼저 선택하세요.")
            return
        try:
            merge_list = merge_file_lists(self.fixed_images, self.moving_images)
            create_images_from_merge_list(merge_list, self.output_dir)
            messagebox.showinfo("완료", "이미지 저장이 완료되었습니다!")
        except Exception as e:
            messagebox.showerror("오류", f"이미지 저장 중 오류 발생: {e}")
