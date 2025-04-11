from bs4 import BeautifulSoup
import requests
from .pygetPlayerInfo import *
#python -m backend.scripts.teamRosterInfo
from datetime import *
import os






def save_html_to_file(content, filename):
    with open(filename, 'w', encoding='utf-8') as file:
        file.write(content)

# Function to load HTML content from a local file
def load_html_from_file(filename):
    with open(filename, 'r', encoding='utf-8') as file:
        return file.read()

def delete_file(filename):
    if os.path.exists(filename):
        os.remove(filename)
    return 



#run in terminal: python -m scripts.teamRosterInfo

#Outputs dictionary of team w/ team_name, team_id, players and their skills using the team's roster link
def team_roster_info(teamURL,season):


    cache_folder = "backend/TeamRosterPage"


    teamID = int(teamURL.split("/")[-1])
    cache_filename = os.path.join(cache_folder, f"{teamID}-{season}.html")
    teamRosterURL = "http://onlinecollegebasketball.org/roster/" + str(teamID)

    


    try:
        # Try to load HTML content from the local cache
        page = load_html_from_file(cache_filename)
        
        
    except FileNotFoundError:
        # If not found, fetch the content from the URL
        page = requests.get(teamRosterURL)

        # Save HTML content to the local cache
        save_html_to_file(page.text, cache_filename)
        page = page.text #to fit in with variable names for soup 
        


    teamRosterSoup = BeautifulSoup(page,"html")


    #Finds Name of Team

    teamRosterSoup.find("h1")
    teamName = teamRosterSoup.find("h1").text.strip("Roster")[:-1]
    teamData = {"teamName": teamName, "teamID": teamID, "players":[]}


    playerRosterList = teamRosterSoup.find("table",id="players").find_all("tr")[1:]



    for index, playerSoup in enumerate(playerRosterList):
        '''
        teamData["players"].append({
            "name": player[0].find_all("td")[0]
        })
        '''
        player = playerSoup.find_all("td")[3:]

        playerAthletics = player[0].find("a").get("alt").split("\n")

        teamData["players"].append({
            "name": player[0].text[:-1],
            "playerID": int(playerSoup.find_all("td")[3].find("a").get("href")[8:]),
            "height": convert_to_inches(player[1].text),
            "weight": float(playerAthletics[1].split(":")[1].split(" ")[2]),
            "wingspan": convert_to_inches(playerAthletics[2].split(":")[1][2:]),
            "vertical": Vert_convert_to_inches(playerAthletics[3].split(":")[1][2:]),
            "Pos": player[16].text,
            "Class": player[20].text,
            "IS": int(player[2].text),
            "OS": int(player[3].text),
            "Rng": int(player[4].text),
            "Fin": int(player[5].text),
            "Reb": int(player[6].text),
            "IDef": int(player[7].text),
            "PDef": int(player[8].text),
            "IQ": int(player[9].text),
            "Pass": int(player[10].text),
            "Hnd": int(player[11].text),
            "Drv": int(player[12].text),
            "Str": int(player[13].text),
            "Spd": int(player[14].text),
            "Sta": int(player[15].text),
            "SI": int(player[17].text),
            "POT": int(player[18].text),
            "Stars": int(player[19].text) if player[19].text != "-" else 0
            
        })

        
    
    return teamData

#print(team_roster_info("http://onlinecollegebasketball.org/team/353",2045))


'''
folder_path = "backend/TeamRosterPage"  # Change this to your target folder

for filename in os.listdir(folder_path):
    old_path = os.path.join(folder_path, filename)

    if os.path.isfile(old_path):  # Ensure it's a file, not a folder
        name, ext = os.path.splitext(filename)
        new_filename = f"{name}-2044{ext}"
        new_path = os.path.join(folder_path, new_filename)
        
        os.rename(old_path, new_path)

print("Renaming complete.")
'''