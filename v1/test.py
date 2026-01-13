# Простой анализ импортов
import ast
import os

def find_imports(file_path):
    """Находит все импорты в Python файле"""
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    imports = set()
    
    try:
        tree = ast.parse(content)
        
        for node in ast.walk(tree):
            # Импорты вида: import module
            if isinstance(node, ast.Import):
                for alias in node.names:
                    imports.add(alias.name.split('.')[0])
            
            # Импорты вида: from module import something
            elif isinstance(node, ast.ImportFrom):
                if node.module:
                    imports.add(node.module.split('.')[0])
    
    except SyntaxError as e:
        print(f"Ошибка синтаксиса в {file_path}: {e}")
    
    return imports

# Пример использования
imports = find_imports('test.py')
print("Используемые модули:", imports)