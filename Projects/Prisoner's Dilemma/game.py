import strategies

class Player:
    
    def __init__(self, playStyle):
        self.playStyle = playStyle()
        self.lastAnswer = -1
        self.totalMoney = 0

    def answer(self, lastOpponentAnswer):
        return self.playStyle.answer(lastOpponentAnswer)

    def setLastAnswer(self, lastAnswer):
        self.lastAnswer = lastAnswer

    def getLastAnswer(self):
        return self.lastAnswer

    def payMoney (self, money):
        self.totalMoney += money


class Game:

    def __init__(self, playStyle1, playStyle2):
        self.player1 = Player(playStyle1)
        self.player2 = Player(playStyle2)
    
    def playWithFeedback(self, iterations):
        for i in range(0, iterations):   
            player1Answer = self.player1.answer(self.player2.getLastAnswer())
            player2Answer = self.player2.answer(self.player1.getLastAnswer())

            # pay time
            self.__pay (player1Answer, player2Answer, self.player1, self.player2)

            self.player1.setLastAnswer(player1Answer)
            self.player2.setLastAnswer(player2Answer)
         
        return [self.player1.totalMoney, self.player2.totalMoney]


    def __pay(self, player1Answer, player2Answer, player1, player2):
        if player1Answer == 0 and player2Answer == 0:
            player1.payMoney(5)
            player2.payMoney(5)
        elif player1Answer == 0 and player2Answer == 1:
            player2.payMoney(10)
        elif player1Answer == 1 and player2Answer == 0:
            player1.payMoney(10)
        elif player1Answer == 1 and player2Answer == 1:
            player1.payMoney(1)
            player2.payMoney(1)

        
