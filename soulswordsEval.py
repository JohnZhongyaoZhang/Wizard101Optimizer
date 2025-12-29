import pandas as pd

from src.data.dataConstruction.gear import Gear
from src.data.dataConstruction.mobs import Mobs
from src.data.dataConstruction.pets import Pets
from src.math.petCreator import Pet

from src.math.wizard import Wizard
from src.math.wizmath import WizMath

import os

DATAFRAME_ROOT = os.path.join('src', 'data', 'dataframes')

class Optimizer:
    def __init__(self):
        self.gearTable = None
        self.setTable = None
        self.mobTable = None

        self.generateTables()

    def generateTables(self):
        GeneratorClass = Gear()
        MobClass = Mobs()
        PetClass = Pets()
        if os.path.exists(os.path.join(DATAFRAME_ROOT, 'allthegear.pkl')):
            self.gearTable = pd.read_pickle(os.path.join(DATAFRAME_ROOT, 'allthegear.pkl'))
        else:
            print("Gear table not found, creating gear table")
            self.gearTable = GeneratorClass.generateGear()

        if os.path.exists(os.path.join(DATAFRAME_ROOT, 'allthesets.pkl')):
            self.setTable = pd.read_pickle(os.path.join(DATAFRAME_ROOT, 'allthesets.pkl'))
        else:
            print("Set bonus table not found, creating set bonus table")
            self.setTable = GeneratorClass.generateAllSets()
        
        if os.path.exists(os.path.join(DATAFRAME_ROOT, 'allthemobs.pkl')):
            self.mobTable = pd.read_pickle(os.path.join(DATAFRAME_ROOT, 'allthemobs.pkl'))
        else:
            print("Mob table not found, creating mob table")
            self.mobTable = MobClass.generateMobs()
            
        if os.path.exists(os.path.join(DATAFRAME_ROOT, 'allthepets.pkl')):
            self.petTable = pd.read_pickle(os.path.join(DATAFRAME_ROOT, 'allthepets.pkl'))
        else:
            print("Pet table not found, creating pet table")
            self.petTable = PetClass.generatePets()

        missingColumns = self.gearTable.columns.difference(self.setTable.columns)

        self.setTable = pd.concat(
        [self.setTable, pd.DataFrame(0, index=self.setTable.index, columns=missingColumns)],
        axis=1
        )

def main():
    TheOptimizer = Optimizer()
    exemptPieces = ['Mount', 'Jewel']

    #filteredTable = TheOptimizer.gearTable

    filteredTable = TheOptimizer.gearTable[
    (TheOptimizer.gearTable['Kind'].isin(exemptPieces)) |
    (TheOptimizer.gearTable['Level'] >= 160)
    ]

    wizards = {}
    wizardsGear = {}

    wizardsGear['Storm'] = {
                "Hat": "Crimefighter",
                "Robe": "Monster Hide",
                "Shoes": "Abomination",
                "Weapon": "Rod",
                "Athame": "Abomination",
                "Amulet": "Crimefighter",
                "Ring": "Abomination",
                "Deck": "Crimefighter",
                "Mount": "Clockwork Courser"
                }
    
    wizardsGear['Fire'] = {
                "Hat": "Crimefighter",
                "Robe": "Monster Hide",
                "Shoes": "Abomination",
                "Weapon": "Rod",
                "Athame": "Abomination",
                "Amulet": "Crimefighter",
                "Ring": "Abomination",
                "Deck": "Crimefighter",
                "Mount": "Stompy Bronto"
                }

    wizardsGear['Myth'] = {
                "Hat": "Private Eye",
                "Robe": "Monster Hide",
                "Shoes": "Private Eye",
                "Weapon": "Rod",
                "Athame": "Abomination",
                "Amulet": "Crimefighter",
                "Ring": "Skyfarer",
                "Deck": "Crimefighter",
                "Mount": "Clockwork Courser"
                }

    wizardsGear['Balance'] = {
                "Hat": "Private Eye",
                "Robe": "Monster Hide",
                "Shoes": "Private Eye",
                "Weapon": "Abomination",
                "Athame": "Abomination",
                "Amulet": "Archival",
                "Ring": "Skyfarer",
                "Deck": "Daemonic",
                "Mount": "Clockwork Courser"
                }

    wizardsGear['Ice'] = {
                "Hat": "Monster Hide",
                "Robe": "Crimefighter",
                "Shoes": "Private Eye",
                "Weapon": "Abomination",
                "Athame": "Abomination",
                "Amulet": "Archival",
                "Ring": "Skyfarer",
                "Deck": "Daemonic",
                "Mount": "Roc (PERM)"
                }
    
    wizardsGear['Life'] = {
                "Hat": "Private Eye",
                "Robe": "Crimefighter",
                "Shoes": "Monster Hide",
                "Weapon": "Alea",
                "Athame": "Private Eye",
                "Amulet": "Crimefighter",
                "Ring": "Skyfarer",
                "Deck": "Imperial Court",
                "Mount": "Clockwork Courser"
                }
    
    wizardsGear['Death'] = {
                "Hat": "Private Eye",
                "Robe": "Monster Hide",
                "Shoes": "Private Eye",
                "Weapon": "Rod",
                "Athame": "Abomination",
                "Amulet": "Clasp",
                "Ring": "Skyfarer",
                "Deck": "Daemonic",
                "Mount": "Clockwork Courser"
                }

    for school in wizardsGear:
        gearFrame = pd.concat(
        [
            filteredTable[
                (filteredTable["Kind"] == kind) &
                (filteredTable["Display"].str.contains(substring, case=False, na=False, regex=False)) &
                (
                    (filteredTable["School"] == school) |
                    (filteredTable["School"] == 'Universal')
                )
            ]
            for kind, substring in wizardsGear[school].items()
        ],
        ignore_index=True
        )

        gearFrame = (
            gearFrame
                .sort_values("Level", ascending=False)
                .drop_duplicates(subset=["Kind"], keep="first")
                .reset_index(drop=True)
        )

        wizardsGear[school] = gearFrame

    for school in wizardsGear:
        wizards[school] = Wizard(school,level=180,gear=wizardsGear[school],pet=Pet(talents=['Mighty', school+'-Bringer', 'Spell-Proof', 'Armor Breaker', 'Spell-Defying', 'Pain-Giver']))
        jewels = { "Tear": ["Health"],
                    "Circle": [school+" Pierce"],
                   "Square": ["Health"],
                   "Shield": ["Outgoing Healing"]}
        if school == "Life":
            wizards[school].addAllStats(jewels, )
        else:
            wizards[school].addAllStats(jewels, Pet(talents=['Mighty', school+'-Dealer', 'Spell-Proof', 'Armor Breaker', 'Spell-Defying', 'Pain-Giver']))
        if school == "Fire":
            wizards[school].stats['Fire Damage']+=8
        if school == "Myth":
            wizards[school].stats['Myth Damage']+=11
            wizards[school].stats['Myth Pierce']-=6
        if school == "Life":
            wizards[school].stats['Life Damage']+=10
            wizards[school].stats['Life Pierce']-=6

    calculator = WizMath()
    for school in wizards:
        print(wizards[school].getStats([school+' Damage', school+' Pierce', school+' Crit Rating', 'Resist', 'Block Rating', 'Health']))
    print(calculator.punchout(wizards['Myth'], wizards['Life']))
    quit()

main()