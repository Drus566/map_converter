import tkinter as tk
from tkinter import ttk, filedialog
from pathlib import Path
import os

class MultiplePathInput(ttk.Frame):
   """Компонент для выбора нескольких файлов"""
   
   def __init__(self, parent, label_text="Файлы:", **kwargs):
       super().__init__(parent, **kwargs)
       
       self.label_text = label_text
       self._paths = []
       
       self._create_widgets()
       self._layout_widgets()
   
   def _create_widgets(self):
       """Создание виджетов"""
       self.label = ttk.Label(self, text=self.label_text)
       
       # Список выбранных файлов
       self.listbox = tk.Listbox(self, height=4)
       self.scrollbar = ttk.Scrollbar(self, orient=tk.VERTICAL, 
                                     command=self.listbox.yview)
       self.listbox.configure(yscrollcommand=self.scrollbar.set)
       
       # Кнопки
       self.button_frame = ttk.Frame(self)
       self.add_button = ttk.Button(
           self.button_frame,
           text="Добавить файлы",
           command=self._add_files
       )
       self.remove_button = ttk.Button(
           self.button_frame,
           text="Удалить выбранное",
           command=self._remove_selected
       )
       self.clear_button = ttk.Button(
           self.button_frame,
           text="Очистить все",
           command=self._clear_all
       )
   
   def _layout_widgets(self):
       """Расположение виджетов"""
       self.columnconfigure(0, weight=1)
       
       self.label.grid(row=0, column=0, sticky=tk.W, pady=(0, 5))
       
       # Список с прокруткой
       self.listbox.grid(row=1, column=0, sticky=tk.W+tk.E+tk.N+tk.S, 
                        padx=(0, 5))
       self.scrollbar.grid(row=1, column=1, sticky=tk.N+tk.S)
       
       # Кнопки
       self.button_frame.grid(row=2, column=0, columnspan=2, 
                             sticky=tk.W, pady=(5, 0))
       self.add_button.pack(side=tk.LEFT, padx=(0, 5))
       self.remove_button.pack(side=tk.LEFT, padx=(0, 5))
       self.clear_button.pack(side=tk.LEFT)
   
   def _add_files(self):
       """Добавить файлы через диалог"""
       files = filedialog.askopenfilenames(
           title="Выберите файлы",
           filetypes=[("Все файлы", "*.*")]
       )
       
       for file in files:
           if file not in self._paths:
               self._paths.append(file)
               self.listbox.insert(tk.END, Path(file).name)
   
   def _remove_selected(self):
       """Удалить выбранные файлы"""
       selected = self.listbox.curselection()
       for index in reversed(selected):
           self.listbox.delete(index)
           del self._paths[index]
   
   def _clear_all(self):
       """Очистить все файлы"""
       self.listbox.delete(0, tk.END)
       self._paths.clear()
   
   def get_paths(self):
       """Получить список путей"""
       return self._paths.copy()
   
   def set_paths(self, paths):
       """Установить список путей"""
       self._clear_all()
       for path in paths:
           self._paths.append(path)
           self.listbox.insert(tk.END, Path(path).name)
