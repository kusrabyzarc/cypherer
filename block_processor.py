import os
import struct
from globals import BLOCK_SIZE
from logger_module import create_logger

logger = create_logger('block_processor')

class BlockProcessor:
    @staticmethod
    def pack_files(files_dict):
        """
        Упаковка файлов из словаря в блоки.
        :param files_dict: Словарь формата {"путь_до_файла": содержимое_файла_в_байтах}
        :return: Словарь блоков формата {"block_номер": содержимое_блока_в_байтах}
        """
        logger.info("Начало упаковки файлов из словаря")

        blocks = {}
        block_number = 0
        current_block = bytearray()

        for relative_path, file_content in files_dict.items():
            try:
                # Подготавливаем метаинформацию
                relative_path_bytes = relative_path.encode()
                path_length_data = struct.pack('<I', len(relative_path_bytes))
                content_length_data = struct.pack('<I', len(file_content))

                # Проверяем, поместится ли метаинформация и содержимое в текущий блок
                meta_data = path_length_data + relative_path_bytes + content_length_data
                if len(current_block) + len(meta_data) + len(file_content) > BLOCK_SIZE:
                    blocks[f"block_{block_number:04d}"] = bytes(current_block)
                    block_number += 1
                    current_block = bytearray()

                current_block.extend(meta_data)
                current_block.extend(file_content)
            except Exception as e:
                logger.error(f"Ошибка упаковки файла {relative_path}: {e}")

        # Добавляем последний блок
        if current_block:
            blocks[f"block_{block_number:04d}"] = bytes(current_block)

        logger.info("Упаковка завершена")
        return blocks

    @staticmethod
    def unpack_files(blocks_dict):
        """
        Распаковка блоков в словарь файлов.
        :param blocks_dict: Словарь блоков формата {"block_номер": содержимое_блока_в_байтах}
        :return: Словарь файлов формата {"путь_до_файла": содержимое_файла_в_байтах}
        """
        logger.info("Начало распаковки блоков в словарь файлов")

        files = {}
        buffer = b""

        # Генератор для последовательного чтения данных из блоков
        def block_generator():
            for block_number, block_content in sorted(blocks_dict.items()):
                logger.info(f"Чтение блока: {block_number}")
                yield block_content
            yield b''  # Обеспечивает завершение

        packed_stream = block_generator()

        # Функция чтения данных с динамическим пополнением буфера
        def read_from_buffer(size):
            nonlocal buffer
            while len(buffer) < size:
                buffer += next(packed_stream)
            result = buffer[:size]
            buffer = buffer[size:]
            return result

        try:
            while True:
                # Читаем длину пути
                relative_path_length = struct.unpack('<I', read_from_buffer(4))[0]
                logger.debug(f"Длина относительного пути: {relative_path_length}")

                # Читаем путь
                relative_path = read_from_buffer(relative_path_length).decode()
                logger.info(f"Восстановление файла: {relative_path}")

                # Читаем длину содержимого
                content_length = struct.unpack('<I', read_from_buffer(4))[0]
                logger.debug(f"Размер содержимого: {content_length} байт")

                # Читаем содержимое файла
                file_content = read_from_buffer(content_length)
                files[relative_path] = file_content

        except StopIteration:
            logger.info("Распаковка завершена")
        except Exception as e:
            logger.error(f"Неожиданная ошибка во время распаковки: {e}")

        return files

# Пример использования
if __name__ == '__main__':
    input_files = {
        "folder1/file1.txt": b"Hello, World!",
        "folder2/file2.txt": b"Python is awesome!",
        "folder3/subfolder/file3.bin": b"\x00\x01\x02\x03",
    }

    # Упаковка
    packed_blocks = BlockProcessor.pack_files(input_files)

    # Распаковка
    restored_files = BlockProcessor.unpack_files(packed_blocks)

    print("Восстановленные файлы:")
    for path, content in restored_files.items():
        print(f"{path}: {content}")
