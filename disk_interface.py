from logger_module import create_logger
import os
import random

logger = create_logger('disk_processor')

class DiskInterface:
    """
    Интерфейс взаимодействия с дисками
    """
    def __init__(self, disk_letter: str) -> None:
        """
        Класс инициализации

        :param disk_letter: Буква диска
        :type disk_letter: str
        """
        if not isinstance(disk_letter, str) or len(disk_letter) != 1 or (disk_letter := disk_letter.upper()) not in "ABCDEFGHIJKLMNOPQRSTUVWXYZ":
            logger.error(f'{disk_letter} это не буква.')
            raise ValueError(f'{disk_letter} это не буква.')

        self.disk_letter = disk_letter
        self.disk_path = f"{self.disk_letter}:\\"
        if not os.path.exists(self.disk_path):
            logger.error(f'Диск {self.disk_letter} не существует.')
            raise FileNotFoundError(f'Диск {self.disk_letter} не существует.')

    def erase(self) -> None:
        """
        Полностью стирает данные с диска без возможности восстановления
        """
        logger.info(f'Начинаю стирание данных с диска {self.disk_letter}...')
        try:
            # Перебираем все файлы на диске
            for root, dirs, files in os.walk(self.disk_path, topdown=False):
                for file in files:
                    file_path = os.path.join(root, file)
                    self._overwrite_and_delete(file_path)
                for dir_ in dirs:
                    dir_path = os.path.join(root, dir_)
                    os.rmdir(dir_path)

            logger.info(f'Стирание данных с диска {self.disk_letter} завершено.')
        except Exception as e:
            logger.error(f'Ошибка при стирании данных: {str(e)}')
            raise

    def _overwrite_and_delete(self, file_path: str) -> None:
        """
        Перезаписывает файл случайными байтами и удаляет его

        :param file_path: Путь к файлу
        :type file_path: str
        """
        try:
            with open(file_path, 'r+b') as f:
                length = os.path.getsize(file_path)
                for _ in range(3):  # Три прохода для надежности
                    f.seek(0)
                    f.write(bytearray(random.getrandbits(8) for _ in range(length)))
            os.remove(file_path)
            logger.info(f'Файл {file_path} успешно удален.')
        except Exception as e:
            logger.warning(f'Ошибка при удалении файла {file_path}: {str(e)}')

    def read_disk_contents(self) -> dict:
        """
        Возвращает словарь с содержимым файлов на диске

        :return: Словарь формата {относительный_путь_файла_от_корня_диска: содержимое_файла_в_bytarray}
        :rtype: dict
        """
        contents = {}
        logger.info(f'Чтение содержимого диска {self.disk_letter}...')
        try:
            for root, _, files in os.walk(self.disk_path):
                for file in files:
                    if not (file.startswith('block_') or file == 'meta'):
                        continue
                    file_path = os.path.join(root, file)
                    relative_path = os.path.relpath(file_path, self.disk_path)
                    try:
                        with open(file_path, 'rb') as f:
                            contents[relative_path] = bytearray(f.read())
                    except Exception as e:
                        logger.warning(f'Не удалось прочитать файл {file_path}: {str(e)}')
            logger.info(f'Чтение содержимого диска {self.disk_letter} завершено.')
        except Exception as e:
            logger.error(f'Ошибка при чтении диска: {str(e)}')
            raise
        return contents

    def write(self, files_dict: dict) -> None:
        """
        Записывает файлы на диск из словаря

        :param files_dict: Словарь формата {относительный_путь_файла_от_корня_диска: содержимое_файла_в_bytearray}
        :type files_dict: dict
        """
        logger.info(f'Начинаю запись файлов на диск {self.disk_letter}...')
        try:
            for relative_path, content in files_dict.items():
                file_path = os.path.join(self.disk_path, relative_path)
                os.makedirs(os.path.dirname(file_path), exist_ok=True)
                with open(file_path, 'wb') as f:
                    f.write(content)
                logger.info(f'Файл {relative_path} успешно записан.')
            logger.info(f'Запись файлов на диск {self.disk_letter} завершена.')
        except Exception as e:
            logger.error(f'Ошибка при записи файлов: {str(e)}')
            raise

if __name__ == '__main__':
    try:
        disk_interface = DiskInterface("E")
        contents = disk_interface.read_disk_contents()
        for relative_path, content in contents.items():
            print(f"Файл: {relative_path}, Размер: {len(content)} байт")

        # Пример использования метода write
        sample_data = {"test_dir/test_file.txt": b"Hello, World!"}
        disk_interface.write(sample_data)

    except Exception as e:
        logger.error(f"Ошибка выполнения: {str(e)}")
