# txt_importer.py

# Типы данных Modbus
TYPES = ["int16", "uint16", "int32", "uint32", "float16", "float32"]
# Столбцы таблицы
COLUMNS = ['№', 'Наименование','Адрес','Бит','Функция','Тип данных','Значение для записи','Примечание']

def getModbusParams(text):
    """
    Получение типа данных, функции, команды
    Args:
        text: входная строка
        adr: адрес
    Returns:
        Tuple: (response, data_type, func, command)
    """

    data_type = ""
    func = ""

    parts = text.split(',')
    
    if (len(parts)) == 0:
        return (False, 0, 0, 0)
    
    for i, part in enumerate(parts):
        clean_part = part.strip()
        if (i == 0):
            is_type = [t for t in TYPES if t == part]
            if (not is_type):
                return (False, 0, 0, 0)
            data_type = clean_part
            continue
        
        if (clean_part == "write"):
            if data_type == "int16" or data_type == "uint16" or data_type == "float16":
                func = "3"
            elif data_type == "int32" or data_type == "uint32" or data_type == "float32":
                func = "16"
            continue

        if (clean_part.startswith("value")):
            value_parts = ""
        
def getTextInParentheses(text):
    """Простая функция для получения текста в первых скобках"""
    if '(' in text and ')' in text:
        start = text.find('(')
        end = text.find(')', start)
        if start < end:
            return text[start + 1:end].strip()
    return None

def checkModbusLine(text):
    """
    Проверяет, является ли первый элемент разбитой строки числом
    Args:
        text: входная строка
    Returns:
        Tuple: (is_number, number_str)
    """
    parts = text.split()
    
    if not parts:
        return False, ""
    
    first = parts[0]
    
    # Проверка на целое число
    if first.isdigit():
        return True, str(int(first))
        
    # Проверка на число с плавающей точкой
    try:
        float_value = float(first)
        
        # Различаем целые и дробные числа
        if '.' in first:
            return True, str(float_value)
        else:
            return True, str(int(float_value))
            
    except ValueError:
        return False, ""
    
def importTextData(file_path):
    """
    Построчно читает текстовый файл и возвращает список обработанных строк
    data = [
        ['Наименование','Адрес','Бит','Функция','Тип данных','Значение для записи', 'Примечание'],
        ['Состояние', '', '', '', '', '', ''],
        ['Статусы', '', '', '', '', '', ''],
        ['ЭПУ на резерве',12,2,3,'int16','',''],
        ['ЭПУ на инверторе',12,3,3,'int16','',''],
        ['Аварии', '', '', '', '', '', ''],
        ['Авария инвертора',13,0,3,'int16','',''],
        ['Выход не в норме',13,1,3,'int16','',''],
        ['Измерения', '', '', '', '', '', ''],
        ['Напряжение на инверторе',1122,'',3,'float32','',''],
        ['Ток инвертора',1124,'',3,'float32','',''],
    ]
    """
    # Счетчик заголовка 1 уровня
    h1_counter = 1
    # Счетчик заголовка 2 уровня
    h2_counter = 1
    # Счетчик заголовка 3 уровня
    h3_counter = 1
    # Область
    area = ""
    # Началась ли область c Modbus адресами
    modbus = False
    # Обработанные строки
    processed_lines = []
    
    try:
        # Используем кодировку UTF-8 для широкой поддержки символов
        with open(file_path, 'r', encoding='utf-8') as f:
            for line in f:
                # Очистка строки от символов перевода строки и лишних пробелов
                clean_line = line.strip()
                if clean_line:
                    if clean_line == "":
                        continue

                    # Если это Modbus раздел
                    if clean_line.startswith("# " + "Modbus") or clean_line.startswith("# " + "Модбас"):
                        modbus = True
                        continue
                    # Если это не Modbus раздел
                    elif clean_line.startswith("#"):
                        modbus = False
                        continue
                    # Пропускаем все строки которые не являются Modbus разделом
                    if (modbus == False):
                        continue

                    # Проверка заголовка первого уровня
                    if (clean_line.startswith("## ")):
                        s_h1 = clean_line[2:].strip()
                        h1_counter = h1_counter + 1
                        h2_counter = 1
                        h3_counter = 1
                        continue
                    # Проверка заголовка второго уровня
                    if (clean_line.startswith("### ")):
                        s_h2 = clean_line[3:].strip()
                        h2_counter = h2_counter + 1
                        h3_counter = 1
                        continue
                    # Проверка заголовка третьего уровня
                    if (clean_line.startswith("#### ")):
                        s_h3 = clean_line[4:].strip()
                        h3_counter = h3_counter + 1
                        continue
                    # Проверка области
                    if (clean_line.startswith("*")):
                        s_area = clean_line[1:].strip()
                        continue

                    # Проверка данных
                    is_number, number_str = checkModbusLine(clean_line)
                    if (not is_number):
                        continue

                    params = getTextInParentheses(clean_line)


                    # Получение параметров
                    processed_lines.append(clean_line.upper()) # Пример: перевод в верхний регистр
        
        print(f"✅ Успешно импортировано {len(processed_lines)} строк из {file_path}")
        return processed_lines
        
    except FileNotFoundError:
        print(f"❌ Ошибка: Файл не найден по пути: {file_path}")
        return None
    except Exception as e:
        print(f"❌ Произошла ошибка при чтении файла: {e}")
        return None

# Пример: если этот файл запустить напрямую, он не сделает ничего, 
# так как его задача - быть импортированным.
if __name__ == '__main__':
    print("Это модуль для импорта данных, предназначен для использования в main.py.")