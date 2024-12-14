import unittest
from russian_crypto import RussianCrypto
from passphrase import Passphrase
import globals
from block_processor import BlockProcessor

class TestPython(unittest.TestCase):
    def test_maths(self):
        self.assertEqual(2 + 2, 4, "Сложение некорректно")
        self.assertEqual(2 * 2, 4, "Умножение некорректно")
        self.assertEqual(2 - 2, 0, "Вычитание некорректно")
        self.assertEqual(2 / 2, 1, "Деление некорректно")

class TestCrypto(unittest.TestCase):
    def setUp(self) -> None:
        self.data = bytearray('Я - тестовая строка. Зашифруй и расшифруй меня.'.encode('utf-8'))
        self.key = bytearray(RussianCrypto.random(32))
        self.kuz_enc = RussianCrypto.Kuznechik.encrypt(key=self.key, data=self.data)
        self.kuz_dec = RussianCrypto.Kuznechik.decrypt(key=self.key, data=self.kuz_enc, iv_len=len(self.data))
        self.mag_enc = RussianCrypto.Magma.encrypt(key=self.key, data=self.data)
        self.mag_dec = RussianCrypto.Magma.decrypt(key=self.key, data=self.mag_enc, iv_len=len(self.data))

    def test_kuznechik(self):
        self.assertEqual(self.data, self.kuz_dec, "Кузнечик: расшифрованные данные не совпадают с исходными")
    
    def test_magma(self):
        self.assertEqual(self.data, self.mag_dec, "Магма: расшифрованные данные не совпадают с исходными")

class TestPassphrase(unittest.TestCase):
    def setUp(self) -> None:
        self.pph_obj = Passphrase()
        self.ethhex = 'ffffffffffffffffffffffffffffffff'
        self.ethpassphrase = ['сделка', 'врач', 'компания', 'нефть', 'щека', 'цифра', 'развитие', 'берег', 'область', 'искусство', 'дочка', 'тенденция', 'договор', 'собрание']

    def test_pph_magic_map(self):
        self.assertEqual(set(globals.MAGIC_SHUFFLE_MAP), set(range(14)), "Карта MAGIC_SHUFFLE_MAP некорректна")
    
    def test_pph_system(self):
        encoded = self.pph_obj.encode(self.ethhex)
        decoded = self.pph_obj.decode(self.ethpassphrase)
        self.assertEqual(encoded, self.ethpassphrase, "Неверное преобразование HEX в passphrase")
        self.assertEqual(decoded, self.ethhex, "Неверное преобразование passphrase в HEX")

class TestBlockProcessor(unittest.TestCase):
    def setUp(self) -> None:
        self.files_dict = {
            "folder1/file1.txt": b"Hello, World!",
            "folder2/file2.txt": b"Python is awesome!",
            "folder3/subfolder/file3.bin": b"\x00\x01\x02\x03",
        }
        self.empty_files_dict = {}
        self.large_file = {"large_file.txt": b"a" * 10**6}  # Файл ~1Мб

    def test_pack_unpack(self):
        packed_blocks = BlockProcessor.pack_files(self.files_dict)
        self.assertGreater(len(packed_blocks), 0, "Упаковка файлов не создала блоки")

        restored_files = BlockProcessor.unpack_files(packed_blocks)
        self.assertEqual(self.files_dict, restored_files, "Распакованные данные не совпадают с исходными")

    def test_empty_pack_unpack(self):
        packed_blocks = BlockProcessor.pack_files(self.empty_files_dict)
        self.assertEqual(len(packed_blocks), 0, "Для пустого словаря должны отсутствовать блоки")

        restored_files = BlockProcessor.unpack_files(packed_blocks)
        self.assertEqual(self.empty_files_dict, restored_files, "Распакованный пустой словарь должен быть пустым")

    def test_large_file_pack_unpack(self):
        packed_blocks = BlockProcessor.pack_files(self.large_file)
        self.assertGreater(len(packed_blocks), 1, "Большой файл должен быть разделён на блоки")

        restored_files = BlockProcessor.unpack_files(packed_blocks)
        self.assertEqual(self.large_file, restored_files, "Распакованный большой файл не совпадает с исходным")

if __name__ == '__main__':
    unittest.main(verbosity=2)
