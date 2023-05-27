class Player:
    """
    Elle représente les données de fin de games pour un joueur
    """
    def __init__(self,dataEndJson:dict,dataTimeJson:dict,gameDuration:int):

        self.id = dataEndJson['puuid']
        self.setSummonerName(dataEndJson['summonerName'])   
        self.setPosition(dataEndJson['lane'],dataEndJson['individualPosition'])
        self.setChampion(dataEndJson['championName'],dataEndJson['champLevel'],dataEndJson['champExperience'])
        self.setKDA(dataEndJson['kills'],dataEndJson['deaths'],dataEndJson['assists'])
        self.setDamagesObjectif(dataEndJson['damageDealtToObjectives'])
        self.setDamagesTurret(dataEndJson['damageDealtToTurrets'])
        self.setTotalDamaged(dataEndJson['totalDamageDealtToChampions'],dataEndJson['totalDamageTaken'])
        self.setWards(dataEndJson['wardsPlaced'],dataEndJson['wardsKilled'],dataEndJson['visionWardsBoughtInGame'],dataEndJson['detectorWardsPlaced'])
        self.setVisionScore(dataEndJson['visionScore'],gameDuration)
        self.setGold(dataEndJson['goldEarned'],dataEndJson['goldSpent'])
        self.setTotalCreep(dataEndJson['totalMinionsKilled'],dataEndJson['neutralMinionsKilled'])
        self.setKillParticipation(dataEndJson['challenges']['killParticipation'])
        self.setCreepPerMin(gameDuration)
        self.setDamagePerGold(dataEndJson['totalDamageDealtToChampions'],dataEndJson['goldSpent'])

    
    def setSummonerName(self,summonerName:str):
        #Attribution du nom d'invocateur
        self.summonerName = summonerName

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
    
    def setVisionScore(self,visionScore:int,gameDuration:int):
        #Attribution du score de vision
        self.visionScore = visionScore
        self.visionScorePerMin = format(60*self.visionScore/gameDuration, '.1f')

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
        self.killParticipation = format(killParticipation, '.4f')

    def setCreepPerMin(self,gameDuration:int):
        #Attribution des valeurs de kill participation
        self.creepPerMin = format(60*self.totalCreepKilled/gameDuration, '.1f')

    def setDamagePerGold(self,totalDamageDealtToChampions:str,goldSpent:str):
        self.damagePerGold = format(totalDamageDealtToChampions/goldSpent,'.2f')


    def __str__(self):
        #fonction to string
        return f"Summoner Name: {self.summonerName.encode('utf-8')}\n" \
               f"ID: {self.id}\n" \
               f"Champion: {self.championName}\n" \
               f"Lane: {self.lane}\n" \
               f"Position: {self.individualPosition}\n" \
               f"Level: {self.lvl}\n" \
               f"Kills: {self.kills}\n" \
               f"Deaths: {self.deaths}\n" \
               f"Assists: {self.assists}\n" \
               f"KDA: {self.kills}/{self.deaths}/{self.assists}\n" \
               f"Damage dealt to objectives: {self.damageDealtToObjectives}\n" \
               f"Damage dealt to turrets: {self.damageDealtToTurrets}\n" \
               f"Total damage dealt to champions: {self.totalDamageDealtToChampions}\n" \
               f"Total damage taken: {self.totalDamageTaken}\n" \
               f"Wards placed: {self.wardsPlaced}\n" \
               f"Wards killed: {self.wardsKilled}\n" \
               f"Vision wards bought in game: {self.visionWardsBoughtInGame}\n" \
               f"Detector wards placed: {self.detectorWardsPlaced}\n" \
               f"Vision score: {self.visionScore}\n" \
               f"Vision score/min: {self.visionScorePerMin}\n"\
               f"Gold earned: {self.goldEarned}\n" \
               f"Gold spent: {self.goldSpent}\n" \
               f"Damage Per Gold {self.damagePerGold}\n"\
               f"Total minion killed: {self.totalMinionsKilled}\n" \
                f"Total neutralMinons killed: {self.neutralMinionsKilled}\n" \
               f"Total creep killed: {self.totalCreepKilled}\n" \
               f"Creep per minute: {self.creepPerMin}\n" \
               f"Kill participation: {self.killParticipation}%\n"
    
    def getPlayerInfo(self):
        info = {
            'summonner_name' : str(self.summonerName),
            'id' : str(self.id),
            'champion' : str(self.championName),
            'lane' : str(self.lane),
            'Position' : str(self.individualPosition),
            'lvl' : str(self.lvl),
            'kills' : str(self.kills),
            'deaths' : str(self.deaths),
            'assists' : str(self.assists),
            'damageToObjective' : str(self.damageDealtToObjectives),
            'damageToTurrets' : str(self.damageDealtToTurrets),
            'totalDamageDealtToChampions' : str(self.totalDamageDealtToChampions),
            'damageTaken' : str(self.totalDamageTaken),
            'wardsPlaced' : str(self.wardsPlaced),
            'wardsKilled' : str(self.wardsKilled),
            'visionWardsBoughtInGame' : str(self.visionWardsBoughtInGame),
            'detectorWardsPlaced' : str(self.detectorWardsPlaced),
            'visionScore' : str(self.visionScore),
            'visionScorePerMin' : str(self.visionScorePerMin),
            'goldEarned' : str(self.goldEarned),
            'goldSpent' : str(self.goldSpent),
            'totalMinionsKilled' : str(self.totalMinionsKilled),
            'neutralMinionsKilled' : str(self.neutralMinionsKilled),
            'totalCreepKilled' : str(self.totalCreepKilled),
            'creepPerMin' : str(self.creepPerMin),
            'killParticipation' : str(self.killParticipation),
        }
        return info
        