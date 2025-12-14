from enum import Enum

class NumberType(Enum):
    INT = 1
    FLOAT = 2

class ColumnsIndex(Enum):
    NAME = 0,
    ADR = 1,
    BIT = 2,
    FUNC = 3,
    DATA_TYPE = 4,
    VALUE = 5,
    COMMENT = 6
    
HEADER_TAGS = ['# ', '## ', '### ', '#### ']
HEADERS = {
    'h1': HEADER_TAGS[0],
    'h2': HEADER_TAGS[1],
    'h3': HEADER_TAGS[2],
    'h4': HEADER_TAGS[3],
}

# Данные о строках в которых хранятся заголовки (№ строки, Уровень заголовка)
DATA_HEADERS = {}
# Набор стандартных столбцов
DATA_COLUMNS_STR = ['Наименование','Адрес','Бит','Функция','Тип данных','Значение для записи', 'Примечание']
# Данные 
DATA = [DATA_COLUMNS_STR]
# Дополнительные данные о строка и данные
ALL_DATA = [
    DATA_HEADERS,
    DATA,
]

# Состояние парсинга
STATE = {
    'modbus': False,
}

def main():
    INPUT_FILENAME = 'source_data.txt'
    processFile(INPUT_FILENAME)
    print(ALL_DATA)
    print('main')

def processFile(filename):
    with open(filename, 'r', encoding='utf-8') as file:
        for num_line, line in enumerate(file, start=1):
            line = line.strip()
            if (line.startswith(HEADERS['h1'])):
                is_modbus = True if isModbusHeader(line) else False
                STATE['modbus'] = is_modbus
            elif STATE['modbus']:
                print(line)
                if (line.startswith(HEADERS['h2'])):
                    DATA_HEADERS[num_line] = 1
                    header = line[2:].strip()
                    header_list = getHeaderList(header)
                    DATA.append(header_list)
                elif (line.startswith(HEADERS['h3'])):
                    DATA_HEADERS[num_line] = 2
                    header = line[3:].strip()
                    header_list = getHeaderList(header)
                    DATA.append(header_list)
                elif (line.startswith(HEADERS['h4'])):
                    DATA_HEADERS[num_line] = 3
                    header = line[4:].strip()
                    header_list = getHeaderList(header)
                    DATA.append(header_list)
                elif (line.startswith('*')):
                    area = getArea(line)
                    if area != None:
                        DATA_HEADERS[num_line] = 4
                        header_list = getHeaderList(area)
                        DATA.append(header_list)
                else:
                    data = parseData(line, num_line)
                    if (data != None):
                        DATA.append(data)

def getArea(line):
    start = line.find('*')
    end = line.find('*', start + 1) if start != -1 else -1
    if start != -1 and end != -1:
        return line[start + 1:end]
    return None

def getHeaderList(header):
    result = [''] * len(DATA_COLUMNS_STR)
    result[0] = header
    return result

# Проверка является ли строка началом модбас области            
def isModbusHeader(line):
    line = line[1:].strip().lower()
    return line in ('модбас','модбас адреса','modbus адреса','modbus')

# Получить подстроку параметров в строке данных
def getParamsStr(line):
    start = line.find('(')
    end = line.find(')', start + 1) if start != -1 else -1
    if start != -1 and end != -1:
        return line[start + 1:end]
    return None

# Получить подстроку наименования и комментария
def getDescriptionStr(line):
    start = line.find('-')
    if start != -1:
        return line[start + 1:]
    return None

# Парсинг строки данных
def parseData(line, num_line):
    parts = line.split()
    if (len(parts) > 0):
        part_one = parts[0].strip()
        result, address, bit = parseAdr(part_one)
        if (not result):
            print(f'Error parse address in line {num_line}: {line}')
            return None

        params_str = getParamsStr(line)
        if params_str == None:
            print(f'Not found parameters in line {num_line}: {line}')
            return None
        result, data_type, func, value = parseParams(params_str)
        if (not result):
            print(f'Error parse parameters in line {num_line}: {line}')
            return None
        
        description_str = getDescriptionStr(line)
        if description_str == None:
            print(f'Error parse description in line {num_line}: {line}')
            return None
        result, name, comment = parseDescription(description_str)
    
    return [name,address,bit,func,data_type,value,comment]
        
def parseDescription(line):
    result = False
    name = ''
    comment = ''

    parts = line.strip().split('#')
    if (parts != None):
        name = parts[0]
        comment = parts[1] if (len(parts) > 1) else ''

    return (result, name, comment)   

# Парсинг параметров
def parseParams(line):
    result = False
    data_type = ''
    func = ''
    value = ''

    parts = line.split(',')
    for i, part in enumerate(parts):
        part = part.lower().strip()
        if i == 0 and part in ('int16', 'uint16', 'float16', 'int32', 'uint32', 'float32', 'bit'):
            data_type = part
            func = 1 if data_type == 'bit' else 3  
            result = True          
        elif i == 1 and part == 'write':
            if data_type != None:
                if data_type in ('int16', 'uint16', 'float16'):
                    func = 6
                elif data_type in ('int32', 'uint32', 'float32'):
                    func = 16
                elif data_type in ('coil'):
                    func = 5
        elif i == 2 and part.startswith('value'):
            p = part.split()
            if (len(p) > 1):
                val_num = p[1]
                type = getNumberType(val_num)
                value = val_num if type != None else None
    
    return (result, data_type, func, value)

# Парсинг адреса
def parseAdr(line):
    address = ''
    type = getNumberType(line)
    if (type == NumberType.INT):
        address = line
        return(True,address,'')
    elif (type == NumberType.FLOAT):
        parts = line.split('.')
        if (len(parts) > 1):
            address = parts[0]
            bit = parts[1]
            return (True,address,bit)
    else:
        return (False,None,None) 

# Получить тип числа
def getNumberType(line):
    try:
        int(line)
        return NumberType.INT
    except ValueError:
        try:
            float(line)
            return NumberType.FLOAT
        except ValueError:
            return None

def parseLine():
    print('parse line')

def getAdr():
    print('get adr')
    
def getParams():
    print('get params')

main()