import output
import strategies as s

#output.twoPlayers(1, 10, s.TitForTat, s.Adaptive)
#output.twoPlayers(2, 1000, s.AlwaysAccept, s.RandomChoice)
#output.allStratsToTXT()
#output.graphFiveGames(s.TitForTat, s.Adaptive, 1000)
#output.twoPlayers(1, 10, s.RandomChoice, s.Adaptive)
output.twoPlayers(1, 1000, s.Adaptive, s.RandomChoice)
