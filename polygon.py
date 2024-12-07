from cypher import Cypher
from keygen import generate_unique_key

with open('./output_folder/block_0000.bin', 'rb') as f:
    data = bytearray(f.read())

key = bytearray.fromhex(generate_unique_key())
result_cyp = Cypher.encrypt(data=data, method='magma', key=key)
# print(result_cyp)
result_dec = Cypher.decrypt(data=result_cyp['cyphered_data'], key=key, method='magma',plain_hash='ca4a87f71e2ba78b801fae43d7030fe4551ec4f9c90b361aa6da2492825ba1be', iv_len=result_cyp['iv_len'])
# print(result_dec)
