from src.math.statCaps import wizardStats

import pandas as pd
import os

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
PROJECT_ROOT = os.path.dirname(os.path.dirname(SCRIPT_DIR))
DATAFRAME_ROOT = os.path.join(PROJECT_ROOT, 'src', 'data', 'dataframes')
JEWEL_TYPES = ["Circle", "Star", "Tear", "Square", "Shield", "Sword", "Power"]
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
                        items: pd.DataFrame | None = pd.DataFrame(),
                        ):
        self.school = school
        self.weave = weave
        self.level = level
        self.items = items
        self.setBonusTable = SETS_TABLE
        self.stats = pd.Series()
        self.addAllStats()


    def wizardSummary(self, statFilter=None):
        statsDisplay = self.stats.drop("Level")
        statsDisplay = statsDisplay[statsDisplay != 0]
        if statFilter:
            statsDisplay = statsDisplay.reindex(statFilter).dropna()
        return {
            "School": self.school,
            "Weave": self.weave,
            "Level": self.level,
            "Items": self.items,
            "Stats": statsDisplay
        }

    def addAllStats(self):
        self.addBaseStats()
        self.additemstats()
        self.addSetBonusStats()

    def addBaseStats(self):
        baseStats = WIZARD_STATS.getBaseStats(school=self.school,level=self.level).select_dtypes(include="number").squeeze()
        self.stats = self.stats.add(baseStats, fill_value=0)

    def additemstats(self):
        itemStats = self.items.select_dtypes(include="number").sum().squeeze()
        self.stats = self.stats.add(itemStats, fill_value=0)

    def addSetBonusStats(self):
        gear_sets = self.items[self.items['Set'] != 'None']['Set']
        set_counts_series = gear_sets.value_counts()
        
        if (set_counts_series >= 2).any():
            setBonusStats = self.setBonusTable[self.setBonusTable['Set'].isin(set_counts_series.index)]
            set_counts = setBonusStats['Set'].map(set_counts_series)
            eligibleSetBonusStats = setBonusStats[setBonusStats['Pieces'] <= set_counts]
            setBonusStatsSum = eligibleSetBonusStats.select_dtypes(include="number").sum().squeeze()
            self.stats = self.stats.add(setBonusStatsSum, fill_value=0)