import tkinter as tk
from tkinter import ttk, filedialog
from pathlib import Path
import os

class PathInput(ttk.Frame):
    """
    Компонент для ввода пути к файлу или папке.
    
    Args:
        parent: Родительский виджет
        label_text (str): Текст метки
        dialog_title (str): Заголовок диалога выбора
        dialog_type (str): Тип диалога: 'file_open', 'file_save', 'directory'
        initial_dir (str): Начальная директория для диалога
        file_types (list): Список кортежей (описание, расширение) для файлового диалога
        allow_empty (bool): Разрешить пустое значение
        validate_path (bool): Проверять существование пути
        required (bool): Обязательное поле
        placeholder (str): Текст подсказки
        **kwargs: Дополнительные параметры для Frame
    """
    
    def __init__(self, parent, label_text="Путь:", dialog_title="Выберите файл",
                 dialog_type='file_open', initial_dir=None, file_types=None,
                 allow_empty=True, validate_path=False, required=False,
                 placeholder="", **kwargs):
        
        super().__init__(parent, **kwargs)
        
        # Сохраняем параметры
        self.label_text = label_text
        self.dialog_title = dialog_title
        self.dialog_type = dialog_type
        self.initial_dir = initial_dir or os.path.expanduser("~")
        self.file_types = file_types or [("Все файлы", "*.*")]
        self.allow_empty = allow_empty
        self.validate_path = validate_path
        self.required = required
        self.placeholder = placeholder
        
        # Переменные для состояния
        self._path_var = tk.StringVar()
        self._is_valid = tk.BooleanVar(value=True)
        self._validation_message = tk.StringVar(value="")
        
        # Создаем виджеты
        self._create_widgets()
        self._layout_widgets()
        
        # Настраиваем валидацию
        if validate_path:
            self._setup_validation()
    
    def _create_widgets(self):
        """Создание всех внутренних виджетов"""
        
        # Метка
        label_text = self.label_text
        if self.required:
            label_text += " *"
        self.label = ttk.Label(self, text=label_text)
        
        # Поле ввода пути
        self.entry = ttk.Entry(
            self,
            textvariable=self._path_var,
            state='normal'
        )
        
        # Устанавливаем подсказку если нужно
        if self.placeholder:
            self._setup_placeholder()
        
        # Кнопка выбора
        button_text = "..." if self.dialog_type == 'directory' else "📁"
        self.browse_button = ttk.Button(
            self,
            text=button_text,
            width=3,
            command=self._browse_path
        )
        
        # Метка для валидации
        self.validation_label = ttk.Label(
            self,
            textvariable=self._validation_message,
            foreground="red",
            font=("TkDefaultFont", 8)
        )
    
    def _setup_placeholder(self):
        """Настройка текста-подсказки"""
        self._path_var.set(self.placeholder)
        
        def on_focus_in(event):
            if self._path_var.get() == self.placeholder:
                self._path_var.set("")
                self.entry.configure(foreground="black")
        
        def on_focus_out(event):
            if not self._path_var.get():
                self._path_var.set(self.placeholder)
                self.entry.configure(foreground="gray")
        
        self.entry.bind("<FocusIn>", on_focus_in)
        self.entry.bind("<FocusOut>", on_focus_out)
        self.entry.configure(foreground="gray")
    
    def _layout_widgets(self):
        """Расположение виджетов"""
        # Используем grid для гибкости
        self.columnconfigure(1, weight=1)  # Колонка с полем ввода растягивается
        
        self.label.grid(row=0, column=0, sticky=tk.W, pady=(0, 5))
        self.entry.grid(row=1, column=0, columnspan=2, sticky=tk.W+tk.E, padx=(0, 5))
        self.browse_button.grid(row=1, column=2, sticky=tk.W)
        self.validation_label.grid(row=2, column=0, columnspan=3, sticky=tk.W, pady=(2, 0))
    
    def _setup_validation(self):
        """Настройка валидации пути"""
        self._path_var.trace_add("write", self._validate_path)
    
    def _validate_path(self, *args):
        """Валидация введенного пути"""
        path = self._path_var.get()
        
        # Игнорируем подсказку
        if path == self.placeholder:
            self._is_valid.set(True)
            self._validation_message.set("")
            self.entry.configure(foreground="gray")
            return
        
        # Проверяем пустое значение
        if not path:
            if self.required:
                self._is_valid.set(False)
                self._validation_message.set("Обязательное поле")
                self.entry.configure(foreground="red")
            else:
                self._is_valid.set(True)
                self._validation_message.set("")
                self.entry.configure(foreground="black")
            return
        
        # Проверяем существование пути
        if self.validate_path:
            path_obj = Path(path)
            if path_obj.exists():
                self._is_valid.set(True)
                self._validation_message.set("✓ Путь существует")
                self.entry.configure(foreground="green")
            else:
                self._is_valid.set(False)
                self._validation_message.set("✗ Путь не существует")
                self.entry.configure(foreground="red")
        else:
            self._is_valid.set(True)
            self._validation_message.set("")
            self.entry.configure(foreground="black")
    
    def _browse_path(self):
        """Открыть диалог выбора файла/папки"""
        
        if self.dialog_type == 'directory':
            # Диалог выбора папки
            path = filedialog.askdirectory(
                title=self.dialog_title,
                initialdir=self.initial_dir
            )
        elif self.dialog_type == 'file_save':
            # Диалог сохранения файла
            path = filedialog.asksaveasfilename(
                title=self.dialog_title,
                initialdir=self.initial_dir,
                filetypes=self.file_types
            )
        else:  # file_open
            # Диалог открытия файла
            path = filedialog.askopenfilename(
                title=self.dialog_title,
                initialdir=self.initial_dir,
                filetypes=self.file_types
            )
        
        # Обновляем поле ввода если путь выбран
        if path:
            self.set_path(path)
    
    def set_path(self, path):
        """Установить путь"""
        if isinstance(path, Path):
            path = str(path)
        
        self._path_var.set(path)
        self._validate_path()
    
    def get_path(self):
        """Получить путь как строку"""
        path = self._path_var.get()
        if path == self.placeholder:
            return ""
        return path
    
    def get_path_object(self):
        """Получить путь как объект Path"""
        path_str = self.get_path()
        if not path_str:
            return None
        return Path(path_str)
    
    def clear(self):
        """Очистить поле ввода"""
        if self.placeholder:
            self._path_var.set(self.placeholder)
            self.entry.configure(foreground="gray")
        else:
            self._path_var.set("")
        self._validate_path()
    
    def is_valid(self):
        """Проверить валидность значения"""
        return self._is_valid.get()
    
    def set_readonly(self, readonly=True):
        """Установить режим только для чтения"""
        if readonly:
            self.entry.configure(state='readonly')
            self.browse_button.configure(state='disabled')
        else:
            self.entry.configure(state='normal')
            self.browse_button.configure(state='normal')
    
    def set_required(self, required=True):
        """Установить обязательность поля"""
        self.required = required
        label_text = self.label_text
        if required:
            label_text += " *"
        else:
            label_text = label_text.rstrip(" *")
        self.label.configure(text=label_text)
        self._validate_path()
    
    # Свойства для удобства
    @property
    def value(self):
        return self.get_path()
    
    @value.setter
    def value(self, path):
        self.set_path(path)
    
    @property
    def path_object(self):
        return self.get_path_object()

