import pandas as pd

from src.math.petCreator import Pet

from src.math.wizard import Wizard
from src.math.wizmath import WizMath

import os

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
PROJECT_ROOT = SCRIPT_DIR
DATAFRAME_ROOT = os.path.join(PROJECT_ROOT, 'src', 'data', 'dataframes')

if os.path.exists(os.path.join(DATAFRAME_ROOT, 'allthegear.pkl')):
    GEAR_TABLE = pd.read_pickle(os.path.join(DATAFRAME_ROOT, 'allthegear.pkl'))
else:
    print("Gear table not found, use optimizer.py to generate gear table")
    quit() 

def gearStatsAutofill(wizardLevel: int, wizardSchool: str, wizardWeave: str, gearDisplayNames: dict | None = pd.DataFrame(),
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

    return gearFrame

def jewelSocketSummation(gear: pd.DataFrame):
    jewel_series = gear['Jewels'].astype(str).str.split('|').explode()
    jewel_series = jewel_series[jewel_series != 'None']
    jewel_series = jewel_series[jewel_series != '']
    totalJewels = jewel_series.value_counts().to_dict()
    return totalJewels

def jewelStatsAutofill(wizardLevel: int, wizardSchool: str, wizardWeave: str, jewelDisplayNames: list | None = []):
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
    return jewelFrame

def combineItemStats(gear: pd.DataFrame, jewel: pd.DataFrame, pet: Pet):
    combinedItems = pd.concat([gear, jewel, pet.stats], ignore_index=True)

    numeric_cols = combinedItems.select_dtypes(include="number").columns
    combinedItems[numeric_cols] = combinedItems[numeric_cols].fillna(0)

    string_cols = combinedItems.select_dtypes(include="object").columns
    combinedItems[string_cols] = combinedItems[string_cols].fillna('None')

    return combinedItems


if __name__ == "__main__":
    wizardLevel = 180
    wizardSchool = "Death"
    wizardWeave = "Fire"

    gearNames = {
            "Hat": "Monster Hide",
            "Robe": "Crimefighter",
            "Shoes": "Private Eye",
            "Weapon": "Malignant Aeon",
            "Athame": "Abomination",
            "Amulet": "Crimefighter",
            "Ring": "Abomination",
            "Deck": "August Sage",
            "Mount": "Stompy Bronto",
            }
    

    gear = gearStatsAutofill(wizardLevel=wizardLevel, wizardSchool=wizardSchool, wizardWeave=wizardWeave, gearDisplayNames=gearNames)
    jewelSlots = jewelSocketSummation(gear)

    jewelNames = (
        {"Name": "Ash Piercing", "Type": "Circle", "Quantity": jewelSlots["Circle"]},
        {"Name": "Flawless Health Opal +155", "Type": "Tear", "Quantity": jewelSlots["Tear"]},
        {"Name": "Bright Health Onyx", "Type": "Square", "Quantity": jewelSlots["Square"]},
        {"Name": "Fire Punishing ", "Type": "Sword", "Quantity": jewelSlots["Sword"]},
        {"Name": "Fire Accurate", "Type": "Power", "Quantity": jewelSlots["Power"]},
        {"Name": "Death Mending", "Type": "Shield", "Quantity": jewelSlots["Shield"]}
    )

    jewels = jewelStatsAutofill(wizardLevel=wizardLevel, wizardSchool=wizardSchool, wizardWeave=wizardWeave, jewelDisplayNames=jewelNames)
    
    pet = Pet(body="PP_FrilledDino_A",
            talents=['Mighty', wizardSchool+'-Dealer', 'Spell-Proof', 'Armor Breaker', 'Spell-Defying', 'Pip O\'Plenty'])
    items = combineItemStats(gear, jewels, pet)
    wizard = Wizard(school=wizardSchool, level=wizardLevel, weave=wizardWeave, items=items)
    print(wizard.wizardSummary([wizardSchool+' Damage', wizardSchool+' Pierce', wizardSchool+' Crit Rating', 'Resist', 'Block Rating', 'Health', 'Shadow Pip Stat Rating']))