from _class.PlayerEnd import *
from RiotAPI import *

gameid = 6313218058
data = Riot_Extract_Data_End_Game(gameid)
data2 = Riot_Extract_Timeline_Game(gameid)
for i in range(0,9):
    print("\n")
    dataJson = data['info']['participants'][i]
    player = PlayerEnd(dataJson,data['info']['gameDuration'])
    print(player)