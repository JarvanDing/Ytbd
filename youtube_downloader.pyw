import os
import subprocess
import tkinter as tk
from tkinter import ttk, messagebox, filedialog
from threading import Thread
from pathlib import Path
import sys
import json

# 在 Windows 上隐藏控制台窗口
if sys.platform.startswith('win'):
    import ctypes
    ctypes.windll.user32.ShowWindow(ctypes.windll.kernel32.GetConsoleWindow(), 0)

def get_application_path():
    """获取应用程序的实际运行路径"""
    if getattr(sys, 'frozen', False):
        # 如果是打包后的程序
        return os.path.dirname(sys.executable)
    else:
        # 如果是源代码运行
        return os.path.dirname(os.path.abspath(__file__))

class Theme:
    """主题类，定义不同的颜色方案"""
    
    DARK_MODERN = {
        'name': '深色现代',
        'bg': '#1E1E1E',
        'fg': '#FFFFFF',
        'accent': '#007ACC',
        'secondary': '#252526',
        'text': '#CCCCCC',
        'border': '#333333',
        'button': '#0E639C',
        'button_fg': '#FFFFFF',
        'hover': '#1177BB',
        'entry_bg': '#3C3C3C',
        'font': ('微软雅黑', 9)
    }
    
    LIGHT_MINIMAL = {
        'name': '浅色简约',
        'bg': '#FFFFFF',
        'fg': '#000000',
        'accent': '#2196F3',
        'secondary': '#F5F5F5',
        'text': '#424242',
        'border': '#E0E0E0',
        'button': '#2196F3',
        'button_fg': '#FFFFFF',
        'hover': '#1976D2',
        'entry_bg': '#FFFFFF',
        'font': ('微软雅黑', 9)
    }
    
    TECH_BLUE = {
        'name': '科技蓝',
        'bg': '#1A2933',
        'fg': '#E1E1E1',
        'accent': '#00B0FF',
        'secondary': '#233240',
        'text': '#B8B8B8',
        'border': '#2C4356',
        'button': '#0091EA',
        'button_fg': '#FFFFFF',
        'hover': '#00A0F0',
        'entry_bg': '#2C4356',
        'font': ('微软雅黑', 9)
    }
    
    NIGHT_PURPLE = {
        'name': '暗夜紫',
        'bg': '#2D1B69',
        'fg': '#FFFFFF',
        'accent': '#9C27B0',
        'secondary': '#1E1246',
        'text': '#E1E1E1',
        'border': '#3D2B79',
        'button': '#7B1FA2',
        'button_fg': '#FFFFFF',
        'hover': '#8E24AA',
        'entry_bg': '#3D2B79',
        'font': ('微软雅黑', 9)
    }
    
    NATURE_GREEN = {
        'name': '自然绿',
        'bg': '#F5F9F0',
        'fg': '#2E7D32',
        'accent': '#4CAF50',
        'secondary': '#E8F5E9',
        'text': '#1B5E20',
        'border': '#A5D6A7',
        'button': '#4CAF50',
        'button_fg': '#FFFFFF',
        'hover': '#43A047',
        'entry_bg': '#FFFFFF',
        'font': ('微软雅黑', 9)
    }
    
    @classmethod
    def get_all_themes(cls):
        return [cls.DARK_MODERN, cls.LIGHT_MINIMAL, cls.TECH_BLUE, 
                cls.NIGHT_PURPLE, cls.NATURE_GREEN]

class YouTubeDownloader:
    def __init__(self, root):
        self.root = root
        self.root.title("YouTube 下载器")
        
        # 获取应用程序路径
        self.app_path = get_application_path()
        
        # 设置窗口大小和位置
        window_width = 420
        window_height = 480
        screen_width = root.winfo_screenwidth()
        screen_height = root.winfo_screenheight()
        center_x = int(screen_width/2 - window_width/2)
        center_y = int(screen_height/2 - window_height/2)
        self.root.geometry(f'{window_width}x{window_height}+{center_x}+{center_y}')
        
        # 加载上次使用的主题或使用默认主题
        self.current_theme = self.load_theme() or Theme.NATURE_GREEN
        
        # 初始化界面
        self.setup_theme()
        self.create_widgets()
        
    def load_theme(self):
        """加载保存的主题设置"""
        try:
            theme_file = os.path.join(self.app_path, 'theme_settings.json')
            if os.path.exists(theme_file):
                with open(theme_file, 'r') as f:
                    theme_name = json.load(f)['theme']
                    return next((theme for theme in Theme.get_all_themes() 
                               if theme['name'] == theme_name), None)
        except:
            return None
            
    def save_theme(self):
        """保存主题设置"""
        theme_file = os.path.join(self.app_path, 'theme_settings.json')
        with open(theme_file, 'w') as f:
            json.dump({'theme': self.current_theme['name']}, f)
            
    def setup_theme(self):
        """设置主题样式"""
        style = ttk.Style()
        style.theme_use('clam')  # 使用clam主题作为基础
        
        # 配置全局样式
        self.root.configure(bg=self.current_theme['bg'])
        
        # 配置框架样式
        style.configure('TFrame', background=self.current_theme['bg'])
        
        # 标准标签样式
        style.configure('TLabel',
                       background=self.current_theme['bg'],
                       foreground=self.current_theme['fg'],
                       font=self.current_theme['font'])
        
        # 标题标签样式
        style.configure('Title.TLabel',
                       background=self.current_theme['bg'],
                       foreground=self.current_theme['accent'],
                       font=('微软雅黑', 16, 'bold'))
        
        # 按钮样式
        style.configure('TButton',
                       background=self.current_theme['button'],
                       foreground=self.current_theme['button_fg'],
                       font=self.current_theme['font'])
        
        # 主按钮样式
        style.configure('Accent.TButton',
                       background=self.current_theme['accent'],
                       foreground=self.current_theme['button_fg'],
                       font=('微软雅黑', 9, 'bold'))
        
        # 输入框样式
        style.configure('TEntry',
                       fieldbackground=self.current_theme['entry_bg'],
                       foreground=self.current_theme['text'],
                       insertcolor=self.current_theme['text'])
        
        # 下拉框样式
        style.configure('TCombobox',
                       fieldbackground=self.current_theme['entry_bg'],
                       foreground=self.current_theme['text'],
                       selectbackground=self.current_theme['accent'],
                       selectforeground=self.current_theme['button_fg'])
        
        # 单选按钮样式
        style.configure('TRadiobutton',
                       background=self.current_theme['bg'],
                       foreground=self.current_theme['fg'],
                       font=self.current_theme['font'])
        
        # 标签框架样式
        style.configure('TLabelframe',
                       background=self.current_theme['bg'],
                       foreground=self.current_theme['fg'])
        style.configure('TLabelframe.Label',
                       background=self.current_theme['bg'],
                       foreground=self.current_theme['fg'],
                       font=self.current_theme['font'])
        
        # 进度条样式
        style.configure('Horizontal.TProgressbar',
                       background=self.current_theme['accent'],
                       troughcolor=self.current_theme['secondary'])
        
        # 按钮悬停效果
        style.map('TButton',
                  background=[('active', self.current_theme['hover'])],
                  foreground=[('active', self.current_theme['button_fg'])])
        
        style.map('Accent.TButton',
                  background=[('active', self.current_theme['hover'])],
                  foreground=[('active', self.current_theme['button_fg'])])
        
        # 单选按钮悬停效果
        style.map('TRadiobutton',
                  background=[('active', self.current_theme['bg'])],
                  foreground=[('active', self.current_theme['accent'])])
        
        # 下拉框悬停效果
        style.map('TCombobox',
                  fieldbackground=[('readonly', self.current_theme['entry_bg']),
                                 ('active', self.current_theme['hover'])],
                  selectbackground=[('readonly', self.current_theme['accent'])],
                  selectforeground=[('readonly', self.current_theme['button_fg'])])
        
    def change_theme(self, theme):
        """切换主题"""
        self.current_theme = theme
        self.setup_theme()
        self.save_theme()
        # 重新创建界面
        self.recreate_widgets()
        
    def create_theme_menu(self):
        """创建主题选择菜单"""
        menu_frame = ttk.Frame(self.root)
        menu_frame.pack(fill='x', padx=10, pady=5)
        
        # 左侧主题选择
        theme_frame = ttk.Frame(menu_frame)
        theme_frame.pack(side='left')
        
        ttk.Label(theme_frame, text="主题:").pack(side='left', padx=(0, 5))
        theme_var = tk.StringVar(value=self.current_theme['name'])
        theme_combo = ttk.Combobox(theme_frame, 
                                 textvariable=theme_var,
                                 values=[theme['name'] for theme in Theme.get_all_themes()],
                                 state='readonly',
                                 width=10)
        theme_combo.pack(side='left')
        
        # 右侧更新按钮
        update_btn = ttk.Button(menu_frame, 
                               text="检查更新",
                               command=self.check_and_update_tools)
        update_btn.pack(side='right', padx=5)
        
        def on_theme_change(event):
            selected_theme = next(theme for theme in Theme.get_all_themes() 
                                if theme['name'] == theme_var.get())
            self.change_theme(selected_theme)
            
        theme_combo.bind('<<ComboboxSelected>>', on_theme_change)
        
    def create_widgets(self):
        """创建界面控件"""
        # 创建主题选择菜单
        self.create_theme_menu()
        
        # 主框架
        main_frame = ttk.Frame(self.root)
        main_frame.pack(expand=True, fill='both', padx=20, pady=10)
        
        # 检查必要文件
        self.yt_dlp_path = self.get_yt_dlp_path()
        self.ffmpeg_path = self.get_ffmpeg_path()
        
        if not self.yt_dlp_path:
            messagebox.showerror("错误", "找不到 yt-dlp，请确保已正确安装")
            root.destroy()
            return
            
        if not self.ffmpeg_path:
            messagebox.showwarning("警告", "找不到 FFmpeg，视频将无法合并！")
        
        # 设置默认下载目录
        self.download_dir = self.app_path
        
        # 标题
        title = ttk.Label(main_frame, 
                         text="YouTube 视频下载器", 
                         style='Title.TLabel')
        title.grid(row=0, column=0, columnspan=3, pady=(0, 20))
        
        # URL输入区域
        url_frame = ttk.Frame(main_frame)
        url_frame.grid(row=1, column=0, columnspan=3, sticky='ew', pady=(0, 15))
        url_frame.columnconfigure(1, weight=1)
        
        ttk.Label(url_frame, text="视频链接:").grid(row=0, column=0, padx=(0, 10))
        self.url_var = tk.StringVar()
        url_entry = ttk.Entry(url_frame, textvariable=self.url_var)
        url_entry.grid(row=0, column=1, sticky='ew')
        
        # 设置区域
        settings_frame = ttk.LabelFrame(main_frame, text="下载设置", padding=15)
        settings_frame.grid(row=2, column=0, columnspan=3, sticky='ew', pady=(0, 15))
        settings_frame.columnconfigure(1, weight=1)
        
        # 保存位置
        ttk.Label(settings_frame, text="保存位置:").grid(row=0, column=0, sticky='w', padx=(0, 10))
        self.dir_var = tk.StringVar(value=self.download_dir)
        ttk.Entry(settings_frame, textvariable=self.dir_var).grid(row=0, column=1, sticky='ew')
        ttk.Button(settings_frame, text="浏览", command=self.choose_directory).grid(row=0, column=2, padx=(10, 0))
        
        # Cookies设置
        ttk.Label(settings_frame, text="Cookies:").grid(row=1, column=0, sticky='w', padx=(0, 10), pady=(10, 0))
        self.cookies_var = tk.StringVar(value=os.path.join(self.app_path, "cookies.txt"))
        cookies_entry = ttk.Entry(settings_frame, textvariable=self.cookies_var)
        cookies_entry.grid(row=1, column=1, sticky='ew', pady=(10, 0))
        
        # Cookies按钮框架
        cookies_btn_frame = ttk.Frame(settings_frame)
        cookies_btn_frame.grid(row=1, column=2, padx=(10, 0), pady=(10, 0))
        
        # 选择文件按钮
        cookies_file_btn = ttk.Button(cookies_btn_frame, text="选择", command=self.choose_cookies, width=6)
        cookies_file_btn.pack(side='left', padx=(0, 5))
        cookies_file_btn.bind('<Button-3>', self.show_cookies_help)  # 右键显示帮助
        
        # 粘贴按钮
        cookies_paste_btn = ttk.Button(cookies_btn_frame, text="粘贴", command=self.paste_cookies, width=6)
        cookies_paste_btn.pack(side='left')
        
        # 下载选项区域
        options_frame = ttk.LabelFrame(main_frame, text="下载选项", padding=15)
        options_frame.grid(row=3, column=0, columnspan=3, sticky='ew', pady=(0, 15))
        
        # 格式选择
        format_frame = ttk.Frame(options_frame)
        format_frame.grid(row=0, column=0, columnspan=2)
        
        self.format_var = tk.StringVar(value="video")
        ttk.Radiobutton(format_frame, text="视频", value="video", 
                       variable=self.format_var, command=self.toggle_quality).grid(row=0, column=0, padx=(0, 20))
        ttk.Radiobutton(format_frame, text="音频(MP3)", value="audio", 
                       variable=self.format_var, command=self.toggle_quality).grid(row=0, column=1)
        
        # 质量选择
        quality_frame = ttk.Frame(options_frame)
        quality_frame.grid(row=1, column=0, columnspan=2, pady=(10, 0))
        
        ttk.Label(quality_frame, text="视频质量:").grid(row=0, column=0, padx=(0, 10))
        self.quality_var = tk.StringVar(value="1080")
        self.quality_combo = ttk.Combobox(quality_frame, textvariable=self.quality_var,
                                        values=["2160", "1440", "1080", "720", "480"],
                                        width=8, state="readonly")
        self.quality_combo.grid(row=0, column=1)
        
        # 下载按钮和进度区域框架
        self.download_frame = ttk.Frame(main_frame)
        self.download_frame.grid(row=4, column=0, columnspan=3, pady=(0, 10))
        
        # 下载按钮
        self.download_btn = ttk.Button(self.download_frame, 
                                     text="开始下载",
                                     command=self.start_download,
                                     style='Accent.TButton')
        self.download_btn.pack(pady=5)
        
        # 进度条（初始隐藏）
        self.progress_frame = ttk.Frame(self.download_frame)
        self.progress = ttk.Progressbar(self.progress_frame, length=200, mode='determinate')
        self.progress.pack(side='left', padx=(0, 5))
        self.progress_label = ttk.Label(self.progress_frame, text="0%")
        self.progress_label.pack(side='left')
        
        # 状态标签
        self.status_var = tk.StringVar(value="准备就绪")
        self.status_label = ttk.Label(main_frame, textvariable=self.status_var)
        self.status_label.grid(row=5, column=0, columnspan=3)

    def get_yt_dlp_path(self):
        """获取yt-dlp可执行文件的路径"""
        if getattr(sys, 'frozen', False):
            # 如果是打包后的程序，从资源目录获取
            return os.path.join(sys._MEIPASS, "yt-dlp.exe")
        else:
            # 如果是源代码运行，从当前目录获取
            return os.path.join(self.app_path, "yt-dlp.exe")

    def get_ffmpeg_path(self):
        """获取ffmpeg可执行文件的路径"""
        if getattr(sys, 'frozen', False):
            # 如果是打包后的程序，从资源目录获取
            return os.path.join(sys._MEIPASS, "ffmpeg.exe")
        else:
            # 如果是源代码运行，从当前目录获取
            return os.path.join(self.app_path, "ffmpeg.exe")

    def choose_directory(self):
        """选择下载目录"""
        dir_path = filedialog.askdirectory(initialdir=self.download_dir)
        if dir_path:
            self.dir_var.set(dir_path)
            self.download_dir = dir_path

    def toggle_quality(self):
        """切换质量选择的可用状态"""
        if self.format_var.get() == "audio":
            self.quality_combo.config(state="disabled")
        else:
            self.quality_combo.config(state="normal")

    def download_video(self):
        """下载视频的具体实现"""
        try:
            url = self.url_var.get()
            if not url:
                messagebox.showerror("错误", "请输入视频URL")
                return
            
            cmd = [self.yt_dlp_path,
                  "--no-playlist",
                  "-o", os.path.join(self.download_dir, "%(title)s.%(ext)s"),
                  "--embed-thumbnail",
                  "--embed-metadata",
                  "--progress-template", "%(progress._percent_str)s"]
            
            if self.ffmpeg_path:
                cmd.extend(["--ffmpeg-location", self.ffmpeg_path])
            
            # 使用cookies文件
            cookies_path = self.cookies_var.get()
            if os.path.exists(cookies_path):
                cmd.extend(["--cookies", cookies_path])
            
            if self.format_var.get() == "audio":
                cmd.extend(["-x", "--audio-format", "mp3", "--audio-quality", "0"])
            else:
                quality = self.quality_var.get()
                cmd.extend(["-f", f"bestvideo[height<={quality}]+bestaudio/best[height<={quality}]",
                          "--merge-output-format", "mp4"])
            
            cmd.append(url)
            
            self.status_var.set("下载中...")
            self.download_btn.pack_forget()
            self.progress_frame.pack()
            self.progress['value'] = 0
            self.progress_label['text'] = "0%"
            
            startupinfo = subprocess.STARTUPINFO()
            startupinfo.dwFlags |= subprocess.STARTF_USESHOWWINDOW
            
            process = subprocess.Popen(cmd, 
                                    stdout=subprocess.PIPE, 
                                    stderr=subprocess.PIPE,
                                    startupinfo=startupinfo,
                                    universal_newlines=True)
            
            # 读取输出并更新进度
            while True:
                line = process.stdout.readline()
                if not line and process.poll() is not None:
                    break
                if '%' in line:
                    try:
                        percent = float(line.strip().rstrip('%'))
                        self.progress['value'] = percent
                        self.progress_label['text'] = f"{percent:.1f}%"
                        self.root.update_idletasks()
                    except:
                        pass
            
            stdout, stderr = process.communicate()
            
            if process.returncode == 0:
                self.status_var.set("下载完成！")
                self.progress['value'] = 100
                self.progress_label['text'] = "100%"
                self.root.update_idletasks()
                # 等待一会儿显示100%
                self.root.after(1000, self.reset_download_ui)
            else:
                self.status_var.set("下载失败")
                messagebox.showerror("错误", stderr)
                self.reset_download_ui()
                
        except Exception as e:
            self.status_var.set("发生错误")
            messagebox.showerror("错误", str(e))
            self.reset_download_ui()

    def reset_download_ui(self):
        """重置下载界面"""
        self.progress_frame.pack_forget()
        self.download_btn.pack(pady=5)
        self.download_btn.config(state="normal")

    def start_download(self):
        """开始下载"""
        self.download_btn.config(state="disabled")
        Thread(target=self.download_video, daemon=True).start()

    def recreate_widgets(self):
        """重新创建界面"""
        # 清除所有控件
        for widget in self.root.winfo_children():
            widget.destroy()
        # 重新创建控件
        self.create_widgets()

    def check_and_update_tools(self):
        """检查并更新yt-dlp和ffmpeg"""
        try:
            self.status_var.set("正在检查更新...")
            
            # 检查yt-dlp更新
            if self.yt_dlp_path:
                update_cmd = [self.yt_dlp_path, "-U"]
                process = subprocess.Popen(
                    update_cmd,
                    stdout=subprocess.PIPE,
                    stderr=subprocess.PIPE,
                    startupinfo=subprocess.STARTUPINFO(),
                    universal_newlines=True
                )
                stdout, stderr = process.communicate()
                if "up to date" not in stdout.lower():
                    self.status_var.set("yt-dlp 已更新")
            
            # 检查ffmpeg是否存在
            if not self.ffmpeg_path:
                self.status_var.set("正在下载 FFmpeg...")
                # 从GitHub下载最新版本的FFmpeg
                import urllib.request
                import zipfile
                import shutil
                
                # 获取最新版本信息
                api_url = "https://api.github.com/repos/BtbN/FFmpeg-Builds/releases/latest"
                with urllib.request.urlopen(api_url) as response:
                    import json
                    data = json.loads(response.read())
                    for asset in data['assets']:
                        if 'ffmpeg-master-latest-win64-gpl.zip' in asset['name']:
                            # 下载FFmpeg
                            zip_path = os.path.join(self.app_path, "ffmpeg.zip")
                            urllib.request.urlretrieve(asset['browser_download_url'], zip_path)
                            
                            # 解压缩
                            with zipfile.ZipFile(zip_path, 'r') as zip_ref:
                                zip_ref.extractall(self.app_path)
                            
                            # 移动ffmpeg.exe到当前目录
                            ffmpeg_dir = next(d for d in os.listdir(self.app_path) if d.startswith('ffmpeg'))
                            src_path = os.path.join(self.app_path, ffmpeg_dir, 'bin', 'ffmpeg.exe')
                            dst_path = os.path.join(self.app_path, 'ffmpeg.exe')
                            shutil.move(src_path, dst_path)
                            
                            # 清理临时文件
                            os.remove(zip_path)
                            shutil.rmtree(os.path.join(self.app_path, ffmpeg_dir))
                            
                            self.ffmpeg_path = dst_path
                            self.status_var.set("FFmpeg 已安装")
                            break
            
            self.status_var.set("准备就绪")
            
        except Exception as e:
            self.status_var.set("更新检查失败")
            messagebox.showerror("错误", f"更新检查失败: {str(e)}")

    def paste_cookies(self):
        """粘贴cookies内容并保存为文件"""
        try:
            # 获取剪贴板内容
            clipboard = self.root.clipboard_get()
            if not clipboard.strip():
                messagebox.showerror("错误", "剪贴板为空")
                return
                
            # 检查是否是有效的cookies格式
            if not any(line.startswith('.youtube.com') for line in clipboard.splitlines()):
                messagebox.showerror("错误", "剪贴板内容不是有效的cookies格式")
                return
            
            # 保存到文件
            cookies_path = os.path.join(self.app_path, "cookies.txt")
            with open(cookies_path, 'w', encoding='utf-8') as f:
                f.write(clipboard)
            
            self.cookies_var.set(cookies_path)
            messagebox.showinfo("成功", "Cookies已保存")
            
        except tk.TclError:
            messagebox.showerror("错误", "剪贴板为空")
        except Exception as e:
            messagebox.showerror("错误", f"保存cookies失败: {str(e)}")

    def show_cookies_help(self, event):
        """显示cookies导出帮助"""
        help_text = """如何获取 cookies：

方法一：使用浏览器扩展
1. 安装 Chrome 扩展 "Get cookies.txt"
2. 打开 YouTube 并登录
3. 点击扩展图标，导出 cookies
4. 点击"选择"按钮，选择保存的 cookies.txt 文件

方法二：直接粘贴
1. 使用 EditThisCookie 等扩展导出 cookies
2. 复制 cookies 内容到剪贴板
3. 点击"粘贴"按钮

注意：cookies 可能会定期失效，需要重新获取"""
        messagebox.showinfo("Cookies 帮助", help_text)

    def choose_cookies(self):
        """选择cookies文件"""
        cookies_path = filedialog.askopenfilename(
            title="选择cookies.txt文件",
            filetypes=[("Text files", "*.txt"), ("All files", "*.*")],
            initialdir=self.app_path
        )
        if cookies_path:
            self.cookies_var.set(cookies_path)

if __name__ == "__main__":
    if sys.platform.startswith('win'):
        import ctypes
        ctypes.windll.user32.ShowWindow(ctypes.windll.kernel32.GetConsoleWindow(), 0)
    
    root = tk.Tk()
    app = YouTubeDownloader(root)
    root.mainloop()