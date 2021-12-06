# Trackmania 2020 
# TMGL 2021 Multiplier Analysis
#
# Justin Schmitz 

# Research question: "What is the probability that the results of a given step in TMGL
#                     accurately match the skill differences between players?" 
# 
# Methods: 
# 
# Represent each track with a "base", "count", and  "risk" value.
# Represent a player with a base mean and variance, and then a "risk" mean and variance. 
# A player who is likely to be more aggressive in shorcuts, but have the same skill, will have a higher variance. 
# For the risk category, the base is the probability that the trick is successful.
# If a trick is successful, minius 1/10th of risk value to time. 
# If a trick is unsuccessful, plus the risk value in time. 


from random import random, choice

def getRandomSet():
    return [random() for x in range(10)]

class Track:
    def __init__(self, base, count, risk):
        self.base = base
        self.count = count
        self.risk = risk
        self.randomValues = getRandomSet()
    
    def __iter__(self):
        return self.randomValues.__iter__()



class Player:
    def __init__(self, base, baseVar, risk, riskVar):
        self.base = base
        self.baseVar = baseVar
        self.risk = risk
        self.riskVar = riskVar
        self.score = 0
        self.trackTime = 0
        self.result = 0

    def addScore(self, score):
        self.score += score

    def getGoodness(self):
        return self.base + random() * self.baseVar + self.risk + random() * 100 * self.riskVar

    def playTrack(self, track: Track):
        trackTime = track.base * self.base
        trackTime += 10 * self.baseVar

        self.randomValuesIterator = track.__iter__()

        for _ in range(track.count):
            playerResult = self.risk + self.randomValuesIterator.__next__() * 75
            if playerResult > 75:
                pass
            else:
                trackTime += 10
        
        self.trackTime = trackTime
    
def main():
    tracks = []
    players = []

    for base in ((100 + x) for x in range(-50, 50, 10)):
        for risk in range(10):
            for count in range(10):
                tracks.append(Track(base, risk, count))
    
    for base in [95, 105]:
        for baseVar in [.25, 1.25]:
            for risk in [60, 90]:
                for riskVar in [.25, 1.25]:
                    players.append(Player(base, baseVar, risk, riskVar))
                
    
    playTracks = [choice(tracks) for _ in range(5)]
    playPlayers = [choice(players) for _ in range(16)]

    playPlayersScore = [x for x in range(30, 22, -1)] + [x for x in range(8, 0, -1)]
    mapMultiplierScore = [5,4,4,3,3,3,2,2,2,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1]
    for track in playTracks[:4]:
        map(lambda x: x.playTrack(track), playPlayers)

        print(playPlayersScore)
        playPlayers = sorted(playPlayers, key=lambda x: x.score)

        for playerScore, player in zip(playPlayersScore, playPlayers):
            player.addScore(playerScore)
        
    map((lambda x: x.playTrack(x) for x in playTracks[-1]), playPlayers)
    playPlayers = sorted(playPlayers, key=lambda x: x.score)

    for mapMultiplier, player in zip(mapMultiplierScore, playPlayers):
            player.score = player.score * mapMultiplier
    
    
    for player in playPlayers:
        player.result = player.score - player.getGoodness()

    results = [player.result for player in playPlayers]

    print(results)

if __name__ == "__main__":
    main()

    
            

        


    
    

