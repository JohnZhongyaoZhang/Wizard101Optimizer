import time
from typing import List, Optional, Literal
import sqlite3

import pandas as pd
import numpy as np

import os


FIND_PET_QUERY = """
SELECT * FROM pets
LEFT JOIN locale_en ON locale_en.id == pets.name
WHERE locale_en.data == ? COLLATE NOCASE
"""

FIND_OBJECT_NAME_QUERY = """
SELECT * FROM pets
INNER JOIN locale_en ON locale_en.id == pets.name
WHERE pets.real_name == ? COLLATE NOCASE
"""

SPELL_NAME_ID_QUERY = """
SELECT locale_en.data FROM spells
INNER JOIN locale_en ON locale_en.id == spells.name
WHERE spells.real_name == ?
"""

EGG_NAME_ID_QUERY = """
SELECT locale_en.data FROM spells
INNER JOIN locale_en ON locale_en.id == spells.name
WHERE spells.real_name == ?
"""

SET_BONUS_NAME_QUERY = """
SELECT locale_en.data FROM set_bonuses
INNER JOIN locale_en ON locale_en.id == set_bonuses.name
WHERE set_bonuses.id == ?
"""

FIND_ITEMCARD_OBJECT_NAME_QUERY = """
SELECT * FROM spells
WHERE spells.template_id == ? COLLATE NOCASE
"""

DISPLAY_NAME_QUERY = """
SELECT locale_en.data FROM pets
INNER JOIN locale_en ON locale_en.id == pets.name
WHERE pets.id == ?
"""

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.dirname(SCRIPT_DIR)))
DATABASE_ROOT = os.path.join(PROJECT_ROOT, 'src', 'data', 'databases')
DATAFRAME_ROOT = os.path.join(PROJECT_ROOT, 'src', 'data', 'dataframes')

def remove_indices(lst, indices):
    return [value for index, value in enumerate(lst) if index not in indices]

class Pets:
    def __init__(self):
        self.db = sqlite3.connect(os.path.join(DATABASE_ROOT, 'everything.db'))
        self.id_list = None
        self.schoolList = ['Fire', 'Ice', 'Storm', 'Balance', 'Life', 'Myth', 'Death', 'Shadow', 'Moon']
        self.universalstats= ['Damage','Accuracy','Pierce','Resist','Crit Rating','Block Rating', 'Pip Conversion Rating']
        
    def fetch_object_name(self, name: str) -> List[tuple]:
        name_bytes = name.encode('utf-8')
        cursor = self.db.execute(FIND_OBJECT_NAME_QUERY, (name_bytes,))
        return cursor.fetchall()
        
    def fetch_itemcard_object_name(self, id: str) -> List[tuple]:
        cursor = self.db.execute(FIND_ITEMCARD_OBJECT_NAME_QUERY, (id,))
        return cursor.fetchall()
    
    def fetch_pet_cards(self, pet: int) :
        card_onames = []
        cursor = self.db.execute(
            "SELECT * FROM pet_cards WHERE pet == ?", (pet,)
        )

        for row in cursor:
                card_onames.append(row[-1])

        card_names = []
        for card in card_onames:
            cursor = self.db.execute(SPELL_NAME_ID_QUERY, (card,))
            card_name = cursor.fetchone()

            object_name = card.decode()

            card_names.append(object_name)

        return card_names
    
    def fetch_set_bonus_name(self, set_id: int) -> Optional[tuple]:
        if set_id == 0:
            return None
        else:
            cursor = self.db.execute(SET_BONUS_NAME_QUERY, (set_id,))
        return cursor.fetchone()[0]
    
    
    def format_card_string(self, cards) -> str:
        res = ""
        for card in cards:
            res += card + "\n"

        return res

    def fetch_pet_attributes(self, pet: int):
        attributes = {}
        
        row = self.db.execute("SELECT * FROM pets WHERE id == ?", (pet,)).fetchone()

        attributes['Name'] = row[2].decode("utf-8")
        attributes['Display'] = self.db.execute(DISPLAY_NAME_QUERY, (pet,)).fetchone()[0] #2
        if '\\n' in attributes['Display']:
            attributes['Display'] = attributes['Display'].replace('\\n',' ')
        attributes['Set'] = self.fetch_set_bonus_name(row[3])
        attributes['School'] = "Universal"
        attributes['Level'] = 0
        attributes['Cards'] = self.fetch_pet_cards(row[0])
        attributes['Cards'] = '|'.join(sorted(attributes['Cards']))

        # Hard Code in some stats
        if attributes['Name'] == "SkeletonArmored":
            attributes['Power Pip Chance'] = 1
        if attributes['Name'] == "Corgi":
            attributes['Energy'] = 8

        # Remove truly redundant pets
        if attributes['Set'] == None and attributes['Cards'] == '' and attributes['Name'] not in ['SkeletonArmored', 'Corgi']:
            return {}

        return attributes
    
    def generatePets(self):
        start = time.time()
        cursor = self.db.execute("SELECT id FROM pets")
        allIDs = cursor.fetchall()
        self.id_list = []
        for i in allIDs:
            self.id_list.append(i[0])
        
        importantIDs = []
        for id in self.id_list:
            attributes = self.fetch_pet_attributes(id)
            if attributes != {}:
                importantIDs.append(attributes)
            #else:
            #    print(id)
        
        table = pd.DataFrame.from_dict(importantIDs)
        table['Set'] = table['Set'].fillna('None')
        table.fillna(0,inplace=True)

        table.to_pickle(os.path.join(DATAFRAME_ROOT, 'allthepets.pkl'))
        table.to_csv(os.path.join(DATAFRAME_ROOT, 'allthepets.csv'), index=False)

        end = time.time()
        print(end-start)

        return table

def main():
    tableGen = Pets()
    tableGen.generatePets()

#main()