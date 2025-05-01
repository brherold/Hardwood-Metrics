import sqlite3
import json

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


