from RiotAPI import Riot_Extract_Data_End_Game
from _class.PlayerEnd import *

class GameEnd:
    """
    Elle représente les données de fin de games
    """
    def __init__(self,gameID:int):
        # Récupération des données via l'api Riot
        data = Riot_Extract_Data_End_Game(gameID)
        
        #Attribution de la durée de la game en seconde
        self.gameDuration = int(data['info']['gameDuration'])

        #--TODO: rajouter un calcul des damages totaux de la team

        #Variable du tableau de joueur
        self.player = []

        #Attribution des joueurs dans la game.
        for i in range(0,10):
            dataJson = data['info']['participants'][i]
            #print(PlayerEnd(dataJson,self.gameDuration))
            self.player.append(PlayerEnd(dataJson,self.gameDuration))
    
    def recupDataJoueur(self,position:str,side:str):
        #Position = ['TOP','JUNLGE','MIDDLE','CARRY','UTILITY']
        if side == 'B':
            for i in range(0,5):
                if(self.player[i].individualPosition == position):
                    print(self.player[i])
        if side == 'R':
            for i in range(6,10):
                if(self.player[i].individualPosition == position):
                    print(self.player[i])