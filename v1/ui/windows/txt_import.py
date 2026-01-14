import tkinter as tk
from tkinter import ttk
from pathlib import Path

import ui.inputs.path_input as path_input

# Пример использования компонента
class FileManagerApp(ttk.Frame):
    """Пример приложения с использованием PathInput"""
    
    def __init__(self, parent):
        super().__init__(parent, padding="20")
        
        self.title = ttk.Label(
            self,
            text="Менеджер файлов",
            font=("Arial", 14, "bold")
        )
        
        # Создаем различные варианты PathInput
        self.source_file = path_input.PathInput(
            self,
            label_text="Исходный файл:",
            dialog_title="Выберите исходный файл",
            dialog_type='file_open',
            file_types=[("Текстовые файлы", "*.txt"), 
                       ("Все файлы", "*.*")],
            validate_path=True,
            required=True,
            placeholder="Выберите или введите путь к файлу..."
        )
        
        # Кнопки действий
        self.button_frame = ttk.Frame(self)
        self.process_button = ttk.Button(
            self.button_frame,
            text="Обработать",
            command=self.process_files
        )
        self.clear_button = ttk.Button(
            self.button_frame,
            text="Сбросить",
            command=self.clear_all
        )
        
        # Информационное поле
        self.info_text = tk.Text(self, height=6, width=50)
        self.info_scrollbar = ttk.Scrollbar(self, orient=tk.VERTICAL,
                                          command=self.info_text.yview)
        self.info_text.configure(yscrollcommand=self.info_scrollbar.set)
        
        self._layout_widgets()
    
    def _layout_widgets(self):
        """Расположение виджетов"""
        self.columnconfigure(0, weight=1)
        
        row = 0
        self.title.grid(row=row, column=0, columnspan=2, pady=(0, 20))
        row += 1
        
        self.source_file.grid(row=row, column=0, columnspan=2, 
                             sticky=tk.W+tk.E, pady=(0, 10))
        row += 1
                
        self.button_frame.grid(row=row, column=0, columnspan=2, 
                              pady=(0, 20))
        self.process_button.pack(side=tk.LEFT, padx=(0, 10))
        self.clear_button.pack(side=tk.LEFT)
        row += 1
        
        ttk.Label(self, text="Информация:").grid(row=row, column=0, 
                                                sticky=tk.W, pady=(0, 5))
        row += 1
        
        self.info_text.grid(row=row, column=0, sticky=tk.W+tk.E+tk.N+tk.S)
        self.info_scrollbar.grid(row=row, column=1, sticky=tk.N+tk.S)
        
        # Делаем строку с текстом растяжимой
        self.rowconfigure(row, weight=1)
    
    def process_files(self):
        """Обработка выбранных файлов"""
        # Проверяем валидность обязательных полей
        if not self.source_file.is_valid():
            self._show_message("Ошибка: укажите корректный исходный файл", "red")
            return
        
        # Собираем информацию
        info_lines = []
        info_lines.append("=== Информация о файлах ===")
        info_lines.append(f"Исходный файл: {self.source_file.value}")
        
        if self.output_dir.value:
            info_lines.append(f"Выходная папка: {self.output_dir.value}")
        
        if self.save_file.value:
            info_lines.append(f"Сохранить как: {self.save_file.value}")
        
        multiple_files = self.multiple_files.get_paths()
        if multiple_files:
            info_lines.append("\nФайлы для обработки:")
            for i, path in enumerate(multiple_files, 1):
                info_lines.append(f"  {i}. {Path(path).name}")
        
        # Выводим информацию
        self._show_message("\n".join(info_lines), "black")
        
        # Здесь можно добавить реальную обработку файлов
        self._show_message("\nОбработка завершена успешно!", "green")
    
    def clear_all(self):
        """Очистить все поля"""
        self.source_file.clear()
        self.output_dir.clear()
        self.save_file.clear()
        self.multiple_files.set_paths([])
        self.info_text.delete(1.0, tk.END)
    
    def _show_message(self, message, color="black"):
        """Показать сообщение в текстовом поле"""
        self.info_text.delete(1.0, tk.END)
        self.info_text.insert(1.0, message)
        self.info_text.tag_add("colored", 1.0, tk.END)
        self.info_text.tag_config("colored", foreground=color)
