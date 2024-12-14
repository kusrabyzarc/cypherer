from disk_interface import DiskInterface
from block_processor import BlockProcessor
from russian_crypto import RussianCrypto
from keygen import generate_unique_key
from passphrase import Passphrase
import json

from logger_module import create_logger

logger = create_logger('CLI')

class CLI:
    """
    Интерфейс взаимодействия с пользователем
    """
    def __init__(self) -> None:
        self.__disk_letter__ = None
        self.__disk_interface__ = None
        self.__command_list__ = {func.lstrip('command_'): self.__getattribute__(func) for func in dir(self) if callable(getattr(self, func)) and func.startswith("command_")}
        self.pph_engine = Passphrase()

    def __build_invitation__(self) -> str:
        if self.__disk_letter__ is not None:
            return f'Cypherer (Disk {self.__disk_letter__}:)> '
        
        return 'Cypherer> '

    def command_set_disk(self, args) -> None:
        if args == '':
            print('Не передана буква диска')
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
            meta[file] = {'iv_len': iv_len, 'algo': algo.__name__, 'key': key, 'hash': hash}
        
        pph_encoded = RussianCrypto.random(16).hex()
        pph = self.pph_engine.encode(pph_encoded)
        meta = json.dumps(meta)
        encrypted_meta = RussianCrypto.Kuznechik.encrypt(data=meta, key=bytearray(bytes.fromhex(generate_unique_key())))
        print(json.loads(RussianCrypto.Kuznechik.decrypt(key=bytearray(bytes.fromhex(generate_unique_key())), data=encrypted_meta, iv_len=len(encrypted_meta))))

        # self.__disk_interface__.erase()
        # self.__disk_interface__.write(encrypted_data)
        # print(encrypted_data)
        # print(meta)
            


    def run(self) -> None:
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


if __name__ != '__main__':
    logger.error('Подразумевается прямой вызов этого модуля')
    exit(-1)

cli = CLI()
cli.run()