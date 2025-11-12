import pandas as pd
import os

SCHOOLS = ['Fire', 'Ice', 'Storm', 'Balance', 'Life', 'Myth', 'Death']
DATAFRAME_ROOT = os.path.join('src', 'data', 'dataframes')

class Talents:
    def __init__(self):
        self.combatTalentFrame = pd.DataFrame(columns=['Name',
                                            'Stat',
                                            'Constant Value Override',
                                            'General Coefficient',
                                            'Strength Coefficient',
                                            'Intellect Coefficient',
                                            'Agility Coefficient',
                                            'Will Coefficient',
                                            'Power Coefficient'])

        self.selfishTalentFrame = pd.DataFrame(columns=['Name',
                                                        'Strength',
                                                        'Intellect',
                                                        'Agility',
                                                        'Will',
                                                        'Power'])

    def combatTalentCreator(self,name,
                             stat,
                             allschools=True,
                             universal=True,
                             hyphenated=True,
                             constantValueOverride=0,
                             generalCoefficient=0,
                             strengthCoefficient=0,
                             intellectCoefficient=0,
                             agilityCoefficient=0,
                             willCoefficient=0,
                             powerCoefficient=0):
        
        newTalentFrame = pd.DataFrame()
        if allschools:
            prefixes = SCHOOLS.copy()
            schoolsused = SCHOOLS.copy()
        else:
            prefixes = []
            schoolsused = []

        if universal == True:
            schoolsused.append("")
            match stat:
                case "Damage":
                    prefixes.append("Pain")
                case "Resist":
                    prefixes.append("Spell")
                case "Accuracy":
                    prefixes.append("Sharp")
                case "Pip Conversion Rating" | "Power Pip Chance":
                    prefixes.append("Pip")
                case "Pierce":
                    prefixes.append("Armor")
                case "Crit Rating":
                    prefixes.append("Critical")

        if len(prefixes) > 0:
            newTalentFrame['Name'] = [prefix + '-' + name if hyphenated else prefix + ' ' + name for prefix in prefixes]
        else:
            newTalentFrame['Name'] = name
        
        if allschools:
            newTalentFrame['Stat'] = [school + ' ' + stat if school != "" else stat for school in schoolsused]
        else:
            newTalentFrame['Stat'] = stat
        
        newTalentFrame['Constant Value Override'] = constantValueOverride
        newTalentFrame['General Coefficient'] = generalCoefficient
        newTalentFrame['Intellect Coefficient'] = intellectCoefficient
        newTalentFrame['Strength Coefficient'] = strengthCoefficient
        newTalentFrame['Agility Coefficient'] = agilityCoefficient
        newTalentFrame['Will Coefficient'] = willCoefficient
        newTalentFrame['Power Coefficient'] = powerCoefficient

        if self.combatTalentFrame.empty:
            self.combatTalentFrame = newTalentFrame
        else:
            self.combatTalentFrame = pd.concat([self.combatTalentFrame, newTalentFrame])

    def generateTalents(self):
        # Damage Talents
        self.combatTalentCreator(name='Dealer',stat='Damage',universal=False,generalCoefficient=3/400,strengthCoefficient=2,willCoefficient=2,powerCoefficient=1)
        self.combatTalentCreator(name='Giver',stat='Damage',generalCoefficient=2/400,strengthCoefficient=2,willCoefficient=2,powerCoefficient=1)
        self.combatTalentCreator(name='Boon',stat='Damage',generalCoefficient=1/400,strengthCoefficient=2,willCoefficient=2,powerCoefficient=1)
        self.combatTalentFrame = self.combatTalentFrame.replace(to_replace="Life-Dealer", value="Life-Bringer")

        # Resist Talents
        self.combatTalentCreator(name='Ward',stat='Resist',universal=False,generalCoefficient=3/250,strengthCoefficient=2,agilityCoefficient=2,powerCoefficient=1)
        self.combatTalentCreator(name='Proof',stat='Resist',generalCoefficient=2/250,strengthCoefficient=2,agilityCoefficient=2,powerCoefficient=1)
        self.combatTalentCreator(name='Away',stat='Resist',generalCoefficient=1/250,strengthCoefficient=2,agilityCoefficient=2,powerCoefficient=1)
        self.combatTalentFrame = self.combatTalentFrame.replace(to_replace="Spell-Away", value="Spell-Defying")
        self.combatTalentFrame = self.combatTalentFrame.replace(to_replace="Balance-Proof", value="Unbalancer")
        self.combatTalentFrame = self.combatTalentFrame.replace(to_replace="Balance-Away", value="Balance-Off")

        # Accuracy Talents
        self.combatTalentCreator(name='Sniper',stat='Accuracy',universal=False,generalCoefficient=3/400,intellectCoefficient=2,agilityCoefficient=2,powerCoefficient=1)
        self.combatTalentCreator(name='Shot',stat='Accuracy',generalCoefficient=2/400,intellectCoefficient=2,agilityCoefficient=2,powerCoefficient=1)
        self.combatTalentCreator(name='Eye',stat='Accuracy',generalCoefficient=1/400,intellectCoefficient=2,agilityCoefficient=2,powerCoefficient=1)
        self.combatTalentFrame = self.combatTalentFrame.replace(to_replace="Balance-Eye", value="Balance-It")

        # Pierce Talents
        self.combatTalentCreator(name='Breaker',stat='Pierce',allschools=False,hyphenated=False,generalCoefficient=5/2000,strengthCoefficient=2,agilityCoefficient=2,powerCoefficient=1)
        self.combatTalentCreator(name='Piercer',stat='Pierce',allschools=False,hyphenated=False,generalCoefficient=3/2000,strengthCoefficient=2,agilityCoefficient=2,powerCoefficient=1)

        # Crit Talents
        self.combatTalentCreator(name='Assailant',stat='Crit Rating',universal=False,hyphenated=False,generalCoefficient=25/1000,agilityCoefficient=2,willCoefficient=2,powerCoefficient=1)
        self.combatTalentCreator(name='Striker',stat='Crit Rating',allschools=False,hyphenated=False,generalCoefficient=24/1000,agilityCoefficient=2,willCoefficient=2,powerCoefficient=1)
        self.combatTalentCreator(name='Striker',stat='Crit Rating',universal=False,hyphenated=False,generalCoefficient=20/1000,agilityCoefficient=2,willCoefficient=2,powerCoefficient=1)
        self.combatTalentCreator(name='Hitter',stat='Crit Rating',allschools=False,hyphenated=False,generalCoefficient=18/1000,agilityCoefficient=2,willCoefficient=2,powerCoefficient=1)

        # Block Talents
        self.combatTalentCreator(name='Defender',stat='Block Rating',allschools=False,hyphenated=False,generalCoefficient=24/1000,intellectCoefficient=2,willCoefficient=2,powerCoefficient=1)
        self.combatTalentCreator(name='Blocker',stat='Block Rating',allschools=False,hyphenated=False,generalCoefficient=18/1000,intellectCoefficient=2,willCoefficient=2,powerCoefficient=1)

        # Pip Conserve Talents
        self.combatTalentCreator(name='Conserver',stat='Pip Conversion Rating',allschools=False,hyphenated=False,generalCoefficient=24/1000,agilityCoefficient=2,willCoefficient=2,powerCoefficient=1)
        self.combatTalentCreator(name='Saver',stat='Pip Conversion Rating',allschools=False,hyphenated=False,generalCoefficient=18/1000,agilityCoefficient=2,willCoefficient=2,powerCoefficient=1)

        # Power Pip Chance Talents
        self.combatTalentCreator(name='O\'Plenty',stat='Power Pip Chance',allschools=False,hyphenated=False,generalCoefficient=1/250,strengthCoefficient=2,intellectCoefficient=2,powerCoefficient=1)
        self.combatTalentCreator(name='Boost',stat='Power Pip Chance',allschools=False,hyphenated=False,constantValueOverride=5)

        # Top Rarity Selfish Talents
        self.selfishTalentFrame.loc[len(self.selfishTalentFrame)] = {"Name": "Mighty", "Strength": 65} 
        self.selfishTalentFrame.loc[len(self.selfishTalentFrame)] = {"Name": "Brilliant", "Intellect": 65}
        self.selfishTalentFrame.loc[len(self.selfishTalentFrame)] = {"Name": "Relentless", "Agility": 65}
        self.selfishTalentFrame.loc[len(self.selfishTalentFrame)] = {"Name": "Thinkin\' Cap", "Will": 65}
        self.selfishTalentFrame.loc[len(self.selfishTalentFrame)] = {"Name": "Powerful", "Powerful": 65}

        self.selfishTalentFrame = self.selfishTalentFrame.fillna(0)

        self.combatTalentFrame.to_pickle(os.path.join(DATAFRAME_ROOT, 'combattalents.pkl'))
        self.combatTalentFrame.to_csv(os.path.join(DATAFRAME_ROOT, 'combattalents.csv'),index=False)

        self.selfishTalentFrame.to_pickle(os.path.join(DATAFRAME_ROOT, 'selfishtalents.pkl'))
        self.selfishTalentFrame.to_csv(os.path.join(DATAFRAME_ROOT, 'selfishtalents.csv'),index=False)

def main():
    talentGenerator = Talents()
    talentGenerator.generateTalents()

main()