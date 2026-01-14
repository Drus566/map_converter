# main.py
import sys
from core import start

def main():
   start()
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
    

def analyze_environment():
    """Выводит используемую версию Python и список установленных пакетов, 
    используя современный API (Python 3.10+)."""
    
    print("--- 🐍 Среда выполнения ---")
    print(f"✅ Используемая версия Python: {sys.version.split()[0]}")
    print("----------------------------")
    
   #  print("\n--- 📦 Установленные библиотеки (Пакеты) ---")
   #  print("FPDF, openpyxl, pandas")

if __name__ == '__main__':
    analyze_environment()
    main()
    # Для теста, создадим фиктивный исходный файл, если его нет
    # try:
    #     with open(INPUT_FILE, 'w', encoding='utf-8') as f:
    #         f.write("Первая строка\n")
    #         f.write("Вторая строка с данными\n")
    #         f.write("Третья\n")
    #         f.write(" ") # Пустая строка, которую обработает importer
    #         f.write("Четвертая, последняя.\n")
    #     print(f"Создан тестовый файл: {INPUT_FILE}")
    # except Exception:
    #     pass # Игнорируем ошибку при создании тестового файла
        
    # main()