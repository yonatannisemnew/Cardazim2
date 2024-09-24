from crypt_image import CryptImage
from PIL import Image

class Card:
    def __init__(self, name, creator, image, riddle, solution):
        self.name = name
        self.creator = creator
        self.image = image
        self.riddle = riddle
        self.solution = solution
    def __repr__(self):
        return f"Card name is {self.name} And creator is {self.creator}"
    def __str__(self):
        first_line = f"Card {self.name} by {self.creator}"
        second_line = f"riddle: {self.riddle}"
        if self.solution:
            third_line = f"solution: {self.solution}"
        else:
            third_line = f"solution: Unsolved"
        return '\n'.join([first_line, second_line, third_line])

    def serialize(self):
        name_length = len(self.name)
        name_length_bytes = name_length.to_bytes(4)
        name_to_send = name_length_bytes + self.name.encode()
        creator_length = len(self.creator)
        creator_len_bytes = creator_length.to_bytes(4)
        creator_to_send = creator_len_bytes + self.creator.encode()
        image_bytes = self.image.convert_to_bytes()
        riddle_length = len(self.riddle)
        riddle_length_bytes = riddle_length.to_bytes(4)
        riddle_to_send = riddle_length_bytes + self.riddle.encode()
        return name_to_send + creator_to_send + image_bytes +  riddle_to_send




    @classmethod
    def create_from_path(cls, name, creator, path, riddle, solution):
        image = CryptImage.create_from_path(path)
        return Card(name, creator, image, riddle, solution)
    @classmethod

    def deserialize(cls , data):
        name_length = int.from_bytes(data[0:4])
        data = data[4:]
        name = data[0:name_length].decode()
        data = data[name_length:]
        creator_length = int.from_bytes(data[0:4])
        data = data[4:]
        creator = data[0:creator_length].decode()
        data = data[creator_length:]
        width = int.from_bytes(data[0:4])
        data = data[4:]
        hight = int.from_bytes(data[0:4])
        data = data[4:]
        image = CryptImage.bytes_to_image(data[0:3*hight*width],hight, width)
        data = data[3*hight*width:]
        key_hash = data[0:32]
        data = data[32:]
        riddle_length = int.from_bytes(data[0:4])
        data = data[4:]
        riddle = data.decode()
        card = Card(name, creator, CryptImage(image), riddle, None)
        card.image.key_hash = key_hash
        return card
def main():
    solution = "Yonatan"
    card = Card.create_from_path("Easy card", "Yonatan", "server_screen.png", "Whats my name?", "Yonatan")
    card.image.encrypt(card.solution)
    data = card.serialize()
    card2 = Card.deserialize(data)
    card2.image.show()
    if card2.image.decrypt(solution):
        card2.solution = solution
    assert (repr(card) == repr(card2))
    card2.image.show()  # will show the same image as in path

if __name__ == "__main__":
    main()


