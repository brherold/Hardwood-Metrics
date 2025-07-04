import sqlite3
import json
from collections import defaultdict

#Converts conference_number to conference_name
def get_conference_name(conference_number):
    if 1 <= conference_number <= 63:
        if conference_number == 1:
            return "I.1"
        elif 2 <= conference_number <= 3:
            return f"II.{conference_number - 1}"
        elif 4 <= conference_number <= 7:
            return f"III.{conference_number - 3}"
        elif 8 <= conference_number <= 15:
            return f"IV.{conference_number - 7}"
        elif 16 <= conference_number <= 31:
            return f"V.{conference_number - 15}"
        elif 32 <= conference_number <= 63:
            return f"VI.{conference_number - 31}"
    else:
        return "Invalid conference number"


def get_connection():
    conn = sqlite3.connect('instance/basketball.db', check_same_thread=False)
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()
    return conn, cursor

# 2. Define your functions
def clean_data(rows):
    cleaned = []
    for row in rows:
        row_dict = dict(row)
        cleaned.append({
            key: (0 if value is None and key.upper() != 'DIST' else value)
            for key, value in row_dict.items()
        })
    return cleaned

def getRoster(team_id, season_id):
    conn, cursor = get_connection()
    with open('referenceQueries/Roster.sql', 'r') as file:
        sql_query = file.read()

    cursor.execute(sql_query, (team_id, season_id))
    rows = cursor.fetchall()
    conn.close()

    return clean_data(rows)

#Gets Avgs or Every team in given conference and year
def getConferenceAvg(conference_id,season_id):
    conn, cursor = get_connection()
    with open('referenceQueries/conferenceStats.sql', 'r') as file:
        sql_query = file.read()

    cursor.execute(sql_query, (conference_id, season_id,))
    rows = cursor.fetchall()

    conn.close()

    team_stats = clean_data(rows)
    #Apply for every team in conference
    for i, team_stat in enumerate(team_stats):
        if i == 0:
            most_wins = team_stat["GW"]
            team_stat["GB"] = "-"
        if i != 0:
            team_stat["GB"] = most_wins - team_stat["GW"] if team_stat["GW"] != most_wins else "-"
        # Adding % of Fg by Shot Type in dic
        
        team_stat["_2PAr"] = team_stat["_2P_A"] / team_stat["FG_A"] if team_stat["FG_A"] != 0 else 0
        team_stat["FAr"] = team_stat["F_A"] / team_stat["FG_A"] if team_stat["FG_A"] != 0 else 0
        team_stat["ISAr"] = team_stat["IS_A"] / team_stat["FG_A"] if team_stat["FG_A"] != 0 else 0
        team_stat["MRAr"] = team_stat["MR_A"] / team_stat["FG_A"] if team_stat["FG_A"] != 0 else 0
    
    
    return team_stats

#Gets Avgs of Every Opponent team in given conference and year
def getConferenceOppAvg(conference_id,season_id):
    conn, cursor = get_connection()
    with open('referenceQueries/conferenceOppStats.sql', 'r') as file:
        sql_query = file.read()

    cursor.execute(sql_query, (conference_id, season_id,))
    rows = cursor.fetchall()

    conn.close()

    team_stats = clean_data(rows)
    #Apply for every team in conference
    for team_stat in team_stats:
        # Adding % of Fg by Shot Type in dic
        
        team_stat["_2PAr"] = team_stat["_2P_A"] / team_stat["FG_A"] if team_stat["FG_A"] != 0 else 0
        team_stat["FAr"] = team_stat["F_A"] / team_stat["FG_A"] if team_stat["FG_A"] != 0 else 0
        team_stat["ISAr"] = team_stat["IS_A"] / team_stat["FG_A"] if team_stat["FG_A"] != 0 else 0
        team_stat["MRAr"] = team_stat["MR_A"] / team_stat["FG_A"] if team_stat["FG_A"] != 0 else 0
    
    
    return team_stats



def getTeamAvg(team_id, season_id, game_type):
    conn, cursor = get_connection()
    with open('referenceQueries/teamAvg.sql', 'r') as file:
        sql_query = file.read()

    cursor.execute(sql_query, (team_id, season_id, game_type))
    rows = cursor.fetchall()

    


    conn.close()

    team_stat = clean_data(rows)[0]
    # Adding % of Fg by Shot Type in dic
    
    team_stat["_2PAr"] = team_stat["_2P_A"] / team_stat["FG_A"] if team_stat["FG_A"] != 0 else 0
    team_stat["FAr"] = team_stat["F_A"] / team_stat["FG_A"] if team_stat["FG_A"] != 0 else 0
    team_stat["ISAr"] = team_stat["IS_A"] / team_stat["FG_A"] if team_stat["FG_A"] != 0 else 0
    team_stat["MRAr"] = team_stat["MR_A"] / team_stat["FG_A"] if team_stat["FG_A"] != 0 else 0

    #Conference ID -> Conference Name (1 _> I.1)
    team_stat["conference_name"] = get_conference_name(team_stat["conference_id"])

        
    

    #return clean_data(rows)[0]
    return team_stat
'''
print()
player_stats = getTeamAvg(533, 2045, "Conference")
print(player_stats)
'''

def getOppAvg(team_id, season_id, game_type):
    conn, cursor = get_connection()
    with open('referenceQueries/teamOppAvg.sql', 'r') as file:
        sql_query = file.read()

    cursor.execute(sql_query, (team_id, season_id, game_type))
    rows = cursor.fetchall()
    conn.close()

    team_stat = clean_data(rows)[0]
    # Adding % of Fg by Shot Type in dic
    
    team_stat["_2PAr"] = team_stat["_2P_A"] / team_stat["FG_A"] if team_stat["FG_A"] != 0 else 0
    team_stat["FAr"] = team_stat["F_A"] / team_stat["FG_A"] if team_stat["FG_A"] != 0 else 0
    team_stat["ISAr"] = team_stat["IS_A"] / team_stat["FG_A"] if team_stat["FG_A"] != 0 else 0
    team_stat["MRAr"] = team_stat["MR_A"] / team_stat["FG_A"] if team_stat["FG_A"] != 0 else 0

    #return clean_data(rows)[0]
    return team_stat

#Gets game info (teams, Date, etc)
def gameInfo(game_id):
    conn, cursor = get_connection()
    with open('referenceQueries/gameInfo.sql', 'r') as file:
        sql_query = file.read()

    cursor.execute(sql_query, (game_id,))
    rows = cursor.fetchall()
    conn.close()

    return clean_data(rows)[0]

#print(gameInfo(1058757))

def getTeamGameLogs(team_id, season_id):
    conn, cursor = get_connection()
    with open('referenceQueries/teamGameLogs.sql', 'r') as file:
        sql_query = file.read()

    cursor.execute(sql_query, (team_id, season_id))
    rows = cursor.fetchall()
    conn.close()

    return clean_data(rows)

def getTeamPlayerAvg(team_id, game_type, season_id):
    conn, cursor = get_connection()
    with open('referenceQueries/teamPlayerAvg.sql', 'r') as file:
        sql_query = file.read()

    cursor.execute(sql_query, (team_id, game_type, season_id))
    rows = cursor.fetchall()
    conn.close()

    
    
    rows = clean_data(rows)

    # Adding % of Fg by Shot Type in dic
    for player in rows:
        player["_2PAr"] = player["_2P_A"] / player["FG_A"] if player["FG_A"] != 0 else 0
        player["FAr"] = player["F_A"] / player["FG_A"] if player["FG_A"] != 0 else 0
        player["ISAr"] = player["IS_A"] / player["FG_A"] if player["FG_A"] != 0 else 0
        player["MRAr"] = player["MR_A"] / player["FG_A"] if player["FG_A"] != 0 else 0
        
        player["O_2PAr"] = player["O_2P_A"] / player["O_FG_A"] if player["O_FG_A"] != 0 else 0 
        player["O_FAr"] = player["O_F_A"] / player["O_FG_A"] if player["O_FG_A"] != 0 else 0 
        player["O_ISAr"] = player["O_IS_A"] / player["O_FG_A"] if player["O_FG_A"] != 0 else 0 
        player["O_MRAr"] = player["O_MR_A"] / player["O_FG_A"] if player["O_FG_A"] != 0 else 0 
        player["O_3PAr"] = player["O_3P_A"] / player["O_FG_A"] if player["O_FG_A"] != 0 else 0

        if player["Poss"] == 0:
            player["Poss"] = 1

    return clean_data(rows)

def getTeamOffense(team_id,season_id,game_type):
    conn, cursor = get_connection()

    #Searches for all College games (non exhibition or invitational) in tuple
    if game_type == "College":
        with open('referenceQueries/teamOffenseStatsConf.sql', 'r') as file:
            sql_query = file.read()
        
        cursor.execute(sql_query, (team_id, season_id, team_id, season_id))

    else:
        with open('referenceQueries/teamOffenseStats.sql', 'r') as file:
            sql_query = file.read()

        cursor.execute(sql_query, (team_id, season_id, game_type, team_id, season_id, game_type))

    rows = cursor.fetchall()
    conn.close()
    
    rows = clean_data(rows)

    #Renaming Defense Types
    for def_type in rows:
        if def_type["defense_type"] == "half":
            def_type["defense_type"] = "half-court"
        elif def_type["defense_type"] == "m_ext":
            def_type["defense_type"] = "man-to-man extended"
        elif def_type["defense_type"] == "m_pck":
            def_type["defense_type"] = "man-to-man packed"        
        elif def_type["defense_type"] == "man":
            def_type["defense_type"] = "man-to-man"
        elif def_type["defense_type"] == "z_ext":
            def_type["defense_type"] = "zone extended"
        elif def_type["defense_type"] == "z_pck":
            def_type["defense_type"] = "zone packed"    

        #Get Rate Stats    
        def_type["_2PAr"] = def_type["_2P_A"] / def_type["FG_A"] if def_type["FG_A"] != 0 else 0
        def_type["FAr"] = def_type["F_A"] / def_type["FG_A"] if def_type["FG_A"] != 0 else 0
        def_type["ISAr"] = def_type["IS_A"] / def_type["FG_A"] if def_type["FG_A"] != 0 else 0
        def_type["MRAr"] = def_type["MR_A"] / def_type["FG_A"] if def_type["FG_A"] != 0 else 0
        def_type["_3PAr"] = def_type["_3P_A"] / def_type["FG_A"] if def_type["FG_A"] != 0 else 0



    return clean_data(rows)

#print(getTeamOffense(533,2045, "College"))

def getTeamDefense(team_id,season_id,game_type):
    conn, cursor = get_connection()

    #Searches for all College games (non exhibition or invitational) in tuple
    if game_type == "College":
        with open('referenceQueries/teamDefenseStatsConf.sql', 'r') as file:
            sql_query = file.read()
        
        cursor.execute(sql_query, (team_id, season_id, team_id, season_id))

    else:
        with open('referenceQueries/teamDefenseStats.sql', 'r') as file:
            sql_query = file.read()

        cursor.execute(sql_query, (team_id, season_id, game_type, team_id, season_id, game_type))

    rows = cursor.fetchall()
    
    conn.close()
    rows = clean_data(rows)



    

    #Renaming Defense Types
    for def_type in rows:
        if def_type["defense_type"] == "half":
            def_type["defense_type"] = "half-court"
        elif def_type["defense_type"] == "m_ext":
            def_type["defense_type"] = "man-to-man extended"
        elif def_type["defense_type"] == "m_pck":
            def_type["defense_type"] = "man-to-man packed"        
        elif def_type["defense_type"] == "man":
            def_type["defense_type"] = "man-to-man"
        elif def_type["defense_type"] == "z_ext":
            def_type["defense_type"] = "zone extended"
        elif def_type["defense_type"] == "z_pck":
            def_type["defense_type"] = "zone packed"
     
        def_type["_2PAr"] = def_type["_2P_A"] / def_type["FG_A"] if def_type["FG_A"] != 0 else 0
        def_type["FAr"] = def_type["F_A"] / def_type["FG_A"] if def_type["FG_A"] != 0 else 0
        def_type["ISAr"] = def_type["IS_A"] / def_type["FG_A"] if def_type["FG_A"] != 0 else 0
        def_type["MRAr"] = def_type["MR_A"] / def_type["FG_A"] if def_type["FG_A"] != 0 else 0
        def_type["_3PAr"] = def_type["_3P_A"] / def_type["FG_A"] if def_type["FG_A"] != 0 else 0

    return clean_data(rows)

#print(getTeamDefense(533,2045, "College"))

def getTeamRank(team_id, season_id,game_type):
    conn, cursor = get_connection()

    if game_type in ("College", "Tournament"):
        with open('referenceQueries/teamDivStatRanked.sql', 'r') as file:
            sql_query = file.read()
    else:
        with open('referenceQueries/teamConfStatRanked.sql', 'r') as file:
            sql_query = file.read()

    cursor.execute(sql_query, (team_id, season_id,game_type,team_id))
    rows = cursor.fetchall()
    conn.close()

    return clean_data(rows)[0]

#print(getTeamRank(533,2045, "College"))

def getOppRank(team_id, season_id,game_type):
    conn, cursor = get_connection()

    if game_type in ("College", "Tournament"):
        with open('referenceQueries/oppDivStatRanked.sql', 'r') as file:
            sql_query = file.read()
    else:
        with open('referenceQueries/oppConfStatRanked.sql', 'r') as file:
            sql_query = file.read()

    cursor.execute(sql_query, (team_id, season_id,game_type,team_id))
    rows = cursor.fetchall()
    conn.close()

    return clean_data(rows)[0]


#print(getOppRank(533,2045, "College"))

def getTeamGameLog(team_id, season_id):
    conn, cursor = get_connection()

    with open('referenceQueries/teamGameLog.sql', 'r') as file:
        sql_query = file.read()


    cursor.execute(sql_query, (team_id, season_id))
    rows = cursor.fetchall()

    rows = clean_data(rows)

    # Add Game 
    for game_number, game in enumerate(rows):
        game["G_Num"] = game_number + 1 #stars at 1
        
        #Convert game date to string
        game_date = str(game["game_date"])
        formatted_date = f"{game_date[:4]}-{game_date[4:6]}-{game_date[6:]}"
        game["game_date"] = formatted_date

    conn.close()


    return clean_data(rows)

#print(getTeamGameLog(533,2045))

#Gets the Box Score stats of all players from a game
def gamePlayerStats(away_team_id, game_id):
    conn, cursor = get_connection()

    with open('referenceQueries/gamePlayerStats.sql', 'r') as file:
        sql_query = file.read()


    cursor.execute(sql_query, (game_id,))
    rows = cursor.fetchall()

    rows = clean_data(rows)

    awayTeam = []
    homeTeam = []

    if not rows:
        return awayTeam, homeTeam

    '''
    # Identify the away team name from the first player's team
    first_team = rows[0]["team_name"]

    for player in rows:
        team = player["team_name"]

        if team == first_team:
            awayTeam.append(player)
        else:
            homeTeam.append(player)
    '''
    for player in rows:
        team_id = player["team_id"]
        if team_id == away_team_id:
            awayTeam.append(player)
        else:
            homeTeam.append(player)

    conn.close()

    return awayTeam, homeTeam

#print(gamePlayerStats(1058757)[1][0])

#Gets the Box Score stats of all teams from a game
def gameTeamStats(away_team_id, game_id):
    conn, cursor = get_connection()

    with open('referenceQueries/gameTeamStats.sql', 'r') as file:
        sql_query = file.read()


    cursor.execute(sql_query, (game_id,))
    rows = cursor.fetchall()

    rows = clean_data(rows)

    for team_stats in rows:
        if team_stats["team_id"] == away_team_id:
            awayTeam = team_stats
        else:
            homeTeam = team_stats


    conn.close()

    return awayTeam, homeTeam
#print(gameTeamStats(1058757))

#Get Defense Stats from specific game and Team
def gameTeamDefense(team_id,game_id):
    conn, cursor = get_connection()


    with open('referenceQueries/gameTeamDefense.sql', 'r') as file:
        sql_query = file.read()

    cursor.execute(sql_query, (team_id, game_id, team_id, game_id,))

    rows = cursor.fetchall()
    
    conn.close()
    rows = clean_data(rows)


    #Renaming Defense Types
    for def_type in rows:
        if def_type["defense_type"] == "half":
            def_type["defense_type"] = "half-court"
        elif def_type["defense_type"] == "m_ext":
            def_type["defense_type"] = "man-to-man extended"
        elif def_type["defense_type"] == "m_pck":
            def_type["defense_type"] = "man-to-man packed"        
        elif def_type["defense_type"] == "man":
            def_type["defense_type"] = "man-to-man"
        elif def_type["defense_type"] == "z_ext":
            def_type["defense_type"] = "zone extended"
        elif def_type["defense_type"] == "z_pck":
            def_type["defense_type"] = "zone packed"
     


    return clean_data(rows)

#print(gameTeamDefense(533,1058757))
'''
print()
player_stats = getTeamPlayerAvg(935, "Conference", 2044)
print(player_stats[-1])
'''
'''
# 3. (Optional) Example usage
if __name__ == "__main__":
    team_id = 533
    season_id = 2045
    game_type = "Conference"

    roster = getRoster(team_id, season_id)
    team_avg = getTeamAvg(team_id, season_id, game_type)
    opp_avg = getOppAvg(team_id, season_id, game_type)
    team_game_logs = getTeamGameLogs(team_id, season_id)
    team_player_avg = getTeamPlayerAvg(team_id, game_type, season_id)

    # Example: Print JSON formatted
    print(json.dumps(roster, indent=2))
    #print(json.dumps(team_avg, indent=2))
    #print(json.dumps(opp_avg, indent=2))
    #print(json.dumps(team_game_logs, indent=2))
    #print(json.dumps(team_player_avg, indent=2))
'''


