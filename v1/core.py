import tkinter as tk

import ui.windows.txt_import as txt_import

# Импортируем функции из других модулей
# from txt_importer import processFile
# from pdf_exporter import export_to_pdf
# from excel_exporter import export_to_excel

# Имя файла, который мы будем импортировать
# INPUT_FILE = "new_source_data.txt"

# Текущие настройки программы
SETTINGS = {
   'file_import_txt': 'source.txt',
   'file_import_excel': 'excel.xlsx',
   
	'file_export_txt': 'export.txt',
   'file_export_pdf': 'export.pdf',
   'file_export_excel': 'export.xlsx',
   'file_export_word': 'export.word',
   'file_export_tmuis': 'export.xml',
	'file_export_icd': 'export.icd',
    
	'import_excel_col_name': 1,
	'import_excel_col_comment': 6,
   'import_excel_col_modbus_adr': 3,
   'import_excel_col_modbus_bit': 4,
   'import_excel_col_modbus_data_type': 5,
   'import_excel_col_modbus_func': 6,
   
	'export_excel_col_name': 1,
	'export_excel_col_comment': 6,
   'export_excel_col_modbus_adr': 3,
   'export_excel_col_modbus_bit': 4,
   'export_excel_col_modbus_data_type': 5,
   'export_excel_col_modbus_func': 6,
   'export_excel_col_iec61850_adr_mms': 4,
   'export_excel_col_iec61850_adr_goose': 4,
   'export_excel_col_iec61850_adr_dataset': 4,
   'export_excel_col_iec61850_adr_report': 4,
   'export_excel_col_iec61850_adr_buf_report': 4,
}

# Данные о строках в которых хранятся заголовки (№ строки, Уровень заголовка)
METADATA = {}
# Набор стандартных столбцов
CORE_COLS = ['Наименование','Адрес','Бит','Функция','Тип данных','Примечание']
# Полезные данные
PAYLOAD = [CORE_COLS]

# Основные данные
DATA = [
   PAYLOAD,
   METADATA,
]

# Состояние программы
STATE = {
	'state': 123,
   'sd': 12
}

def start():
   print("--- 🐍 Core start ---")
   root = tk.Tk()
   root.title("Компонент PathInput - Демонстрация")
   root.geometry("700x600")
   
   app = txt_import.FileManagerApp(root)
   app.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
    
   root.mainloop()

   pass

   #  data = processFile(INPUT_FILE)
   #  print(data)
   #  print('main')

   #  print("--- Запуск Проекта Экспорта ---")
    
    # # 1. Импорт и обработка данных
    # data = import_text_data(INPUT_FILE)
    
    # if data is None or not data:
    #     print("\n🚫 Процесс остановлен из-за отсутствия или ошибки в данных.")
    #     return
        
    # print(f"\nДанные готовы к экспорту ({len(data)} элементов).")
    
    # # 2. Экспорт данных в PDF
    # export_to_pdf(data, output_filename="Report_Data.pdf")
    
    # # 3. Экспорт данных в Excel
    # export_to_excel(data, output_filename="Report_Data.xlsx")
    
    # print("\n--- Работа завершена ---")
    