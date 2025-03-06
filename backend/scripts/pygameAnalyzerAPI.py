#updated with player defense and uses playerCode instead of playername (useful for same name players)


from bs4 import BeautifulSoup

import requests
import re
import os

def save_html_to_file(content, filename):
    with open(filename, 'w', encoding='utf-8') as file:
        file.write(content)

# Function to load HTML content from a local file
def load_html_from_file(filename):
    with open(filename, 'r', encoding='utf-8') as file:
        return file.read()






def gameAnalyzer(gameURL):

    cache_folder = "backend/GamesHTML"
    gameURLCode = gameURL.split("/")[-1]
    cache_filename = os.path.join(cache_folder, f"{gameURLCode}.html")

    
    
    
    try:
        # Try to load HTML content from the local cache
        page = load_html_from_file(cache_filename)
        
        
    except FileNotFoundError:
        # If not found, fetch the content from the URL
        page = requests.get(gameURL)

        # Save HTML content to the local cache
        save_html_to_file(page.text, cache_filename)
        page = page.text #to fit in with variable names for soup 
        


    soup = BeautifulSoup(page,"html")

    infoList = soup.find_all("td",class_="left")



    #'''
    gameData = {
    "awayTeam":{
        "name": infoList[1].text.replace("\xa0"," "),
        "teamCode":(infoList[1].find("a").get("href")).split("/")[2],
        "outcome": 0,
        "stats":{"Min": 0, "FG": [0,0], "3P": [0,0], "FT": [0,0], "PTS": 0, "Off": 0, "Reb": 0, "AST": 0, "STL": 0, "BLK": 0, "TO": 0, "PF": 0, "+/-": 0, "DIST": 0, "PITP": 0, "FBP": 0, "FD": 0, "Fat": "","Poss": 0,  "OPoss": 0,"OPTS": 0, "OFG": [0,0], "O3P": [0,0] },
        "players":[],
        "totalShots":{"Finishing": [0, 0], "Inside Shot": [0, 0], "Mid-Range": [0, 0], "3-Pointer": [0, 0]},
        "totalDefense": {"Finishing": [0, 0], "Inside Shot": [0, 0], "Mid-Range": [0, 0], "3-Pointer": [0, 0], "Turnovers": [0, 0]},
        "defense" : {"man-to-man": {"Finishing": [0, 0], "Inside Shot": [0, 0], "Mid-Range": [0, 0], "3-Pointer": [0, 0], "Turnovers": [0, 0]},
                    "man-to-man defense packed" : {"Finishing": [0, 0], "Inside Shot": [0, 0], "Mid-Range": [0, 0], "3-Pointer": [0, 0], "Turnovers": [0, 0]},
                    "man-to-man defense extended" : {"Finishing": [0, 0], "Inside Shot": [0, 0], "Mid-Range": [0, 0], "3-Pointer": [0, 0], "Turnovers": [0, 0]},    
        "zone":{"Finishing": [0, 0], "Inside Shot": [0, 0], "Mid-Range": [0, 0], "3-Pointer": [0, 0], "Turnovers": [0, 0]},
        "zone defense packed":{"Finishing": [0, 0], "Inside Shot": [0, 0], "Mid-Range": [0, 0], "3-Pointer": [0, 0], "Turnovers": [0, 0]},
        "zone defense extended":{"Finishing": [0, 0], "Inside Shot": [0, 0], "Mid-Range": [0, 0], "3-Pointer": [0, 0], "Turnovers": [0, 0]},
        "pressure":{"Finishing": [0, 0], "Inside Shot": [0, 0], "Mid-Range": [0, 0], "3-Pointer": [0, 0], "Turnovers": [0, 0]},
        "transition": {"Finishing": [0, 0], "Inside Shot": [0, 0], "Mid-Range": [0, 0], "3-Pointer": [0, 0], "Turnovers": [0, 0]},
        "half-court": {"Finishing": [0, 0], "Inside Shot": [0, 0], "Mid-Range": [0, 0], "3-Pointer": [0, 0], "Turnovers": [0, 0]}}
        
    }
    ,
    "homeTeam":{
        "name": infoList[2].text.replace("\xa0"," "),
        "teamCode":(infoList[2].find("a").get("href")).split("/")[2],
        "outcome": 0,
        "stats":{"Min": 0, "FG": [0,0], "3P": [0,0], "FT": [0,0], "PTS": 0, "Off": 0, "Reb": 0, "AST": 0, "STL": 0, "BLK": 0, "TO": 0, "PF": 0, "+/-": 0, "DIST": 0, "PITP": 0, "FBP": 0, "FD": 0, "Fat": "","Poss": 0,  "OPoss": 0, "OPTS": 0, "OFG": [0,0], "O3P": [0,0] },
        "players":[],
        "totalShots":{"Finishing": [0, 0], "Inside Shot": [0, 0], "Mid-Range": [0, 0], "3-Pointer": [0, 0]},
        "totalDefense": {"Finishing": [0, 0], "Inside Shot": [0, 0], "Mid-Range": [0, 0], "3-Pointer": [0, 0], "Turnovers": [0, 0]},
        "defense" : {"man-to-man": {"Finishing": [0, 0], "Inside Shot": [0, 0], "Mid-Range": [0, 0], "3-Pointer": [0, 0], "Turnovers": [0, 0]},
                    "man-to-man defense packed" : {"Finishing": [0, 0], "Inside Shot": [0, 0], "Mid-Range": [0, 0], "3-Pointer": [0, 0], "Turnovers": [0, 0]},
                    "man-to-man defense extended" : {"Finishing": [0, 0], "Inside Shot": [0, 0], "Mid-Range": [0, 0], "3-Pointer": [0, 0], "Turnovers": [0, 0]},    
        "zone":{"Finishing": [0, 0], "Inside Shot": [0, 0], "Mid-Range": [0, 0], "3-Pointer": [0, 0], "Turnovers": [0, 0]},
        "zone defense packed":{"Finishing": [0, 0], "Inside Shot": [0, 0], "Mid-Range": [0, 0], "3-Pointer": [0, 0], "Turnovers": [0, 0]},
        "zone defense extended":{"Finishing": [0, 0], "Inside Shot": [0, 0], "Mid-Range": [0, 0], "3-Pointer": [0, 0], "Turnovers": [0, 0]},
        "pressure":{"Finishing": [0, 0], "Inside Shot": [0, 0], "Mid-Range": [0, 0], "3-Pointer": [0, 0], "Turnovers": [0, 0]},
        "transition": {"Finishing": [0, 0], "Inside Shot": [0, 0], "Mid-Range": [0, 0], "3-Pointer": [0, 0], "Turnovers": [0, 0]},
        "half-court": {"Finishing": [0, 0], "Inside Shot": [0, 0], "Mid-Range": [0, 0], "3-Pointer": [0, 0], "Turnovers": [0, 0]}}
        
    }
    }




    curTeam = "awayTeam"
    infoListPlayers = infoList[4:]  # cuts it to the first player in BoxScore
    #print(infoList)
    for i in range(len(infoListPlayers)):
        #print(infoListPlayers[i])
        if len(infoListPlayers[i].text.split("\xa0")) > 1:
            #name, position = infoListPlayers[i].text.split("\xa0")[1:]
            name = " ".join(infoListPlayers[i].text.split("\xa0")[0:-1])
            playerCode = infoListPlayers[i].find("a").get("href").split("/")[2]
            position = infoListPlayers[i].text.split("\xa0")[1:][-1]
            # Append a new player dictionary if the player index exceeds the current list length
            if len(gameData[curTeam]["players"]) <= i:
                gameData[curTeam]["players"].append({
                    "name": name, "position": position.upper(),
                    "playerCode": playerCode,
                    "shots": {"Finishing": [0, 0], "Inside Shot": [0, 0], "Mid-Range": [0, 0], "3-Pointer": [0, 0]},
                    "defense": {"Finishing": [0, 0], "Inside Shot": [0, 0], "Mid-Range": [0, 0], "3-Pointer": [0, 0]}, 
                    "driving": [0, 0], 
                    "stats":{"Min": 0, "FG": [0,0], "3P": [0,0], "FT": [0,0], "PTS": 0, "Off": 0, "Reb": 0, "AST": 0, "STL": 0, "BLK": 0, "TO": 0, "PF": 0, "+/-": 0, "DIST": 0, "PITP": 0, "FBP": 0, "FD": 0, "Fat": "", "Poss": 0, "OPoss": 0, "OPTS": 0, "OFG": [0,0], "O3P": [0,0] }})
            else:
                # Update existing player information
                gameData[curTeam]["players"][i]["name"] = name
                gameData[curTeam]["players"][i]["playerCode"] = playerCode
                gameData[curTeam]["players"][i]["position"] = position.upper()
                gameData[curTeam]["players"][i]["shots"] = {"Finishing": [0, 0], "Inside Shot": [0, 0], "Mid-Range": [0, 0], "3-Pointer": [0, 0]}
                gameData[curTeam]["players"][i]["defense"] = {"Finishing": [0, 0], "Inside Shot": [0, 0], "Mid-Range": [0, 0], "3-Pointer": [0, 0]}
                gameData[curTeam]["players"][i]["driving"] = [0, 0]
                gameData[curTeam]["players"][i]["stats"] = {"Min": 0, "FG": [0,0], "3P": [0,0], "FT": [0,0], "PTS": 0, "Off": 0, "Reb": 0, "AST": 0, "STL": 0, "BLK": 0, "TO": 0, "PF": 0, "+/-": 0, "DIST": 0, "PITP": 0, "FBP": 0, "FD": 0, "Fat": "", "Poss": 0,"OPoss": 0, "OPTS": 0, "OFG": [0,0], "O3P": [0,0] }

            # Switch the team if the next player is "Total" and the current team is "homeTeam"
            if infoListPlayers[i + 1].text == "Total" and curTeam == "awayTeam":
                curTeam = "homeTeam"

    #Adds player box score stats 
    statsInfoArr = soup.find_all("table",class_="box-score")[-1].find_all("tr")[3:]


    awayPlayerCount = 0
    for index, line in enumerate(statsInfoArr):
        if any(char.isalpha() for char in line.text):
            if statsInfoArr[index + 1].text and not statsInfoArr[index + 1].text[0].isdigit():
                break
            awayPlayerCount += 1

    playerTeamLines = []
    teamLines = []

    for i in statsInfoArr:
        if i.text and i.text[0].isdigit() or "Total" in i.text:
            playerTeamLines.append(i)

    curTeam = "awayTeam"


    for index , string in enumerate(playerTeamLines):
        statList = string.find_all("td")[3:]
        #If minutes of the line < 200 -> then thats a playerLine else thats a teamLine
        minCheck = int(statList[0].text)

        if minCheck < 200:
            
            playerID = string.find("a").get("href").split("/")[-1]
            for player in gameData[curTeam]["players"]:
                if player["playerCode"] == playerID:
                    player["stats"]["Min"] = int(statList[0].text)
                    player["stats"]["FG"][0] = int(statList[1].text.split("-")[0])
                    player["stats"]["FG"][1] = int(statList[1].text.split("-")[1])
                    player["stats"]["3P"][0] = int(statList[2].text.split("-")[0])
                    player["stats"]["3P"][1] = int(statList[2].text.split("-")[1])
                    player["stats"]["FT"][0] = int(statList[3].text.split("-")[0])
                    player["stats"]["FT"][1] = int(statList[3].text.split("-")[1])
                    player["stats"]["PTS"] = int(statList[4].text)
                    player["stats"]["Off"] = int(statList[5].text)
                    player["stats"]["Reb"] = int(statList[6].text)
                    player["stats"]["AST"] = int(statList[7].text)
                    player["stats"]["STL"] = int(statList[8].text)
                    player["stats"]["BLK"] = int(statList[9].text)
                    player["stats"]["TO"] = int(statList[10].text)
                    player["stats"]["PF"] = int(statList[11].text)
                    player["stats"]["+/-"] = int(statList[12].text)                         
                    try:
                        player["stats"]["DIST"] = float(statList[13].text)
                    except:
                        player["stats"]["DIST"] = "-" #NULL                                       
                    player["stats"]["PITP"] = int(statList[14].text)
                    player["stats"]["FBP"] = int(statList[15].text)
                    player["stats"]["FD"] = int(statList[16].text)
                    player["stats"]["Fat"] = statList[17].text
                    
                    
        else:
            
            team = gameData[curTeam]
            
            team["stats"]["Min"] = int(statList[0].text)
            team["stats"]["FG"][0] = int(statList[1].text.split("-")[0])
            team["stats"]["FG"][1] = int(statList[1].text.split("-")[1])
            team["stats"]["3P"][0] = int(statList[2].text.split("-")[0])
            team["stats"]["3P"][1] = int(statList[2].text.split("-")[1])
            team["stats"]["FT"][0] = int(statList[3].text.split("-")[0])
            team["stats"]["FT"][1] = int(statList[3].text.split("-")[1])
            team["stats"]["PTS"] = int(statList[4].text)
            team["stats"]["Off"] = int(statList[5].text)
            team["stats"]["Reb"] = int(statList[6].text)
            team["stats"]["AST"] = int(statList[7].text)
            team["stats"]["STL"] = int(statList[8].text)
            team["stats"]["BLK"] = int(statList[9].text)
            team["stats"]["TO"] = int(statList[10].text)
            team["stats"]["PF"] = int(statList[11].text)
            team["stats"]["+/-"] = int(statList[12].text)                         
            try:
                team["stats"]["DIST"] = float(statList[13].text)
            except:
                team["stats"]["DIST"] = "-" #NULL    
                                                    
            team["stats"]["PITP"] = int(statList[14].text)
            team["stats"]["FBP"] = int(statList[15].text)
            team["stats"]["FD"] = int(statList[16].text)
            team["stats"]["Fat"] = statList[17].text
        if index  + 1 > awayPlayerCount:
            curTeam = "homeTeam"
    
    
    
    #For getting box score logs
    playbyText = soup.find_all("div",id="Boxscore")[1].text
    gameArr = playbyText.split("\n")
    tipOff = gameArr[10]

    #Finds names of team to fit with gamelog names
    x = soup.find_all("div",id="Boxscore")[1].get_text(separator="\n")
                                                    
    split_content = re.split(r'\n|:', x)


    away_team_name = split_content[8]
    home_team_name = split_content[12]

    gameData["awayTeam"]["name"] = away_team_name
    gameData["homeTeam"]["name"] = home_team_name

    #Lines up the events of gameEventsArr and teamEventArr
    gameEventsArr = gameArr[10:] # play-by-play Events
    for i in gameEventsArr:
        if i == "":
            gameEventsArr.remove(i)

    #Delete "Game Event","2nd Half","Overtime" and lines w/o ":" from gameEventsArr 
    gameEventsArr = [
    string for string in gameEventsArr
    if "Game Event" not in string
    and "2nd Half" not in string
    and "Overtime" not in string
    and ":" in string
]

    #Changes all Exclamations to Periods
    for i in range(len(gameEventsArr)):
        gameEventsArr[i] = gameEventsArr[i].replace("!",".")
    
    #Deletes time of play-by-play, Makes it easier to get the Offensive Team
    for i in range(len(gameEventsArr)):
        dash = "-"
        index = 0
        while(dash != gameEventsArr[i][index]):
            index += 1
        gameEventsArr[i] = gameEventsArr[i][index + 2:]

    
    # For splitting every shot attempt to a new line (including tip ins from missed shots)
    newGameEventsArr = []

    for i, event in enumerate(gameEventsArr):
        "Finds team in the event and replaces it with either 'homeTeam' or 'awayTeam'"
        "Standardizes finding the team "
        event_team = event.split(":")[0]
        if home_team_name == event_team:
            event = event.replace(home_team_name, "homeTeam")
        else:
            event = event.replace(away_team_name, "awayTeam")


        if ("misses" in event or "blocks" in event or "blocked" in event) and ("tips it in") in event:           
            words = event.split(":")
            team = words[0]
            sentence_event = event.split(". ")    
            newGameEventsArr.append("".join(sentence_event[0:-3])) #before tip on
            newGameEventsArr.append(team + ": " + "".join(sentence_event[-3:])) #from tip n on..
        else:
            newGameEventsArr.append(event)
    
    #Delete Game Events with Non-And One Fouls (second free throws occur) and Charging Fouls
    gameEventsArr = [string for string in newGameEventsArr if "second free throw" not in string or "blocking out" in string or  ("second free throw" in string and "shot goes in" in string)]
    gameEventsArr = [string for string in newGameEventsArr if "charged with the foul" not in string]

    #Holds shot types and turnover phrases
    shotTypes = {    
        "Inside Shot": ["shoots from the inside","shoots from the low post", "shoots in the paint", "shoots from inside the arc", "shoots from the block","tips it in","attempts to dunk it" , "lays it up", "goes for the dunk"],
        "Mid-Range": ["with a fadeaway jumper","shoots a jumper"],
        "3-Pointer": ["shoots from beyond the arc","shoots from well beyond the arc","shoots from the three point line", "shoots from deep" , "shoots from the corner","shoots from downtown"]
    }

    Finishing = {"attempts to dunk it" , "lays it up", "goes for the dunk"}

    Turnover = {"turns the ball over", "steals the pass"}
    
    fg_attempts = {"shot goes in", "Slam dunk", "tips it in", "shot misses", "blocks the shot", "blocked", "Air ball"}

    missed_attempts = {"shot misses", "blocks the shot", "blocked", "Air ball"} #missed shots

    made_attempts = {"shot goes in", "Slam dunk", "tips it"}

    turnover_phrases = {"steals the pass", "turns the ball over", "on the shot."}


    #From Script game logs to get full playerName and defender name
    
    #playerName:playerCode
    player_dic = {} #matches playerCode with playerName (use to match when going through shots to determine which player is which (for players with same last name))

    textArr = []
    for index in soup.find_all("script"):
        if "myFunction" in index.text:
            textArr.append(index.text)
      
    shotTextArr = []

    for text in textArr:
        splitted = text.split("\\")
        name = splitted[10].replace(">","<").split("<")[1]
        id_text = text.split(" ")[17][12:-2] #gets ID of team or player

        if len(id_text) > 5:
            playerCode = id_text
            player_dic[name] = playerCode
            #thats playerID
        if len(id_text) < 5:
            shotTextArr.append(text)

    shotTextArr[0].split("\\")

    shotArr = []
    curTeam = "awayTeam"
    away_shots = []
    home_shots = []
    total_team_shots = {"awayTeam": [], "homeTeam": []}

    for i in range(len(shotTextArr)):
        arr = shotTextArr[i].split("\\")
        for text in arr:
            if "shot clock" in text:

                shot_parsedArr = text.replace(":  ", " [").split(" [")
                offense_player = shot_parsedArr[1].split(" - ")[0] #gets offensive player for shot 
                defense_player = shot_parsedArr[1].split(" by ")[-1]
                total_team_shots[curTeam].append((offense_player,defense_player))

        curTeam = "homeTeam"

        #shotsTextArr = shotArr[::2]

    total_team_shots["awayTeam"] = total_team_shots["awayTeam"][::2]
    total_team_shots["homeTeam"] = total_team_shots["homeTeam"][::2]

    awayTeamEventCounter = -1 #starts at -1 so initial gets event gets incremented (align with gamelog shot events)
    homeTeamEventCounter = -1

    #Scrapes gamelog and matches it with total_team_shots
    #shot_attempt 0 -> missed 1 -> made
    for i, event in enumerate(gameEventsArr):
        team = event.split(":")[0]
        #Find team 
        if team == "homeTeam":
            team = "homeTeam"
            oppTeam = "awayTeam"  
        else:
            team = "awayTeam"
            oppTeam = "homeTeam"
        
        #Find type of defense being played
        try:
            defense = [defense for defense in gameData["awayTeam"]["defense"] if defense in event][-1]
        
        except IndexError:
            defense = "half-court"
        

        
        if any(phrase in event for phrase in fg_attempts):
            for shot_type, shots in shotTypes.items():

                for shot in shots:
                    shot_attempt = 0
                    if shot in event:

                        if ("Breakaway" in event or "Fast break opportunity" in event) and "slow it down" not in event:
                            defense = "transition"
                            if shot in Finishing:
                                shot_type = "Finishing"

                        #For Drives
                        if shot in Finishing and "drives" in event:
                            #Find who drove and whether that player shot it
                            split_event = event.split(". ")
                            drive_index = next(i for i, s in enumerate(split_event) if "drives" in s)
                            shot_index = next(i for i, s in enumerate(split_event) if shot in s)
                            if shot_index == drive_index + 1:
                                shot_type = "Finishing"

                        #finds player and accumlates the shot in gameData
                        if team == "awayTeam":
                            awayTeamEventCounter += 1
                            shot_event = total_team_shots["awayTeam"][awayTeamEventCounter]
                        else:
                            homeTeamEventCounter += 1
                            shot_event = total_team_shots["homeTeam"][homeTeamEventCounter]


                        #Finds the offensive and defensive playerCode
                        offense_playerCode = player_dic[shot_event[0]]
            
                        try:
                            defense_playerCode = player_dic[shot_event[1]]
                        except: 
                            defense_playerCode = None #if shot had no defenders (tip in)

                        #determines if player made or missed the shot  
                        if any(phrase in event for phrase in missed_attempts):  
                            shot_attempt = 0
                        elif any(phrase in event for phrase in made_attempts): 
                            shot_attempt = 1
                            #For Fast-breaks

                        #Adds the shot to teamData w/o finding player 
                        gameData[team]["totalShots"][shot_type][0] += shot_attempt
                        gameData[team]["totalShots"][shot_type][1] += 1

                        #Adds Defended Fg to team stat
                        gameData[oppTeam]["stats"]["OFG"][0] += shot_attempt
                        gameData[oppTeam]["stats"]["OFG"][1] += 1
                        if shot_type == "3-Pointer":
                            gameData[oppTeam]["stats"]["O3P"][0] += shot_attempt
                            gameData[oppTeam]["stats"]["O3P"][1] += 1
                            gameData[oppTeam]["stats"]["OPTS"] += shot_attempt * 3
                        else:
                            gameData[oppTeam]["stats"]["OPTS"] += shot_attempt * 2
                        

                        gameData[oppTeam]["totalDefense"][shot_type][0] += shot_attempt
                        gameData[oppTeam]["totalDefense"][shot_type][1] += 1
                        gameData[oppTeam]["totalDefense"]["Turnovers"][1] += 1 #Defense event counter [forced turnovers,defensive events occured]

                        #Adds type of defense event
                        gameData[oppTeam]["defense"][defense][shot_type][0] += shot_attempt
                        gameData[oppTeam]["defense"][defense][shot_type][1] += 1
                        gameData[oppTeam]["defense"][defense]["Turnovers"][1] += 1 #Defense event counter [forced turnovers,defensive events occured]
                        
                        
                        for player in gameData[team]["players"]:     
                            
                            if offense_playerCode == player["playerCode"]:
                                
                                player["shots"][shot_type][0] += shot_attempt
                                player["shots"][shot_type][1] += 1
                                
                        
                        for player in gameData[oppTeam]["players"]:
                            
                            if defense_playerCode and defense_playerCode == player["playerCode"]:
                                
                                player["defense"][shot_type][0] += shot_attempt
                                player["defense"][shot_type][1] += 1

                                #Adds Defended Fg to player stat
                                player["stats"]["OFG"][0] += shot_attempt
                                player["stats"]["OFG"][1] += 1
                                if shot_type == "3-Pointer":
                                    player["stats"]["O3P"][0] += shot_attempt
                                    player["stats"]["O3P"][1] += 1
                                    player["stats"]["OPTS"] += shot_attempt * 3
                                else:
                                    player["stats"]["OPTS"] += shot_attempt * 2


            
        else:
            if any(phrase in event for phrase in turnover_phrases):
                #Adds turnovers in totalDefense (not offensive fouls)
                gameData[oppTeam]["totalDefense"]["Turnovers"][0] += 1
                gameData[oppTeam]["totalDefense"]["Turnovers"][1] += 1 #Defense event counter [forced turnovers,defensive events occured]

                #Adds turnovers in defense (not offensive fouls)
                gameData[oppTeam]["defense"][defense]["Turnovers"][0] += 1
                gameData[oppTeam]["defense"][defense]["Turnovers"][1] += 1 #Defense event counter [forced turnovers,defensive events occured]


    #used for getting GAME CODE and GAME TYPE
    soup2 = soup 

    date = soup2.find("div",{"id": "Main"}).find_all("h3")[0]
    type_id = soup2.find("div",{"id": "Main"}).find_all("h3")[1]

    first_half_months = ["October","November","December"]

    date_split = date.text[7:].replace(",","").split(" ")

    month = date_split[0]
    year = int(date_split[-1])

    if month in first_half_months:
        season = year + 1
    else:
        season = year




    game_type_unparsed = type_id.text[15:].split(" ")[0]
    game_id_unparsed = type_id.text[15:].split(" ")[-2]

    game_type = game_type_unparsed.strip("[]")

    game_id = int(game_id_unparsed.strip("[]#"))

    gameData["seasonYear"] = season
    gameData["gameCode"] = game_id
    gameData["gameType"] = game_type

    if gameData["awayTeam"]["stats"]["PTS"] > gameData["homeTeam"]["stats"]["PTS"]:
        gameData["awayTeam"]["outcome"] = 1
    else:
        gameData["homeTeam"]["outcome"] = 1

    #Calculates # of possessions for each team
    gameData["awayTeam"]["stats"]["Poss"] = round(gameData["awayTeam"]["stats"]["FG"][1] + .44 * gameData["awayTeam"]["stats"]["FT"][1] - gameData["awayTeam"]["stats"]["Off"] + gameData["awayTeam"]["stats"]["TO"],1)
    gameData["homeTeam"]["stats"]["Poss"] = round(gameData["homeTeam"]["stats"]["FG"][1] + .44 * gameData["homeTeam"]["stats"]["FT"][1] - gameData["homeTeam"]["stats"]["Off"] + gameData["homeTeam"]["stats"]["TO"],1)
    gameData["awayTeam"]["stats"]["OPoss"] = gameData["homeTeam"]["stats"]["Poss"]
    gameData["homeTeam"]["stats"]["OPoss"] = gameData["awayTeam"]["stats"]["Poss"]

    for curTeam in ["awayTeam","homeTeam"]:
        for player in gameData[curTeam]["players"]:
            player["stats"]["Poss"] = round(gameData[curTeam]["stats"]["Poss"] * (player["stats"]["Min"]/(.2*gameData[curTeam]["stats"]["Min"])),1)
            player["stats"]["OPoss"] = round(gameData[curTeam]["stats"]["OPoss"] * (player["stats"]["Min"]/(.2*gameData[curTeam]["stats"]["Min"])),1)

    return gameData

#print(gameAnalyzer("http://onlinecollegebasketball.org/game/1033201"))

