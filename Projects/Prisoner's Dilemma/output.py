import strategies
import game

import numpy as np
import matplotlib.pyplot as plt


'''
Let play two players given number of games with given number of turns
Print the outcome
And return it in a list, where 0th index is 1st player's score,
1st index is 2nd player's score
'''
def twoPlayers(noOfGames, noOfTurns, strategy1, strategy2):
    output = []
    for i in range(0, noOfGames):
        theGame = game.Game(strategy1, strategy2)
        output = theGame.playWithFeedback(noOfTurns)
        print("Game " + str(i+1) + ":")
        strToPrint1 = str(strategy1.__name__) + "'s money"
        print (strToPrint1, output[0], end = "\n")
        strToPrint2 = str(strategy2.__name__) + "'s money"
        print (strToPrint2, output[1], end = "\n")
        print(end = "\n")
    return output
        
'''
Let play all strategies against each other (one game of 1000 turns)
Save the output in 'prissoners dilemma.txt' as a table for Excel
'''
def allStratsToTXT():
    allStrats = [strategies.RandomChoice, strategies.Cooperative, strategies.AlwaysAccept, strategies.TitForTat, strategies.Adaptive]
    #allStrats = [strategies.Cooperative, strategies.TitForTat, strategies.Adaptive]
    f = open('prisoners dilemma.txt', 'w')

    # label columns
    f.write('Prisoner\'s dilemma\t')
    for s in allStrats:
        f.write(s.__name__)
        f.write('\t')
    f.write('\n')

    for a in range(allStrats.__len__()):
        f.write(allStrats[a].__name__)
        f.write('\t')
        for b in range(allStrats.__len__()):
            theGame = game.Game(allStrats[a], allStrats[b])
            output = theGame.playWithFeedback(1000)
            print(allStrats[a].__name__ + "X" + allStrats[b].__name__ + " " + str(output[0]) + "," + str(output[1]), end='\n')
            f.write(str(output[1]))
            f.write('\t')
        f.write('\n')

'''
Let two given strategies play 5 games of given number of turns
Create and show a graph of their money in each game
'''
def graphFiveGames(strategy1, strategy2, noOfTurns=100):
    N = 5
    outputFirstPlayer = []
    outputSecondPlayer = []
    for i in range(0, N):
        theGame = game.Game(strategy1, strategy2)
        output = theGame.playWithFeedback(noOfTurns)
        outputFirstPlayer.append(output[0])
        outputSecondPlayer.append(output[1])

    ind = np.arange(N)
    width = 0.35

    fig, ax = plt.subplots()
    rects1 = ax.bar(ind, outputFirstPlayer, width, color='r')
    rects2 = ax.bar(ind + width, outputSecondPlayer, width, color='y')

    ax.set_ylabel('Money gained')
    ax.set_title('Scores by strategies')
    ax.set_xticks(ind + width)
    ax.set_xticklabels(('G1', 'G2', 'G3', 'G4', 'G5'))

    ax.legend((rects1[0], rects2[0]), (strategy1.__name__, strategy2.__name__))

    def autolabel(rects):
        # attach some text labels
        for rect in rects:
            height = rect.get_height()
            ax.text(rect.get_x() + rect.get_width()/2., 1.05*height,
                    '%d' % int(height),
                    ha='center', va='bottom')
    autolabel(rects1)
    autolabel(rects2)

    plt.show()
            
    
