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

url_solo = str(parser.get('supabase', 'SUPABASE_URL_SOLO'))
key_solo= str(parser.get('supabase', 'SUPABASE_KEY_SOLO'))
supabase_soloQ = create_client(url_solo, key_solo)

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
                        print("add "+str(data))
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
    add_kills_position_supabase(game.gameID,game)
# data = supabase.table("games").insert({'id':123121412}).execute()
# print(data)

def add_value_supabase_soloQ(game,id,puuid,name):
    data_account = Riot_Get_Rank(id)
    rank = {
        'IRON' :  0,
        'BRONZE': 400,
        'SILVER' : 800,
        'GOLD' : 1200,
        'PLATINUM' : 1600,
        'DIAMOND' : 2000,
        'MASTER' : 2400,
    }
    Div = {
        'I' : 300,
        'II': 200,
        'III': 100,
        'IV': 0,
    }
    
    lp= 0
    for i in range(0,len(data_account)):
        if data_account[i]['queueType'] == 'RANKED_SOLO_5x5':
            lp = int(rank[data_account[i]['tier']]) + int(Div[data_account[i]['rank']]) +int(data_account[i]['leaguePoints'])

    data = {'id':int(game.gameID),'date':game.date,'lp':lp,'win':'L'}
    position_player = ''
    for i in range(0,10):
        player = game.player[i]
        if player.id == puuid:
            if i>=0 and i<=4:
                if game.win == "B":
                    data['win'] = 'W'
            elif game.win == "R":
                    data['win'] = 'W'
            position_player = player.individualPosition
            data['player'] = name
            data['position'] = player.individualPosition
            data["player_champion"] = player.championName
            data['player_level'] = player.lvl
            data['player_kills'] = player.kills
            data['player_deaths'] = player.deaths
            data['player_assists'] = player.assists
            data['player_kp'] = player.killParticipation

            data['player_damage_deal'] = player.totalDamageDealtToChampions
            data['player_damage_taken'] = player.totalDamageTaken
            data['player_damage_objective'] = player.damageDealtToObjectives
            data['player_damage_turret'] = player.damageDealtToTurrets

            data['player_creep'] = player.totalCreepKilled
            data['player_sbire'] = player.neutralMinionsKilled
            data['player_jungle_sbire'] = player.totalMinionsKilled
            data['player_creep_min'] = player.creepPerMin

            data['player_ward_placed'] = player.wardsPlaced
            data['player_ward_killed'] = player.wardsKilled
            data['player_control_ward_by'] = player.visionWardsBoughtInGame
            data['player_control_ward_placed'] = player.detectorWardsPlaced
            data['player_vision_score'] = player.visionScore
            data['player_vision_score_min'] = player.visionScorePerMin

            data['player_gold_earn'] = player.goldEarned
            data['player_gold_spend'] = player.goldSpent
            data['player_damage_gold'] = player.damagePerGold

    for i in range(0,10):
        player = game.player[i]
        if player.individualPosition == position_player:
            if player.id != puuid:
                data["enemy_champion"] = player.championName
                data['enemy_level'] = player.lvl
                data['enemy_kills'] = player.kills
                data['enemy_deaths'] = player.deaths
                data['enemy_assists'] = player.assists
                data['enemy_kp'] = player.killParticipation

                data['enemy_damage_deal'] = player.totalDamageDealtToChampions
                data['enemy_damage_taken'] = player.totalDamageTaken
                data['enemy_damage_objective'] = player.damageDealtToObjectives
                data['enemy_damage_turret'] = player.damageDealtToTurrets

                data['enemy_creep'] = player.totalCreepKilled
                data['enemy_sbire'] = player.neutralMinionsKilled
                data['enemy_jungle_sbire'] = player.totalMinionsKilled
                data['enemy_creep_min'] = player.creepPerMin

                data['enemy_ward_placed'] = player.wardsPlaced
                data['enemy_ward_killed'] = player.wardsKilled
                data['enemy_control_ward_by'] = player.visionWardsBoughtInGame
                data['enemy_control_ward_placed'] = player.detectorWardsPlaced
                data['enemy_vision_score'] = player.visionScore
                data['enemy_vision_score_min'] = player.visionScorePerMin

                data['enemy_gold_earn'] = player.goldEarned
                data['enemy_gold_spend'] = player.goldSpent
                data['enemy_damage_gold'] = player.damagePerGold
    supabase_soloQ.table('soloq').insert(data).execute()

def init_supabase_soloQ(players):
    for i in range(0,len(players)):
        # Construire la requête SELECT
        try:
            query = supabase_soloQ.table('soloq').select('id').eq('player', ''+players[i]['name']).order('date', desc=True)
            # Exécuter la requête
            response = query.execute()
            players[i]["last_game"] = response.data[0]["id"]
        except:
            players[i]["last_game"] = 0