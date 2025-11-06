import pandas as pd

import os

DATAFRAME_ROOT = os.path.join('src', 'data', 'dataframes')

JEWEL_TYPES = ["Circle", "Star", "Tear", "Square", "Shield", "Sword", "Power"]

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
        masterystring = f"All schools except {self.school}"
        self.gearTable = self.gearTable[~(self.gearTable["School"] == masterystring)]

        self.jewelTable = self.gearTable[
                                        (self.gearTable['Kind'] == "Jewel") &
                                        (self.gearTable['Level'] <= self.level) &
                                        (
                                            (self.gearTable['School'] == self.school) |
                                            (self.gearTable['School'] == "Universal") |
                                            (
                                                self.gearTable['School'].str.contains("All schools except", na=False) &
                                                ~self.gearTable['School'].str.contains(f"All schools except {self.school}", na=False)
                                            )
                                        ) &
                                        (
                                            (self.gearTable['Weave'] == self.weave) |
                                            (self.gearTable['Weave'] == "Universal")
                                        )
                                    ]

    def optimalJewel(self, stat: str, type: str):
        specifiedJewelTable = self.jewelTable[(self.gearTable[stat] > 0) &
                                           (self.gearTable["Jewel Type"] == type)]
        print(specifiedJewelTable)
    


def main():
    woop = JewelLogic("Storm", 180, "Fire")
    woop.optimalJewel("Outgoing Healing", "Shield")

main()