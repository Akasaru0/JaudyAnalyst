from configparser import ConfigParser
parser = ConfigParser()

parser.read('src/config.ini')
from RiotAPI import *
from supabase import create_client
from _class.Game import *


import sys, os


url = str(parser.get('supabase', 'SUPABASE_URL'))
key= str(parser.get('supabase', 'SUPABASE_KEY'))
supabase = create_client(url, key)

def add_kills_position_supabase(game_id,game):
    data_game = Riot_Extract_Timeline_Game(game_id)
    for i in range(0,len(data_game['info']['frames'])):
        for j in range(0,len(data_game['info']['frames'][i]['events'])):
            if data_game["info"]["frames"][i]["events"][j]['type'] == 'CHAMPION_KILL':
                # try:
                    #Pour simplifier le code je met tout dans tab
                    tab = data_game["info"]["frames"][i]["events"][j]

                    #Je vais recupérer les positions et side des joueurs
                    hash_victim = str(data_game["metadata"]["participants"][tab["victimId"]-1])
                    hash_killer = str(data_game["metadata"]["participants"][tab["killerId"]-1])
                    # On check si le side de la victime


                    data = {"id":int(game_id),"time":int(tab["timestamp"]),'position_x':int(tab["position"]["x"]),'position_y':int(tab["position"]["y"])}
                    for k in range(0,10):
                        player = game.player[k]
                        if str(player.id) == str(hash_victim):
                            data["victim_position"] = player.individualPosition
                            if k>=0 and k<=4:
                                data["victim_side"] = "B"
                            elif k>=5 and k<=10:
                                data["victim_side"] = "R"
                        if player.id == hash_killer:
                            data["killer_position"] = player.individualPosition
                            if k>=0 and k<=4:
                                data["killer_side"] = "B"
                            elif k>=5 and k<=10:
                                data["killer_side"] = "R"
                    try:
                        supabase.table('position_kills').insert(data).execute()
                    except:
                        pass
                # except Exception as e:
                #     pass

def add_value_supabase(game):
    data = {"id":int(game.gameID),"duration":int(game.gameDuration),"win":str(game.win)}
    #Ajout des données de la game dans la base de donnée 
    supabase.table('games').insert(data).execute()

    #Ajout des données de team de la game
    data = {"id":int(game.gameID),"side":'B',"name":str(game.teamBlue),'kills':game.kills_blue,'deaths':game.deaths_blue,'assists':game.assists_blue,'firstblood':game.firstblood_blue}
    compteur = 1
    for champs in game.bans_blue:
        data["bans"+str(compteur)] = champs
        compteur = compteur+1
    supabase.table('teams').insert(data).execute()

    data = {"id":int(game.gameID),"side":'R',"name":str(game.teamRed),'kills':game.kills_red,'deaths':game.deaths_red,'assists':game.assists_red,'firstblood':game.firstblood_red}
    compteur = 1
    for champs in game.bans_red:
        data["bans"+str(compteur)] = champs
        compteur = compteur+1
    supabase.table('teams').insert(data).execute()

    for i in range(0,10):
        player = game.player[i]
        data = {"id":int(game.gameID)}
        if i>=0 and i<=4:
            data["side"] = "B"
        elif i>=5 and i<=10:
            data["side"] = "R"

        data["summoners"] = player.summonerName
        data["champion"] = player.championName
        data["position"] = player.individualPosition
        data["level"] = player.lvl
        
        data["kills"] = player.kills
        data['deaths'] = player.deaths
        data['assists'] = player.assists
        data['kp'] = player.killParticipation

        data['damage_deal'] = player.totalDamageDealtToChampions
        data['damage_taken'] = player.totalDamageTaken
        data['damage_objective'] = player.damageDealtToObjectives
        data['damage_turret'] = player.damageDealtToTurrets

        data['creep'] = player.totalCreepKilled
        data['sbire'] = player.neutralMinionsKilled
        data['jungle_sbire'] = player.totalMinionsKilled
        data['creep_min'] = player.creepPerMin

        data['ward_placed'] = player.wardsPlaced
        data['ward_killed'] = player.wardsKilled
        data["control_ward_by"] = player.visionWardsBoughtInGame
        data["control_ward_placed"] = player.detectorWardsPlaced
        data["vision_score"] = player.visionScore
        data["vision_score_min"] = player.visionScorePerMin

        data["gold_earn"] = player.goldEarned
        data["gold_spend"] = player.goldSpent
        data["damage_gold"] = player.damagePerGold
        supabase.table('players').insert(data).execute()
    #add_kills_position_supabase(game.gameID,game)
# data = supabase.table("games").insert({'id':123121412}).execute()
# print(data)
