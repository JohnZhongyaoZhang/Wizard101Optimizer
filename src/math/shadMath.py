import random
import math
from collections import Counter
import json
import numpy as np

ITERATIONS = 100000
RATINGLOWERBOUND = 45
RATINGUPPERBOUND = 187

class shadMath:
    def createDistribution(self, generatingRating, defendingRating, thresholdFactor, ratingFactor):
        threshold = defendingRating * thresholdFactor
        minimumGeneration = generatingRating * ratingFactor
        maximumGeneration = generatingRating
        maxRounds = int(math.ceil(threshold / minimumGeneration))

        rolls = np.random.uniform(
            minimumGeneration,
            maximumGeneration,
            size=(ITERATIONS, maxRounds)
        )

        cumulativeSum = np.cumsum(rolls, axis=1)
        rounds = np.argmax(cumulativeSum >= threshold, axis=1) + 1

        unique, counts = np.unique(rounds, return_counts=True)
        dist = {int(k): float(v / ITERATIONS) for k, v in zip(unique, counts)}
        dist["Average"] = float(rounds.mean())

        return dist

    def getRatingPairs(self):
        ratios_seen = set()
        pairs = []

        for g in range(RATINGLOWERBOUND, RATINGUPPERBOUND + 1):
            for d in range(RATINGLOWERBOUND, RATINGUPPERBOUND + 1):
                gcd = math.gcd(g, d)
                if gcd != 1:
                    reduced = (g // gcd, d // gcd)
                    if reduced in ratios_seen:
                        continue
                    ratios_seen.add(reduced)
                pairs.append((g, d))

        return pairs
    
    def createFile(self, thresholdFactor, ratingFactor, fileName):
        ratingPairs = self.getRatingPairs()
        fileOutput = {}
        counter = 0
        for pair in ratingPairs:
            if counter % 100 == 0:
                print(str(counter)+"/"+str(len(ratingPairs)))
            # Convert indexing from tuples to strings
            fileOutput[str(pair[0])+","+str(pair[1])] = self.createDistribution(pair[0], pair[1], thresholdFactor, ratingFactor)
            counter+=1

        with open(fileName+".json", "w") as f:
            json.dump(fileOutput, f,indent=4)

def main():
    test = shadMath()
    print(test.createDistribution(159,142,5,.75))
    #test.createFile(1.5,0,"PvE")

main()