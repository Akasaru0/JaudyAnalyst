from _class.Player import *
from _class.Game import *
from _class.Daft import *
from RiotAPI import *
from DataAnalyse import *
from PlayWithSupabase import *
from DataAnalyse import *


import datetime,time
from supabase import create_client
url = str(parser.get('supabase', 'SUPABASE_URL'))
key= str(parser.get('supabase', 'SUPABASE_KEY'))

psuedo = 'M6GU1rw0AwMPKcRlVjmF1Awa5yN8OC3K0qokHeUGVLapNeddyEWpiXmbZDpz6CjEkqqMdWbSWRGFVA'
id_player = 'LAT6RUfQ_Xqhqgp0h0N5j4FRZ3lWN8a_cZn1R5_vDjkFU4M'

game = Game(6299264893,teamBlue='',teamRed='')

players = [
    {
        'pseudo' : "Tomu",
        "id" : "LAT6RUfQ_Xqhqgp0h0N5j4FRZ3lWN8a_cZn1R5_vDjkFU4M",
        "puuid" : 'M6GU1rw0AwMPKcRlVjmF1Awa5yN8OC3K0qokHeUGVLapNeddyEWpiXmbZDpz6CjEkqqMdWbSWRGFVA',
        "last_game" : 0
    },
    {
        'pseudo' : "BL Levi",
        "id" : "NSFdyalgCoCcy5ZWTiPk-hwHQ4Ydb8wfEidb5iRplTBJxhU",
        "puuid" : 'N1OSZ7PwrW3el3BvahXy8wTRERjJNpxzb0XvuTFdUvZRVaDib_nA8PmKrarL3N0eDCglr0wn3ch8Gw',
        "last_game" : 0
    },
    {
        'pseudo' : "BL YMZ",
        "id" : "Hhy1MJCM3R9WTGPOT5h5vjacLWbPQv5YnIl7wkUT96nI3OI",
        "puuid" : '4XIfntsM2BzQ3RI3PAwKg8aBgeLe3HG4jGexRjL3aekY7ytGkB4JHEiFVtaXT9QyA3h_pkNaXhDS7g',
        "last_game" : 0
    },
    {
        'pseudo' : "BL Héraclèss",
        "id" : "mhBoh_HRjK4GxdOOqxvLYZczBeS8nekHy7fzZskNdyAx3zg",
        "puuid" : 'hh5RproKBBe7wO-InOX8t3LhxxIsb8K2l7pcorNTUXnZRGzO6N_OEbNy0uROr26Zkic0Q-vpl5n0qw',
        "last_game" : 0
    },
    {
        'pseudo' : "BL ZNK",
        "id" : "AwGyaW7brYNo2gTFhhAEKf1-MIyeYCrrqMzBjxcz5i_NNqsHPF7q3gpd9g",
        "puuid" : 'G0XNd7SGMVsQW0tK-5r0zVSjLjhcMnKhidVwdnuPaNXALATt3RN2A0L7UW_8XkbK4ED2ded31WS_LA',
        "last_game" : 0
    },
]

while(1):
    print("TEST")
    for i in range(0,len(players)):
        history = Riot_Get_Last_Ranked(players[i]['puuid'])
        if(history[0].split('_')[1] != players[i]["last_game"]):
            print('NEW game for '+players[i]["pseudo"])
            add_value_supabase_soloQ(Game(history[0].split('_')[1]),players[i]['id'],players[i]['puuid'])
            players[i]['last_game']=history[0].split('_')[1]
    time.sleep()
