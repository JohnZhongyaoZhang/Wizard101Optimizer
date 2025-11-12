import os
import pandas as pd

DATAFRAME_ROOT = os.path.join('src', 'data', 'dataframes')
UNIVERSAL_STATS = ['Damage','Accuracy','Pierce','Resist','Crit Rating','Block Rating', 'Pip Conversion Rating']
SCHOOLS = ['Fire', 'Ice', 'Storm', 'Balance', 'Life', 'Myth', 'Death']

class PetCreator:
    def __init__(self, talents, strength=255,intellect=250,agility=260,will=260,power=250):
        self.petStats = pd.Series(data={"Strength": strength,
                      "Intellect": intellect,
                      "Agility": agility,
                      "Will": will,
                      "Power": power})
        self.talents = talents
        self.stats = pd.Series()
        self.generateTables()
        self.processTalents()
    
    def generateTables(self):
        if os.path.exists(os.path.join(DATAFRAME_ROOT, 'selfishtalents.pkl')):
            self.selfishTalents = pd.read_pickle(os.path.join(DATAFRAME_ROOT, 'selfishtalents.pkl'))
        else:
            print("Selfish talent table not found.")
            quit()

        if os.path.exists(os.path.join(DATAFRAME_ROOT, 'combattalents.pkl')):
            self.combatTalents = pd.read_pickle(os.path.join(DATAFRAME_ROOT, 'combattalents.pkl'))
        else:
            print("Combat talent table not found.")
            quit()
    
    def processTalents(self):
        selfishTalents = self.selfishTalents[self.selfishTalents["Name"].isin(self.talents)].copy()
        combatTalents = self.combatTalents[self.combatTalents["Name"].isin(self.talents)].copy()

        self.petStats = self.petStats.add(
            selfishTalents.select_dtypes(include="number").sum().squeeze(), fill_value=0
        )

        combatTalents["Value"] = (
            combatTalents["General Coefficient"] * (
                combatTalents["Strength Coefficient"] * self.petStats["Strength"] +
                combatTalents["Intellect Coefficient"] * self.petStats["Intellect"] +
                combatTalents["Agility Coefficient"] * self.petStats["Agility"] +
                combatTalents["Will Coefficient"] * self.petStats["Will"] +
                combatTalents["Power Coefficient"] * self.petStats["Power"]
            ) + combatTalents["Constant Value Override"]
        ).round()

        self.stats = combatTalents.groupby("Stat")["Value"].sum()

        universalStats = self.stats[self.stats.index.isin(UNIVERSAL_STATS)]
        schoolAndStatCombinations = pd.MultiIndex.from_product([SCHOOLS, universalStats.index],
                                        names=["School", "Stat"])
        expanded = pd.Series(universalStats.reindex(schoolAndStatCombinations.get_level_values("Stat")).values, index=schoolAndStatCombinations)
        expanded.index = expanded.index.map(" ".join)
        self.stats = self.stats.add(expanded, fill_value=0)

def main():
    tester = PetCreator(talents=['Mighty', 'Fire-Dealer', 'Spell-Proof', 'Fire-Giver', 'Spell-Defying', 'Pain-Giver'])
    print(tester.stats)

main()