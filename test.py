import unittest
from russian_crypto import RussianCrypto
from passphrase import Passphrase
import globals
from keygen import generate_unique_key

class TestPython(unittest.TestCase):
    def setUp(self) -> None:
        pass

    def test_maths(self):
        self.assertEqual(2 + 2, 4)
        self.assertEqual(2 * 2, 4)
        self.assertEqual(2 - 2, 0)
        self.assertEqual(2 / 2, 1)

class TestCrypto(unittest.TestCase):
    def setUp(self) -> None:
        self.data = bytearray('Я - тестовая строка. Зашифруй и расшифруй меня.'.encode('utf-8'))
        self.key = bytearray(RussianCrypto.random(32))
        self.kuz_enc = RussianCrypto.Kuznechik.encrypt(key=self.key, data=self.data)
        self.kuz_dec = RussianCrypto.Kuznechik.decrypt(key=self.key, data=self.kuz_enc, iv_len=len(self.data))
        self.mag_enc = RussianCrypto.Magma.encrypt(key=self.key, data=self.data)
        self.mag_dec = RussianCrypto.Magma.decrypt(key=self.key, data=self.mag_enc, iv_len=len(self.data))

    def test_kuznechik(self):
        self.assertEqual(self.data, self.kuz_dec)
    
    def test_magma(self):
        self.assertEqual(self.data, self.mag_dec)

class TestPassphrase(unittest.TestCase):
    def setUp(self) -> None:
        self.pph_obj = Passphrase()
        self.ethhex = 'ffffffffffffffffffffffffffffffff'
        self.ethpassphrase = ['сделка', 'врач', 'компания', 'нефть', 'щека', 'цифра', 'развитие', 'берег', 'область', 'искусство', 'дочка', 'тенденция', 'договор', 'собрание']

    def test_pph_magic_map(self):
        self.assertEqual(set(globals.MAGIC_SHUFFLE_MAP), set(range(14))) # Проверка, что карта верной длины и содержания
    
    def test_pph_system(self):
        self.assertEqual(self.pph_obj.encode(self.ethhex), self.ethpassphrase)
        self.assertEqual(self.pph_obj.decode(self.ethpassphrase), self.ethhex)



if __name__ == '__main__':
    unittest.main(verbosity=2)