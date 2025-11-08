import pandas as pd

SCHOOLS = ['Fire', 'Ice', 'Storm', 'Balance', 'Life', 'Myth', 'Death']

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

    def genericTalentCreator(self,name,
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
        
        newTalentFrame = pd.DataFrame(columns=self.combatTalentFrame.columns)
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
                case "Pip Conversion Rating", "Power Pip Chance":
                    prefixes.append("Pip")
                case "Pierce":
                    prefixes.append("Armor")
                case "Crit Rating":
                    prefixes.append("Critical")
                case _:
                    prefixes.append("")

        if hyphenated:
            newTalentFrame['Name'] = [prefix + '-' + name for prefix in prefixes]
        else:
            newTalentFrame['Name'] = [prefix + ' ' + name for prefix in prefixes]
        newTalentFrame['Stat'] = [school + ' ' + stat for school in schoolsused]
        newTalentFrame['Constant Value Override'] = constantValueOverride
        newTalentFrame['General Coefficient'] = generalCoefficient
        newTalentFrame['Intellect Coefficient'] = intellectCoefficient
        newTalentFrame['Strength Coefficient'] = strengthCoefficient
        newTalentFrame['Agility Coefficient'] = agilityCoefficient
        newTalentFrame['Will Coefficient'] = willCoefficient
        newTalentFrame['Power Coefficient'] = powerCoefficient

        self.combatTalentFrame = pd.concat([self.combatTalentFrame, newTalentFrame])

    def generateTalents(self):
        # Damage Talents
        self.genericTalentCreator(name='Dealer',stat='Damage',universal=False,generalCoefficient=3/400,strengthCoefficient=2,willCoefficient=2,powerCoefficient=1)
        self.genericTalentCreator(name='Giver',stat='Damage',generalCoefficient=2/400,strengthCoefficient=2,willCoefficient=2,powerCoefficient=1)
        self.genericTalentCreator(name='Boon',stat='Damage',generalCoefficient=1/400,strengthCoefficient=2,willCoefficient=2,powerCoefficient=1)
        self.combatTalentFrame = self.combatTalentFrame.replace(to_replace="Life-Dealer", value="Life-Bringer")

        # Resist Talents
        self.genericTalentCreator(name='Ward',stat='Resist',universal=False,generalCoefficient=3/250,strengthCoefficient=2,agilityCoefficient=2,powerCoefficient=1)
        self.genericTalentCreator(name='Proof',stat='Resist',generalCoefficient=2/250,strengthCoefficient=2,agilityCoefficient=2,powerCoefficient=1)
        self.genericTalentCreator(name='Away',stat='Resist',generalCoefficient=1/250,strengthCoefficient=2,agilityCoefficient=2,powerCoefficient=1)
        self.combatTalentFrame = self.combatTalentFrame.replace(to_replace="Spell-Away", value="Spell-Defying")
        self.combatTalentFrame = self.combatTalentFrame.replace(to_replace="Balance-Proof", value="Unbalancer")
        self.combatTalentFrame = self.combatTalentFrame.replace(to_replace="Balance-Away", value="Balance-Off")

        # Accuracy Talents
        self.genericTalentCreator(name='Sniper',stat='Accuracy',universal=False,generalCoefficient=3/400,intellectCoefficient=2,agilityCoefficient=2,powerCoefficient=1)
        self.genericTalentCreator(name='Shot',stat='Accuracy',generalCoefficient=2/400,intellectCoefficient=2,agilityCoefficient=2,powerCoefficient=1)
        self.genericTalentCreator(name='Eye',stat='Accuracy',generalCoefficient=1/400,intellectCoefficient=2,agilityCoefficient=2,powerCoefficient=1)
        self.combatTalentFrame = self.combatTalentFrame.replace(to_replace="Balance-Eye", value="Balance-It")

        # Pierce Talents
        self.genericTalentCreator(name='Breaker',stat='Pierce',allschools=False,hyphenated=False,generalCoefficient=5/2000,strengthCoefficient=2,agilityCoefficient=2,powerCoefficient=1)
        self.genericTalentCreator(name='Piercer',stat='Pierce',allschools=False,hyphenated=False,generalCoefficient=3/2000,strengthCoefficient=2,agilityCoefficient=2,powerCoefficient=1)

        # Crit Talents
        self.genericTalentCreator(name='Assailant',stat='Crit Rating',universal=False,hyphenated=False,generalCoefficient=25/1000,agilityCoefficient=2,willCoefficient=2,powerCoefficient=1)
        self.genericTalentCreator(name='Striker',stat='Crit Rating',allschools=False,hyphenated=False,generalCoefficient=24/1000,agilityCoefficient=2,willCoefficient=2,powerCoefficient=1)
        self.genericTalentCreator(name='Striker',stat='Crit Rating',universal=False,hyphenated=False,generalCoefficient=20/1000,agilityCoefficient=2,willCoefficient=2,powerCoefficient=1)
        self.genericTalentCreator(name='Hitter',stat='Crit Rating',allschools=False,hyphenated=False,generalCoefficient=18/1000,agilityCoefficient=2,willCoefficient=2,powerCoefficient=1)

        # Block Talents
        self.genericTalentCreator(name='Defender',stat='Block Rating',allschools=False,hyphenated=False,generalCoefficient=24/1000,intellectCoefficient=2,willCoefficient=2,powerCoefficient=1)
        self.genericTalentCreator(name='Blocker',stat='Block Rating',allschools=False,hyphenated=False,generalCoefficient=18/1000,intellectCoefficient=2,willCoefficient=2,powerCoefficient=1)

        # Pip Talents
        self.genericTalentCreator(name='Conserver',stat='Pip Conversion Rating',allschools=False,hyphenated=False,generalCoefficient=24/1000,agilityCoefficient=2,willCoefficient=2,powerCoefficient=1)

def main():
    talentGenerator = Talents()
    talentGenerator.generateTalents()
    print(talentGenerator.combatTalentFrame)

main()