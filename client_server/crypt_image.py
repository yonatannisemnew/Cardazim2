import hashlib
from PIL import Image
from Crypto.Cipher import AES

class CryptImage:

    def hash_key(self, key):
        if isinstance(key, str):
            key_hash_object = hashlib.sha256(key.encode())
        else:
            key_hash_object = hashlib.sha256(key)
        hashed_key = key_hash_object.digest()
        return hashed_key

    def __init__(self, image: Image.Image):
        self.image = image.convert('RGB')
        self.key_hash = None
    def show(self):
        self.image.show()

    def convert_to_bytes(self):
        width, hight = self.image.size
        return width.to_bytes(4) + hight.to_bytes(4) + self.image.tobytes() + self.key_hash.ljust(32, b'\x00')



    def encrypt(self, s):
        mode = self.image.mode
        key = self.hash_key(s)
        self.key_hash = self.hash_key(key)

        nonce = b'arazim'
        cipher = AES.new(key, AES.MODE_EAX, nonce=nonce)
        bytes_image = self.image.tobytes()
        encrypted_image_bytes = cipher.encrypt(bytes_image)
        self.image = Image.frombytes(mode, self.image.size, encrypted_image_bytes)

    def decrypt(self, s):
        mode = self.image.mode
        if self.key_hash is None:
            print("The image is not encrypted")
            return True

        key = self.hash_key(s)

        if self.hash_key(key) == self.key_hash:
            nonce = b'arazim'
            cipher = AES.new(key, AES.MODE_EAX, nonce=nonce)
            bytes_image = self.image.tobytes()
            decrypted_image_bytes = cipher.decrypt(bytes_image)
            self.image = Image.frombytes(mode, self.image.size, decrypted_image_bytes)
            self.key_hash = None
            return True
        else:
            return False

    @classmethod
    def create_from_path(cls, path):
        img = Image.open(path)
        return CryptImage(img)
    @classmethod
    def bytes_to_image(cls, bytes, hight, width):
        size = (width, hight)
        im = Image.frombytes('RGB', size, bytes)
        return im

def main():
    im = CryptImage.create_from_path('server_screen.png')
    im.image.show()
    im.encrypt("hello world")
    im.image.show()
    # try decrypting with the wrong key
    im.decrypt("hey")
    im.decrypt("hello world")
    im.image.show()

if __name__ == "__main__":
    main()
