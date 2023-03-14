class PlayerEnd:
    """
    Elle représente les données de fin de games pour un joueur
    """
    def __init__(self,id:str,dataJson:dict):
        #Attribution de l'id riot du joueur
        self.id = id

        #Attribution du nom d'invocateur
        self.summonerName = dataJson['summonerName']
        
        # /!\ la lane et la posiiton individuel sont différentes :
        # - la lane est souvent associer au champion | Exemple : ["TOP","JUNGLE","MIDDLE","BOTTOM","BOTTOM"]
        # - la position indiv est la position des joueurs | Exemple : ["TOP","JUNGLE","MIDDLE","BOTTOM","UTILITY"]  
        #Attribution de la lane 
        self.lane = dataJson['lane']
        #Attribution de la Position individuel
        self.individualPosition = dataJson['individualPosition']

    def setPosition(self, lane:str, individualPosition:str):
        # /!\ la lane et la posiiton individuel sont différentes :
        # - la lane est souvent associer au champion | Exemple : ["TOP","JUNGLE","MIDDLE","BOTTOM","BOTTOM"]
        # - la position indiv est la position des joueurs | Exemple : ["TOP","JUNGLE","MIDDLE","BOTTOM","UTILITY"]  
        #Attribution de la lane 
        self.lane = lane
        #Attribution de la Position individuel
        self.individualPosition = individualPosition
    
    def setChampion(self,championName:str,champLevel:int,champExperience:int):
        #Attribution du Champion
        self.championName = championName 
        #Attribution du Champion
        self.champExperience = champExperience
        #Attribution du lvl du champion
        self.lvl = champLevel
    
    def setKDA(self,kills:int,deaths:int,assists:int):
        #Attribution du KDA du joueur
        self.kills = kills
        self.assists = assists
        self.deaths = deaths
    
    def setDamagesObjectif(self,damageDealtToObjectives:int):
        #Attribution des damages fais sur les objectifs
        self.damageDealtToObjectives = damageDealtToObjectives
    
    def setDamagesTurret(self,damageDealtToTurrets:int):
        #Attribution des damages sur les tours
        self.damageDealtToTurrets = damageDealtToTurrets
    
    def setTotalDamaged(self,totalDamageDealtToChampions:int,totalDamageTaken:int):
        #Attribution des damages totaux fait sur les champions
        self.totalDamageDealtToChampions = totalDamageDealtToChampions
        #Attribution des damages totaux subis
        self.totalDamageTaken = totalDamageTaken

    def setWards(self,wardsPlaced:int,wardsKilled:int,visionWardsBoughtInGame:int,detectorWardsPlaced:int):
        #Attribution des ward placées
        self.wardsPlaced = wardsPlaced
        #Attribution des ward tuées
        self.wardsKilled = wardsKilled
        #Attribution des controls ward achetées
        self.visionWardsBoughtInGame = visionWardsBoughtInGame
        #Attribution du nombre de controls ward posées
        self.detectorWardsPlaced = detectorWardsPlaced
    
    def setVisionScore(self,visionScore:int):
        #Attribution du score de vision
        self.visionScore = visionScore

    def setGold(self,goldEarned:int,goldSpent:int):
        #Attribution du montant de gold gagné
        self.goldEarned = goldEarned
        #Attribution du montant de gold utilisé
        self.goldSpent = goldSpent
    
    def setTotalCreep(self,totalMinionsKilled:int,neutralMinionsKilled:int):
        #Attribution du nombre total de sbires tués
        self.totalMinionsKilled = totalMinionsKilled
        #Attribution du nombre total de monstre de la jungle tués
        self.neutralMinionsKilled = neutralMinionsKilled

        #Attribution du nombre total de creep a la fin de la partie
        self.totalCreepKilled = self.totalMinionsKilled + self.neutralMinionsKilled

    def setKillParticipation(self,killParticipation:float):
        #Attribution des valeurs de kill participation
        self.killParticipation = format(killParticipation*100, '.0f')

    def setCreepPerMin(self,gameDuration:int):
        #Attribution des valeurs de kill participation
        self.creepPerMin = format(60*self.totalCreepKilled/gameDuration, '.1f')