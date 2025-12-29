from src.math.statCaps import wizardStats
from src.math.petCreator import Pet

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
    def __init__(self, school: str,
                        level: int,
                        weave: str | None = "Universal",
                        gear: pd.DataFrame | None = pd.DataFrame(),
                        pet: Pet | None = pd.DataFrame()):
        self.school = school
        self.weave = weave
        self.level = level
        self.gear = None
        self.pet = None
        self.gearTable = GEAR_TABLE
        self.setBonusTable = SETS_TABLE
        self.stats = pd.Series()

    def addAllStats(self):
        self.addBaseStats()
        self.addGearStats()
        self.addPetStats()
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

    def addGearStats(self):
        gearStats = self.gear.select_dtypes(include="number").sum().squeeze()
        self.stats = self.stats.add(gearStats, fill_value=0)
    
    def gearStatsAutofill(self, gearDisplayNames: dict | None = pd.DataFrame(),
                                jewelDisplayNames: list | None = []):
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
            for kind, substring in gearDisplayNames.items()
        ],
        ignore_index=True
        )

        gearFrame = (
            gearFrame
                .sort_values("Level", ascending=False)
                .drop_duplicates(subset=["Kind"], keep="first")
                .reset_index(drop=True)
        )
        
        jewelFrame = pd.concat(
        [
            GEAR_TABLE[
                (GEAR_TABLE["Kind"] == "Jewel") &
                (GEAR_TABLE["Display"].str.contains(jewel, case=False, na=False, regex=False)) &
                (
                    (GEAR_TABLE["School"] == self.school) |
                    (GEAR_TABLE["School"] == 'Universal')
                )
            ]
            for jewel in jewelDisplayNames
        ],
        ignore_index=True
        )

        jewelFrame = (
            jewelFrame
                .sort_values("Level", ascending=False)
                .drop_duplicates(subset=["Kind"], keep="first")
                .reset_index(drop=True)
        )

        return pd.concat(gearFrame, jewelFrame)

    def jewelSocketSummation(self):
        jewel_series = self.gear['Jewels'].astype(str).str.split('|').explode()
        jewel_series = jewel_series[jewel_series != 'None']
        jewel_series = jewel_series[jewel_series != '']
        totalJewels = jewel_series.value_counts().to_dict()
        return totalJewels

    def addPetStats(self, pet: Pet):
        self.pet = pet
        self.stats = self.stats.add(pet.stats, fill_value=0)
    
    def addSetBonusStats(self):
        gear_sets = self.gear[self.gear['Set'] != 'None']['Set']
        set_counts_series = gear_sets.value_counts()
        
        if (set_counts_series > 2).any():
            setBonusStats = self.setBonusTable[self.setBonusTable['Set'].isin(set_counts_series.index)]
            
            set_counts = setBonusStats['Set'].map(set_counts_series)
            eligibleSetBonusStats = setBonusStats[setBonusStats['Pieces'] <= set_counts]
            
            setBonusStatsSum = eligibleSetBonusStats.select_dtypes(include="number").sum().squeeze()
            self.stats = self.stats.add(setBonusStatsSum, fill_value=0)