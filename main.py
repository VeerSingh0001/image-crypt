from Crypto.Cipher import DES3
from Crypto.Random import get_random_bytes
from Crypto.Util.Padding import pad, unpad
from Crypto.Protocol.KDF import PBKDF2
import os


def encrypt_img(i_path, phrase):
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

        print("Encryption Successful")
    except FileNotFoundError:
        print(f"Error: File '{i_path}' not found.")
    except Exception as e:
        print(f"An error occurred during encryption: {e}")


def decrypt_img(enc_img_path, img_path, phrase):
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

        with open(img_path, "wb") as file:
            file.write(decrypted_data)

        print("Decryption Successful")
    except FileNotFoundError:
        print(f"Error: File '{enc_img_path}' not found.")
    except ValueError as e:
        print(f"Decryption failed: Incorrect passphrase.")
    except Exception as e:
        print(f"An error occurred during decryption: {e}")


if __name__ == "__main__":
    try:
        passphrase = input("Enter the passphrase: ")

        img_path = r"D:\Pictures\RR_Phantom_US_exterior_40.jpg"
        dec_img_path = r"D:\RR_Phantom_US_exterior_40.jpg"

        encrypt_img(img_path, passphrase)

        passphrase2 = input("Enter the passphrase: ")

        decrypt_img(f"{img_path}.des", dec_img_path, passphrase2)
    except KeyboardInterrupt:
        print("\nOperation canceled by user.")
    except Exception as e:
        print(f"An unexpected error occurred: {e}")
