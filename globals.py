
# Длина блока данных
BLOCK_SIZE = 64 * 1024 # 64 Кб

# Размер буфера чтения
BUFFER_SIZE = 1024 * 1024 * 1024 # 1Гб

# Уровень логгирования
# CRITICAL = 50
# ERROR = 40
# WARNING = 30
# INFO = 20
# DEBUG = 10
LOGGER_LEVEL = 10


# Количество перемешиваний парольной фразы в раундах
PASSPHRASE_SHUFFLE_ROUNDS = 16

# Волшебная карта перемешиваний парольной фразы
MAGIC_SHUFFLE_MAP = [9, 13, 5, 0, 12, 7, 3, 4, 6, 2, 1, 10, 8, 11]