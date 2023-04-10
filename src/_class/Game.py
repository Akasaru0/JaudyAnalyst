from RiotAPI import Riot_Extract_Data_End_Game
from _class.Player import Player

class Game:
    """
    Elle représente les données de fin de games
    """
    def __init__(self,gameID:int,win:int=None,teamBlue:str=None,teamRed:str=None):
        # Récupération des données via l'api Riot
        data = Riot_Extract_Data_End_Game(gameID)
        self.gameID = gameID
        
        #Attribution de la durée de la game en seconde
        self.gameDuration = int(data['info']['gameDuration'])

        #Variable du tableau de joueur
        self.player = []

        #Attribution des joueurs dans la game.
        for i in range(0,10):
            dataJson = data['info']['participants'][i]
            #print(PlayerEnd(dataJson,self.gameDuration))
            self.player.append(Player(dataJson,self.gameDuration))     

        #Attribution des noms de team
        if (teamBlue != None and teamRed != None):
            self.teamBlue = teamBlue
            self.teamRed = teamRed
        self.win = win
        self.recupKDATotaux()
        self.recupDamagesTotaux()
        
    #Elle permet de retourner les données d'un joueur en fonction d'une postion et d'un side
    def recupDataJoueur(self,position:str,side:str):
        if position in ['TOP','JUNLGE','MIDDLE','CARRY','UTILITY']:
            if side == 'B' and side == "BLUE":
                for i in range(0,5):
                    if(self.player[i].individualPosition == position):
                        return self.player[i]
            elif side == 'R' and side == "RED":
                for i in range(6,10):
                    if(self.player[i].individualPosition == position):
                        return self.player[i]
            else:
                #Déclenchement d'une execption si le side n'est pas correct
                raise Exception("GamedEnd Execption. The input side isn't in the list of value : ['R','B']")
        else:
            #Déclenchement d'une expection pour le cas ou la position n'est pas bonne
            raise Exception("GamedEnd Execption. The input position isn't in the list of value : ['TOP','JUNLGE','MIDDLE','CARRY','UTILITY']")
    
    def recupKDATotaux(self):
        self.kills_blue = 0
        self.kills_red = 0
        self.deaths_blue = 0
        self.deaths_red = 0
        self.assists_blue = 0
        self.assists_red = 0
        for i in range(0,5):
                self.kills_blue = self.kills_blue + self.player[i].kills
                self.kills_red = self.kills_red + self.player[i+5].kills
                self.deaths_blue = self.deaths_blue + self.player[i].deaths
                self.deaths_red = self.deaths_red + self.player[i+5].deaths
                self.assists_blue = self.assists_blue + self.player[i].assists
                self.assists_red = self.assists_red + self.player[i+5].assists
    def recupDeathsTotaux(self):
        self.deaths_blue = 0
        self.deaths_red = 0
        for i in range(0,5):
                self.kills_blue = self.kills_blue + self.player[i].kills
                self.kills_red = self.kills_red + self.player[i+5].kills
    def recupDamagesTotaux(self):
        self.damages_blue = 0
        self.damages_red = 0
        for i in range(0,5):
                self.damages_blue = self.damages_blue + self.player[i].totalDamageDealtToChampions
                self.damages_red = self.damages_red + self.player[i+5].totalDamageDealtToChampions
    def __str__(self):
        player_str = "\n".join(str(p) for p in self.player)
        return f"GameEnd(gameID={self.gameID}, gameDuration={self.gameDuration},\n" \
               f"teamBlue={self.teamBlue}, teamRed={self.teamRed},\n" \
               f"kills_blue={self.kills_blue}, kills_red={self.kills_red},\n" \
               f"players=\n{player_str})"
    
    def exportcsv(self,output:str="output.csv"):
        with open(output+"",'w') as f:
            line = str(self.gameID)+';'+str(self.teamBlue)+";"+str(self.teamRed)+";"+str(self.win)+";"+str(self.gameDuration)
            line = line+';'+str(self.kills_blue)+';'+str(self.deaths_blue)+";"+str(self.assists_blue)+';;;;'+str(self.kills_red)+';'+str(self.deaths_red)+";"+str(self.assists_red)+';;;;\n'
            f.write(line)
            for i in range(0,10):
                line = str(self.gameID)
                player = self.player[i]
                
                line = line+';'+str(player.individualPosition)
                if i>=0 and i<=4:
                    line = line +';B'
                if i>=5 and i<=10:
                    line = line +';R'
                line = line+';'+str(player.summonerName)+';'+str(player.championName)+';'+str(player.lvl)
                #Set the KDA of the player
                line = line+';'+str(player.kills)+';'+str(player.deaths)+';'+str(player.assists)+';'+str(player.killParticipation)
                #Set the Damage of the player
                line = line+';'+str(player.totalDamageDealtToChampions)+';'+str(player.totalDamageTaken)+';'+str(player.damageDealtToObjectives)+';'+str(player.damageDealtToTurrets)
                #Set the Farming
                line = line+';'+str(player.totalCreepKilled)+';'+str(player.neutralMinionsKilled)+';'+str(player.totalMinionsKilled)+';'+str(player.creepPerMin)
                #Set the Vision
                line = line+';'+str(player.wardsPlaced)+';'+str(player.wardsKilled)+';'+str(player.visionWardsBoughtInGame)+';'+str(player.detectorWardsPlaced)+';'+str(player.visionScore)+';'+str(player.visionScorePerMin)
                #Set the gold
                line = line+';'+str(player.goldEarned)+';'+str(player.goldSpent)+';'+str(player.damagePerGold)+'\n'
                line=line.replace('.',',')
                f.write(line)
