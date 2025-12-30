import os
import pandas as pd

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
PROJECT_ROOT = os.path.dirname(os.path.dirname(SCRIPT_DIR))
DATAFRAME_ROOT = os.path.join(PROJECT_ROOT, 'src', 'data', 'dataframes')
UNIVERSAL_STATS = ['Damage','Accuracy','Pierce','Resist','Crit Rating','Block Rating', 'Pip Conversion Rating']
SCHOOLS = ['Fire', 'Ice', 'Storm', 'Balance', 'Life', 'Myth', 'Death']

if os.path.exists(os.path.join(DATAFRAME_ROOT, 'selfishtalents.pkl')):
    SELFISH_TALENTS = pd.read_pickle(os.path.join(DATAFRAME_ROOT, 'selfishtalents.pkl'))
else:
    print("Selfish talent table not found.")
    quit()

if os.path.exists(os.path.join(DATAFRAME_ROOT, 'allthepets.pkl')):
    PETS_TABLE = pd.read_pickle(os.path.join(DATAFRAME_ROOT, 'allthepets.pkl'))
else:
    print("Pet table not found.")
    quit()

if os.path.exists(os.path.join(DATAFRAME_ROOT, 'combattalents.pkl')):
    COMBAT_TALENTS = pd.read_pickle(os.path.join(DATAFRAME_ROOT, 'combattalents.pkl'))
else:
    print("Combat talent table not found.")
    quit()

class Pet:
    def __init__(self, name="Generic", body="Generic", talents=[], strength=255,intellect=250,agility=260,will=260,power=250):
        self.petStats = pd.Series(data={"Strength": strength,
                      "Intellect": intellect,
                      "Agility": agility,
                      "Will": will,
                      "Power": power})
        self.talents = talents
        self.stats = pd.DataFrame(columns=PETS_TABLE.columns)
        self.name = name
        self.body = body
        self.processBody()
        self.processTalents()
        self.stats.reset_index(drop=True, inplace=True)

    def processBody(self):
        if self.body == "Generic":
            row_data = {col: None for col in PETS_TABLE.columns}
            row_data['Name'] = self.body
            row_data['Display'] = self.name
            row_data['Set'] = None
            row_data['Cards'] = None
            row_data['Level'] = 0
            row_data['School'] = "Universal"
            self.stats = pd.DataFrame([row_data])
            return
        self.stats = PETS_TABLE[PETS_TABLE["Name"] == self.body].copy()
        

    def processTalents(self):
        selfishTalents = SELFISH_TALENTS[SELFISH_TALENTS["Name"].isin(self.talents)].copy()
        combatTalents = COMBAT_TALENTS[COMBAT_TALENTS["Name"].isin(self.talents)].copy()

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

        preUniversalStats = combatTalents.groupby("Stat")["Value"].sum()
        universalStats = preUniversalStats[preUniversalStats.index.isin(UNIVERSAL_STATS)]
        schoolAndStatCombinations = pd.MultiIndex.from_product([SCHOOLS, universalStats.index],
                                        names=["School", "Stat"])
        universalExpanded = pd.Series(universalStats.reindex(schoolAndStatCombinations.get_level_values("Stat")).values, index=schoolAndStatCombinations)
        universalExpanded.index = universalExpanded.index.map(" ".join)
        
        allStats = preUniversalStats.add(universalExpanded, fill_value=0)
        self.stats[allStats.index] = allStats.to_numpy()
        #for col in allStats.index:
        #    self.stats[col] = allStats[col]

if __name__ == "__main__":
    tester = Pet(body="PP_FrilledDino_A",talents=['Mighty', 'Fire-Dealer', 'Spell-Proof', 'Fire-Giver', 'Spell-Defying', 'Pain-Giver'])
    print(tester.stats)