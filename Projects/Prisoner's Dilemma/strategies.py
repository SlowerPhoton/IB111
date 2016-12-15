# 0 means refuse the money (10 €)
# 1 means accept the money (10 €)

# 0 0 both get 5 €
# 0 1 the second one gets all 10 €
# 1 0 the first one gets all 10 €
# 1 1 both get 1 €

import random   # to use randint

# The answer is random
# 1/2 chance of refusing, 1/2 of accepting
class RandomChoice:
    def answer(self, lastOpponentAnswer):
        return random.randint(0,1)

# Attempts to cooperate with the second player
# As long as the second player also refuses, refuse
# If the 2nd player betrays, refuse random amount of turns
# Then attempt to cooperate again
class Cooperative:
    #__betray = False
    #__attemptToCooperate = False

    def __init__(self):
        self.__betray = False
        self.__attemptToCooperate = False

    def answer(self, lastOpponentAnswer):
        if lastOpponentAnswer == -1:
            return 0
        if self.__attemptToCooperate == True:
            self.__attemptToCooperate = False
            return 0
        if lastOpponentAnswer == 1:
            self.__betray = True
        if self.__betray == True:
            if lastOpponentAnswer == 0: # if opponent refused in the last turn
                if random.randint(0,1) == 1: # 1/2 chance of forgiving
                    self.__betray = False
                    self.__attemptToCooperate = True
                    return 0
                else:
                    return 1
            else:
                if random.randint(0,4) == 4: # 1/5 chance of forgiving
                    self.__betray = False
                    self.__attemptToCooperate = True
                    return 0
                else:
                    return 1

        return 0

# Enables a human to play via keyboard input
class RealPlayer:
    def answer(self, lastOpponentAnswer):
        print ("Opponent's last answer: ", lastOpponentAnswer)
        while True:
            ans = int(input("Your answer: "))
            if ans == 0 or ans == 1:
                return ans;

# Always accepts the money
class AlwaysAccept:
    def answer(self, lastOpponentAnswer):
        return 1

# Always refuses the money
class AlwaysRefuse:
    def answer(self, lastOpponentAnswer):
        return 0
    
# Repeat opponent's last choice
# First turn is random
class TitForTat:
    def answer(self, lastOpponentAnswer):
        if lastOpponentAnswer == -1:
            return random.randint(0,1)
        return lastOpponentAnswer

class Adaptive:
    #testTitForTatCounter = 0
    #currentTurn = 0
    #myStrategy = [0, 0, 1, 1, 1]
    #opponentStrategy = []

    def __init__(self):
        self.testTitForTatCounter = 0
        self.currentTurn = 0
        self.myStrategy = [0, 0, 1, 1, 1]
        self.opponentStrategy = []   
    
    def answer(self, lastOpponentAnswer):
        if self.currentTurn > 0:
            self.opponentStrategy.append(lastOpponentAnswer)
        if self.currentTurn == 5:
            self.analyseData()
        if self.currentTurn >= 5:
            self.chooseNextMove()
        ans = self.myStrategy[self.currentTurn]
        self.currentTurn+=1
        #if self.currentTurn == 10:
            #print(self.testTitForTatCounter, end = '\n')
        
        return ans

    def analyseData(self):
        # always refuse
        if self.opponentStrategy.count(0) == self.opponentStrategy.__len__():
            self.alwaysRefuse = True
            return

        # always accept
        if self.opponentStrategy.count(1) == self.opponentStrategy.__len__():
            self.alwaysAccept = True
            return

        # tit for tat
        titForTatMatches = 0
        for i in range(1, 5):
            if self.myStrategy[i-1] == self.opponentStrategy[i]:
                titForTatMatches += 1
        if titForTatMatches == 4: # it probably is tit for tat
            self.titForTat = True
            return
        #print("tit for tat matches" + str(titForTatMatches), end='\n')

        if self.opponentStrategy[0] == 0 and self.opponentStrategy[1] == 0: # probably wants to cooperate
            if self.opponentStrategy[2] == 1: # it punishes me for not cooperating
                for i in range(2, self.opponentStrategy.__len__()):
                    if self.opponentStrategy[i] == 0: # it gives me another chance
                        self.forgiveLength = i - 2;
                        if i == 3:
                            if self.opponentStrategy[4] == 0: # it gives me at least 2 chances
                                self.pavlovSuperForgiving = True
                                return
                            else: # it gave me one chance
                                self.pavlovForgiving = True
                                return
                        else: # it punished me too late
                            self.unknown = True
                            return

        # if it is not anything anything from above
        self.unknown = True

    # always cooperate
    def __titForTat(self):
        # check if the strategy is still the same
        if self.myStrategy[self.currentTurn-2] != self.opponentStrategy[self.currentTurn-1]:
            del self.titForTat
            self.unknown = True
            self.__unknown()
            return False

        self.testTitForTatCounter+=1
        self.myStrategy.append(0)
        return True

    # always defect
    def __alwaysRefuse(self):
        if self.opponentStrategy[-1] != 0:
            del self.alwaysRefuse
            self.unknown = True
            self.__unknown()
            return False

        self.myStrategy.append(1)
        return True

    # always defect
    def __alwaysAccept(self):
        if self.opponentStrategy[-1] != 1:
            del self.alwaysAccept
            self.unknown = True
            self.__unknown()
            return False

        self.myStrategy.append(1)
        return True

    # use tit for tat
    def __unknown(self):
        # check if it isn't aproximating a truly random algorithm
        if self.currentTurn > 10:
            randomnessRatio = self.opponentStrategy.count(1) / self.opponentStrategy.__len__()
            if randomnessRatio >= 0.4 and randomnessRatio <= 0.6:
                del self.unknown
                self.random = True
                self.__random()
                return False
            
        self.myStrategy.append(self.opponentStrategy[-1])
        return True

    # always defect
    def __random(self):
        # check if it still seems to be random
        randomnessRatio = self.opponentStrategy.count(1) / self.opponentStrategy.__len__()
        if not (randomnessRatio >= 0.4 and randomnessRatio <= 0.6):
            del self.random
            self.unknown = True
            self.__unknown()
            return False

        self.myStrategy.append(1)
        return True

    # attempt to cooperate
    def __pavlovForgiving(self):
        if self.opponentStrategy[-1] == 1: #I must have betrayed or it's a different algorithm
            # check if it is a different algorithm
            if self.myStrategy[self.currentTurn-2] == 0 and self.opponentStrategy[self.currentTurn-2] == 0 and self.myStrategy[self.currentTurn-1] == 0:
                # it defects me when I don't
                self.unknown = True;

            opponentLastCooperationIndex = 0
            myLastCooperationIndex = 0
            for i in range(self.opponentStrategy.__len__()-1, -1, -1): # find the last turn opponent tried to cooperate
                if self.opponentStrategy[i] == 0:
                    opponentLastCooperationIndex = i
                    break
            for i in range(self.myStrategy[self.currentTurn-1], -1, -1): # find the last turn I tried to cooperate
                if self.myStrategy[i] == 0:
                    myLastCooperationIndex = i
                    break
            # if the last time I tried to cooperate was the last turn find how long is the row
            if myLastCooperationIndex == self.currentTurn-1:
                row = 0
                for i in range(self.myStrategy[self.currentTurn-1], opponentLastCooperationIndex, -1):
                    if self.myStrategy[i] == 0:
                        row += 1
                    else:
                        break
                if row > 5: # if it hasn't forgiven me in 5 turns, give up, it isn't forgiving
                    del self.pavlovForgiving
                    self.pavlovUnforgiving = True
                    self.__pavlovUnforgiving()
                    return False
                else: # try to make it forgive and cooperate
                    self.myStrategy.append(0)
                    return True
        else: # it cooperates
            if hasattr(self, 'pavlovSuperForgiving'):
                del self.pavlovForgiving
                self.__pavlovSuperForgiving()
                return False

            self.myStrategy.append(0) # also cooperate
            return True

    def __pavlovUnforgiving(self):
        # anyway check if it has forgiven
        if self.opponentStrategy[-1] == 0:
            del self.pavlovUnforgiving
            self.pavlovForgiving = True
            self.__pavlovForgiving(self)
            return False

        # otherwise always defect
        self.myStrategy.append(1)
        return True

    def __pavlovSuperForgiving(self):
        if hasattr(self, 'forgiveCount') == False and self.opponentStrategy[-1] == 0:
            self.myStrategy.append(1)
            return True
        if hasattr(self, 'forgiveCount') == True and self.opponentStrategy[-1] == 0:
            del self.pavlovSuperForgiving
            self.pavlovForgiving = True
            return False
        if hasattr(self, 'forgiveCount') == False:
            # count how many times it has forgiven me
            self.forgiveCount = 0
            for i in range(self.currentTurn-2, -1, -1):
                if self.myStrategy[i] == 1 and self.opponentStrategy[i+1] == 0:
                        self.forgiveCount += 1
                else:
                    break
            # try to make it cooperate again
            self.pavlovForgiving = True
            self.__pavlovForgiving()
            return False
        else:
            if self.forgiveCount > 0:
                self.myStrategy.append(1)
                self.forgiveCount -= 1
            else:
                self.myStrategy.append(0)
            return True

    def chooseNextMove(self):
        if hasattr(self, 'titForTat'):
            self.__titForTat()
        elif hasattr(self, 'alwaysRefuse'):
            self.__alwaysRefuse()
        elif hasattr(self, 'alwaysAccept'):
            self.__alwaysAccept()
        elif hasattr(self, 'unknown'):
            self.__unknown()
        elif hasattr(self, 'random'):
            self.__random()
        elif hasattr(self, 'pavlovForgiving'):
            self.__pavlovForgiving()
        elif hasattr(self, 'pavlovUnforgiving'):
            self.__pavlovUnforgiving()
        elif hasattr(self, 'pavlovSuperForgiving'):
            self.__pavlovSuperForgiving()
        else:
            print ("error: no pattern chosen", end="\n") # should not happen




### HERE END THE STRATEGIES ###
