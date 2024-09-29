from card import Card
import json
import os
from card import Card
from crypt_image import CryptImage
from PIL import Image



class CardManager:
    def __init__(self, dir_path):
        self.dir_path = dir_path

    def save(self, card: Card):
        card_dir = os.path.join(self.dir_path, self.get_identifier(card))
        os.makedirs(card_dir, exist_ok=True)  # Ensure directory exists

        meta_data_path = os.path.join(card_dir, "metadata.json")
        img_path = os.path.join(card_dir, "image.png")

        metadata = {
            "name": card.name,
            "creator": card.creator,
            "riddle": card.riddle,
            "solution": card.solution,
        }

        with open(meta_data_path, "w") as metafile:
            json.dump(metadata, metafile)

        card.image.image.save(img_path)

    def get_identifier(self, card: Card):
        return f"{card.creator}/{card.name}"

    def load(self, identifier):
        card_dir = os.path.join(self.dir_path, identifier)
        meta_data_path = os.path.join(card_dir,"metadata.json")
        img_path = os.path.join(card_dir, "image.png")
        with open(meta_data_path, 'r') as metafile:
            json_dict = json.load(metafile)
            name = json_dict["name"]
            creator = json_dict["creator"]
            riddle = json_dict["riddle"]
            solution = json_dict["solution"]
            img = CryptImage(Image.open(img_path))
            card = Card(name, creator,img, riddle, solution)
            return card




def main():
    card  = Card.create_from_path("my fav drink", "yonatan", "server_screen.png", "what's my drink", None)
    maneger = CardManager('.')
    maneger.save(card)
    print(maneger.load('yonatan/my fav drink'))




if __name__ =="__main__":
    main()
