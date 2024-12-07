import os
import struct
from globals import BUFFER_SIZE
from logger_module import create_logger

logger = create_logger('block_disassembler')  # Создаем логгер

def unpack_files(input_dir, output_dir):
    logger.info(f"Начало распаковки блоков из {input_dir} в {output_dir}")
    
    # Получаем список блоков
    try:
        block_files = sorted(
            [os.path.join(input_dir, f) for f in os.listdir(input_dir) if f.startswith("block_")],
            key=lambda x: int(os.path.basename(x).split('_')[1].split('.')[0])
        )
        logger.debug(f"Найдено {len(block_files)} блоков для обработки")
    except Exception as e:
        logger.error(f"Ошибка при получении списка блоков: {e}")
        return

    os.makedirs(output_dir, exist_ok=True)
    logger.debug(f"Каталог {output_dir} создан или уже существует")
    
    # Генератор для чтения блоков по мере необходимости
    def block_generator():
        for block_file in block_files:
            logger.info(f"Чтение блока: {block_file}")
            try:
                with open(block_file, 'rb') as bf:
                    while chunk := bf.read(BUFFER_SIZE):
                        yield chunk
            except Exception as e:
                logger.error(f"Ошибка при чтении блока {block_file}: {e}")
        yield b''  # Обеспечивает завершение, чтобы избежать ошибки StopIteration
    
    packed_stream = block_generator()
    buffer = b""

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
            
            # Восстанавливаем файл
            output_path = os.path.join(output_dir, relative_path)
            os.makedirs(os.path.dirname(output_path), exist_ok=True)
            try:
                with open(output_path, 'wb') as f:
                    remaining = content_length
                    while remaining > 0:
                        chunk_size = min(BUFFER_SIZE, remaining)
                        chunk = read_from_buffer(chunk_size)
                        f.write(chunk)
                        remaining -= len(chunk)
                logger.info(f"Файл {output_path} успешно восстановлен")
            except Exception as e:
                logger.error(f"Ошибка при записи файла {output_path}: {e}")
    except StopIteration:
        logger.info("Распаковка завершена")
    except Exception as e:
        logger.error(f"Неожиданная ошибка во время распаковки: {e}")

# Пример использования
if __name__ == '__main__':
    input_directory = "output_folder"  # Папка с блоками
    output_directory = "restored_files"  # Папка для восстановленных файлов
    unpack_files(input_directory, output_directory)
