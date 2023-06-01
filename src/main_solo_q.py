from _class.Game import *
from PlayWithSupabase import *



import json,time
from supabase import create_client
url = str(parser.get('supabase', 'SUPABASE_URL_SOLO'))
key= str(parser.get('supabase', 'SUPABASE_KEY_SOLO'))

supabase = create_client(url, key)


psuedo = 'M6GU1rw0AwMPKcRlVjmF1Awa5yN8OC3K0qokHeUGVLapNeddyEWpiXmbZDpz6CjEkqqMdWbSWRGFVA'
id_player = 'LAT6RUfQ_Xqhqgp0h0N5j4FRZ3lWN8a_cZn1R5_vDjkFU4M'

def add_player_to_soloQ(username):
    query_riot = Riot_Get_UserId(username)
    if "id" in query_riot:
        print(json.dumps(query_riot, indent=4))

    else:
        print('Le pseudo n\'existe pas')

players=[
    {
        "id": "aRabKKX2ytT022E-Oq2H_OD2W82HfwZ6Ufv1OXKyNzCR34w",
        "accountId": "qWhf9l0jNT-t8ya1rt6ZlXN_3MDak_LmIye3KnGPfiA5mww",
        "puuid": "oEEHBRQ_agUnMxOsYGktLoqE6-R9LUoBeiM5ZSCyszDjFWuRQUzncCuCtDCXUZU2ulFrF61tfx1kJg",
        "name": "Tomu"
    },
    {
        "id": "03hTWYOmRhynDloJuDOXs0bKizO8ewImK0l455npS0mOWlw",
        "accountId": "S6z6nQ4fBOFT6652Whntm7x1Gjx8BbgEbUeiREGRx01uKqc",
        "puuid": "x0gU9mSsU4AcL4Au9GEfrZhSeqVWr_gIEZu53Hc45zuGO2XvFbcuA1_hfJuC3rcVT5fwUX86o8lnOw",
        "name": "BL Levi"
    },
    {
        "id": "kg46_9UTo5eXEtAUNFeBGTYI0qserfzdNmJ1o9xg0aFJT6I",
        "accountId": "Wg5Xn-330Yist0wfSw2AdhQpiSSTcSfgsJ5doaSV7-t9So0",
        "puuid": "emAo8MC2aKdBYFCIxB-Kj-5ZH7FEdnl1c_qp_Qc-GN7Padfr1akf1QsiaaqKIKfXnUPY-sHqfsPw6Q",
        "name": "BL YMZ"
    },
    {
        "id": "pyNOujiPvaweUcI11AHzRNUaN0Va5HT_JJ-BWFsErTMrE6E",
        "accountId": "sS16jgGtclbPzKCeUSXFcT--2RJ_Jc5PdXbUIBDiUsfCmg",
        "puuid": "vjVnfmc0-6j9aTdISGhXgfBkl0o1I9IsNX8x62ovMRp3H7dDfVC9ItOwaCjNxdedmk2V7mcbYDmGVg",
        "name": "BL Héraclèss"
    },
    {
        "id": "4FfHlR8IFEMUkRo2-FmgzcWVOoA3bYY5mFIszeVDuccwk3cVmWsiW8g38Q",      
        "accountId": "DyX4EmQYUxx1OJBpmZamWgEKXDELSrjaGhnXAMhU0qVuCBR9rhTwsHeA", 
        "puuid": "yflSAx6zN9xTJ-4t_EOHzuNIxg1r2JYSer8f12eCHcZRyET8X9f8wNwYu0xdg-0Zdut2Fa1iWTJRDA",
        "name": "BL ZNK"
    }
]

print("INIT")
init_supabase_soloQ(players)
while(1):
    print("New Scan")
    for i in range(0,len(players)):
        history = Riot_Get_Last_Ranked(players[i]['puuid'])
        #print(history)
        if(int(history[0].split('_')[1]) != int(players[i]["last_game"])):
            game = Game(history[0].split('_')[1])
            if int(game.gameDuration) > 600:
                print('NEW game for '+players[i]["name"]+":"+history[0].split('_')[1])
                add_value_supabase_soloQ(game,players[i]['id'],players[i]['puuid'],players[i]['name'])
            players[i]['last_game']=history[0].split('_')[1]
    print("Scan Finished")
    time.sleep(300)
