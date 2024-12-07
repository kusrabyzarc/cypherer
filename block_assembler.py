import os
import struct
from globals import BUFFER_SIZE, BLOCK_SIZE
from logger_module import create_logger

logger = create_logger('block_assembler')

def pack_files(input_dir, output_dir):
    logger.info(f"Начало упаковки файлов из {input_dir} в {output_dir}")
    os.makedirs(output_dir, exist_ok=True)
    logger.debug(f"Каталог {output_dir} создан или уже существует")

    block_number = 0

    def create_block_file():
        """Открывает новый файл для записи блока."""
        nonlocal block_number
        block_filename = os.path.join(output_dir, f"block_{block_number:04d}.bin")
        block_number += 1
        logger.debug(f"Создание нового блока: {block_filename}")
        return open(block_filename, 'wb')

    # Рекурсивно обходим директорию
    current_block_file = create_block_file()
    current_block_size = 0

    for root, _, files in os.walk(input_dir):
        for file in files:
            file_path = os.path.join(root, file)
            relative_path = os.path.relpath(file_path, input_dir)
            logger.info(f"Обработка файла: {file_path} (относительный путь: {relative_path})")

            try:
                # Подготавливаем метаинформацию
                relative_path_bytes = relative_path.encode()
                path_length_data = struct.pack('<I', len(relative_path_bytes))
                content_length = os.path.getsize(file_path)
                content_length_data = struct.pack('<I', content_length)

                # Записываем метаинформацию в блок
                meta_data = path_length_data + relative_path_bytes + content_length_data
                if current_block_size + len(meta_data) > BLOCK_SIZE:
                    current_block_file.close()
                    current_block_file = create_block_file()
                    current_block_size = 0

                current_block_file.write(meta_data)
                current_block_size += len(meta_data)

                # Читаем содержимое файла по частям
                with open(file_path, 'rb') as f:
                    while chunk := f.read(BUFFER_SIZE):
                        if current_block_size + len(chunk) > BLOCK_SIZE:
                            current_block_file.close()
                            current_block_file = create_block_file()
                            current_block_size = 0
                        current_block_file.write(chunk)
                        current_block_size += len(chunk)
            except Exception as e:
                logger.error(f"Ошибка обработки файла {file_path}: {e}")

    # Закрываем текущий блок
    if current_block_file:
        current_block_file.close()
    logger.info("Упаковка завершена")

if __name__ == '__main__':
    input_directory = "E:"  # Папка с файлами
    output_directory = "output_folder"  # Папка для блоков
    pack_files(input_directory, output_directory)