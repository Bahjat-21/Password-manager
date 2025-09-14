# Pssword-manager
Password Manager (CLI, Python)

A small, learning-oriented command-line password manager.
It uses SQLite for storage, PBKDF2 for login password hashing, and AES (via PyCryptodome) to encrypt service passwords.

Requirements

Python 3.12+

PyCryptodome (pip install pycryptodome)

What it does

Register/login users; update/delete accounts (SQLite).

Store/list/update/delete service credentials per user.

Hash login passwords with PBKDF2-HMAC-SHA512 + salt.

Encrypt stored service passwords with AES (CBC + PKCS7) and a random IV.

Generate secure random passwords with secrets
