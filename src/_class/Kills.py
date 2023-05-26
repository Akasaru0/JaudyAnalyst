from _class.Player import Player


class Kill:
    """
    Elle représente un kill d'une partie
    """
    def __init__(self,victim:Player,killer:Player,position_x:int,position_y:int,assists:list[Player]=None):
        self.victim = victim
        self.killer = killer
        self.position_x = position_x
        self.position_y = position_y
        self.assists = list[Player]
        if assists !=None and len(assists) !=0:
            self.assists = list[Player]
            for i in range(0,len(assists)):
                self.assists.append(assists[i])
    
    def getPosition(self):
        return self.position_x,self.position_y
    
    def getVictim(self):
        return self.victim
    
    def getKiller(self):
        return self.killer

    def __str__(self) -> str:
        return f"V:{self.victim.summonerName} K:{self.killer.summonerName} P:{self.position_x},{self.position_y}"
