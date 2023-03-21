from RiotAPI import Riot_Extract_Data_End_Game
from _class.PlayerEnd import PlayerEnd

class GameEnd:
    """
    Elle représente les données de fin de games
    """
    def __init__(self,gameID:int,teamBlue:str=None,teamRed:str=None):
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
            self.player.append(PlayerEnd(dataJson,self.gameDuration))     

        #Attribution des noms de team
        if (teamBlue != None and teamRed != None):
            self.teamBlue = teamBlue
            self.teamRed = teamRed
        
        self.recupKillsTotaux()
        self.recupDamagesTotaux()
        
    
    def recupDataJoueur(self,position:str,side:str):
        if position in ['TOP','JUNLGE','MIDDLE','CARRY','UTILITY']:
            if side == 'B':
                for i in range(0,5):
                    if(self.player[i].individualPosition == position):
                        return self.player[i]
            elif side == 'R':
                for i in range(6,10):
                    if(self.player[i].individualPosition == position):
                        return self.player[i]
            else:
                #Déclenchement d'une execption si le side n'est pas correct
                raise Exception("GamedEnd Execption. The input side isn't in the list of value : ['R','B']")
        else:
            #Déclenchement d'une expection pour le cas ou la position n'est pas bonne
            raise Exception("GamedEnd Execption. The input position isn't in the list of value : ['TOP','JUNLGE','MIDDLE','CARRY','UTILITY']")
    
    def recupKillsTotaux(self):
        self.kills_blue = 0
        self.kills_red = 0
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