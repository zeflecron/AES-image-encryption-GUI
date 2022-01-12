import os
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
import base64

class EncFunc:
    def __init__(self):
        pass

    # generate new key and iv
    # NOTE: can overwrite existing files
    @staticmethod
    def generate_key(aes_file, iv_file):
        # use true random number instead of pseudo-random
        aes = os.urandom(32)    # 32 bytes = 256 bits (strong for AES)
        iv = os.urandom(16)     # 16 bytes = block size
        aes_path = '../keys/' + aes_file + '.txt'
        iv_path = '../keys/' + iv_file + '.txt'
        with open(aes_path, 'wb') as new_aes_file:
            new_aes_file.write(aes)
        with open(iv_path, 'wb') as new_iv_file:
            new_iv_file.write(iv)

        print('Successfully generated new AES and iv key')


    # to add an extra layer of encryption
    # `rb` because the library requires them to be read in byte-like object
    @staticmethod
    def mode(option, aes_path, iv_path):
        global cipher
        with open(aes_path, 'rb') as file:
            aes = file.read()
        with open(iv_path, 'rb') as file:
            iv = file.read()

        if option == 'CTR':
            cipher = Cipher(algorithms.AES(aes), modes.CTR(iv))
        elif option == 'CFB':
            cipher = Cipher(algorithms.AES(aes), modes.CFB(iv))
        elif option == 'OFB':
            cipher = Cipher(algorithms.AES(aes), modes.OFB(iv))


    # images must be converted into string before it can be encrypted
    # NOTE: can overwrite existing files
    def encrypt(self, image_paths, option, aes_path, iv_path):
        self.mode(option, aes_path, iv_path)
        for path in image_paths:
            # convert image to string
            with open(path, 'rb') as image:
                encoded = base64.b64encode(image.read())

            # encrypt string
            encryptor = cipher.encryptor()
            encrypted_string = encryptor.update(encoded) + encryptor.finalize()

            no_extension = os.path.splitext(path)[0]
            file_name = os.path.basename(no_extension)
            file_path = '../enc_images/' + file_name + '.bin'
            with open(file_path, 'wb') as file:
                file.write(encrypted_string)

            print('Image has been encrypted')


    # strings must be converted back to image format
    # result only in .png
    # NOTE: can overwrite existing files
    def decrypt(self, data_paths, option, aes_path, iv_path):
        self.mode(option, aes_path, iv_path)
        for path in data_paths:
            with open(path, 'rb') as file:
                encrypted_string = file.read()

            # decrypt string
            decryptor = cipher.decryptor()
            decrypted_string = \
                decryptor.update(encrypted_string) + \
                decryptor.finalize()

            # convert string to image
            decoded = base64.b64decode(decrypted_string)

            no_extension = os.path.splitext(path)[0]
            file_name = os.path.basename(no_extension)
            file_path = '../dec_images/' + file_name + '.png'
            with open(file_path, 'wb') as file:
                file.write(decoded)

            print('Image has been decrypted')
