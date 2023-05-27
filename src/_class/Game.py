from RiotAPI import Riot_Extract_Data_End_Game , Riot_Extract_Timeline_Game
from _class.Player import Player
from _class.Kills import Kill
import requests,datetime

class Game:
    """
    Elle représente les données de fin de games
    """
    def __init__(self,gameID:int,teamBlue:str=None,teamRed:str=None):
        # Récupération des données via l'api Riot
        data_end = Riot_Extract_Data_End_Game(gameID)
        data_time = Riot_Extract_Timeline_Game(gameID)

        #Attribution du game id de la partie
        self.gameID = gameID

        #Attribution de la date
        unix_time = int(data_end['info']['gameCreation']/1000)
        date_time = datetime.datetime.fromtimestamp(unix_time)
        self.date = date_time.strftime('%Y-%m-%d %H:%M:%S')
        
        #Attribution de la durée de la game en seconde
        self.gameDuration = int(data_end['info']['gameDuration'])

        #Variable du tableau de joueur
        self.player = []

        #Attribution des joueurs dans la game.
        for i in range(0,10):
            data_end_json = data_end['info']['participants'][i]
            #print(PlayerEnd(dataJson,self.gameDuration))
            self.player.append(Player(data_end_json,data_time,self.gameDuration))     

        #Attribution des noms de team
        if (teamBlue != None and teamRed != None):
            self.teamBlue = teamBlue
            self.teamRed = teamRed
        else:
            self.teamBlue = None
            self.teamRed = None
        
        self.recupKDATotaux()
        self.recupDamagesTotaux()

        # Récupération de la variable win
        if data_end["info"]['teams'][0]["win"]:
            self.win = "B"
        else:
            self.win = "R"

        # Récupération du frist blood
        if data_end["info"]['teams'][0]["objectives"]["champion"]["first"]:
            self.firstblood_blue = True
            self.firstblood_red = False
        else:
            self.firstblood_blue = False
            self.firstblood_red = True
        
        self.recup_bans_team(data_end["info"]["teams"])
        self.set_kill_position(data_time)
        # for i in range(0,len(self.kills)):
        #     print(self.kills[i])
    
    #Fonction de création d'object kill.
    def set_kill_position(self,dataJson):
        self.kills = []
        for i in range(0,len(dataJson["info"]["frames"])):
            data_frames = dataJson["info"]["frames"][i]
            for j in range(0,len(data_frames["events"])):
                data_event = data_frames["events"][j]
                if data_event["type"] == "CHAMPION_KILL":

                    victim = ""
                    killer = ""
                    #get the killer and victim player object
                    for k in range(0,len(self.player)):
                        if self.player[k].id == dataJson["metadata"]["participants"][int(data_event["killerId"]-1)]:
                            killer = self.player[k]
                        if self.player[k].id == dataJson["metadata"]["participants"][int(data_event["victimId"]-1)]:
                            victim = self.player[k]
                    
                    #get all the assist
                    assist = []
                    if "assistingParticipantIds" in data_event:
                        for id_assist in data_event["assistingParticipantIds"]:
                            for k in range(0,len(self.player)):
                                if self.player[k].id == id_assist:
                                    assist.append(self.player[k])
                    if len(assist) != 0:
                        self.kills.append(Kill(victim,killer,data_event["position"]["x"],data_event["position"]["y"],assists=assist))
                    else:
                        self.kills.append(Kill(victim,killer,data_event["position"]["x"],data_event["position"]["y"]))

    #Récuperation des bans des différentes teams
    def recup_bans_team(self, dataJson):
        #Récuperation du patch actuel
        version = (requests.get("https://ddragon.leagueoflegends.com/api/versions.json")).json()
        #Récuperation du dictionnaire contetant les informations des champions
        champ_data = requests.get('https://ddragon.leagueoflegends.com/cdn/'+version[0]+'/data/en_US/champion.json').json()
        self.bans_blue = []
        self.bans_red = []
        for i in range(0,5):
            id_champ_blue = dataJson[0]['bans'][i]["championId"]
            id_champ_red = dataJson[1]['bans'][i]["championId"]
            for champs in champ_data["data"]:
                if champ_data["data"][champs]["key"] == str(id_champ_blue):
                    self.bans_blue.append(champs)
                if champ_data["data"][champs]["key"] == str(id_champ_red):
                    self.bans_red.append(champs)

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
