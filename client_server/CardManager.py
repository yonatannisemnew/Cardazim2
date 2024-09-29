from card import Card
from abc import ABC, abstractmethod
import json
import os
from card import Card
from crypt_image import CryptImage
from PIL import Image
import sqlite3
from hashlib import sha256
class CardDriver(ABC):
    @abstractmethod
    def Save(self, metadata: dict, identifier: str) ->None:
        ...
    def Load(self, identifier: str)-> dict:
        ...
    def GetCreators(self) -> list:
        ...
    def GetCreatorCards(self, creator: str) ->list:
        ...

class FileSystemDriver(CardDriver):
    def __init__(self):
        self.dirpath = './database'
    def Save(self, metadata, identifier: str):
        metadata_path = os.path.join(self.dirpath, identifier) + ".json"
        with open(metadata_path, "w") as metafile:
            json.dump(metadata, metafile)
    def Load(self, identifier: str):

        metadata_path = os.path.join(self.dirpath, identifier) + ".json"
        with open(metadata_path, 'r') as metafile:
            json_dict = json.load(metafile)
            return json_dict
    def GetCreators(self) -> list:
        Creators = []
        for path in os.listdir(self.dirpath):
            identifier = path[:-5]
            #it is +1 because there is a / after
            creator = self.Load(identifier)["creator"]
            if creator not in Creators:
                Creators.append(creator)
        return Creators

    def GetCreatorCards(self, the_creator: str) -> list:
        Metadatas = []
        for filename in os.listdir(self.dirpath):
            identifier = filename[:-5]
            metadata = self.Load(identifier)
            if metadata and metadata["creator"] == the_creator:
                Metadatas.append(metadata)
        return Metadatas


class CardDriverSQL(CardDriver):
    def __init__(self):
        self.database = 'sql_cards'
        conn = sqlite3.connect(self.database)
        cursor = conn.cursor()
        cursor.execute('''
                    CREATE TABLE IF NOT EXISTS sql_cards (
                        identifier TEXT NOT NULL,
                        name TEXT NOT NULL,
                        creator TEXT NOT NULL,
                        riddle TEXT NOT NULL,
                        solution TEXT
                    )
                ''')
        conn.commit()
        conn.close()
    def Save(self, metadata, identifier: str) ->None:
        name = metadata["name"]
        riddle = metadata["riddle"]
        creator = metadata["creator"]
        solution = metadata["solution"]
        conn = sqlite3.connect(self.database)
        cursor = conn.cursor()
        #add element to the cards table
        cursor.execute('''
            INSERT INTO sql_cards (identifier, name, creator, riddle, solution)
            VALUES (?,?, ?, ?,?)
        ''', (identifier, name, creator, riddle, solution))
        conn.commit()
        conn.close()

    def Load(self, identifier: str):
        conn = sqlite3.connect(self.database)
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM sql_cards')
        rows = cursor.fetchall()
        for row in rows:
            #a row is [identifier, name, creator riddle, solution]
            if row[0] == identifier:
                metadata = {}
                metadata["identifier"] = row[0]
                metadata["name"] = row[1]
                metadata["creator"] = row[2]
                metadata["riddle"] = row[3]
                metadata["solution"] = row[4]
                conn.close()
                return metadata
        print("No card found")
        conn.close()


    def GetCreators(self) -> list:
        Creators = []
        conn = sqlite3.connect(self.database)
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM sql_cards')
        rows = cursor.fetchall()
        for row in rows:
            if row[2] not in Creators:
                Creators.append((row[2]))
        return Creators

    def GetCreatorCards(self, creator: str) ->list:
        Metadatas = []
        conn = sqlite3.connect(self.database)
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM sql_cards')
        rows = cursor.fetchall()
        for row in rows:
            if row[2] == creator:
                Metadatas.append(self.Load(row[0]))
                #loading th card by its identifier
        return Metadatas
class Saver:
    def __init__(self, driver_type, images_dir):
        if driver_type =="filesystem":
            self.driver = FileSystemDriver()
        if driver_type == "sql":
            self.driver = CardDriverSQL()
        self.images_dir = images_dir
    def Save(self, card: Card):
        metadata, image = Saver.parse_card(card)
        image.save(os.path.join(self.images_dir, f"{Saver.generate_identifier(card)}.png"))
        self.driver.Save(metadata, Saver.generate_identifier(card))
    @classmethod
    def parse_card(cls, card: Card):
        image = card.image.image
        metadata = {}
        metadata["name"] = card.name
        metadata["creator"] = card.creator
        metadata["riddle"] = card.riddle
        metadata["solution"] = card.solution
        return metadata, image
    @classmethod
    def generate_identifier(cls, card):
        creator_hash = sha256(card.creator.encode()).hexdigest()
        name_hash = sha256(card.name.encode()).hexdigest()
        return creator_hash + name_hash



def main():
    saver = Saver("filesystem", "./images")
    card = Card.create_from_path("a good riddle", "yonatan", "server_screen.png", "what's my name", None)
    saver.Save(card)
    print(saver.driver.Load(Saver.generate_identifier(card)))
    print(saver.driver.GetCreatorCards("yonatan"))
    print(saver.driver.GetCreators())



if __name__ == "__main__":
    main()
