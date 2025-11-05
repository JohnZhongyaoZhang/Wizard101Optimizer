import random
import math
from collections import Counter
import json

ITERATIONS = 1000
RATINGLOWERBOUND = 45
RATINGUPPERBOUND = 183

class shadMath:
    def createDistribution(self, generatingRating, defendingRating, thresholdFactor, ratingFactor):
        threshold = defendingRating * thresholdFactor
        minimumGeneration = generatingRating * ratingFactor
        maximumGeneration = generatingRating

        trialOutcomes = []

        # Simulate ingame generation
        for i in range(ITERATIONS):
            accumulatedShad = 0
            rounds = 0
            while (accumulatedShad < threshold):
                accumulatedShad+=random.uniform(minimumGeneration, maximumGeneration)
                rounds+=1
            trialOutcomes.append(rounds)
        
        distribution = sorted(dict(Counter(trialOutcomes)).items())

        # Normalization
        normalizedDistribution = {}
        for round in distribution:
            normalizedDistribution[round[0]] = round[1]/ITERATIONS

        normalizedDistribution['Average'] = sum(trialOutcomes) / len(trialOutcomes)

        return normalizedDistribution

    def getRatingPairs(self):
        ratios = []
        ratingPairs = []
        for i in range(RATINGLOWERBOUND, RATINGUPPERBOUND+1):
            for j in range(RATINGLOWERBOUND, RATINGUPPERBOUND+1):
                gcd = math.gcd(i, j)
                if gcd != 1:
                    reduced = (i/gcd, j/gcd)
                    if reduced not in ratios:
                        ratingPairs.append((i, j))
                        ratios.append(reduced)
                else:
                    ratingPairs.append((i, j))
        
        return ratingPairs
    
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
    test.createFile(1.5,0,"PvE")

#main()