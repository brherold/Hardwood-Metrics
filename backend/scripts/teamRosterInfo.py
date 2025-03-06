from bs4 import BeautifulSoup
import requests
from .pygetPlayerInfo import *

#run in terminal: python -m scripts.teamRosterInfo

#Outputs dictionary of team w/ team_name, team_id, players and their skills using the team's roster link
def team_roster_info(teamURL):
    
    teamID = int(teamURL.split("/")[-1])
    teamRosterURL = "http://onlinecollegebasketball.org/roster/" + str(teamID)

    teamRosterPage = requests.get(teamRosterURL)
    teamRosterSoup = BeautifulSoup(teamRosterPage.text,"html")

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
            "Height": convert_to_inches(player[1].text),
            "Weight": float(playerAthletics[1].split(":")[1].split(" ")[2]),
            "Wingspan": convert_to_inches(playerAthletics[2].split(":")[1][2:]),
            "Vertical": Vert_convert_to_inches(playerAthletics[3].split(":")[1][2:]),
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

#print(team_roster_info("http://onlinecollegebasketball.org/team/533"))

