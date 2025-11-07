from src.math.statCaps import wizardStats

from collections import Counter

import pandas as pd
import os

DATAFRAME_ROOT = os.path.join('src', 'data', 'dataframes')
JEWEL_TYPES = ["Circle", "Star", "Tear", "Square", "Shield", "Sword", "Power"]

class Wizard:
    def __init__(self, school: str, level: int, gear: pd.DataFrame, weave: str | None = "Universal"):
        self.wizardStats = wizardStats()
        self.school = school
        self.weave = weave
        self.level = level
        self.gear = gear
        self.jewels = None
        self.pet = None
        self.stats = pd.Series()

    def addAllStats(self, statPerJewelType: dict):
        self.addBaseStats()
        self.addGearStats()
        self.addJewelStats(statPerJewelType)
        self.addSetBonusStats()

    def getStats(self, statFilter=None):
        self.stats = self.stats.drop("Level")
        self.stats = self.stats[self.stats != 0]
        if statFilter:
            return self.stats[statFilter]
        else:
            return self.stats

    def addBaseStats(self):
        baseStats = self.wizardStats.getBaseStats(school=self.school,level=self.level).select_dtypes(include="number").squeeze()
        self.stats = self.stats.add(baseStats, fill_value=0)

    def addGearStats(self):
        gearStats = self.gear.select_dtypes(include="number").sum().squeeze()
        self.stats = self.stats.add(gearStats, fill_value=0)
    
    def addJewelStats(self, statPerJewelType: dict):
        self.generateTables()
        jewelsAvailable = self.jewelSummation()
        self.jewels = pd.DataFrame(columns=self.gear.index)

        for JewelType in jewelsAvailable:
            if JewelType in statPerJewelType:
                optimalJewel = self.optimalJewel(stats=statPerJewelType[JewelType], type=JewelType)
                slotsOfTypeAvailable = jewelsAvailable[JewelType]
                self.jewels = pd.concat([self.jewels, pd.DataFrame([optimalJewel] * slotsOfTypeAvailable)], ignore_index=True)

        jewelStats = self.jewels.select_dtypes(include="number").sum().squeeze()

        self.stats = self.stats.add(jewelStats, fill_value=0)

    def addSetBonusStats(self):
        return
    
    def jewelSummation(self):
        totalJewels = list(filter(None, '|'.join(self.gear['Jewels'].astype(str)).split('|')))
        totalJewels = dict(Counter(totalJewels))
        return totalJewels
    
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

    def optimalJewel(self, stats: list[str], type: str):
        specifiedJewelTable = self.jewelTable[
            (self.jewelTable["Jewel Type"] == type) &
            (self.jewelTable[stats].gt(0).any(axis=1))
        ]

        if specifiedJewelTable.empty:
            print("No matching jewels found.")
            return None

        table = specifiedJewelTable.copy()
        table = table.sort_values(by=stats, ascending=[False] * len(stats))
        optimal = table.iloc[0]
        return optimal
