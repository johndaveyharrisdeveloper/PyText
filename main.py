import tkinter as tk
from tkinter import ttk, messagebox, colorchooser, scrolledtext
import random

class TextEditor:
    def __init__(self, root):
        self.root = root
        self.root.title("PyText")
        self.root.geometry("800x600")
        
        self.create_menu()
        
        self.create_toolbar()

        self.text_area = scrolledtext.ScrolledText(
            self.root, 
            wrap=tk.WORD, 
            font=("Arial", 12),
            undo=True,
            maxundo=-1
        )
        self.text_area.pack(fill=tk.BOTH, expand=True)

        self.status_var = tk.StringVar()
        self.status_bar = ttk.Label(self.root, textvariable=self.status_var)
        self.status_bar.pack(side=tk.BOTTOM, fill=tk.X)

        self.text_area.bind('<KeyPress>', self.update_status)
        self.text_area.bind('<Button-1>', self.update_status)
        
    def create_menu(self):
        menubar = tk.Menu(self.root)

        file_menu = tk.Menu(menubar, tearoff=0)
        file_menu.add_command(label="Новый", command=self.new_file, accelerator="Ctrl+N")
        file_menu.add_command(label="Открыть", command=self.open_file, accelerator="Ctrl+O")
        file_menu.add_command(label="Сохранить", command=self.save_file, accelerator="Ctrl+S")
        file_menu.add_separator()
        file_menu.add_command(label="Выход", command=self.root.quit)
        menubar.add_cascade(label="Файл", menu=file_menu)

        format_menu = tk.Menu(menubar, tearoff=0)
        format_menu.add_command(label="Жирный", command=self.toggle_bold, accelerator="Ctrl+B")
        format_menu.add_command(label="Курсив", command=self.toggle_italic, accelerator="Ctrl+I")
        format_menu.add_command(label="Подчеркнутый", command=self.toggle_underline, accelerator="Ctrl+U")
        format_menu.add_separator()
        format_menu.add_command(label="Цвет текста", command=self.choose_text_color)
        format_menu.add_command(label="Цвет фона", command=self.choose_bg_color)
        menubar.add_cascade(label="Формат", menu=format_menu)

        extra_menu = tk.Menu(menubar, tearoff=0)
        extra_menu.add_command(label="Случайная шутка", command=self.insert_joke)
        extra_menu.add_command(label="Статистика", command=self.show_stats)
        menubar.add_cascade(label="Дополнительно", menu=extra_menu)
        
        self.root.config(menu=menubar)

        self.root.bind('<Control-n>', lambda e: self.new_file())
        self.root.bind('<Control-o>', lambda e: self.open_file())
        self.root.bind('<Control-s>', lambda e: self.save_file())
        self.root.bind('<Control-b>', lambda e: self.toggle_bold())
        self.root.bind('<Control-i>', lambda e: self.toggle_italic())
        self.root.bind('<Control-u>', lambda e: self.toggle_underline())
        
    def create_toolbar(self):
        toolbar = ttk.Frame(self.root)
        toolbar.pack(side=tk.TOP, fill=tk.X)

        ttk.Button(toolbar, text="Ж", command=self.toggle_bold, width=3).pack(side=tk.LEFT, padx=2)
        ttk.Button(toolbar, text="К", command=self.toggle_italic, width=3).pack(side=tk.LEFT, padx=2)
        ttk.Button(toolbar, text="Ч", command=self.toggle_underline, width=3).pack(side=tk.LEFT, padx=2)

        self.font_var = tk.StringVar(value="Arial")
        font_combo = ttk.Combobox(toolbar, textvariable=self.font_var, values=["Arial", "Times New Roman", "Courier New", "Verdana"])
        font_combo.pack(side=tk.LEFT, padx=5)
        font_combo.bind('<<ComboboxSelected>>', self.change_font)

        self.size_var = tk.StringVar(value="12")
        size_combo = ttk.Combobox(toolbar, textvariable=self.size_var, values=["8", "10", "12", "14", "16", "18", "20"])
        size_combo.pack(side=tk.LEFT, padx=5)
        size_combo.bind('<<ComboboxSelected>>', self.change_font)
        
    def toggle_bold(self):
        try:
            current_tags = self.text_area.tag_names("sel.first")
            if "bold" in current_tags:
                self.text_area.tag_remove("bold", "sel.first", "sel.last")
            else:
                self.text_area.tag_add("bold", "sel.first", "sel.last")
                self.text_area.tag_config("bold", font=(self.font_var.get(), self.size_var.get(), "bold"))
        except tk.TclError:
            pass
            
    def toggle_italic(self):
        try:
            current_tags = self.text_area.tag_names("sel.first")
            if "italic" in current_tags:
                self.text_area.tag_remove("italic", "sel.first", "sel.last")
            else:
                self.text_area.tag_add("italic", "sel.first", "sel.last")
                self.text_area.tag_config("italic", font=(self.font_var.get(), self.size_var.get(), "italic"))
        except tk.TclError:
            pass
            
    def toggle_underline(self):
        try:
            current_tags = self.text_area.tag_names("sel.first")
            if "underline" in current_tags:
                self.text_area.tag_remove("underline", "sel.first", "sel.last")
            else:
                self.text_area.tag_add("underline", "sel.first", "sel.last")
                self.text_area.tag_config("underline", font=(self.font_var.get(), self.size_var.get(), "underline"))
        except tk.TclError:
            pass
            
    def change_font(self, event=None):
        font = self.font_var.get()
        size = self.size_var.get()
        self.text_area.config(font=(font, size))
        
    def choose_text_color(self):
        color = colorchooser.askcolor()[1]
        if color:
            try:
                self.text_area.tag_add("color", "sel.first", "sel.last")
                self.text_area.tag_config("color", foreground=color)
            except tk.TclError:
                pass
                
    def choose_bg_color(self):
        color = colorchooser.askcolor()[1]
        if color:
            try:
                self.text_area.tag_add("bgcolor", "sel.first", "sel.last")
                self.text_area.tag_config("bgcolor", background=color)
            except tk.TclError:
                pass
                
    def new_file(self):
        self.text_area.delete(1.0, tk.END)
        
    def open_file(self):
        try:
            with open("document.txt", "r", encoding="utf-8") as file:
                self.text_area.delete(1.0, tk.END)
                self.text_area.insert(1.0, file.read())
        except FileNotFoundError:
            messagebox.showerror("Ошибка", "Файл не найден")
            
    def save_file(self):
        try:
            with open("document.txt", "w", encoding="utf-8") as file:
                file.write(self.text_area.get(1.0, tk.END))
            messagebox.showinfo("Успех", "Файл сохранен")
        except Exception as e:
            messagebox.showerror("Ошибка", f"Не удалось сохранить файл: {str(e)}")
            
    def insert_joke(self):
        jokes = [
            "Почему программисты путают Хэллоуин и Рождество? Потому что Oct 31 == Dec 25!",
            "Сколько программистов нужно, чтобы вкрутить лампочку? Ни одного. Это аппаратная проблема!",
            "Почему Python стал таким популярным? Потому что он не оставляет тебя в неведении — всегда говорит, где ошибка!"
        ]
        joke = random.choice(jokes)
        self.text_area.insert(tk.INSERT, f"\n{joke}\n")
        
    def show_stats(self):
        text = self.text_area.get(1.0, tk.END)
        words = len(text.split())
        chars = len(text.replace("\n", ""))
        lines = text.count("\n")
        messagebox.showinfo("Статистика", f"Слов: {words}\nСимволов: {chars}\nСтрок: {lines}")
        
    def update_status(self, event=None):
        line, column = self.text_area.index(tk.INSERT).split('.')
        self.status_var.set(f"Строка: {line}, Колонка: {column}")

if __name__ == "__main__":
    root = tk.Tk()
    app = TextEditor(root)
    root.mainloop()