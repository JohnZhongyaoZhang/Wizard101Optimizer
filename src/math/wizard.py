from src.math.statCaps import wizardStats
import pandas as pd
from collections import Counter

class Wizard:
    def __init__(self, school: str, level: int, gear: pd.DataFrame, weave: str | None = "Universal"):
        self.wizardStats = wizardStats()
        self.school = school
        self.weave = weave
        self.level = level
        self.gear = gear
        self.jewels = None
        self.pet = None
        self.stats = None

    def gearStatSummation(self):
        # get base stats
        baseStats = self.wizardStats.getBaseStats(school=self.school,level=self.level).select_dtypes(include="number").squeeze()

        # get gear stats
        gearStats = self.gear.select_dtypes(include="number").sum().squeeze()

        # sum of stats
        totalStats = gearStats.add(baseStats, fill_value=0)
        totalStats = totalStats.drop("Level")
        totalStats = totalStats[totalStats != 0]
        self.stats = totalStats

        return self.stats

    def jewelSummation(self):
        totalJewels = list(filter(None, '|'.join(self.gear['Jewels'].astype(str)).split('|')))
        totalJewels = dict(Counter(totalJewels))
        return totalJewels
    
    def jewelHandler(self):
        
        return
