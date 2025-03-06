from bs4 import BeautifulSoup
import requests
import hashlib
import os


#USE PYTHON ANACADONA 3.8.5 to RUN



def gameAnaylzer(gameUrl):
  #url= "http://onlinecollegebasketball.org/game/856168"


  page = requests.get(gameUrl)
  soup = BeautifulSoup(page.text,"html")

  date = soup.find("div",{"id": "Main"}).find_all("h3")[0]
  type_id = soup.find("div",{"id": "Main"}).find_all("h3")[1]

  first_half_months = ["October","November","December"]

  date_split = date.text[7:].replace(",","").split(" ")

  month = date_split[0]
  year = int(date_split[-1])

  if month in first_half_months:
      season = year + 1
  else:
      season = year




  game_type_unparsed = type_id.text[15:].split(" ")[0]

  game_type = game_type_unparsed.strip("[]")

  game_Code = gameUrl.split("/")[-1]


  infoList = soup.find_all("td",class_="left")
  infoList = soup.find_all("td",class_="left")

  gameData = {
    "gameCode" : game_Code,
    "seasonYear" : season,
    "gameType" : game_type,
  "awayTeam":{
    "name": infoList[1].text.replace("\xa0"," "),
    "teamCode": int((infoList[1].find("a").get("href")).split("/")[2]),
    "players":[],
    "totalShots":{"Finishing": [0, 0], "Inside Shot": [0, 0], "Mid-Range": [0, 0], "3-Pointer": [0, 0]},
    "totalDriving":[0,0],
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
    "teamCode": int((infoList[2].find("a").get("href")).split("/")[2]),
    "players":[],
    "totalShots":{"Finishing": [0, 0], "Inside Shot": [0, 0], "Mid-Range": [0, 0], "3-Pointer": [0, 0]},
    "totalDriving":[0,0],
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


  teamSwitch = 0 
  curTeam = "awayTeam"
  infoListPlayers = infoList[4:]  # cuts it to the first player in BoxScore
  

  

  for i in range(len(infoListPlayers)):
      
      '''
      if len(infoListPlayers[i].text.split("\xa0")) == 3 :
          playerCode = infoListPlayers[i].find("a").get("href").split("/")[2]
      '''
      try:
          infoListPlayers[i].find("a").get("href").split("/")[2]
          playerCode = int(infoListPlayers[i].find("a").get("href").split("/")[2])
          

          name = " ".join(infoListPlayers[i].text.split("\xa0")[0:2])
          position = infoListPlayers[i].text.split("\xa0")[1:][-1]

          

          
          # Append a new player dictionary if the player index exceeds the current list length
          if len(gameData[curTeam]["players"]) <= i:
              gameData[curTeam]["players"].append({
                "name": name, "playerCode": 
                playerCode,"position": position.upper(), 
                "shots": {"Finishing": [0, 0], "Inside Shot": [0, 0], "Mid-Range": [0, 0], "3-Pointer": [0, 0]}, 
                "driving": [0, 0],
                "stats":{"Min": 0, "FT": [0,0], "PTS": 0, "Reb": 0, "AST": 0, "STL": 0, "BLK": 0, "TO": 0, "PF": 0, "FD": 0 }})
                
          else:
              # Update existing player information
              gameData[curTeam]["players"][i]["name"] = name
              gameData[curTeam]["players"][i]["playerCode"] = playerCode
              gameData[curTeam]["players"][i]["position"] = position.upper()
              gameData[curTeam]["players"][i]["shots"] = {"Finishing": [0, 0], "Inside Shot": [0, 0], "Mid-Range": [0, 0], "3-Pointer": [0, 0]}
              gameData[curTeam]["players"][i]["driving"] = [0, 0]
              gameData[curTeam]["players"][i]["stats"] = {"Min": 0, "FT": [0,0], "PTS": 0, "Reb": 0, "AST": 0, "STL": 0, "BLK": 0, "TO": 0, "PF": 0, "FD": 0 }


          # Switch the team if the next player is "Total" and the current team is "homeTeam"
          if infoListPlayers[i + 1].text == "Total" and curTeam == "awayTeam":
              curTeam = "homeTeam"
      except AttributeError:
          continue
      
  ####################################
  statsInfoArr = soup.find_all("table",class_="box-score")[-1].find_all("tr")[3:]
  findHomeTeam = []
  playerLines = []

  awayPlayerCount = 0
  for index, line in enumerate(statsInfoArr):
      if any(char.isalpha() for char in line.text):
          if statsInfoArr[index + 1].text and not statsInfoArr[index + 1].text[0].isdigit():
              break
          awayPlayerCount += 1

  for i in statsInfoArr:
      if i.text and i.text[0].isdigit():
          playerLines.append(i)


  curTeam = "awayTeam"
  for playerIndex, playerString in enumerate(playerLines):
      playerStatList = playerString.find_all("td")
      playerName = " ".join(playerStatList[2].text.split("\xa0")[0:2])
      playerStatList = playerStatList[3:]
      #print(gameData[curTeam]["players"]["name"])
      for player in gameData[curTeam]["players"]:
          if player["name"] == playerName:
              
              player["stats"]["Min"] = int(playerStatList[0].text)
              player["stats"]["FT"][0] = int(playerStatList[3].text.split("-")[0])
              player["stats"]["FT"][1] = int(playerStatList[3].text.split("-")[1])
              player["stats"]["PTS"] = int(playerStatList[4].text)
              player["stats"]["Reb"] = int(playerStatList[6].text)
              player["stats"]["AST"] = int(playerStatList[7].text)
              player["stats"]["STL"] = int(playerStatList[8].text)
              player["stats"]["BLK"] = int(playerStatList[9].text)
              player["stats"]["TO"] = int(playerStatList[10].text)
              player["stats"]["PF"] = int(playerStatList[11].text)
              player["stats"]["FD"] = int(playerStatList[16].text)
              if playerIndex + 1 == awayPlayerCount:
                  curTeam = "homeTeam"
  ####################################

  




  playbyText = soup.find_all("div",id="Boxscore")[1].text
  gameArr = playbyText.split("\n")
  tipOff = gameArr[10]
  x = soup.find_all("div",id="Boxscore")[1]
  teamEventArr = x.find_all("b")[3:]  #shows time and Team for each play-by-play Event (lined up with gameStartArr)





  #Lines up the events of gameEventsArr and teamEventArr
  gameEventsArr = gameArr[10:] # play-by-play Events
  for i in gameEventsArr:
    if i == "":
      gameEventsArr.remove(i)
  #Changes all Exclamations to Periods
  for i in range(len(gameEventsArr)):
    gameEventsArr[i] = gameEventsArr[i].replace("!",".")
  gameEventsArr = gameEventsArr[:-1]
  #Delete "Game Event","2nd Half","Overtime" and lines w/o ":" from gameEventsArr 

  gameEventsArr = [
    string for string in gameEventsArr
    if "Game Event" not in string
    and "2nd Half" not in string
    and "Overtime" not in string
    and ":" in string
]
  #Deletes time of play-by-play, Makes it easier to get the Offensive Team


  for i in range(len(gameEventsArr)):
    dash = "-"
    index = 0
    while(dash != gameEventsArr[i][index]):
        index += 1
    gameEventsArr[i] = gameEventsArr[i][index + 2:]
  #Determines whether a drive is successful or not
  Driving = {
    "Fail":"drive ",
    "Success":"drives "
  }

  #Driving["Fail"] in event
  #Adds all the drivers
  drive_attempt = -1 #-1: No Drive, 0: Fail, 1: Success
  for event in gameEventsArr:
    if Driving["Fail"] in event or Driving["Success"] in event:
      drive_attempt = 0
      if Driving["Success"] in event:
        drive_attempt = 1
      words = event.split()
      team = words[0][:-1] #team of driver
      if drive_attempt == 0:
        drive_index = words.index("drive")
        player_index = drive_index - 3
      else:
        drive_index = words.index("drives")
        player_index = drive_index - 1
      player_name = words[player_index] #driver name
      

      
      if team in gameData["homeTeam"]["name"]:
        team = "homeTeam"
      else:
        team = "awayTeam"
      for player in gameData[team]["players"]:
        if player["name"] == player_name:
          player["driving"][0] += drive_attempt
          player["driving"][1] += 1
          gameData[team]["totalDriving"][0] += drive_attempt
          gameData[team]["totalDriving"][1] += 1


  #Delete Game Events with Non-And One Fouls (second free throws occur) and Charging Fouls
  gameEventsArr = [string for string in gameEventsArr if "second free throw" not in string or "blocking out" in string]
  gameEventsArr = [string for string in gameEventsArr if "charged with the foul" not in string]

  shotTypes = {    
      "Inside Shot": ["shoots from the inside","shoots from the low post", "shoots in the paint", "shoots from inside the arc", "shoots from the block","tips it in","attempts to dunk it" , "lays it up", "goes for the dunk"],
      "Mid-Range": ["with a fadeaway jumper","shoots a jumper"],
      "3-Pointer": ["shoots from beyond the arc","shoots from well beyond the arc","shoots from the three point line", "shoots from deep" , "shoots from the corner","shoots from downtown"]
  }

  Finishing = {"attempts to dunk it" , "lays it up", "goes for the dunk"}


  #Adds every FG into the gameData per Player
  for event in gameEventsArr:
    #Adds turnovers in defense (not offensive fouls)
    if "turns the ball over" in event or "steals the pass" in event:

      words = event.split()
      team = words[0][:-1]
      if team in gameData["homeTeam"]["name"]:
        team = "homeTeam"
        oppTeam = "awayTeam"  
      else:
        team = "awayTeam"
        oppTeam = "homeTeam"

      try:
        defense = [defense for defense in gameData["awayTeam"]["defense"] if defense in event][-1]
        
      except IndexError:
        #print(event)
        defense = "half-court"
      
      gameData[oppTeam]["defense"][defense]["Turnovers"][0] += 1 #increments turnovers
      gameData[oppTeam]["defense"][defense]["Turnovers"][1] += 1 #Defense event counter [forced turnovers,defensive events occured]
      
    #For searching shots
    for shot_type, shots in shotTypes.items():
      for shot in shots:
        shot_attempt = 0
        if shot in event:
          words = event.split()
          player_index = words.index(shot.split()[0]) - 1
          player_name = words[player_index]
          team = words[0][:-1]

          

          #Finds the type of defense (doesn't matter for gameData["team"])
          try:
            defense = [defense for defense in gameData["awayTeam"]["defense"] if defense in event][-1]
            
            

          except IndexError:
            defense = "half-court"
          
          

          if "Slam dunk" in event or "shot goes in" in event or "tips it in" == shot:
            shot_attempt = 1
          

          #For Fast-breaks

          if ("Breakaway" in event or "Fast break opportunity" in event) and "slow it down" not in event:
            defense = "transition"
            if shot in Finishing:
              shot_type = "Finishing"

          #For Drives
          if shot in Finishing and "drives" in event and words[words.index("drives") - 1] == player_name:
            shot_type = "Finishing"
          
          
              

          #finds player and accumlates the shot in gameData
          if team in gameData["homeTeam"]["name"]:
            team = "homeTeam"
            oppTeam = "awayTeam"
            
          else:
            team = "awayTeam"
            oppTeam = "homeTeam"
          
          
            
        
          for player in gameData[team]["players"]:
            
            
            
            if player_name in player["name"]:
              
              player["shots"][shot_type][0] += shot_attempt
              player["shots"][shot_type][1] += 1
              gameData[team]["totalShots"][shot_type][0] += shot_attempt
              gameData[team]["totalShots"][shot_type][1] += 1

              gameData[oppTeam]["defense"][defense][shot_type][0] += shot_attempt
              gameData[oppTeam]["defense"][defense][shot_type][1] += 1

              gameData[oppTeam]["defense"][defense]["Turnovers"][1] += 1 #Defense event counter [forced turnovers,defensive events occured]




  
  
  
  return gameData
   



#print(gameAnaylzer("http://onlinecollegebasketball.org/game/1027313"))
