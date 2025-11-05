from src.math.statCaps import wizardStats
import pandas as pd

class Wizard:
    def __init__(self, school: str, level: int, gear: pd.DataFrame, jewels: pd.DataFrame):
        self.wizardStats = wizardStats()
        self.school = school
        self.level = level
        self.gear = gear
        self.jewels = jewels
        self.pet = None
        self.stats = {}

    def statSummation(self):
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