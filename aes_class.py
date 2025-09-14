# aes_class.py
from Crypto.Cipher import AES
from Crypto.Random import get_random_bytes
from Crypto.Util.Padding import pad, unpad
import base64, hashlib

class AESclass:
    def encrypt(self, message, key):
        key_bytes = hashlib.sha256(key.encode()).digest()
        iv = get_random_bytes(16)
        cipher = AES.new(key_bytes, AES.MODE_CBC, iv)
        ct = cipher.encrypt(pad(message.encode('utf-8'), AES.block_size))
        return base64.b64encode(iv + ct).decode('ascii')

    def decrypt(self, ciphertext, key):
        raw = base64.b64decode(ciphertext)
        iv, ct = raw[:16], raw[16:]
        key_bytes = hashlib.sha256(key.encode()).digest()
        cipher = AES.new(key_bytes, AES.MODE_CBC, iv)
        pt = unpad(cipher.decrypt(ct), AES.block_size)
        return pt.decode('utf-8')

aes = AESclass()
