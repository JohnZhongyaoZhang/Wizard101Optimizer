import pandas as pd

from src.data.dataConstruction.gear import Gear
from src.data.dataConstruction.mobs import Mobs
from src.data.dataConstruction.pets import Pets
from src.math.petCreator import Pet

from src.math.wizard import Wizard
from src.math.wizmath import WizMath

import os

DATAFRAME_ROOT = os.path.join('src', 'data', 'dataframes')

if os.path.exists(os.path.join(DATAFRAME_ROOT, 'allthegear.pkl')):
    GEAR_TABLE = pd.read_pickle(os.path.join(DATAFRAME_ROOT, 'allthegear.pkl'))
else:
    print("Gear table not found, use optimizer.py to generate gear table")
    quit()


wizardLevel = 180
wizardSchool = "Storm"
wizardWeave = "Fire"    

def gearStatsAutofill(gearDisplayNames: dict | None = pd.DataFrame(),
                            jewelDisplayNames: list | None = []):
    gearFrame = pd.concat(
    [
        GEAR_TABLE[
            (GEAR_TABLE["Kind"] == kind) &
            (GEAR_TABLE["Display"].str.contains(substring, case=False, na=False, regex=False)) &
            (
                (GEAR_TABLE["School"] == wizardSchool) |
                (GEAR_TABLE["School"] == 'Universal')
            ) &
            (GEAR_TABLE["Level"] <= wizardLevel)
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
    
    jewelFrame = pd.DataFrame()
    for jewel in jewelDisplayNames:
        bestMatch = GEAR_TABLE[
                (GEAR_TABLE["Kind"] == "Jewel") &
                (GEAR_TABLE["Jewel Type"] == jewel["Type"]) &
                (GEAR_TABLE["Display"].str.contains(jewel["Name"], case=False, na=False, regex=False)) &
                (
                    (GEAR_TABLE["School"] == wizardSchool) |
                    (GEAR_TABLE["School"] == 'Universal')
                ) &
                (GEAR_TABLE["Level"] <= wizardLevel)
            ].sort_values("Level", ascending=False)
        if len(bestMatch) > 0:
            bestMatchRow = bestMatch.iloc[0:1]
            jewelFrame = pd.concat([jewelFrame] + [bestMatchRow] * jewel["Quantity"], ignore_index=True)
    return pd.concat([gearFrame, jewelFrame],ignore_index=True)

if __name__ == "__main__":
    gearNames = {
            "Hat": "Crimefighter",
            "Robe": "Monster Hide",
            "Shoes": "Abomination",
            "Weapon": "Rod",
            "Athame": "Abomination",
            "Amulet": "Crimefighter",
            "Ring": "Abomination",
            "Deck": "Crimefighter",
            "Mount": "Clockwork Courser",
            }
    
    jewelNames = (
        {"Name": "Lightning Piercing", "Type": "Circle", "Quantity": 4},
        {"Name": "Flawless Health Opal +155", "Type": "Tear", "Quantity": 3},
        {"Name": "Bright Health Amethyst", "Type": "Square", "Quantity": 3},
        {"Name": "Fire Punishing", "Type": "Sword", "Quantity": 5},
        {"Name": "Fire Accurate", "Type": "Power", "Quantity": 4},
        {"Name": "Storm Mending", "Type": "Shield", "Quantity": 1}
    )

    pet = Pet(name="FrostBeetleRain",
            talents=['Mighty', wizardSchool+'-Dealer', 'Spell-Proof', 'Armor Breaker', 'Spell-Defying', 'Pain-Giver'])
    

    gear = gearStatsAutofill(gearDisplayNames=gearNames, jewelDisplayNames=jewelNames)
    print(gear)
    wizard = Wizard(school=wizardSchool, level=wizardLevel, weave=wizardWeave, gear=gear, pet=pet)
    print(wizard.getStats(['Storm Damage', 'Storm Pierce', 'Storm Crit Rating', 'Resist', 'Block Rating', 'Health']))