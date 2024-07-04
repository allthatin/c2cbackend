
import random
import datetime
import os

from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.primitives.padding import PKCS7
import string

def encrypt(key: bytes, data: bytes):
    iv = b"\x00" * 16
    # PKCS7 padding
    padder = PKCS7(algorithms.AES.block_size).padder()
    cipher = Cipher(algorithms.AES(key), modes.CBC(iv))

    # Encrypt a message
    padded_data = padder.update(data) + padder.finalize()
    encryptor = cipher.encryptor()
    ciphertext: bytes = encryptor.update(padded_data) + encryptor.finalize()
    hex_str = ciphertext.hex()
    return hex_str.upper()


def decrypt(key: bytes, data: bytes):
    # Decrypt the ciphertext
    iv = b"\x00" * 16
    cipher = Cipher(algorithms.AES(key), modes.CBC(iv))
    decryptor = cipher.decryptor()
    decrypted_message = decryptor.update(data) + decryptor.finalize()
    unpadder = PKCS7(algorithms.AES.block_size).unpadder()
    output = unpadder.update(decrypted_message) + unpadder.finalize()
    return output
