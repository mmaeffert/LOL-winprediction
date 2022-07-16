import requests

#url = "https://europe.api.riotgames.com/lol/match/v5/matches/by-puuid/7GOiFyyzuAwHn7DGDQwbanldrc5CUCITRWXsUAzL-dWVHyB-dQEoR-qalVQmapZ2Vbhxt-Iewq0OGA/ids?start=0&count=20&api_key=RGAPI-856f15c8-b9a9-4aa7-b2f6-6c2c36bc830b"
url = "https://euw1.api.riotgames.com/lol/league/v4/entries/RANKED_SOLO_5x5/BRONZE/III?page=1&api_key=RGAPI-5499ada9-2fcd-411a-b544-98f034aad6e0"
header = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/103.0.5060.114 Safari/537.36', 'Accept-Language': 'de-DE,de;q=0.9,en-US;q=0.8,en;q=0.7', 'Accept-Charset': 'application/x-www-form-urlencoded; charset=UTF-8', 'Origin': 'https://developer.riotgames.com'}
print(requests.get(url, header))