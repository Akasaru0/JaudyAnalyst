from _class.PlayerEnd import *
from _class.GameEnd import *
from _class.Daft import *
from RiotAPI import *
from DataAnalyse import *
# game1 = GameEnd(6317145488)
# game1 = GameEnd(6300818823,'Bluereal','BDS')
# game1.recupDataJoueur('UTILITY','B')
# game1.recupKillsTotaux()

# def findChampionWithId(id:int):
#     responce_version = requests.get(url = 'https://ddragon.leagueoflegends.com/api/versions.json')
#     version = (responce_version.json())[0]
#     responce_champions = requests.get(url = 'https://ddragon.leagueoflegends.com/cdn/'+version+'/data/en_US/champion.json')
#     data = responce_champions.json()
#     for champion in data['data']:
#         if(data['data'][champion]['key']==str(119)):
#             return champion

draft_1 = Draft()
draft_1.importDataDraft(6319684504)

draft_2 = Draft()
draft_2.importDataDraft(6322308433)

draft_3 = Draft()
draft_3.importDataDraft(67)

draft = []
draft.append(draft_1.getDataTeam('Projet Bluereal','bans'))
draft.append(draft_2.getDataTeam('Projet Bluereal','bans'))
draft.append(draft_3.getDataTeam('Projet Bluereal','bans'))
print(AnalyseDraft(draft))

game = GameEnd(6322308433,teamBlue='R',teamRed='B')
print(game)