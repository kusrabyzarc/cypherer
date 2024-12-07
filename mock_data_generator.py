import os
import random
import string

def generate_mock_tree(base_path, depth=3, max_dirs=5, max_files=10, file_size_range=(512, 2048)):
    """
    Генерирует моковое файловое древо в указанной папке с записью случайных данных в файлы.

    :param base_path: Корневая директория для генерации.
    :param depth: Максимальная глубина древа.
    :param max_dirs: Максимальное количество директорий в одной папке.
    :param max_files: Максимальное количество файлов в одной папке.
    :param file_size_range: Диапазон размеров файла (min, max) в байтах.
    """
    if depth < 1:
        return

    # Генерация директорий
    for _ in range(random.randint(1, max_dirs)):
        dir_name = ''.join(random.choices(string.ascii_letters + string.digits, k=8))
        dir_path = os.path.join(base_path, dir_name)
        os.makedirs(dir_path, exist_ok=True)
        # Рекурсивное создание вложенных директорий
        generate_mock_tree(dir_path, depth - 1, max_dirs, max_files, file_size_range)

    # Генерация файлов
    for _ in range(random.randint(1, max_files)):
        file_name = ''.join(random.choices(string.ascii_letters + string.digits, k=12)) + '.txt'
        file_path = os.path.join(base_path, file_name)
        file_size = random.randint(*file_size_range)  # Размер файла в байтах
        with open(file_path, 'wb') as f:
            random_data = os.urandom(file_size)  # Генерация случайных байтов
            f.write(random_data)

if __name__ == '__main__':
    root = 'E:'
    os.makedirs(root, exist_ok=True)
    generate_mock_tree(root)
