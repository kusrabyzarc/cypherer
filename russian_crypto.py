import gostcrypto
from type_stricter import strict_type
from logger_module import create_logger

logger = create_logger('russian_crypt')

class RussianCrypto:
    """
    Межслойный интерфейс абстракции для разработки проекта "Прозрачное шифрование"
    """
    def __init__(self) -> None:
        pass

    @strict_type
    @staticmethod
    def hash(data: bytearray) -> str:
        """
        Возвращает хэш заданных данных по алгоритму ГОСТ Р 34.11-2012 (Стрибог)
        256-битной вариации

        
        :param data: Входные данные
        :type data: bytearray
        :return: Хэш данных в виде шестнадцатиричной строки
        :rtype: str
        """
        try:
            logger.debug("Начало хэширования данных")
            result = gostcrypto.gosthash.new('streebog256', data=data).hexdigest()
            logger.debug(f"Хэширование завершено успешно: {result}")
            return result
        except Exception as e:
            logger.critical(f"Ошибка при хэшировании данных: {e}")
            raise
    
    @staticmethod
    def random(length: int) -> bytearray:
        """
        Возвращает псевдослучайную поледовательность байт в bytearray по алгориму
        Р 1323565.1.006-2017
        В качестве сида используется os.urandom (Подробнее: https://github.com/drobotun/gostcrypto/blob/1590311620d6d03d1d8e1b6abe1966da4c8550ed/gostcrypto/gostrandom/r_1323565_1_006_2017.py#L38C5-L38C8)

        :param length: Длина массива
        :type length: int
        :return: Массив байт
        :rtype: bytearray
        """
        try:
            return bytearray(gostcrypto.gostrandom.new(length).random())
        except Exception as e:
            logger.critical(f"Ошибка при шифровании данных: {e}")
            raise

    class Kuznechik:
        """
        Промежуточный класс для алгоритма ГОСТ 34.12-2018 ("Кузнечик")
        """
        def __init__(self) -> None:
            pass

        @strict_type
        @staticmethod
        def encrypt(key: bytearray, data: bytearray) -> bytearray:
            """
            Шифрование данных

            :param key: Ключ шифрования
            :type key: bytearray
            :param data: Данные, которые нужно зашифровать
            :type data: bytearray
            :return: Шифрованные данные
            :rtype: bytearray
            """
            try:
                logger.debug("Начало шифрования данных с использованием Кузнечика")
                api = gostcrypto.gostcipher.new('kuznechik',
                                                key,
                                                gostcrypto.gostcipher.MODE_ECB,
                                                pad_mode=gostcrypto.gostcipher.PAD_MODE_1)
                result = api.encrypt(data)
                logger.debug(f"Шифрование завершено успешно: {result}")
                return result
            except Exception as e:
                logger.critical(f"Ошибка при шифровании данных: {e}")
                raise

        @strict_type
        @staticmethod
        def decrypt(key: bytearray, data: bytearray, iv_len: int) -> bytearray:
            """
            Дешифрование данных

            :param key: Ключ шифрования
            :type key: bytearray
            :param data: Данные, которые нужно расшифровать
            :type data: bytearray
            :param iv_len: Длина исходных данных
            :type iv_len: int
            :return: Расшифрованные данные
            :rtype: bytearray
            """
            try:
                logger.debug("Начало дешифрования данных с использованием Кузнечика")
                api = gostcrypto.gostcipher.new('kuznechik',
                                                key,
                                                gostcrypto.gostcipher.MODE_ECB,
                                                pad_mode=gostcrypto.gostcipher.PAD_MODE_1)
                result = api.decrypt(data)[:iv_len]
                logger.debug(f"Дешифрование завершено успешно: {result}")
                return result
            except Exception as e:
                logger.critical(f"Ошибка при дешифровании данных: {e}")
                raise

    class Magma:
        """
        Промежуточный класс для алгоритма ГОСТ 34.12-2018 ("Магма")
        """
        def __init__(self) -> None:
            pass

        @strict_type
        @staticmethod
        def encrypt(key: bytearray, data: bytearray) -> bytearray:
            """
            Шифрование данных

            :param key: Ключ шифрования
            :type key: bytearray
            :param data: Данные, которые нужно зашифровать
            :type data: bytearray
            :return: Шифрованные данные
            :rtype: bytearray
            """
            try:
                logger.debug("Начало шифрования данных с использованием Магмы")
                api = gostcrypto.gostcipher.new('magma',
                                                key,
                                                gostcrypto.gostcipher.MODE_ECB,
                                                pad_mode=gostcrypto.gostcipher.PAD_MODE_1)
                result = api.encrypt(data)
                logger.debug(f"Шифрование завершено успешно: {result}")
                return result
            except Exception as e:
                logger.critical(f"Ошибка при шифровании данных: {e}")
                raise

        @strict_type
        @staticmethod
        def decrypt(key: bytearray, data: bytearray, iv_len: int) -> bytearray:
            """
            Дешифрование данных

            :param key: Ключ шифрования
            :type key: bytearray
            :param data: Данные, которые нужно расшифровать
            :type data: bytearray
            :param iv_len: Длина исходных данных
            :type iv_len: int
            :return: Расшифрованные данные
            :rtype: bytearray
            """
            try:
                logger.debug("Начало дешифрования данных с использованием Магмы")
                api = gostcrypto.gostcipher.new('magma',
                                                key,
                                                gostcrypto.gostcipher.MODE_ECB,
                                                pad_mode=gostcrypto.gostcipher.PAD_MODE_1)
                result = api.decrypt(data)[:iv_len]
                logger.debug(f"Дешифрование завершено успешно: {result}")
                return result
            except Exception as e:
                logger.critical(f"Ошибка при дешифровании данных: {e}")
                raise
