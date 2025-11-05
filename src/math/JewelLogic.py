import pandas as pd

import os

DATAFRAME_ROOT = os.path.join('src', 'data', 'dataframes')

class JewelLogic():
    def __init__(self, school: str, level: int, weave: str | None = "Universal"):
        self.school = school
        self.level = level
        self.weave = weave
        self.generateTables()
    
    def generateTables(self):
        if os.path.exists(os.path.join(DATAFRAME_ROOT, 'allthegear.pkl')):
            self.gearTable = pd.read_pickle(os.path.join(DATAFRAME_ROOT, 'allthegear.pkl'))
        else:
            print("Gear table not found, use optimizer.py to generate gear table")

        # Only appropriate level jewels available for the weave combo allowed
        self.jewelTable = self.gearTable[(self.gearTable['Kind'] == "Jewel") &
                                        (self.gearTable['Level'] <= self.level) &
                                        ((self.gearTable['School'] == self.school) | (self.gearTable['School'] == "Universal")) &
                                        ((self.gearTable['Weave'] == self.weave) | (self.gearTable['Weave'] == "Universal"))]

    def optimalCirclePierceJewel(self):
        statString = self.school + " Pierce"
        pierceJewelTable = self.jewelTable[self.gearTable[statString] > 0]
        print(pierceJewelTable)
        return
    


def main():
    woop = JewelLogic("Storm", 180, "Fire")
    woop.optimalCirclePierceJewel()

main()