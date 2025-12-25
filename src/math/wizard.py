from src.math.statCaps import wizardStats
from src.math.petCreator import Pet

from collections import Counter

import pandas as pd
import os

DATAFRAME_ROOT = os.path.join('src', 'data', 'dataframes')
JEWEL_TYPES = ["Circle", "Star", "Tear", "Square", "Shield", "Sword", "Power"]

if os.path.exists(os.path.join(DATAFRAME_ROOT, 'allthegear.pkl')):
    GEAR_TABLE = pd.read_pickle(os.path.join(DATAFRAME_ROOT, 'allthegear.pkl'))
else:
    print("Gear table not found, use optimizer.py to generate gear table")
    quit()

if os.path.exists(os.path.join(DATAFRAME_ROOT, 'allthesets.pkl')):
    SETS_TABLE = pd.read_pickle(os.path.join(DATAFRAME_ROOT, 'allthesets.pkl'))
else:
    print("Set table not found, use optimizer.py to generate gear table")
    quit()

WIZARD_STATS = wizardStats()

class Wizard:
    def __init__(self, school: str, level: int, weave: str | None = "Universal"):
        self.school = school
        self.weave = weave
        self.level = level
        self.gear = None
        self.jewels = None
        self.pet = None
        self.itemCards = []
        self.gearTable = GEAR_TABLE
        self.setBonusTable = SETS_TABLE
        self.stats = pd.Series()

    def addAllStats(self, statPerJewelType: dict, pet: Pet):
        self.addBaseStats()
        self.addGearStats()
        self.addJewelStats(statPerJewelType)
        self.addPetStats(pet)
        self.addSetBonusStats()

    def getStats(self, statFilter=None):
        self.stats = self.stats.drop("Level")
        self.stats = self.stats[self.stats != 0]
        if statFilter:
            return self.stats[statFilter]
        else:
            return self.stats

    def addBaseStats(self):
        baseStats = WIZARD_STATS.getBaseStats(school=self.school,level=self.level).select_dtypes(include="number").squeeze()
        self.stats = self.stats.add(baseStats, fill_value=0)

    def addGearStats(self, gear: pd.DataFrame):
        self.gear = gear
        gearStats = self.gear.select_dtypes(include="number").sum().squeeze()
        self.stats = self.stats.add(gearStats, fill_value=0)
    
    def addGearStatsAutofill(self, gear: dict):
        gearFrame = pd.concat(
        [
            GEAR_TABLE[
                (GEAR_TABLE["Kind"] == kind) &
                (GEAR_TABLE["Display"].str.contains(substring, case=False, na=False, regex=False)) &
                (
                    (GEAR_TABLE["School"] == self.school) |
                    (GEAR_TABLE["School"] == 'Universal')
                )
            ]
            for kind, substring in gear.items()
        ],
        ignore_index=True
        )

        gearFrame = (
            gearFrame
                .sort_values("Level", ascending=False)
                .drop_duplicates(subset=["Kind"], keep="first")
                .reset_index(drop=True)
        )
        
        self.addGearStats(gearFrame)
    
    def addJewelStats(self, jewels: pd.DataFrame):
        self.jewels = jewels
        jewelStats = self.jewels.select_dtypes(include="number").sum().squeeze()
        self.stats = self.stats.add(jewelStats, fill_value=0)

    def addJewelStatsAutofill(self, statPerJewelType: dict):
        self.generateJewelTables()
        jewelsAvailable = self.jewelSummation()
        self.jewels = pd.DataFrame(columns=self.gear.index)

        for JewelType in jewelsAvailable:
            if JewelType in statPerJewelType:
                optimalJewel = self.optimalJewel(stats=statPerJewelType[JewelType], type=JewelType)
                slotsOfTypeAvailable = jewelsAvailable[JewelType]
                self.jewels = pd.concat([self.jewels, pd.DataFrame([optimalJewel] * slotsOfTypeAvailable)], ignore_index=True)

        jewelStats = self.jewels.select_dtypes(include="number").sum().squeeze()

        self.stats = self.stats.add(jewelStats, fill_value=0)

    def generateJewelTables(self):
        # Only appropriate level jewels available for the weave combo allowed
        self.gearTable = self.gearTable[~(self.gearTable["School"] == f"All schools except {self.school}")]

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

    def jewelSummation(self):
        totalJewels = list(filter(None, '|'.join(self.gear['Jewels'].astype(str)).split('|')))
        totalJewels = dict(Counter(totalJewels))
        return totalJewels

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
    
    def addPetStats(self, pet: Pet):
        self.pet = pet
        self.stats = self.stats.add(pet.stats, fill_value=0)
    
    def addSetBonusStats(self):
        
        return