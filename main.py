from pyparsing import line
import requests
import time
import sys


header_param = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/103.0.5060.114 Safari/537.36",
    "Accept-Language": "de-DE,de;q=0.9,en-US;q=0.8,en;q=0.7",
    "Accept-Charset": "application/x-www-form-urlencoded; charset=UTF-8",
    "Origin": "https://developer.riotgames.com",
}

league_scores = {
    "IRON": 0,
    "BRONZE": 4,
    "SILVER": 8,
    "GOLD": 12,
    "PLATINUM": 16,
    "DIAMOND": 20
}

division_scores = {
    "I": 3,
    "II": 2,
    "III": 1,
    "IV": 0,
}

errors = open("errors.log", "a")
data = open("data.csv", "a")
last_stand = open("last_stand.log", "w")

api_key = sys.argv[1]

division_string = ["I", "II", "III", "IV"]
league_string = ["IRON", "BRONZE", "SILVER", "GOLD", "PLATINUM", "DIAMOND"]
page = 1
current_instance = ""

if len(sys.argv) > 2:
    if sys.argv[2] != "":
        page = int(sys.argv[2])

if len(sys.argv) > 3:
    if sys.argv[3] != "":
        current_instance = str(sys.argv[3])

def fetch_api(my_query):
    #print(my_query)
    response = requests.get(my_query, header_param)
    #print(response)
    #print(response)
    while response.status_code == 429:
        print("waiting...")
        time.sleep(10)
        response = requests.get(my_query,header_param)
    if response.status_code != 200:
        print("Failed: " + my_query)
        errors = open("errors" + current_instance + ".log", "a")
        errors.write(my_query + "\n")
        errors.close()
        return ""
    response_json = response.json()
    #print(response_json)
    return response_json

# rank, champion, champion experience, .... , team1 or team2 won
def analyze_match(match):
    line_to_print = ""

    # Make sure match is not empty
    if "metadata" not in match:
        return

    # Make sure we only look at 5v5 summoners rift
    if match['info']['gameMode'] != 'CLASSIC':
        return 
    
    # Go through each participant in the game
    participants = match['info']['participants']
    for participant in participants:
        rank = fetch_api("https://euw1.api.riotgames.com/lol/league/v4/entries/by-summoner/" + participant['summonerId'] + "?api_key=" + api_key)
        rankscore = -1

        # Search the solo5v5 queue
        for queue in rank:
            if queue['queueType'] == "RANKED_SOLO_5x5":
                rankscore = league_scores[queue['tier']] + division_scores[queue['rank']]
        
        line_to_print = line_to_print + str(rankscore) + ';' + participant['championName'] + ';' + str(participant['champExperience']) + ';'
    
    line_to_print = line_to_print + str(participants[0]['win']) + "\n"
    print(line_to_print)
    data = open("data" + current_instance + ".csv", "a")
    data.write(line_to_print)
    data.close()


while True:
    print(page)
    # First I loop through each league
    for league in league_string:

        # Then through each division
        for division in division_string:
            print('Division: ' + division + "   league: " + league)

            # Then I fetch players in that division
            players = fetch_api("https://euw1.api.riotgames.com/lol/league/v4/entries/RANKED_SOLO_5x5/"+league+"/"+division+"?page=" + str(page) + "&api_key=" + api_key)
            if players == "":
                continue

            # And go through each player
            for player in players:
                puuid = fetch_api("https://euw1.api.riotgames.com/lol/summoner/v4/summoners/by-name/" + player['summonerName'] + "?api_key=" + api_key)

                # Check if puuid could be fetched
                if 'puuid' in puuid:
                    print('Summoner: ' + player['summonerName'] + '   puuid: ' + puuid['puuid'])

                    # get matches of this player
                    matches = fetch_api("https://europe.api.riotgames.com/lol/match/v5/matches/by-puuid/" + puuid['puuid'] + "/ids?start=0&count=20&api_key=" + api_key) # Gets the last 20 matches

                    #Go through each match
                    for match_id in matches:
                        #print("MatchID: " + str(match_id))
                        match = fetch_api("https://europe.api.riotgames.com/lol/match/v5/matches/" + match_id + "?api_key=" + api_key)

                        analyze_match(match)





    page = page + 1
    last_stand.write(str(page))




