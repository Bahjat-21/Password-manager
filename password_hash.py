import hashlib
import os


class ENCRYPTOR:
    def __init__(self):
        self.password_uncode = None

    def encrypt_password(self, ptpw):
        encoded_password = ptpw.encode()
        salt = hashlib.sha256(os.urandom(64)).hexdigest().encode()
        hashed_pw = hashlib.pbkdf2_hmac("sha512", encoded_password, salt, 100000).hex().encode()
        storable_pw = (salt + hashed_pw).decode()
        return storable_pw

    def verify_password(self, password, stored_password):
        salt = stored_password[:64].encode()
        self.password_uncode = password
        password = password.encode()
        test_password = hashlib.pbkdf2_hmac("sha512", password, salt, 100000).hex().encode()
        test_password = (salt + test_password).decode()
        print(test_password)
        print(stored_password)
        return test_password == stored_password


    def get_password(self, password):
        return password

crypto = ENCRYPTOR()

