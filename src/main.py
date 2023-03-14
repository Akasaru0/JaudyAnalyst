from _class.PlayerEnd import *
from RiotAPI import *

gameid = 6313218058
data = Riot_Extract_Data_End_Game(gameid)
data2 = Riot_Extract_Timeline_Game(gameid)
dataJson = data['info']['participants'][0]

player = PlayerEnd(dataJson,data['info']['gameDuration'])
print(player)