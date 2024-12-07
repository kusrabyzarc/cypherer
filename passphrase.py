from globals import PASSPHRASE_SHUFFLE_ROUNDS, MAGIC_SHUFFLE_MAP
from logger_module import create_logger

logger = create_logger('passphrase')

class Passphrase:
    def __init__(self) -> None:
        with open('words.txt', mode='r', encoding='utf-8') as f:
            data = f.read().split('\n')
            self.map = data[:]
            self.MAGIC_BORDERS = {
                'min': 0,  # Беззнак
                'max': 2**128 - 1  # 256 бит
            }
        logger.info(f"Экземпляр Passphrase успешно создан. Размер словаря: {len(self.map)}")

    def __base_list_to_int__(self, bases: list) -> int:
        logger.debug(f"Преобразование списка баз в целое число: {bases}")
        n = 0
        for i, k in zip(bases[::-1], range(len(bases))):
            n += i * 566 ** k
        logger.debug(f"Результирующее целое число: {n}")

        # Проверка на попадание числа в допустимый диапазон
        if not (self.MAGIC_BORDERS['min'] <= n <= self.MAGIC_BORDERS['max']):
            logger.error(f"Число {n} выходит за пределы диапазона.")
            raise ValueError(f"Число выходит за пределы диапазона: {self.MAGIC_BORDERS['min']} <= n <= {self.MAGIC_BORDERS['max']}")
        
        return n

    def __int_to_base_list__(self, n: int) -> list:
        logger.debug(f"Преобразование числа {n} в список баз")
        
        # Проверка на попадание числа в допустимый диапазон
        if not (self.MAGIC_BORDERS['min'] <= n <= self.MAGIC_BORDERS['max']):
            logger.error(f"Число {n} выходит за пределы диапазона.")
            raise ValueError(f"Число выходит за пределы диапазона: {self.MAGIC_BORDERS['min']} <= n <= {self.MAGIC_BORDERS['max']}")
        
        bases = []
        for _ in range(14):
            bases.append(n % 566)
            n //= 566
        logger.debug(f"Результирующий список баз: {bases[::-1]}")
        return bases[::-1]

    def decode(self, words: list) -> str:
        logger.debug(f"Декодирование парольной фразы: {words}")
        if len(words) != 14:
            logger.error(f"Неверное количество слов в парольной фразе: {len(words)}")
            raise ValueError('Парольная фраза должна содержать ровно 14 слов')
        
        for word in words:
            if word not in self.map:
                logger.error(f"Неизвестное слово в парольной фразе: {word}")
                raise ValueError(f'Неизвестное слово: {word}')
        
        map = [self.map.index(word) for word in words]
        logger.debug(f"Прямая карта индексов: {map}")

        for _ in range(PASSPHRASE_SHUFFLE_ROUNDS):
            for k, i in zip(MAGIC_SHUFFLE_MAP, range(len(map))):
                map[i], map[k] = map[k], map[i]
        logger.debug(f"Индексы после перемешивания: {map}")

        result = hex(self.__base_list_to_int__(map))[2:].rjust(32, '0')
        logger.debug(f"Парольная фраза декодирована в: {result}")
        return result

    def encode(self, passphrase: str) -> list:
        logger.debug(f"Кодирование парольной фразы: {passphrase}")
        n = int(passphrase, 16)
        logger.debug(f"Парольная фраза преобразована в число: {n}")

        # Проверка на попадание числа в допустимый диапазон
        if not (self.MAGIC_BORDERS['min'] <= n <= self.MAGIC_BORDERS['max']):
            logger.error(f"Число {n} выходит за пределы диапазона.")
            raise ValueError(f"Число выходит за пределы диапазона: {self.MAGIC_BORDERS['min']} <= n <= {self.MAGIC_BORDERS['max']}")

        base_list = self.__int_to_base_list__(n)
        logger.debug(f"Список баз до обратного перемешивания: {base_list}")

        for _ in range(PASSPHRASE_SHUFFLE_ROUNDS):
            for i, k in reversed(list(zip(MAGIC_SHUFFLE_MAP, range(len(base_list))))):
                base_list[i], base_list[k] = base_list[k], base_list[i]
        logger.debug(f"Список баз после обратного перемешивания: {base_list}")

        result = [self.map[i] for i in base_list]
        logger.debug(f"Парольная фраза закодирована в слова: {result}")

        if len(result) != 14:
            logger.error('Длина декодированной парольной фразы не равна 14')
            raise ValueError('Длина полученной парольной фразы не равно 14')

        return result

