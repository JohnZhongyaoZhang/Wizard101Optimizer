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

if __name__ == "__main__":
    TheOptimizer = Optimizer()

    wizardLevel = 180
    wizardSchool = "Storm"
    wizardWeave = "Fire"    

    gear = {
            "Hat": "Crimefighter",
            "Robe": "Monster Hide",
            "Shoes": "Abomination",
            "Weapon": "Rod",
            "Athame": "Abomination",
            "Amulet": "Crimefighter",
            "Ring": "Abomination",
            "Deck": "Crimefighter",
            "Mount": "Clockwork Courser"
            "Jewel": "Polished"
            }
