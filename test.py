import pandas as pd
from openpyxl import load_workbook
from openpyxl.styles import PatternFill, Font, Alignment

# Создаем данные
data = [
    ['ОТДЕЛ РАЗРАБОТКИ', '', ''],  # Строка-подзаголовок
    ['Имя', 'Должность', 'Зарплата'],
    ['Анна', 'Разработчик', 50000],
    ['Борис', 'Тестировщик', 45000],
    ['', '', ''],  # Пустая строка-разделитель
    ['ОТДЕЛ ПРОДАЖ', '', ''],  # Еще один подзаголовок
    ['Имя', 'Должность', 'Зарплата'],
    ['Виктор', 'Менеджер', 60000],
    ['Дарья', 'Аналитик', 55000],
    ['', '', ''],  # Еще разделитель
    ['ОТДЕЛ МАРКЕТИНГА', '', ''],
    ['Имя', 'Должность', 'Зарплата'],
    ['Елена', 'Дизайнер', 48000],
    ['Федор', 'Копирайтер', 42000]
]

df = pd.DataFrame(data)

# Сначала сохраняем
df.to_excel('авто_подзаголовки.xlsx', index=False, header=False)

# Автоматически находим и форматируем подзаголовки
wb = load_workbook('авто_подзаголовки.xlsx')
ws = wb.active

# Определяем критерии для подзаголовков
subheader_keywords = ['ОТДЕЛ', 'РАЗДЕЛ', 'ГЛАВА', 'ЧАСТЬ']

for row in range(1, ws.max_row + 1):
    cell_value = ws.cell(row=row, column=1).value
    
    if cell_value and any(keyword in str(cell_value).upper() for keyword in subheader_keywords):
        # Объединяем все ячейки в строке
        ws.merge_cells(start_row=row, start_column=1, end_row=row, end_column=ws.max_column)
        
        # Форматируем
        cell = ws.cell(row=row, column=1)
        cell.alignment = Alignment(horizontal='right', vertical='center')
        cell.font = Font(bold=True, size=14, color="FFFFFF")
        
        # Чередуем цвета для разных отделов
        if 'РАЗРАБОТКИ' in cell_value:
            cell.fill = PatternFill(start_color="4F81BD", fill_type="solid")
        elif 'ПРОДАЖ' in cell_value:
            cell.fill = PatternFill(start_color="ED7D31", fill_type="solid")
        elif 'МАРКЕТИНГА' in cell_value:
            cell.fill = PatternFill(start_color="A9D08E", fill_type="solid")
        else:
            cell.fill = PatternFill(start_color="7030A0", fill_type="solid")
        
        # Форматируем заголовки столбцов (следующую строку)
        for col in range(1, ws.max_column + 1):
            header_cell = ws.cell(row=row + 1, column=col)
            header_cell.font = Font(bold=True)
            header_cell.fill = PatternFill(start_color="E2EFDA", fill_type="solid")

# Сохраняем
wb.save('авто_подзаголовки.xlsx')
print("Файл сохранен: авто_подзаголовки.xlsx")