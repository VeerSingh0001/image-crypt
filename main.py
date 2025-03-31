from Crypto.Cipher import DES3
from Crypto.Random import get_random_bytes
from Crypto.Util.Padding import pad, unpad
from Crypto.Protocol.KDF import PBKDF2
import os
import glob

def encrypt_img(i_path, phrase):
    # [FUNCTION] Encrypt an image file using DES3.
    try:
        salt = os.urandom(24)
        key = PBKDF2(phrase, salt, dkLen=24)

        with open(i_path, "rb") as file:
            plaintext_bytes = file.read()

        iv = get_random_bytes(8)

        padded_data = pad(plaintext_bytes, DES3.block_size)
        cipher = DES3.new(key, DES3.MODE_CBC, iv)
        encrypted_img = cipher.encrypt(padded_data)

        with open(f"{i_path}.des", "wb") as file:
            file.write(salt + iv + encrypted_img)

        print(f"Encryption Successful: {i_path}")
        return 1
    except Exception as e:
        print(f"An error occurred during encryption: {e}")
        return 0

def decrypt_img(enc_img_path, phrase):
    # [FUNCTION] Decrypt an encrypted image file using DES3.
    try:
        with open(enc_img_path, "rb") as file:
            file_data = file.read()

        salt = file_data[:24]
        iv = file_data[24:32]
        enc_img_data = file_data[32:]

        key = PBKDF2(phrase, salt, dkLen=24)

        cipher = DES3.new(key, DES3.MODE_CBC, iv)

        decrypted_padded = cipher.decrypt(enc_img_data)
        decrypted_data = unpad(decrypted_padded, DES3.block_size)

        img_path = enc_img_path.replace(".des", "")

        with open(img_path, "wb") as file:
            file.write(decrypted_data)

        print(f"Decryption Successful: {enc_img_path}")
        return 1
    except ValueError as e:
        print(f"Decryption failed: Incorrect passphrase for {enc_img_path}.")
        return 0
    except Exception as e:
        print(f"An error occurred during decryption: {e}")
        return -1 

def encrypt_multiple_files(file_paths, passphrase):
    # [BATCH] Loop through files to encrypt each image.
    try:
        for file_path in file_paths:
            encrypt_img(file_path, passphrase)
        return 1
    except Exception as e:
        print("main file")
        print(f"An error occurred during encryption: {e}")
        return 0

def decrypt_multiple_files(encrypted_files, passphrase):
    # [BATCH] Loop through files to decrypt each image.
    try:
        for enc_file in encrypted_files:
            decrypt_img(enc_file, passphrase)
        return 1
    except Exception as e:
        print(f"An error occurred during decryption: {e}")
        return 0
