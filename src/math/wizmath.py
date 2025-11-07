import numpy as np
from src.math.wizard import Wizard

schools = ['Fire', 'Ice', 'Storm', 'Myth', 'Life', 'Death', 'Balance']
schoolDPPs = dict(zip(schools, [100,83,125,90,83,85,85]))

class WizMath:
    def __init__(self, mode='Premiere League'):
        self.setMode(mode)

    def setMode(self, mode):
        self.mode = mode
        match self.mode:
            case "PvE":
                self.dk0, self.dn0, self.dL = 237, 0, 247
                self.rk0, self.rn0, self.rL = 120, -20, 125
                self.thresholdFactor = 1.5
                self.ratingFactor = 0
                self.crit = "PvE"
                self.incoming = True
            case "Premiere League":
                self.dk0, self.dn0, self.dL = 207, 0, 212
                self.rk0, self.rn0, self.rL = 94, 0, 99
                self.thresholdFactor = 5
                self.ratingFactor = .75
                self.crit = "PvP"
                self.incoming = False
            case "Raid":
                self.dk0, self.dn0, self.dL = 120, 20, 250
                self.rk0, self.rn0, self.rL = 65, -20, 70
                self.thresholdFactor = 5
                self.ratingFactor = .75
                self.crit = "PvP"
                self.incoming = True
            case "Legacy":
                self.dk0, self.dn0, self.dL = 190, -40, 200
                self.rk0, self.rn0, self.rL = 120, -20, 125
                self.crit = "PvE"
                self.incoming = True
            case "Exalted League":
                self.dk0, self.dn0, self.dL = 123, 0, 128
                self.rk0, self.rn0, self.rL = 51, 0, 56
                self.crit = "PvP"
                self.incoming = False
            case "Legendary League":
                self.dk0, self.dn0, self.dL = 87, 0, 92
                self.rk0, self.rn0, self.rL = 27, 0, 32
                self.crit = "None"
                self.incoming = False
            case "Grandmaster League":
                self.dk0, self.dn0, self.dL = 82, 0, 87
                self.rk0, self.rn0, self.rL = 22, 0, 27
                self.crit = "None"
                self.incoming = False
            case _:
                print("Unknown mode")
                quit()

            
    def damageMultiplier(self, damageRating):
        if damageRating > self.dk0 + self.dn0:
            k = np.log(self.dL/(self.dL - self.dk0))/self.dk0
            n = np.log(1-(self.dk0+self.dn0)/self.dL) + k * (self.dk0+self.dn0)
            percentage = self.dL - (self.dL/np.e**(k * damageRating - n))
            return (percentage + 100)/100.0
        else:
            return (damageRating + 100)/100.0
    
    def resistMultiplier(self, resistRating):
        if resistRating > self.rk0 + self.rn0:
            k = np.log(self.rL/(self.rL - self.rk0))/self.rk0
            n = np.log(1-(self.rk0+self.rn0)/self.rL) + k * (self.rk0+self.rn0)
            percentage = self.rL - (self.rL/np.e**(k * resistRating - n))
            return max((100-percentage)/100.0,0.0)
        else:
            return max((100-resistRating)/100.0,0.0)
        
    def resistAfterPierceMultiplier(self, resistRating, pierceRating):
        resistAfterPierce = max(resistRating-pierceRating,0)
        if resistAfterPierce > self.rk0 + self.rn0:
            k = np.log(self.rL/(self.rL - self.rk0))/self.rk0
            n = np.log(1-(self.rk0+self.rn0)/self.rL) + k * (self.rk0+self.rn0)
            percentage = self.rL - (self.rL/np.e**(k * resistAfterPierce - n))
            return max((100-percentage)/100.0,0.0)
        else:
            return max((100-resistAfterPierce)/100.0,0.0)

    def critdamage(self,criticalRating,blockRating):
        if criticalRating == 0 and blockRating == 0:
            return 1
        match self.crit:
            case "PvE":
                return 2 - (3*blockRating)/(criticalRating+3*blockRating)
            case "PvP":
                 return 2 - (5*blockRating)/(criticalRating+5*blockRating)
            case "None":
                 return 1
    
    def critchance(self,criticalRating,blockRating,casterlevel=170):
        if criticalRating == 0 and blockRating == 0:
            return 0
        match self.crit:
            case "PvE":
                return min(min(casterlevel/100,1) * (3*criticalRating)/(3*criticalRating+blockRating),.95)
            case "PvP":
                return min(min(casterlevel/185,1) * (12*criticalRating)/(12*criticalRating+blockRating),.95)
            case "None":
                return 0
    
    def blockchance(self,criticalRating,blockRating,receiverlevel=170):
        if criticalRating == 0 and blockRating == 0:
            return 0
        match self.crit:
            case "PvE":
                receiverlevel = 40
                return (1-(min(receiverlevel/100,1) * (3*criticalRating)/(3*criticalRating+blockRating)))
            case "PvP":
                return min(receiverlevel/185,1) * blockRating/(blockRating + 12*criticalRating)
            case "None":
                return 0
    
    def effectivecrit(self,criticalRating,blockRating,casterlevel=170,receiverlevel=170):
        if self.crit == "None":
            return 1
        effectivecritchance = self.critchance(criticalRating,blockRating,casterlevel) * (1-self.blockchance(criticalRating,blockRating,receiverlevel))
        return 1 + effectivecritchance * (self.critdamage(criticalRating,blockRating)-1)
    
    def effectiveMultipllier(self,criticalRating,blockRating, damageRating, resistRating, pierceRating, casterlevel=170,receiverlevel=170):
        return self.effectivecrit(criticalRating,blockRating,casterlevel,receiverlevel) * self.damageMultiplier(damageRating) * self.resistAfterPierceMultiplier(resistRating,pierceRating)

    def shadDistribution(self, generatingRating, defendingRating):
        if self.mode not in ['Premiere League', 'Raid', 'PvE']:
             raise ValueError("No shad in current mode.")  

    def punchout(self, wizard1: Wizard, wizard2: Wizard, utility=False):
        wizard1value = (wizard1.stats["Health"] *
                        (wizard1.stats[wizard1.school + " Damage"]/100.0 + 1) *
                        self.effectivecrit(wizard1.stats[wizard1.school + " Crit Rating"], wizard2.stats[wizard1.school + " Block Rating"]) *
                        (1 - max(0, wizard2.stats[wizard1.school + " Resist"]/100.0 - wizard1.stats[wizard1.school + " Pierce"]/100.0)) *
                        schoolDPPs[wizard1.school])
        wizard2value = (wizard2.stats["Health"] *
                        (wizard2.stats[wizard2.school + " Damage"]/100.0 + 1) *
                        self.effectivecrit(wizard2.stats[wizard2.school + " Crit Rating"], wizard1.stats[wizard2.school + " Block Rating"]) *
                        (1 - max(0, wizard1.stats[wizard2.school + " Resist"]/100.0 - wizard2.stats[wizard2.school + " Pierce"]/100.0)) *
                        schoolDPPs[wizard2.school])
        return wizard1value/wizard2value
    
def main():
    testing = WizMath(mode='P')
#main()