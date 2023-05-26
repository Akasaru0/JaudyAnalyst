from _class.Player import *
from _class.Game import *
from _class.Daft import *
from RiotAPI import *
from DataAnalyse import *
from PlayWithSupabase import *
from DataAnalyse import *
#game1 = GameEnd(6317145488)
#add_kills_position_supabase(6322721766,Game(6322721766,teamBlue='Bluereal',teamRed='BDS'))
game1 = Game(6418170525,teamBlue='TESrt',teamRed='Bluereal')
create_heatmap(game1)
#create_heatmap(game1,debug=True)
#add_value_supabase(Game(6313218058,teamBlue='',teamRed='Bluereal'))
# add_value_supabase(Game(6328369266,teamBlue='BDS',teamRed='Bluereal'))
# add_value_supabase(Game(6300818823,teamBlue='Bluereal',teamRed='BDS'))
# version = (requests.get("https://ddragon.leagueoflegends.com/api/versions.json")).json()
# champ_data = requests.get('https://ddragon.leagueoflegends.com/cdn/'+version[0]+'/data/en_US/champion.json').json()

# for champs in champ_data["data"]:
#     if champ_data["data"][champs]["key"] == str(103):
#         print("alalalall")s
#         break