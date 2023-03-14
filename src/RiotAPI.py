import requests ,os.path,json
from configparser import ConfigParser
parser = ConfigParser()

parser.read('config.ini')

PARAMS = {'api_key': str(parser.get('riot_api', 'api_key'))}

def check_in_database(Gameid,type):
    if type == 'timeline':
        return os.path.isfile("database/timeline_game/EUW1_"+str(Gameid)+".json")
    elif type == 'end':
        return os.path.isfile("database/end_game/EUW1_"+str(Gameid)+".json")

def import_in_database(Gameid,data,type):
    datadump = json.dumps(data, indent=4)
    if type == 'timeline':
        with open("database/timeline_game/EUW1_"+str(Gameid)+".json","w") as out:
            out.write(datadump)
    elif type == 'end':
        with open("database/end_game/EUW1_"+str(Gameid)+".json","w") as out:
            out.write(datadump)

def load_data_in_database(Gameid,type):
    if type == 'timeline':
        with open("database/timeline_game/EUW1_"+str(Gameid)+".json") as json_file:
            data = json.load(json_file)
            return data
    elif type == 'end':
        with open("database/end_game/EUW1_"+str(Gameid)+".json") as json_file:
            data = json.load(json_file)
            return data        
   

def Riot_Extract_Data_End_Game(Gameid):
    #Checking in database
    if check_in_database(Gameid=Gameid,type='end'):
        data = load_data_in_database(Gameid=Gameid,type='end')
        return data
    else:
        url = str(parser.get('riot_url', 'url_base_game'))+str(Gameid)
        r = requests.get(url = url, params = PARAMS)
        if r.status_code == 200:
            data = r.json()
            import_in_database(Gameid=Gameid,data=data,type='end')
            return data
        elif r.status_code == 403:
            raise Exception("Error request. Status code : "+str(r.status_code)+"\nPlease check the validity of you api key.")
        elif r.status_code == 404:
            raise Exception("Error request. Status code : "+str(r.status_code)+"\nPlease check the validity of the gameid.")
        else:
            raise Exception("Error request. Status code : "+str(r.status_code))

def Riot_Extract_Timeline_Game(Gameid):
    if check_in_database(Gameid=Gameid,type='timeline'):
        data = load_data_in_database(Gameid=Gameid,type='timeline')
        return data
    else:
        url = str(parser.get('riot_url', 'url_base_game'))+str(Gameid)+"/timeline"
        r = requests.get(url = url, params = PARAMS)
        if r.status_code == 200:
            data = r.json()
            import_in_database(Gameid=Gameid,data=data,type='timeline')
            return data
        elif r.status_code == 403:
            raise Exception("Error request. Status code : "+str(r.status_code)+"\nPlease check the validity of you api key.")
        elif r.status_code == 404:
            raise Exception("Error request. Status code : "+str(r.status_code)+"\nPlease check the validity of the gameid.")
        else:
            raise Exception("Error request. Status code : "+str(r.status_code))

def Riot_Get_UserId(username):
    #URL pour avoir les informations sur le pseudo
    url = str(parser.get('riot_url', 'url_summoner_id'))+str(username)
    response_pseudo = requests.get(url = url, params = PARAMS)
    #Parsing de la réponce
    query_pseudo = response_pseudo.json()
    return query_pseudo['puuid']

def Riot_Get_Username(id):
    #URL pour avoir les informations sur le pseudo
    url = str(parser.get('riot_url', 'url_id_summoner'))+str(id)
    response_summoner = requests.get(url = url, params = PARAMS)
    #Parsing de la réponce
    query_summoner = response_summoner.json()
    return query_summoner[0]['summonerName']

