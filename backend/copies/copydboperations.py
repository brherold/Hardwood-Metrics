from .pygetPlayerInfo import * #have to run like this in terminal: python -m scripts.pygetPlayerInfo
from models import *
from .getTeamInfo import * #have to run like this in terminal: python -m scripts.pygetPlayerInfo
#from .pygameAnaylzerAPI import *
from .updpygameAnaylzerAPI import *
current_season = find_current_season()
print(1)

'''
def season_id_finder(year):
    #Function to find season_id 
    return year - 2042
'''

def id_to_url(id):
    '''
    Converts either playerID or teamID into urls
    '''
    if id > 1020:
        return "http://onlinecollegebasketball.org/player/" + str(id)
    else:
        return "http://onlinecollegebasketball.org/team/" + str(id)

#Shortens names of the defense types
DEFENSE_NAME_MAPPING = {
    "man-to-man": "man",
    "man-to-man defense packed": "m_pck",
    "man-to-man defense extended": "m_ext",
    "zone": "zone",
    "zone defense packed": "z_pck",
    "zone defense extended": "z_ext",
    "pressure": "press",
    "transition": "trans",
    "half-court": "half",
}

# Step 2: Create a function to transform defense names
def transform_defense_names(defense_data):
    """
    Transforms defense names in the defense_data dictionary using the DEFENSE_NAME_MAPPING.
    """
    transformed_data = {}
    for defense_type, stats in defense_data.items():
        # Get the abbreviated name from the mapping
        abbreviated_name = DEFENSE_NAME_MAPPING.get(defense_type, defense_type)
        transformed_data[abbreviated_name] = stats
    return transformed_data

def add_to_player(player_id):
    '''
    Adds playerID to player Table
    '''
    player_url = id_to_url(player_id)

    player_data = get_player_info(player_url)  # Fetch player data using the URL
    #print(player_data)
    if player_data["Team_ID"] > 1010:
        #If player is not a current player (graduated or recruit)
        return None
    
    # Add into Player Table (DB)
    new_player = Player(
        player_id=player_data["Player_ID"],
        team_id=player_data["Team_ID"],
        name=player_data["Name"]
    )

    db.session.add(new_player)  # Add the new player to the session
    db.session.commit()  # Commit the transaction

    return new_player


def add_to_playerSkills(player_id):
    # Adds or updates playerID in PlayerSkills Table

    player_url = id_to_url(player_id)
    player_data = get_player_info(player_url)

    # Check if skills already exist for the player in the current season

    existing_player_skills = PlayerSkills.query.filter_by(player_id=player_id, season_id=current_season).first()

    if existing_player_skills:
        # Update existing player skills
        existing_player_skills.height = player_data["Height_inches"]
        existing_player_skills.weight = player_data["Weight"]
        existing_player_skills.wingspan = player_data["Wingspan_inches"]
        existing_player_skills.vertical = player_data["Vertical_float"]
        existing_player_skills.IS = player_data["IS"]
        existing_player_skills.IQ = player_data["IQ"]
        existing_player_skills.OS = player_data["OS"]
        existing_player_skills.Pass = player_data["Pass"]
        existing_player_skills.Rng = player_data["Rng"]
        existing_player_skills.Hnd = player_data["Hnd"]
        existing_player_skills.Fin = player_data["Fin"]
        existing_player_skills.Drv = player_data["Drv"]
        existing_player_skills.Reb = player_data["Reb"]
        existing_player_skills.Str = player_data["Str"]
        existing_player_skills.IDef = player_data["IDef"]
        existing_player_skills.Spd = player_data["Spd"]
        existing_player_skills.PDef = player_data["PDef"]
        existing_player_skills.Sta = player_data["Sta"]

        db.session.commit()  
        return existing_player_skills, "Player skills updated successfully"
    
    else:
        # If no existing skills, add new skills to the table
        new_player_skills = PlayerSkills(
            player_id=player_data["Player_ID"],
            season_id=player_data["Season_ID"],
            height=player_data["Height_inches"],
            weight=player_data["Weight"],
            wingspan=player_data["Wingspan_inches"],
            vertical=player_data["Vertical_float"],
            IS=player_data["IS"],
            IQ=player_data["IQ"],
            OS=player_data["OS"],
            Pass=player_data["Pass"],
            Rng=player_data["Rng"],
            Hnd=player_data["Hnd"],
            Fin=player_data["Fin"],
            Drv=player_data["Drv"],
            Reb=player_data["Reb"],
            Str=player_data["Str"],
            IDef=player_data["IDef"],
            Spd=player_data["Spd"],
            PDef=player_data["PDef"],
            Sta=player_data["Sta"]
        )

        db.session.add(new_player_skills)  # Add the new player skills to the session
        db.session.commit()  
        return new_player_skills, "Player skills added successfully"

def get_or_add_player(player_id):
    """ 
    NO UPDATING Data
    Checks if player is in Player Table 
    Checks to see if player in current season is in Player Skill table (using seasonID)
    """
    # Check if Player is in DB
    existing_player = Player.query.filter_by(player_id=player_id).first()

    if existing_player:
        #Checks if that player Skills is for the current Season
        

        existing_player_skill_season = PlayerSkills.query.filter_by(player_id=player_id, season_id=current_season).first()

        if not existing_player_skill_season:
            #If the player skills for current season is not in Player Skills Table, add their skills
            add_to_playerSkills(player_id)

        return existing_player


    new_player = add_to_player(player_id)
    add_to_playerSkills(player_id)

    return new_player  # Return the newly added player

def update_player_helper(player_id):
    '''
    Updates player skills (or adds them into db (player and playerskills Table)
    '''
    existing_player = Player.query.filter_by(player_id=player_id).first()

    if existing_player:
        #If player is in Player Table, then instantly update playerSkills for current season
        add_to_playerSkills(player_id)
        return existing_player

    new_player = add_to_player(player_id) #adds new player to Player Table
    add_to_playerSkills(player_id) #adds the new player's skills to PlayerSkills Table

    return new_player

def get_or_add_team(team_id):
    '''
    Check or add a team to the DB using the team_id
    '''
    existing_team = Team.query.filter_by(team_id=team_id).first()

    if existing_team:
        return existing_team
    
    # If the team does not exist, fetch their data
    team_url = id_to_url(team_id)
    teamID, teamName = get_team_info(team_url)

    new_team = Team(team_id = teamID, team_name = teamName)
    db.session.add(new_team)  # Add the new player to the session
    db.session.commit()  # Commit the transaction

    return new_team



def create_team_stats(game_id, team_id, team_shots, opponent_shots):
    """
    Helper function to create a TeamStats table.
    """
    return TeamStats(
        game_id=game_id,
        team_id=team_id,
        #season_id=season_id,
        F_M =team_shots["Finishing"][0],
        F_A =team_shots["Finishing"][1],
        IS_M =team_shots["Inside Shot"][0],
        IS_A =team_shots["Inside Shot"][1],
        MR_M =team_shots["Mid-Range"][0],
        MR_A =team_shots["Mid-Range"][1],
        _3P_M =team_shots["3-Pointer"][0],
        _3P_A =team_shots["3-Pointer"][1],

        opp_F_M = opponent_shots["Finishing"][0],
        opp_F_A = opponent_shots["Finishing"][1],
        opp_IS_M = opponent_shots["Inside Shot"][0],
        opp_IS_A = opponent_shots["Inside Shot"][1],
        opp_MR_M = opponent_shots["Mid-Range"][0],
        opp_MR_A = opponent_shots["Mid-Range"][1],
        opp__3P_M = opponent_shots["3-Pointer"][0],
        opp_3P_A = opponent_shots["3-Pointer"][1],
    )

def game_data_to_team_stats(game_data):
    """
    Takes in game_data from gameAnalyzer(game_id) and inputs stats into DB (TeamStats).
    """
    try:
        # Extract game data
        game_id = int(game_data["gameCode"])
        #season_id = game_data["seasonYear"] - 2042

        home_team_data = game_data["homeTeam"]
        away_team_data = game_data["awayTeam"]

        home_team_id = home_team_data["teamCode"]
        away_team_id = away_team_data["teamCode"]

        home_team_shots = home_team_data["totalShots"]
        away_team_shots = away_team_data["totalShots"]

        # Create TeamStats instances

        home_team_stats = create_team_stats(
            game_id,
            home_team_id,
            #season_id,
            home_team_shots,
            away_team_shots,
        )

        away_team_stats = create_team_stats(
            game_id,
            away_team_id,
            #season_id,
            away_team_shots,
            home_team_shots,
        )

        # Add to the database session
        db.session.add(home_team_stats)
        db.session.add(away_team_stats)
        db.session.commit()

    except KeyError as e:
        print(f"Missing key in game_data: {e}")
        db.session.rollback()  # Rollback the transaction in case of an error
    except Exception as e:
        print(f"An error occurred: {e}")
        db.session.rollback()  # Rollback the transaction in case of an error

def create_off_def_stats (game_id,team_id,def_type,defense):
    """
    Helper function to create a TeamStats table.
    [0] -> offenseStats
    [1] -> defenseStats
    """
    return (OffenseStats(
        game_id = game_id,
        team_id = team_id,
        defense_type = def_type,
        plays = defense["Turnovers"][1],
        F_M =defense["Finishing"][0],
        F_A =defense["Finishing"][1],
        IS_M =defense["Inside Shot"][0],
        IS_A =defense["Inside Shot"][1],
        MR_M =defense["Mid-Range"][0],
        MR_A =defense["Mid-Range"][1],
        _3P_M =defense["3-Pointer"][0],
        _3P_A =defense["3-Pointer"][1],
        TOV = defense["Turnovers"][0]
    ), DefenseStats(
        game_id = game_id,
        team_id = team_id,
        defense_type = def_type,
        plays = defense["Turnovers"][1],
        F_M =defense["Finishing"][0],
        F_A =defense["Finishing"][1],
        IS_M =defense["Inside Shot"][0],
        IS_A =defense["Inside Shot"][1],
        MR_M =defense["Mid-Range"][0],
        MR_A =defense["Mid-Range"][1],
        _3P_M =defense["3-Pointer"][0],
        _3P_A =defense["3-Pointer"][1],
        TOV = defense["Turnovers"][0]
    ))

def game_data_to_team_off_deff_stats(game_data):
    """
    Takes in game_data from gameAnalyzer(game_id) and inputs stats into DB (offense_stats + defensive_stats).
    
    """
    try:
        # Extract game data
        game_id = int(game_data["gameCode"])
        season_id = game_data["seasonYear"]

        home_team_data = game_data["homeTeam"]
        away_team_data = game_data["awayTeam"]

        home_team_id = home_team_data["teamCode"]
        away_team_id = away_team_data["teamCode"]

        home_team_defense = home_team_data["defense"]
        away_team_defense = away_team_data["defense"]

        # Create TeamStats/OffenseStats/DefenseStats instances
        for def_type in home_team_defense:
            home_team_off = create_off_def_stats(
                game_id,
                home_team_id,
                def_type,
                away_team_defense[def_type])[0]
            
            home_team_def = create_off_def_stats(
                game_id,
                home_team_id,
                def_type,
                home_team_defense[def_type]
            )[1]

            away_team_off = create_off_def_stats(
                game_id,
                away_team_id,
                def_type,
                home_team_defense[def_type])[0]
            
            away_team_def = create_off_def_stats(
                game_id,
                away_team_id,
                def_type,
                away_team_defense[def_type]
            )[1]

            # Add to the database session
            db.session.add(home_team_off)
            db.session.add(away_team_off)
            db.session.add(home_team_def)
            db.session.add(away_team_def)
            db.session.commit()

    except KeyError as e:
        print(f"Missing key in game_data: {e}")
        db.session.rollback()  # Rollback the transaction in case of an error
    except Exception as e:
        print(f"An error occurred: {e}")
        db.session.rollback()  # Rollback the transaction in case of an error


def create_player_stats(player_id,game_id,player_shots,player_driving,player_stats):
    '''
    Inputs player_id, game_id, player_shots,... and puts in PlayerStats db 
    '''
    return PlayerStats(
        player_id = player_id,
        game_id=game_id,
        Min = player_stats["Min"],
        PTS = player_stats["PTS"],
        FT_M = player_stats["FT"][0],
        FT_A =  player_stats["FT"][1],
        Rebs = player_stats["Reb"],
        AST = player_stats["AST"],
        STL = player_stats["STL"],
        BLK = player_stats["BLK"],
        TO = player_stats["TO"],
        PF = player_stats["PF"],
        FD = player_stats["FD"],

        F_M = player_shots["Finishing"][0],
        F_A = player_shots["Finishing"][1],
        IS_M = player_shots["Inside Shot"][0],
        IS_A = player_shots["Inside Shot"][1],
        MR_M = player_shots["Mid-Range"][0],
        MR_A = player_shots["Mid-Range"][1],
        _3P_M = player_shots["3-Pointer"][0],
        _3P_A = player_shots["3-Pointer"][1],
        DR_M = player_driving[0],
        DR_A = player_driving[1])

def add_player_stats(game_data):
    '''
    Takes in game_data from gameAnalyzer(game_id) and inputs the player's stats in PlayerStats
    '''
    try:
        # Extract game data
        game_id = int(game_data["gameCode"])
        season_year = game_data["seasonYear"]

        home_team_data = game_data["homeTeam"]
        away_team_data = game_data["awayTeam"]

        home_team_id = home_team_data["teamCode"]
        away_team_id = away_team_data["teamCode"]

        home_team_players = home_team_data["players"] #array of players
        away_team_players = away_team_data["players"]

        #Adds home team's players into PlayerStats Table
        for player in home_team_players:
            #print(player)
            player_name = player["name"]
            player_id = player["playerCode"]
            player_shots = player["shots"]
            player_driving = player["driving"]
            player_stats = player["stats"]
            new_player = create_player_stats(player_id,game_id,player_shots,player_driving,player_stats)
            db.session.add(new_player)

            #Add players in Players Table and PlayerSkills Table if game in currrent season
            if season_year == current_season:
                #update_player_helper(player_id) 
                get_or_add_player(player_id)
                db.session.add(new_player)
            
            db.session.commit()

        #Adds away team's players into PlayerStats Table
        for player in away_team_players:
            player_name = player["name"]
            player_id = player["playerCode"]
            player_shots = player["shots"]
            player_driving = player["driving"]
            player_stats = player["stats"]
            new_player = create_player_stats(player_id,game_id,player_shots,player_driving,player_stats)    
            db.session.add(new_player)
            #Add players in Players Table and PlayerSkills Table if game in currrent season
            if season_year == current_season:
                #update_player_helper(player_id)
                get_or_add_player(player_id)
                db.session.add(new_player)      
              
            db.session.commit()



    except KeyError as e:
        print(f"Missing key in game_data: {e}")
        db.session.rollback()  # Rollback the transaction in case of an error
    except Exception as e:
        print(f"An error occurred: {e}")
        db.session.rollback()  # Rollback the transaction in case of an error
    


def add_game_helper(game_id):
    '''
    #Adds game to DB (Games Table and Offensive and Defense Stats Table)
    #use multiple helper functions 
    '''
    existing_game = Game.query.filter_by(game_id=game_id).first()

    if existing_game:
        return existing_game
    
    #If game is not in DB Add it 

    gameURL = "http://onlinecollegebasketball.org/game/" + str(game_id)

    game_data = gameAnaylzer(gameURL)
    #print(game_data)
    ####
    game_data["homeTeam"]["defense"] = transform_defense_names(game_data["homeTeam"]["defense"])
    game_data["awayTeam"]["defense"] = transform_defense_names(game_data["awayTeam"]["defense"])
    ####
    homeTeamID = game_data["homeTeam"]["teamCode"]
    awayTeamID = game_data["awayTeam"]["teamCode"]

    new_game = Game(game_id=game_data["gameCode"], game_type=game_data["gameType"], season_id = game_data["seasonYear"], 
                    home_team_id = homeTeamID, away_team_id = awayTeamID)
 
    db.session.add(new_game)  # Add the new player to the session
    db.session.commit()  # Commit the transaction

    #Add Game Data to Team_stats/offensive_stats/defensive_stats/player_stats
    game_data_to_team_stats(game_data)
    game_data_to_team_off_deff_stats(game_data)

    #Adds Game Data Data to playerStats
    add_player_stats(game_data)

    #Adds both home and away teams to the DB 
    get_or_add_team(homeTeamID)
    get_or_add_team(awayTeamID)

    return new_game