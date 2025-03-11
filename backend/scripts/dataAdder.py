import requests
from bs4 import BeautifulSoup
#from .dbOperations import *
#from .helperFunctions import *
import os

    
#Caching Team Schedule (TeamsHTML) for Year
def save_html_to_file(content, filename):
    with open(filename, 'w', encoding='utf-8') as file:
        file.write(content)

# Function to load HTML content from a local file
def load_html_from_file(filename):
    with open(filename, 'r', encoding='utf-8') as file:
        return file.read()
    
def delete_file(filename):
    """Deletes the specified file if it exists."""
    if os.path.exists(filename):
        os.remove(filename)
        print(f"{filename} has been deleted.")
    else:
        print(f"{filename} does not exist.")


#run python -m backend.scripts.dataAdder | python -m scripts.dataAdder

def id_to_url(id):
    '''
    Converts either playerID or teamID into urls
    '''
    id = int(id)
    if id > 1020:
        return "http://onlinecollegebasketball.org/player/" + str(id)
    else:
        return "http://onlinecollegebasketball.org/team/" + str(id)
    
def team_games_played(team_id):
    #Finds all the games played in current season for inputted Team
    teamScheduleUrl = "http://onlinecollegebasketball.org/schedule/" + str(team_id)


    cache_folder = "backend/TeamsHTML"
    
    cache_filename = os.path.join(cache_folder, f"{team_id}-{2044}.html")
    
    
    try:
        # Try to load HTML content from the local cache
        page = load_html_from_file(cache_filename)
        
        
    except FileNotFoundError:
        # If not found, fetch the content from the URL
        page = requests.get(teamScheduleUrl)

        # Save HTML content to the local cache
        save_html_to_file(page.text, cache_filename)
        page = page.text 


    soup = BeautifulSoup(page, "html.parser")


    scheduleSoup = BeautifulSoup(page,"html")

    columnList = scheduleSoup.find_all("tr")

    gameList = []
    for row in columnList:
        rowData = row.find_all("td")
        #Adds ALL games from the team's schedule (current Year)
        if len(rowData) == 8 :
            gameList.append("http://onlinecollegebasketball.org" + rowData[5].find("a").get("href"))
    return gameList


#API Endpoint
API_URL = "http://127.0.0.1:5000/"
team_post_API_URL = API_URL + "teams"
game_post_API_URL = API_URL + "games"


def addTeam(team_id):
    team_url = id_to_url(team_id)
    response = requests.post(team_post_API_URL,json={"team_url": id_to_url(team_id)})

    print(f"Adding team {team_id}: {response.status_code} - {response.json()}")

'''
team_id = 1
while(team_id < 1000):
    addTeam(team_id)
    team_id += 1
'''

def addGame(game_url):
    response = requests.post(game_post_API_URL,json={"game_url": game_url})

    print(f"Adding game {game_url}: {response.status_code} - {response.json()}")
    



def add_games_for_team(team_id):
    count = 0
    for game in team_games_played(team_id):
        try:       
            addGame(game)
            count += 1
        except:
            #if it hits NPY games then delete the html file from the GamesHTML folder and break 
            cache_folder = "backend/GamesHTML"
            gameURLCode = game.split("/")[-1]
            cache_filename = os.path.join(cache_folder, f"{gameURLCode}.html")
            delete_file(cache_filename)
            
            break #if it hits NPY games

    print(f"Added All {count} games for team: {team_id}")
    print()


#''' Adds All games for each Team (new games played since old ones are cached in GamesHTML)
team_id = 1
while(team_id < 3):
    add_games_for_team(team_id)
    team_id += 1
#'''
#add_games_for_team(2)


