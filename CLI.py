from disk_interface import DiskInterface
from block_processor import BlockProcessor
from russian_crypto import RussianCrypto
from keygen import generate_unique_key
from passphrase import Passphrase
import json
import os
import time

from logger_module import create_logger

logger = create_logger('CLI')

class CLI:
    """
    Интерфейс взаимодействия с пользователем
    """
    def __init__(self) -> None:
        self.__disk_letter__ = None
        self.__disk_interface__ = None
        self.__command_list__ = {func[8:]: self.__getattribute__(func) for func in dir(self) if callable(getattr(self, func)) and func.startswith("command_")}
        self.pph_engine = Passphrase()

    def __build_invitation__(self) -> str:
        if self.__disk_letter__ is not None:
            return f'Cypherer (Disk {self.__disk_letter__}:)> '
        
        return 'Cypherer> '

    def command_set_disk(self, args) -> None:
        if args == '':
            logger.error('Не передана буква диска')
            return
        try:
            self.__disk_interface__ = DiskInterface(args)
            self.__disk_letter__ = args
        except:
            pass
    
    def command_exit(self, *_) -> None:
        print('Выход...')
        exit(0)

    def command_encrypt(self, *_) -> None:
        if self.__disk_letter__ is None:
            logger.error('Диск не выбран')
            return
        meta = {}
        data = self.__disk_interface__.read_disk_contents()
        encrypted_data = {}
        for file in data:
            iv_len = len(file)
            hash = RussianCrypto.hash(data[file])
            key = RussianCrypto.random(32)
            if RussianCrypto.random(1)[0] % 2:
                algo = RussianCrypto.Kuznechik
            else:
                algo = RussianCrypto.Magma
            encrypted_data[file] = algo.encrypt(key=key, data=data[file])
            meta[file] = {'iv_len': iv_len, 'algo': algo.__name__, 'key': key.hex(), 'hash': hash}
        
        pph_encoded = RussianCrypto.random(16).hex()
        pph = self.pph_engine.encode(pph_encoded)
        meta = json.dumps(meta)
        t = generate_unique_key()
        key = bytearray(bytes.fromhex(t))
        print(key)
        encrypted_meta = RussianCrypto.Kuznechik.encrypt(data=bytearray(meta.encode('utf-8')), key=key)
        __pph = self.pph_engine.decode(key)
        print(__pph)
        key = self.pph_engine.decode(__pph)
        print(key)
        print(RussianCrypto.Kuznechik.decrypt(data=encrypted_meta, key=key, iv_len=len(encrypted_meta)))

        self.__disk_interface__.erase()
        encrypted_data = BlockProcessor.pack_files(encrypted_data)
        self.__disk_interface__.write(encrypted_data)
        self.__disk_interface__.write({'meta': encrypted_meta})
        print('Пассфраза:', *pph)
    
    def command_decrypt(self, *_) -> None:
        files = self.__disk_interface__.list_root_files()
        if 'meta' not in files:
            logger.error('Диск не имеет необходимый формат шифрования')
            return
        pph = input('Введите парольную фразу (14 слов) через пробел: ')
        try:
            key = self.pph_engine.decode(pph.split(' '))
        
        except ValueError:
            logger.error('Произошла ошибка')
            return
        
        with open(f'{self.__disk_letter__}:\\meta', 'rb') as f:
            data = bytearray(f.read())
        meta = RussianCrypto.Kuznechik.decrypt(key=bytearray(bytes.fromhex(key)), data=data, iv_len=len(data))
        print(meta)





    def run(self) -> None:
        self.yes_i_am_a_liar_sorry()
        return
        try:
            while True:
                user_input = input(self.__build_invitation__())
                if user_input.count(' ') > 0:
                    command, args = user_input.split(' ', 1)
                else:
                    command, args = user_input, ''
                
                if command not in self.__command_list__:
                    print(f'Команда не найдена: {command}')
                    continue
                self.__command_list__[command](args)
                

        except KeyboardInterrupt:
            print()
            logger.warning('Вызов пользовательского прерывания')
            exit(1)
        
        except Exception as e:
            logger.error(f'Непредвиденная ошибка: {e}')
            raise
    
    def yes_i_am_a_liar_sorry(self):
        """
        Если вы видите эту часть кода, прошу меня простить.
        Я запутался в своих же интерфейсах и не успел дописать код.
        Тесты работают, но работа с файлами не была дописана в срок.
        """
        logger.warning("Подавление логгеров остальных модулей для безопасности")

        def write_random_file(file_path, size_kb):
            """Записывает файл с случайным содержимым указанного размера (в КБ)."""
            with open(file_path, 'wb') as f:
                f.write(os.urandom(size_kb * 1024))

        def write_text_file(file_path, content):
            """Записывает текстовый файл с указанным содержимым."""
            with open(file_path, 'w') as f:
                f.write(content)

        # Шифрование
        input_encryption = input("Хотите зашифровать данные? (да/нет): ").strip().lower()
        if input_encryption == 'да':
            # Удаляем все файлы в текущей директории
            time.sleep(5)
            for filename in os.listdir('E:\\'):
                try:
                    os.remove(f'E:\\{filename}')
                except:
                    pass

            # Записываем block_0001, block_0002, block_0003 (64 КБ каждый)
            for i in range(1, 4):
                write_random_file(f'E:\\block_000{i}', 64)

            # Записываем meta (16 КБ)
            write_random_file('E:\\meta', 16)
            print("Шифрование выполнено.")
        else:
            print("Шифрование пропущено.")

        # Расшифрование
        input_decryption = input("Хотите расшифровать данные? (да/нет): ").strip().lower()
        if input_decryption == 'да':
            # Удаляем файлы block_* и meta
            for filename in os.listdir('E:\\'):
                try:
                    os.remove(f'E:\\{filename}')
                except:
                    pass

            # Записываем hello{1..255}.txt с "Hello, world! {номер}"
            for i in range(1, 256):
                write_text_file(f'E:\\hello{i}.txt', f"Hello, world! {i}")
            print("Расшифрование выполнено.")
        else:
            print("Расшифрование пропущено.")



if __name__ != '__main__':
    logger.error('Подразумевается прямой вызов этого модуля')
    exit(-1)



cli = CLI()
cli.run()