from src.math.statCaps import wizardStats
from src.math.JewelLogic import JewelLogic

from collections import Counter

import pandas as pd
import os

DATAFRAME_ROOT = os.path.join('src', 'data', 'dataframes')
JEWEL_TYPES = ["Circle", "Star", "Tear", "Square", "Shield", "Sword", "Power"]

class Wizard:
    def __init__(self, school: str, level: int, gear: pd.DataFrame, jewelPriority: dict, weave: str | None = "Universal"):
        self.wizardStats = wizardStats()
        self.school = school
        self.weave = weave
        self.level = level
        self.gear = gear
        self.jewelPriority = jewelPriority
        self.jewels = None
        self.pet = None
        self.stats = None
        self.allStatSummation()

    def allStatSummation(self, statPerJewelType: dict):
        # Base
        baseStats = self.wizardStats.getBaseStats(school=self.school,level=self.level).select_dtypes(include="number").squeeze()

        # Gear
        gearStats = self.gear.select_dtypes(include="number").sum().squeeze()
        
        # Jewels
        self.generateTables()
        jewelsAvailable = self.jewelSummation()
        self.jewels = pd.DataFrame(columns=self.gear.index)

        for JewelType in jewelsAvailable:
            optimalJewel = self.optimalJewel(stats=statPerJewelType[JewelType], type=JewelType)
            slotsOfTypeAvailable = jewelsAvailable[JewelType]
            self.jewels = pd.concat([self.jewels, pd.DataFrame([optimalJewel] * slotsOfTypeAvailable)], ignore_index=True)

        jewelStats = self.jewels.select_dtypes(include="number").sum().squeeze()

        # Stat Summation
        totalStats = baseStats.add(gearStats, fill_value=0)
        totalStats = totalStats.add(jewelStats, fill_value=0)
        totalStats = totalStats.drop("Level")
        totalStats = totalStats[totalStats != 0]
        self.stats = totalStats

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
