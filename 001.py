import tkinter as tk
from tkinter import filedialog, messagebox
from PIL import Image, ImageTk
import os
import sys


class RankerApp:
    def __init__(self, root):
        # 设置主窗口
        self.root = root
        self.root.title("从夯到拉排行器")
        self.root.geometry("1000x600")
        self.root.resizable(True, True)

        # 存储图片路径和它们的分类
        self.images = []  # 格式: (图片路径, 分类索引, 缩略图对象)
        self.categories = ["夯", "顶级", "人上人", "NPC", "拉完了"]
        self.category_colors = [
            "#FF0000",  # 红色 - 夯
            "#FF7F00",  # 橙色 - 顶级
            "#FFFF00",  # 黄色 - 人上人
            "#FFFFCC",  # 浅黄色 - NPC
            "#C0C0C0"  # 灰色 - 拉完了
        ]

        # 当前选中的图片
        self.selected_image = None
        self.selected_thumbnail = None
        self.popup_window = None  # 用于悬浮展示的窗口

        # 解决双击运行出现输入框的问题
        self.root.withdraw()  # 先隐藏主窗口
        self.root.after(100, self.create_base_ui)  # 延迟显示主界面

    def create_base_ui(self):
        """创建初始界面，包含开始和退出按钮"""
        # 显示主窗口
        self.root.deiconify()

        # 清空当前窗口
        for widget in self.root.winfo_children():
            widget.destroy()

        # 创建标题
        title_label = tk.Label(self.root, text="从夯到拉排行器", font=("SimHei", 24, "bold"))
        title_label.pack(pady=50)

        # 创建按钮框架
        button_frame = tk.Frame(self.root)
        button_frame.pack(expand=True)

        # 开始按钮
        start_button = tk.Button(
            button_frame,
            text="开始",
            font=("SimHei", 16),
            width=15,
            height=2,
            command=self.start_ranking
        )
        start_button.pack(pady=20)

        # 退出按钮
        exit_button = tk.Button(
            button_frame,
            text="退出",
            font=("SimHei", 16),
            width=15,
            height=2,
            command=self.root.quit
        )
        exit_button.pack(pady=10)

    def start_ranking(self):
        """开始排行，提示用户导入图片"""
        messagebox.showinfo("提示", "请导入图片")
        self.import_images()

    def import_images(self):
        """打开文件选择对话框，让用户选择图片"""
        file_paths = filedialog.askopenfilenames(
            title="选择图片",
            filetypes=[
                ("图片文件", "*.png;*.jpg;*.jpeg;*.bmp;*.gif"),
                ("所有文件", "*.*")
            ]
        )

        if file_paths:
            # 处理选中的图片
            for path in file_paths:
                # 检查图片是否已导入
                if not any(img_path == path for img_path, _, _ in self.images):
                    # 创建缩略图
                    thumbnail = self.create_thumbnail(path)
                    self.images.append((path, None, thumbnail))

            # 显示排行界面
            self.create_ranking_ui()
        else:
            # 如果没有选择图片，返回基础界面
            messagebox.showwarning("警告", "没有选择任何图片")

    def create_thumbnail(self, image_path, size=(100, 100)):
        """创建图片的缩略图"""
        try:
            img = Image.open(image_path)
            img.thumbnail(size)
            return ImageTk.PhotoImage(img)
        except Exception as e:
            messagebox.showerror("错误", f"无法打开图片 {image_path}: {str(e)}")
            return None

    def create_ranking_ui(self):
        """创建排行界面"""
        # 清空当前窗口
        for widget in self.root.winfo_children():
            widget.destroy()

        # 创建顶部按钮栏
        top_frame = tk.Frame(self.root)
        top_frame.pack(fill=tk.X, padx=10, pady=5)  # 减少顶部间距

        # 返回按钮
        back_button = tk.Button(top_frame, text="撤", command=self.create_base_ui)
        back_button.pack(side=tk.LEFT)

        # 导入更多图片按钮
        import_button = tk.Button(top_frame, text="导入更多图片", command=self.import_images)
        import_button.pack(side=tk.RIGHT)

        # 创建主容器
        main_container = tk.Frame(self.root)
        main_container.pack(fill=tk.BOTH, expand=True, padx=10, pady=0)  # 去掉主容器上下边距

        # 创建分类行
        self.category_frames = []
        for i, (category, color) in enumerate(zip(self.categories, self.category_colors)):
            # 创建行框架 - 去掉边框
            row_frame = tk.Frame(main_container)
            row_frame.pack(fill=tk.X, pady=0)  # 去掉行间距

            # 分类标签（带底色）
            cat_label = tk.Label(
                row_frame,
                text=category,
                bg=color,
                font=("SimHei", 12, "bold"),
                width=10,
                height=5,
                cursor="hand2"
            )
            cat_label.pack(side=tk.LEFT, padx=5)
            cat_label.bind("<Button-1>", lambda e, idx=i: self.assign_category(idx))

            # 固定行宽度：用 Canvas+Frame 组合
            img_wrap_frame = tk.Frame(row_frame)
            img_wrap_frame.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=5)

            img_canvas = tk.Canvas(img_wrap_frame, height=120)
            img_scrollbar = tk.Scrollbar(img_wrap_frame, orient=tk.HORIZONTAL, command=img_canvas.xview)
            img_container = tk.Frame(img_canvas)

            img_container.bind(
                "<Configure>",
                lambda e, c=img_canvas: c.configure(scrollregion=c.bbox("all"))
            )

            img_canvas.create_window((0, 0), window=img_container, anchor=tk.NW)
            img_canvas.configure(xscrollcommand=img_scrollbar.set)

            img_canvas.pack(side=tk.LEFT, fill=tk.X, expand=True)
            img_scrollbar.pack(side=tk.BOTTOM, fill=tk.X)

            self.category_frames.append(img_container)

        # 创建未分类区域
        uncat_frame = tk.Frame(main_container)
        uncat_frame.pack(fill=tk.X, pady=5)  # 只保留少量间距

        uncat_label = tk.Label(
            uncat_frame,
            text="未分类",
            bg="#FFFFFF",
            font=("SimHei", 12, "bold"),
            width=10,
            height=2
        )
        uncat_label.pack(side=tk.LEFT, padx=5)

        # 未分类区域固定宽度
        uncat_wrap_frame = tk.Frame(uncat_frame)
        uncat_wrap_frame.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=5)

        uncat_canvas = tk.Canvas(uncat_wrap_frame, height=120)
        uncat_scrollbar = tk.Scrollbar(uncat_wrap_frame, orient=tk.HORIZONTAL, command=uncat_canvas.xview)
        self.uncategorized_container = tk.Frame(uncat_canvas)

        self.uncategorized_container.bind(
            "<Configure>",
            lambda e, c=uncat_canvas: c.configure(scrollregion=c.bbox("all"))
        )

        uncat_canvas.create_window((0, 0), window=self.uncategorized_container, anchor=tk.NW)
        uncat_canvas.configure(xscrollcommand=uncat_scrollbar.set)

        uncat_canvas.pack(side=tk.LEFT, fill=tk.X, expand=True)
        uncat_scrollbar.pack(side=tk.BOTTOM, fill=tk.X)

        # 更新显示
        self.update_display()

    def update_display(self):
        """更新界面上的图片显示"""
        # 清空所有容器
        for container in self.category_frames + [self.uncategorized_container]:
            for widget in container.winfo_children():
                widget.destroy()

        # 显示已分类的图片
        for img_path, category_idx, thumbnail in self.images:
            if category_idx is not None and 0 <= category_idx < len(self.categories):
                # 在对应分类行显示图片
                if thumbnail:
                    img_label = tk.Label(self.category_frames[category_idx], image=thumbnail)
                    img_label.image = thumbnail  # 保持引用
                    img_label.pack(side=tk.LEFT, padx=5, pady=5)
                    img_label.bind("<Button-1>", lambda e, path=img_path: self.show_image_popup(path))
                    # 防止双击出现文本框
                    img_label.bind("<Double-1>", lambda e: "break")
            elif category_idx is None:
                # 显示未分类的图片
                if thumbnail:
                    img_label = tk.Label(self.uncategorized_container, image=thumbnail)
                    img_label.image = thumbnail  # 保持引用
                    img_label.pack(side=tk.LEFT, padx=5, pady=5)
                    img_label.bind("<Button-1>", lambda e, path=img_path: self.show_image_popup(path))
                    # 防止双击出现文本框
                    img_label.bind("<Double-1>", lambda e: "break")

    def show_image_popup(self, image_path):
        """显示图片的悬浮放大窗口"""
        # 关闭已有的悬浮窗口
        if self.popup_window:
            self.popup_window.destroy()

        # 找到选中的图片索引
        for i, (path, _, _) in enumerate(self.images):
            if path == image_path:
                self.selected_image = i
                break

        # 创建新的悬浮窗口
        self.popup_window = tk.Toplevel(self.root)
        self.popup_window.title("")
        self.popup_window.geometry("400x400")

        # 计算居中位置
        x = self.root.winfo_x() + (self.root.winfo_width() // 2) - 200
        y = self.root.winfo_y() + (self.root.winfo_height() // 2) - 200
        self.popup_window.geometry(f"+{x}+{y}")

        # 显示放大的图片
        try:
            original_img = Image.open(image_path)

            # 调整大小为界面的四分之一
            max_size = (self.root.winfo_width() // 2, self.root.winfo_height() // 2)
            original_img.thumbnail(max_size)
            large_img = ImageTk.PhotoImage(original_img)

            img_label = tk.Label(self.popup_window, image=large_img)
            img_label.image = large_img  # 保持引用
            img_label.pack(expand=True)

            # 添加提示信息
            info_label = tk.Label(
                self.popup_window,
                text="点击分类标签将图片移动到对应类别",
                font=("SimHei", 10)
            )
            info_label.pack(pady=5)

        except Exception as e:
            messagebox.showerror("错误", f"无法显示图片: {str(e)}")
            self.popup_window.destroy()

    def assign_category(self, category_idx):
        """将选中的图片分配到指定的分类"""
        if self.selected_image is not None and 0 <= category_idx < len(self.categories):
            # 更新图片的分类
            img_path, _, thumbnail = self.images[self.selected_image]
            self.images[self.selected_image] = (img_path, category_idx, thumbnail)

            # 关闭悬浮窗口
            if self.popup_window:
                self.popup_window.destroy()
                self.popup_window = None

            # 取消选择
            self.selected_image = None

            # 更新显示
            self.update_display()


def resource_path(relative_path):
    """获取资源的绝对路径，用于打包后的应用"""
    try:
        # PyInstaller创建临时文件夹，并将路径存储在_MEIPASS
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")

    return os.path.join(base_path, relative_path)


if __name__ == "__main__":
    # 解决双击运行出现额外输入框的问题
    root = tk.Tk()
    # 确保中文显示正常
    app = RankerApp(root)
    root.mainloop()
