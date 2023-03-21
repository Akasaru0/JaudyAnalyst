
import json, os
class Draft:
    """
    Elle représente les données de draft
    """
    def __init__(self):
        self.draft = {
            "blue":{
                "picks":{
            
                },
                "bans":{
            
                }
            },
            "red":{
                "picks":{
            
                },
                "bans":{
            
                }        
            }
        }
    def setTeamName(self,TeamBlue:str,TeamRed:str):
        self.draft["blue"]["team"] = TeamBlue
        self.draft["red"]["team"] =  TeamRed

    def setPick(self,side:str,champion):
        if side == 'B':
            for i in range(0,5):
                self.draft["blue"]["picks"][str(i)] = champion[i]
        elif side == 'R':
            for i in range(0,5):
                self.draft["red"]["picks"][str(i)] = champion[i]

    def setBan(self,side:str,bans):
        if side == 'B':
            for i in range(0,5):
                self.draft["blue"]["bans"][str(i)] = bans[i]
        elif side == 'R':
            for i in range(0,5):
                self.draft["red"]["bans"][str(i)] = bans[i]
    
    def getPick(self,side:str):
        res = []
        if side == 'B':
            for i in range(0,5):
                res.append(self.draft["blue"]['picks'][str(i)])
        elif side == 'R':        
            for i in range(0,5):
                res.append(self.draft["red"]['picks'][str(i)])
        return res
                    
    def getBan(self,side:str):
        res = []
        if side == 'B':
            for i in range(0,5):
                res.append(self.draft["blue"]['bans'][str(i)])
        elif side == 'R':        
            for i in range(0,5):
                res.append(self.draft["red"]['bans'][str(i)])
        return res
    
    def importDataDraft(self,Gameid:int):
        if(os.path.isfile("database/draft_game/DRAFT_"+str(Gameid)+".json")):
            with open("database/draft_game/DRAFT_"+str(Gameid)+".json") as json_file:
                self.draft = json.load(json_file)
        else:
            raise Exception("Draft Error. The Draft doesn't exist")

    def saveDataDraft(self,Gameid:int):
        data = json.dumps(self.draft, indent=4)
        with open("database/draft_game/DRAFT_"+str(Gameid)+".json","w") as out:
            out.write(data)

    def getDataTeam(self,teamName:str,type:str):
        res = []
        if teamName == self.draft["blue"]["team"]:
            for i in range(0,5):
                res.append(self.draft["blue"][type][str(i)])         
        elif teamName == self.draft["red"]["team"]:
            for i in range(0,5):
                res.append(self.draft["red"][type][str(i)])  
        return res

    def getDataVS(self,teamName:str,type:str):
        res = []
        if teamName == self.draft["blue"]["team"]:
            for i in range(0,5):
                res.append(self.draft["red"][type][str(i)])       
        elif teamName == self.draft["red"]["team"]:
            for i in range(0,5):
                res.append(self.draft["blue"][type][str(i)])  
        return res

    def __str__(self):
        res = "Draft Information\n"
        res += "Blue Team: " + self.draft["blue"]["team"] + "\n"
        res += "Red Team: " + self.draft["red"]["team"] + "\n\n"
        res += "Blue Team Bans: " + str(self.getBan("B")) + "\n"
        res += "Red Team Bans: " + str(self.getBan("R")) + "\n\n"
        res += "Blue Team Picks: " + str(self.getPick("B")) + "\n"
        res += "Red Team Picks: " + str(self.getPick("R")) + "\n"
        return res