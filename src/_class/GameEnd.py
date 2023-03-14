from RiotAPI import Riot_Extract_Data_End_Game
class GameEnd:
    """
    Elle représente les données de fin de games
    """
    def __init__(self,gameID):
        """
        Fonction d'initalisation.
        Elle va chercher les donnés dans la réponces de l'api pour les stocker dans les variables.
        """
        # Récupération des données via l'api Riot
        data = Riot_Extract_Data_End_Game(gameID)
        #Attribution des données
        self.gameDuration = int(data['info']["gameDuration"]) #Attribution de la durée de la game en seconde
        