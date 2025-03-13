from .pygetPlayerInfo import * #have to run like this in terminal: python -m scripts.pygetPlayerInfo
from models import *
from .pygameAnalyzerAPI import *
from .helperFunctions import *
from scripts.teamRosterInfo import *
from .predict import *
from .getConferenceDivison import *
from .getTeamConference import *
from sqlalchemy import *

#DONT ADD OLD SEASON GAMES WHEN THIS IS HARDCODED
#current_season = find_current_season()
current_season = 2044
#print(1)



def id_to_url(id):
    '''
    Converts either playerID or teamID into urls
    '''
    id = int(id)
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


#Finds eFG given FG Made, 3P Made, FG Attempted
def eFg_percentage(FGM,_3PM,FGA):
    
    return round(((FGM + 0.5 * _3PM) / FGA),3) if FGA != 0 else None

#Finds shot% given FGM, FGA
def fg_percentage(FGM,FGA):
    return round((FGM / FGA),3) if FGA != 0 else None
    




#Adds Conference data to Conference Table

def conference_adder():
    conference_data = get_divisons()

    for conference_id in conference_data:
        conference_name, division_id = conference_data[conference_id]

        new_conference = Conference(
            conference_id = conference_id,
            conference_name = conference_name,
            division_id = division_id,
        )
        db.session.add(new_conference)
        db.session.commit()
    return 



def add_to_player(player_id):
    '''
    Adds playerID to player Table
    Adds team and players and players skills if they are not in DB
    '''
    player_url = id_to_url(player_id)

    player_data = get_player_info(player_url)  # Fetch player data using the URL


    if player_data["Team_ID"] == player_data["Player_ID"]:

        #Player is not in a Team (prospect or graduated)
        return None
    

    get_or_add_team(player_data["Team_ID"]) #Add team and their players to DB
    new_player = Player.query.filter_by(player_id=player_id).first()

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
    If new player/team adds them aswell as PlayerSkill
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
    
    if not new_player:
        return None
    
    add_to_playerSkills(player_id)

    
    return new_player  # Return the newly added player


def update_player_helper(player_id):
    #Updates player skills (or adds them into db (player and playerskills Table)
    
    existing_player = Player.query.filter_by(player_id=player_id).first()

    if existing_player:

        get_or_add_team(existing_player.team_id)
        return existing_player
    
    new_player = get_or_add_player(player_id)

    return new_player

def team_data_to_playerDB(team_data):
    '''
    Adds team_data from team_roster_info(teamURL) to player and playerSkills table
    Updates player skills
    '''
    teamID = team_data["teamID"]
    for player in team_data["players"]:
        player_name = player["name"]
        player_id = player["playerID"]

        existing_player = Player.query.filter_by(player_id=player_id).first()

        if existing_player:
            # Update existing player skills
            existing_player_skills = PlayerSkills.query.filter_by(player_id=player_id, season_id=current_season).first()
            if existing_player_skills:
                # Update existing player skills
                existing_player_skills.Pos = player["Pos"]
                existing_player_skills.Class = player["Class"]
                existing_player_skills.height = player["Height"]
                existing_player_skills.weight = player["Weight"]
                existing_player_skills.wingspan = player["Wingspan"]
                existing_player_skills.vertical = player["Vertical"]
                existing_player_skills.IS = player["IS"]
                existing_player_skills.IQ = player["IQ"]
                existing_player_skills.OS = player["OS"]
                existing_player_skills.Pass = player["Pass"]
                existing_player_skills.Rng = player["Rng"]
                existing_player_skills.Hnd = player["Hnd"]
                existing_player_skills.Fin = player["Fin"]
                existing_player_skills.Drv = player["Drv"]
                existing_player_skills.Reb = player["Reb"]
                existing_player_skills.Str = player["Str"]
                existing_player_skills.IDef = player["IDef"]
                existing_player_skills.Spd = player["Spd"]
                existing_player_skills.PDef = player["PDef"]
                existing_player_skills.Sta = player["Sta"]
                existing_player_skills.SI = player["SI"]
                existing_player_skills.POT = player["POT"]
                existing_player_skills.Stars = player["Stars"]

                db.session.commit()  
                return existing_player_skills, "Player skills updated successfully"
                
            else:
                # If no existing skills for player in current season, add new skills to the table
                new_player_skills = PlayerSkills(
                player_id = player_id,
                season_id = current_season,
                Pos = player["Pos"],
                Class = player["Class"],
                height = player["Height"],
                weight=player["Weight"],
                wingspan=player["Wingspan"],
                vertical=player["Vertical"],
                IS=player["IS"],
                IQ=player["IQ"],
                OS=player["OS"],
                Pass=player["Pass"],
                Rng=player["Rng"],
                Hnd=player["Hnd"],
                Fin=player["Fin"],
                Drv=player["Drv"],
                Reb=player["Reb"],
                Str=player["Str"],
                IDef=player["IDef"],
                Spd=player["Spd"],
                PDef=player["PDef"],
                Sta=player["Sta"],
                SI = player["SI"],
                POT = player["POT"],
                Stars = player["Stars"]
                )

                db.session.add(new_player_skills)  # Add the new player skills to the session
                db.session.commit()  
            return 

        new_player = Player(
        player_id=player_id,
        team_id=teamID,
        name = player_name
    )
        db.session.add(new_player)  # Add the new player skills to the session
        
        new_player_skills = PlayerSkills(
                player_id = player_id,
                season_id = current_season,
                Pos = player["Pos"],
                Class = player["Class"],
                height = player["Height"],
                weight=player["Weight"],
                wingspan=player["Wingspan"],
                vertical=player["Vertical"],
                IS=player["IS"],
                IQ=player["IQ"],
                OS=player["OS"],
                Pass=player["Pass"],
                Rng=player["Rng"],
                Hnd=player["Hnd"],
                Fin=player["Fin"],
                Drv=player["Drv"],
                Reb=player["Reb"],
                Str=player["Str"],
                IDef=player["IDef"],
                Spd=player["Spd"],
                PDef=player["PDef"],
                Sta=player["Sta"],
                SI = player["SI"],
                POT = player["POT"],
                Stars = player["Stars"]
                )
        db.session.add(new_player_skills)  # Add the new player skills to the session
        db.session.commit()
    return 

def get_or_add_team(team_id):
    '''
    Check or add a team to the DB using the team_id
    '''
    existing_team = Team.query.filter_by(team_id=team_id).first()
    
    if existing_team:
        return existing_team
    
    # If the team does not exist, fetch their data
    team_url = id_to_url(team_id)
    
    
    team_data = team_roster_info(team_url)
    team_data_to_playerDB(team_data)
    
    new_team = Team(team_id = team_data["teamID"], team_name = team_data["teamName"]) 
    db.session.add(new_team)  # Add the new player to the session
    db.session.commit()  # Commit the transaction

    
    return new_team


#Updates Team Stat Averages for game
def update_team_avg(team_id,season_id,game_type,stat_type,team_outcome,team_shots, team_stats, opponent_shots,team_conference_id): 
    team_avg = db.session.query(TeamAvg).filter_by(team_id = team_id,season_id = season_id,game_type=game_type,stat_type = stat_type).first()


    if team_avg:
        
        #Accumalate avg
        
        team_avg.GW += team_outcome
        new_games_played = team_avg.GP + 1

        
        team_avg.F_M = round(((team_avg.F_M * team_avg.GP) + team_shots["Finishing"][0]) / new_games_played, 3)
        team_avg.F_A = round(((team_avg.F_A * team_avg.GP) + team_shots["Finishing"][1]) / new_games_played, 3)
        team_avg.F_P = fg_percentage(team_avg.F_M,team_avg.F_A)

        
        team_avg.IS_M = round(((team_avg.IS_M * team_avg.GP) + team_shots["Inside Shot"][0]) / new_games_played, 3)
        team_avg.IS_A = round(((team_avg.IS_A * team_avg.GP) + team_shots["Inside Shot"][1]) / new_games_played, 3)
        team_avg.IS_P = fg_percentage(team_avg.IS_M,team_avg.IS_A)

        
        team_avg.MR_M = round(((team_avg.MR_M * team_avg.GP) + team_shots["Mid-Range"][0]) / new_games_played, 3)
        team_avg.MR_A = round(((team_avg.MR_A * team_avg.GP) + team_shots["Mid-Range"][1]) / new_games_played, 3)
        team_avg.MR_P = fg_percentage(team_avg.MR_M,team_avg.MR_A)

        
        team_avg._3P_M = round(((team_avg._3P_M * team_avg.GP) + team_shots["3-Pointer"][0]) / new_games_played, 3)
        team_avg._3P_A = round(((team_avg._3P_A * team_avg.GP) + team_shots["3-Pointer"][1]) / new_games_played, 3)
        team_avg._3P_P = fg_percentage(team_avg._3P_M,team_avg._3P_A)

        
        team_avg.Min = round(((team_avg.Min * team_avg.GP) + team_stats["Min"]) / new_games_played, 3)
        team_avg.PTS = round(((team_avg.PTS * team_avg.GP) + team_stats["PTS"]) / new_games_played, 3)

        team_avg.FG_M = round(((team_avg.FG_M * team_avg.GP) + team_stats["FG"][0]) / new_games_played, 3)
        team_avg.FG_A = round(((team_avg.FG_A * team_avg.GP) + team_stats["FG"][1]) / new_games_played, 3)
        team_avg.eFG_P = eFg_percentage(team_avg.FG_M,team_avg._3P_M,team_avg.FG_A)

        team_avg._2P_M = round(((team_avg._2P_M * team_avg.GP) +  (team_stats["FG"][0] - team_shots["3-Pointer"][0])) / new_games_played, 3)
        team_avg._2P_A = round(((team_avg._2P_A * team_avg.GP) + (team_stats["FG"][1] - team_shots["3-Pointer"][1])) / new_games_played, 3)
        team_avg._2P_P = fg_percentage(team_avg._2P_M,team_avg._2P_A)

        team_avg.FT_M = round(((team_avg.FT_M * team_avg.GP) + team_stats["FT"][0]) / new_games_played, 3)
        team_avg.FT_A = round(((team_avg.FT_A * team_avg.GP) + team_stats["FT"][1]) / new_games_played, 3)
        team_avg.FT_P = fg_percentage(team_avg.FT_M,team_avg.FT_A)


        team_avg.Off = round(((team_avg.Off * team_avg.GP) + team_stats["Off"]) / new_games_played, 3)
        team_avg.Rebs = round(((team_avg.Rebs * team_avg.GP) + team_stats["Reb"]) / new_games_played, 3)
        team_avg.Def = team_avg.Rebs - team_avg.Off
        team_avg.AST = round(((team_avg.AST * team_avg.GP) + team_stats["AST"]) / new_games_played, 3)
        team_avg.STL = round(((team_avg.STL * team_avg.GP) + team_stats["STL"]) / new_games_played, 3)
        team_avg.BLK = round(((team_avg.BLK * team_avg.GP) + team_stats["BLK"]) / new_games_played, 3)
        team_avg.TO = round(((team_avg.TO * team_avg.GP) + team_stats["TO"]) / new_games_played, 3)
        team_avg.PF = round(((team_avg.PF * team_avg.GP) + team_stats["PF"]) / new_games_played, 3)
        team_avg.PLUS = round(((team_avg.PLUS * team_avg.GP) + team_stats["+/-"]) / new_games_played, 3)
        
        #No updating DIST if it is None ("-")
        if team_stats["DIST"] != "-":
            if team_avg.DIST is None:
                team_avg.DIST = round(float(team_stats["DIST"]),1)
            else:
                team_avg.DIST = round(((team_avg.DIST * team_avg.GP) + float(team_stats["DIST"])) / new_games_played,3)



        team_avg.PITP = round(((team_avg.PITP * team_avg.GP) + team_stats["PITP"]) / new_games_played,3)
        team_avg.FBP = round(((team_avg.FBP * team_avg.GP) + team_stats["FBP"]) / new_games_played,3)
        team_avg.FD = round(((team_avg.FD * team_avg.GP) + team_stats["FD"]) / new_games_played,3)
        team_avg.Poss = round(((team_avg.Poss * team_avg.GP) + team_stats["Poss"]) / new_games_played,3)


        if stat_type != "opponent":
            opp_avg = db.session.query(TeamAvg).filter_by(team_id = team_id,season_id = season_id,game_type=game_type,stat_type = "opponent").first()
            #Prep for BPM Training 
            off_values = [team_avg.Poss, team_avg.PTS,team_avg.FG_A,
                            team_avg.FT_A,team_avg.Off,team_avg.AST,
                            team_avg.TO,team_avg.FD]

            def_values = [opp_avg.Poss, opp_avg.PTS,opp_avg.FG_A,
                            team_avg.Rebs -  team_avg.Off, team_avg.STL,
                            team_avg.PF]

            bpm_values = predict_bpm("team",off_values,def_values)

            team_avg.OBPM = bpm_values[0]
            team_avg.DBPM = bpm_values[1]
            team_avg.BPM =  bpm_values[2]
        
        team_avg.GP = new_games_played #Last because Needed to calculate Avg for Stats Before
            


    else:
       
        if stat_type != "opponent":
            #Prep for BPM Training 
            off_values = [team_stats["Poss"], team_stats["PTS"],team_stats["FG"][1],
                            team_stats["FT"][1],team_stats["Off"],team_stats["AST"],
                            team_stats["TO"],team_stats["FD"]]

            def_values = [team_stats["OPoss"], team_stats["OPTS"],team_stats["OFG"][1],
                            team_stats["Reb"] -  team_stats["Off"], team_stats["STL"],
                            team_stats["PF"]]

            bpm_values = predict_bpm("team",off_values,def_values)
        else:
            #No BPM for opponent stats
            bpm_values = []
        
    #First game for team
        team_avg = TeamAvg(
        
            team_id=team_id,
            season_id = season_id,
            game_type=game_type, 
            conference_id = team_conference_id,
            stat_type = stat_type,

            GW = team_outcome,
            GP = 1,

            F_M =team_shots["Finishing"][0],
            F_A =team_shots["Finishing"][1],
            F_P = fg_percentage(team_shots["Finishing"][0],team_shots["Finishing"][1]),

            
            IS_M =team_shots["Inside Shot"][0],
            IS_A =team_shots["Inside Shot"][1],
            IS_P = fg_percentage(team_shots["Inside Shot"][0],team_shots["Inside Shot"][1]),

            
            MR_M =team_shots["Mid-Range"][0],
            MR_A =team_shots["Mid-Range"][1],
            MR_P = fg_percentage(team_shots["Mid-Range"][0],team_shots["Mid-Range"][1]),

            
            _3P_M = team_shots["3-Pointer"][0],
            _3P_A =team_shots["3-Pointer"][1],
            _3P_P = fg_percentage(team_shots["3-Pointer"][0],team_shots["3-Pointer"][1]),

            _2P_M = team_stats["FG"][0] - team_shots["3-Pointer"][0],
            _2P_A = team_stats["FG"][1] - team_shots["3-Pointer"][1],
            _2P_P = fg_percentage(team_stats["FG"][0] - team_shots["3-Pointer"][0] , team_stats["FG"][1] - team_shots["3-Pointer"][1]),


           
            Min = team_stats["Min"],
            PTS = team_stats["PTS"],
            
            FG_M = team_stats["FG"][0],
            FG_A = team_stats["FG"][1],
            eFG_P = eFg_percentage(team_stats["FG"][0],team_shots["3-Pointer"][0],team_stats["FG"][1]),

            
            FT_M = team_stats["FT"][0],
            FT_A =  team_stats["FT"][1],
            FT_P = fg_percentage(team_stats["FT"][0],team_stats["FT"][1]),
            
            Off = team_stats["Off"],
            Rebs = team_stats["Reb"],
            AST = team_stats["AST"],
            STL = team_stats["STL"],
            BLK = team_stats["BLK"],
            TO = team_stats["TO"],
            PF = team_stats["PF"],
            PLUS = team_stats["+/-"],
            DIST = float(team_stats["DIST"]) if team_stats["DIST"] != "-" else None,
            PITP = team_stats["PITP"],
            FBP = team_stats["FBP"],
            FD = team_stats["FD"],
            Poss = team_stats["Poss"],

            
            OBPM = bpm_values[0] if bpm_values else None, 
            DBPM = bpm_values[1] if bpm_values else None, 
            BPM =  bpm_values[2] if bpm_values else None,
        )
        db.session.add(team_avg)
    db.session.commit()

  




def create_team_stats(game_id, team_id, team_outcome, team_shots, team_stats, opponent_shots):
    """
    Helper function to create a TeamStats table.
    """


    

    #Prep for BPM Training 
    off_values = [team_stats["Poss"], team_stats["PTS"],team_stats["FG"][1],
                      team_stats["FT"][1],team_stats["Off"],team_stats["AST"],
                      team_stats["TO"],team_stats["FD"]]

    def_values = [team_stats["OPoss"], team_stats["OPTS"],team_stats["OFG"][1],
                      team_stats["Reb"] -  team_stats["Off"], team_stats["STL"],
                      team_stats["PF"]]

    bpm_values = predict_bpm("team",off_values,def_values)


    return TeamStats(
        game_id=game_id,
        team_id=team_id,
        outcome= team_outcome,
        #season_id=season_id,
        F_M =team_shots["Finishing"][0],
        F_A =team_shots["Finishing"][1],
        F_P = fg_percentage(team_shots["Finishing"][0],team_shots["Finishing"][1]),

        
        IS_M =team_shots["Inside Shot"][0],
        IS_A =team_shots["Inside Shot"][1],
        IS_P = fg_percentage(team_shots["Inside Shot"][0],team_shots["Inside Shot"][1]),

        
        MR_M =team_shots["Mid-Range"][0],
        MR_A =team_shots["Mid-Range"][1],
        MR_P = fg_percentage(team_shots["Mid-Range"][0],team_shots["Mid-Range"][1]),

        
        _3P_M = team_shots["3-Pointer"][0],
        _3P_A =team_shots["3-Pointer"][1],
        _3P_P = fg_percentage(team_shots["3-Pointer"][0],team_shots["3-Pointer"][1]),

        _2P_M = team_stats["FG"][0] - team_shots["3-Pointer"][0],
        _2P_A = team_stats["FG"][1] - team_shots["3-Pointer"][1],
        _2P_P = fg_percentage(team_stats["FG"][0] - team_shots["3-Pointer"][0] , team_stats["FG"][1] - team_shots["3-Pointer"][1]),

        O_PTS = team_stats["OPTS"],
        O_FG_M = team_stats["OFG"][0],
        O_FG_A = team_stats["OFG"][1],
        O_eFG_P = eFg_percentage(team_stats["OFG"][0],opponent_shots["3-Pointer"][0],team_stats["OFG"][1]),

        
        O_3P_M = opponent_shots["3-Pointer"][0],
        O_3P_A = opponent_shots["3-Pointer"][1],
        O_3P_P = fg_percentage(opponent_shots["3-Pointer"][0],opponent_shots["3-Pointer"][1]),

        
        O_2P_M = team_stats["OFG"][0] - team_stats["O3P"][0],
        O_2P_A = team_stats["OFG"][1] - team_stats["O3P"][1],
        O_2P_P = fg_percentage(team_stats["OFG"][0] - team_stats["O3P"][0], team_stats["OFG"][1] - team_stats["O3P"][1]),
       
        O_F_M = opponent_shots["Finishing"][0],
        O_F_A = opponent_shots["Finishing"][1],
        O_F_P = fg_percentage(opponent_shots["Finishing"][0],opponent_shots["Finishing"][1]),
       
        O_IS_M = opponent_shots["Inside Shot"][0],
        O_IS_A = opponent_shots["Inside Shot"][1],
        O_IS_P = fg_percentage(opponent_shots["Inside Shot"][0],opponent_shots["Inside Shot"][1]),

        O_MR_M = opponent_shots["Mid-Range"][0],
        O_MR_A = opponent_shots["Mid-Range"][1],
        O_MR_P = fg_percentage(opponent_shots["Mid-Range"][0],opponent_shots["Mid-Range"][1]),

        O_Poss = team_stats["OPoss"],
        Min = team_stats["Min"],
        PTS = team_stats["PTS"],
        
        FG_M = team_stats["FG"][0],
        FG_A = team_stats["FG"][1],
        eFG_P = eFg_percentage(team_stats["FG"][0],team_shots["3-Pointer"][0],team_stats["FG"][1]),

        
        FT_M = team_stats["FT"][0],
        FT_A =  team_stats["FT"][1],
        FT_P = fg_percentage(team_stats["FT"][0],team_stats["FT"][1]),
        
        Off = team_stats["Off"],
        Def = team_stats["Reb"] - team_stats["Off"],
        Rebs = team_stats["Reb"],
        AST = team_stats["AST"],
        STL = team_stats["STL"],
        BLK = team_stats["BLK"],
        TO = team_stats["TO"],
        PF = team_stats["PF"],
        PLUS = team_stats["+/-"],
        DIST = float(team_stats["DIST"]) if team_stats["DIST"] != "-" else None,
        PITP = team_stats["PITP"],
        FBP = team_stats["FBP"],
        FD = team_stats["FD"],
        Fat = team_stats["Fat"],
        Poss = team_stats["Poss"],

        OBPM = bpm_values[0], 
        DBPM = bpm_values[1], 
        BPM =  bpm_values[2],

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

        home_team_outcome = home_team_data["outcome"]
        away_team_outcome = away_team_data["outcome"]

        home_team_shots = home_team_data["totalShots"]
        away_team_shots = away_team_data["totalShots"]

        home_team_stats = home_team_data["stats"]
        away_team_stats = away_team_data["stats"]
        # Create TeamStats instances

        home_team_stats = create_team_stats(
            game_id,
            home_team_id,
            home_team_outcome,
            #season_id,
            home_team_shots,
            home_team_stats,
            away_team_shots,
        )

        away_team_stats = create_team_stats(
            game_id,
            away_team_id,
            away_team_outcome,
            #season_id,
            away_team_shots,
            away_team_stats,
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


def create_player_stats(player_id,game_id,player_position,player_shots,player_defense,player_stats):
    '''
    Inputs player_id, game_id, player_shots,... and puts in PlayerStats db 
    '''



    #Prep for BPM Training 
    off_values = [player_stats["Poss"], player_stats["PTS"],player_stats["FG"][1],
                      player_stats["FT"][1],player_stats["Off"],player_stats["AST"],
                      player_stats["TO"],player_stats["FD"]]

    def_values = [player_stats["OPoss"], player_stats["OPTS"],player_stats["OFG"][1],
                      player_stats["Reb"] -  player_stats["Off"], player_stats["STL"],
                      player_stats["PF"]]

    bpm_values = predict_bpm(player_position,off_values,def_values)
    
    return PlayerStats(
        player_id = player_id,
        game_id=game_id,
        Pos = player_position,
        GS = player_stats["Start"],
        Min = player_stats["Min"],
        PTS = player_stats["PTS"],
        FG_M = player_stats["FG"][0],
        FG_A = player_stats["FG"][1],
        eFG_P = eFg_percentage(player_stats["FG"][0],player_shots["3-Pointer"][0],player_stats["FG"][1]),
        
        _2P_M = player_stats["FG"][0] - player_shots["3-Pointer"][0],
        _2P_A = player_stats["FG"][1] - player_shots["3-Pointer"][1],
        _2P_P = fg_percentage((player_stats["FG"][0] - player_shots["3-Pointer"][0]),(player_stats["FG"][1] - player_shots["3-Pointer"][1])),
        
        _3P_M = player_shots["3-Pointer"][0],
        _3P_A = player_shots["3-Pointer"][1],
        _3P_P = fg_percentage(player_shots["3-Pointer"][0],player_shots["3-Pointer"][1]),
        
        FT_M = player_stats["FT"][0],
        FT_A =  player_stats["FT"][1],
        FT_P = fg_percentage(player_stats["FT"][0],player_stats["FT"][1]),
        
        Off = player_stats["Off"],
        Def = player_stats["Reb"] - player_stats["Off"],
        Rebs = player_stats["Reb"],
        AST = player_stats["AST"],
        STL = player_stats["STL"],
        BLK = player_stats["BLK"],
        TO = player_stats["TO"],
        PF = player_stats["PF"],
        PLUS = player_stats["+/-"],
        DIST = float(player_stats["DIST"]) if player_stats["DIST"] != "-" else None,
        PITP = player_stats["PITP"],
        FBP = player_stats["FBP"],
        FD = player_stats["FD"],
        Fat = player_stats["Fat"],
        Poss = player_stats["Poss"],

        F_M = player_shots["Finishing"][0],
        F_A = player_shots["Finishing"][1],
        F_P = fg_percentage(player_shots["Finishing"][0],player_shots["Finishing"][1]),

        IS_M = player_shots["Inside Shot"][0],
        IS_A = player_shots["Inside Shot"][1],
        IS_P = fg_percentage(player_shots["Inside Shot"][0],player_shots["Inside Shot"][1]),
       
        MR_M = player_shots["Mid-Range"][0],
        MR_A = player_shots["Mid-Range"][1],
        MR_P = fg_percentage(player_shots["Mid-Range"][0],player_shots["Mid-Range"][1]),

        O_PTS = player_stats["OPTS"],
        O_FG_M = player_stats["OFG"][0],
        O_FG_A = player_stats["OFG"][1],
        O_eFG_P = eFg_percentage(player_stats["OFG"][0],player_defense["3-Pointer"][0],player_stats["OFG"][1]),
       
        O_F_M = player_defense["Finishing"][0],
        O_F_A = player_defense["Finishing"][1],
        O_F_P = fg_percentage(player_defense["Finishing"][0],player_defense["Finishing"][1]),
       
        O_IS_M = player_defense["Inside Shot"][0],
        O_IS_A = player_defense["Inside Shot"][1],
        O_IS_P = fg_percentage(player_defense["Inside Shot"][0],player_defense["Inside Shot"][1]),
       
        O_MR_M = player_defense["Mid-Range"][0],
        O_MR_A = player_defense["Mid-Range"][1],
        O_MR_P = fg_percentage(player_defense["Mid-Range"][0],player_defense["Mid-Range"][1]),

        O_3P_M = player_defense["3-Pointer"][0],
        O_3P_A = player_defense["3-Pointer"][1],
        O_3P_P = fg_percentage(player_defense["3-Pointer"][0],player_defense["3-Pointer"][1]),

        O_2P_M = player_stats["OFG"][0] - player_stats["O3P"][0],
        O_2P_A = player_stats["OFG"][1] - player_stats["O3P"][1],
        O_2P_P = fg_percentage(player_stats["OFG"][0] - player_stats["O3P"][0], player_stats["OFG"][1] - player_stats["O3P"][1]),

        O_Poss = player_stats["OPoss"],
            
        OBPM = bpm_values[0], 
        DBPM = bpm_values[1], 
        BPM =  bpm_values[2]
        )
    

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
            player_position = player["position"]
            player_shots = player["shots"]
            player_defense = player["defense"]
            player_stats = player["stats"]
            new_player = create_player_stats(player_id,game_id,player_position,player_shots,player_defense,player_stats)
            

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
            player_position = player["position"]
            player_shots = player["shots"]
            player_defense = player["defense"]
            player_stats = player["stats"]
            new_player = create_player_stats(player_id,game_id,player_position,player_shots,player_defense,player_stats)    

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
    


#Updates Player Stat Averages for game
def update_player_avg(player_id,season_id,game_type,player_position,player_shots,player_defense,player_stats,player_pos_min): 
    player_avg = db.session.query(PlayerAvg).filter_by(player_id = player_id,season_id = season_id,game_type=game_type).first()
    
    #Gets Team and Opponent Team Avg Stats (for calculating advanced statistics like AST%)
    team_id_of_player = db.session.query(Player.team_id).filter_by(player_id=player_id).scalar()
    team_avg = db.session.query(TeamAvg).filter_by(team_id=team_id_of_player, season_id = season_id,game_type=game_type,stat_type="team").first()
    opp_team_avg = db.session.query(TeamAvg).filter_by(team_id=team_id_of_player, season_id = season_id,game_type=game_type,stat_type="opponent").first()
    
    

    if player_avg:
        
        #Accumalate avg
        

        new_games_played = player_avg.GP + 1

        player_avg.GS = player_avg.GS + player_stats["Start"]
         
        player_avg.PG_Min = round(((player_avg.PG_Min * player_avg.GP) + player_pos_min["PG"]) / new_games_played, 3) 
        player_avg.SG_Min = round(((player_avg.SG_Min * player_avg.GP) + player_pos_min["SG"]) / new_games_played, 3) 
        player_avg.SF_Min = round(((player_avg.SF_Min * player_avg.GP) + player_pos_min["SF"]) / new_games_played, 3) 
        player_avg.PF_Min = round(((player_avg.PF_Min * player_avg.GP) + player_pos_min["PF"]) / new_games_played, 3) 
        player_avg.C_Min = round(((player_avg.C_Min * player_avg.GP) + player_pos_min["C"]) / new_games_played, 3) 
        
        player_avg.F_M = round(((player_avg.F_M * player_avg.GP) + player_shots["Finishing"][0]) / new_games_played, 3)
        player_avg.F_A = round(((player_avg.F_A * player_avg.GP) + player_shots["Finishing"][1]) / new_games_played, 3)
        player_avg.F_P = fg_percentage(player_avg.F_M,player_avg.F_A)
        
       
        player_avg.IS_M = round(((player_avg.IS_M * player_avg.GP) + player_shots["Inside Shot"][0]) / new_games_played, 3)
        player_avg.IS_A = round(((player_avg.IS_A * player_avg.GP) + player_shots["Inside Shot"][1]) / new_games_played, 3)
        player_avg.IS_P = fg_percentage(player_avg.IS_M,player_avg.IS_A)
       
        player_avg.MR_M = round(((player_avg.MR_M * player_avg.GP) + player_shots["Mid-Range"][0]) / new_games_played, 3)
        player_avg.MR_A = round(((player_avg.MR_A * player_avg.GP) + player_shots["Mid-Range"][1]) / new_games_played, 3)
        player_avg.MR_P = fg_percentage(player_avg.MR_M,player_avg.MR_A)
        
        player_avg._3P_M = round(((player_avg._3P_M * player_avg.GP) + player_shots["3-Pointer"][0]) / new_games_played, 3)
        player_avg._3P_A = round(((player_avg._3P_A * player_avg.GP) + player_shots["3-Pointer"][1]) / new_games_played, 3)
        player_avg._3P_P = fg_percentage(player_avg._3P_M,player_avg._3P_A)

        
        player_avg.O_PTS = round(((player_avg.O_PTS * player_avg.GP) + player_stats["OPTS"]) / new_games_played, 3)
        player_avg.O_FG_M = round(((player_avg.O_FG_M * player_avg.GP) + player_stats["OFG"][0]) / new_games_played, 3)
        player_avg.O_FG_A = round(((player_avg.O_FG_A * player_avg.GP) + player_stats["OFG"][1]) / new_games_played, 3)
        player_avg.O_3P_M = round(((player_avg.O_3P_M * player_avg.GP) + player_defense["3-Pointer"][0]) / new_games_played, 3)
        player_avg.O_3P_A = round(((player_avg.O_3P_A * player_avg.GP) + player_defense["3-Pointer"][1]) / new_games_played, 3)
        player_avg.O_3P_P = fg_percentage(player_avg.O_3P_M,player_avg.O_3P_A)
        
        player_avg.O_eFG_P = eFg_percentage(player_avg.O_FG_M,player_avg.O_3P_M,player_avg.O_FG_A)

        player_avg.O_2P_M = round(((player_avg.O_2P_M * player_avg.GP) +  (player_stats["OFG"][0] - player_defense["3-Pointer"][0])) / new_games_played, 3)
        player_avg.O_2P_A = round(((player_avg.O_2P_A * player_avg.GP) + (player_stats["OFG"][1] - player_defense["3-Pointer"][1])) / new_games_played, 3)
        player_avg.O_2P_P = fg_percentage(player_avg.O_2P_M,player_avg.O_2P_A) 
        
        player_avg.O_F_M = round(((player_avg.O_F_M * player_avg.GP) + player_defense["Finishing"][0]) / new_games_played, 3)
        player_avg.O_F_A = round(((player_avg.O_F_A * player_avg.GP) + player_defense["Finishing"][1]) / new_games_played, 3)
        player_avg.O_F_P = fg_percentage(player_avg.O_F_M,player_avg.O_F_A)
        
        player_avg.O_IS_M = round(((player_avg.O_IS_M * player_avg.GP) + player_defense["Inside Shot"][0]) / new_games_played, 3)
        player_avg.O_IS_A = round(((player_avg.O_IS_A * player_avg.GP) + player_defense["Inside Shot"][1]) / new_games_played, 3)
        player_avg.O_IS_P = fg_percentage(player_avg.O_IS_M,player_avg.O_IS_A)
        
        player_avg.O_MR_M = round(((player_avg.O_MR_M * player_avg.GP) + player_defense["Mid-Range"][0]) / new_games_played, 3)
        player_avg.O_MR_A = round(((player_avg.O_MR_A * player_avg.GP) + player_defense["Mid-Range"][1]) / new_games_played, 3)
        player_avg.O_MR_P = fg_percentage(player_avg.O_MR_M,player_avg.O_MR_A)
        
        player_avg.O_Poss = round(((player_avg.O_Poss * player_avg.GP) + player_stats["OPoss"]) / new_games_played, 3)
        player_avg.Min = round(((player_avg.Min * player_avg.GP) + player_stats["Min"]) / new_games_played, 3)
        player_avg.PTS = round(((player_avg.PTS * player_avg.GP) + player_stats["PTS"]) / new_games_played, 3)
        
        player_avg.FG_M = round(((player_avg.FG_M * player_avg.GP) + player_stats["FG"][0]) / new_games_played, 3)
        player_avg.FG_A = round(((player_avg.FG_A * player_avg.GP) + player_stats["FG"][1]) / new_games_played, 3)
        player_avg.eFG_P = eFg_percentage(player_avg.FG_M,player_avg._3P_M,player_avg.FG_A)

        player_avg._2P_M = round(((player_avg._2P_M * player_avg.GP) +  (player_stats["FG"][0] - player_shots["3-Pointer"][0])) / new_games_played, 3)
        player_avg._2P_A = round(((player_avg._2P_A * player_avg.GP) + (player_stats["FG"][1] - player_shots["3-Pointer"][1])) / new_games_played, 3)
        player_avg._2P_P = fg_percentage(player_avg._2P_M,player_avg._2P_A)
        
        player_avg.FT_M = round(((player_avg.FT_M * player_avg.GP) + player_stats["FT"][0]) / new_games_played, 3)
        player_avg.FT_A = round(((player_avg.FT_A * player_avg.GP) + player_stats["FT"][1]) / new_games_played, 3)
        player_avg.FT_P = fg_percentage(player_avg.FT_M,player_avg.FT_A)
        

        player_avg.Off = round(((player_avg.Off * player_avg.GP) + player_stats["Off"]) / new_games_played, 3)
        player_avg.Rebs = round(((player_avg.Rebs * player_avg.GP) + player_stats["Reb"]) / new_games_played, 3)
        player_avg.Def = player_avg.Rebs - player_avg.Off
        player_avg.AST = round(((player_avg.AST * player_avg.GP) + player_stats["AST"]) / new_games_played, 3)
        player_avg.STL = round(((player_avg.STL * player_avg.GP) + player_stats["STL"]) / new_games_played, 3)
        player_avg.BLK = round(((player_avg.BLK * player_avg.GP) + player_stats["BLK"]) / new_games_played, 3)
        player_avg.TO = round(((player_avg.TO * player_avg.GP) + player_stats["TO"]) / new_games_played, 3)
        player_avg.PF = round(((player_avg.PF * player_avg.GP) + player_stats["PF"]) / new_games_played, 3)
        player_avg.PLUS = round(((player_avg.PLUS * player_avg.GP) + player_stats["+/-"]) / new_games_played, 3)

        # No updating DIST if it is None ("-")
        if player_stats["DIST"] != "-":
            if player_avg.DIST is None:
                player_avg.DIST = round(float(player_stats["DIST"]), 1)
            else:
                player_avg.DIST = round(((player_avg.DIST * player_avg.GP) + float(player_stats["DIST"])) / new_games_played, 3)

        player_avg.PITP = round(((player_avg.PITP * player_avg.GP) + player_stats["PITP"]) / new_games_played, 3)
        player_avg.FBP = round(((player_avg.FBP * player_avg.GP) + player_stats["FBP"]) / new_games_played, 3)
        player_avg.FD = round(((player_avg.FD * player_avg.GP) + player_stats["FD"]) / new_games_played, 3)
        player_avg.Poss = round(((player_avg.Poss * player_avg.GP) + player_stats["Poss"]) / new_games_played, 3)

        # Prep for BPM Training 
        off_values = [player_avg.Poss, player_avg.PTS, player_avg.FG_A,
                    player_avg.FT_A, player_avg.Off, player_avg.AST,
                    player_avg.TO, player_avg.FD]
        
        def_values = [player_avg.O_Poss, player_avg.O_PTS,player_avg.O_FG_A,
                        player_avg.Rebs -  player_avg.Off, player_avg.STL,
                        player_avg.PF]

        bpm_values = predict_bpm(player_position,off_values,def_values)        
        


        player_avg.OBPM = bpm_values[0]
        player_avg.DBPM = bpm_values[1]
        player_avg.BPM = bpm_values[2]
        
        #Advanced Statistics
        player_avg.TS = round((player_avg.PTS) / (2 * (player_avg.FG_A + 0.44 * player_avg.FT_A)), 3) if (player_avg.FG_A + 0.44 * player_avg.FT_A) != 0 else 0

        player_avg._3PAr = round(player_avg._3P_A / player_avg.FG_A, 3) if player_avg.FG_A != 0 else 0

        player_avg.FTr = round(player_avg.FT_A / player_avg.FG_A, 3) if player_avg.FG_A != 0 else 0

        denom = player_avg.Min * (team_avg.Off + opp_team_avg.Def)
        player_avg.ORB_P = round(100 * (player_avg.Off * (team_avg.Min / 5)) / denom, 1) if denom != 0 else 0

        denom = player_avg.Min * (team_avg.Def + opp_team_avg.Off)
        player_avg.DRB_P = round(100 * (player_avg.Def * (team_avg.Min / 5)) / denom, 1) if denom != 0 else 0

        denom = player_avg.Min * (team_avg.Rebs + opp_team_avg.Rebs)
        player_avg.TRB_P = round(100 * (player_avg.Rebs * (team_avg.Min / 5)) / denom, 1) if denom != 0 else 0

        denom = ((player_avg.Min / (team_avg.Min / 5)) * team_avg.FG_M) - player_avg.FG_M
        player_avg.AST_P = round(100 * player_avg.AST / denom, 1) if denom != 0 else 0

        denom = player_avg.Min * opp_team_avg.Poss
        player_avg.STL_P = round(100 * (player_avg.STL * (team_avg.Min / 5)) / denom, 1) if denom != 0 else 0

        denom = player_avg.Min * (opp_team_avg.FG_A - opp_team_avg._3P_A)
        player_avg.BLK_P = round(100 * (player_avg.BLK * (team_avg.Min / 5)) / denom, 1) if denom != 0 else 0

        denom = player_avg.FG_A + 0.44 * player_avg.FT_A + player_avg.TO
        player_avg.TO_P = round(100 * player_avg.TO / denom, 1) if denom != 0 else 0

        denom = player_avg.Min * (team_avg.FG_A + 0.44 * team_avg.FT_A + team_avg.TO)
        player_avg.USG_P = round(100 * ((player_avg.FG_A + 0.44 * player_avg.FT_A + player_avg.TO) * (team_avg.Min / 5)) / denom, 1) if denom != 0 else 0
        
        player_avg.GP = new_games_played  # Last because Needed to calculate Avg for Stats Before
                


    else:
        
        team_game_stats = (
            db.session.query(TeamStats)
            .filter_by(team_id=team_id_of_player)
            .order_by(TeamStats.G.desc())  
            .first()
        )

        game_result = (
            db.session.query(TeamStats.game_id)
            .filter_by(team_id=team_id_of_player)
            .order_by(TeamStats.G.desc())
            .first()
        )

        # Accessing the game_id from the result
        game_id = game_result[0] if game_result else None

        #Gets opp stats from game
        opp_team_game_stats = (
            db.session.query(TeamStats)
            .filter(TeamStats.game_id == game_id)  
            .filter(TeamStats.team_id != team_id_of_player)  
            .first()  
        )
        
       
        
        #Prep for BPM Training 
        off_values = [player_stats["Poss"], player_stats["PTS"],player_stats["FG"][1],
                        player_stats["FT"][1],player_stats["Off"],player_stats["AST"],
                        player_stats["TO"],player_stats["FD"]]

        def_values = [player_stats["OPoss"], player_stats["OPTS"],player_stats["OFG"][1],
                        player_stats["Reb"] -  player_stats["Off"], player_stats["STL"],
                        player_stats["PF"]]

        bpm_values = predict_bpm(player_position,off_values,def_values)
        
    #First game for team
        player_avg = PlayerAvg(
        
            player_id=player_id,
            season_id = season_id,
            game_type=game_type, 

            GP = 1,
            GS = player_stats["Start"],
            
            PG_Min = player_pos_min["PG"],
            SG_Min = player_pos_min["SG"],
            SF_Min = player_pos_min["SF"],
            PF_Min = player_pos_min["PF"],
            C_Min = player_pos_min["C"],

            F_M =player_shots["Finishing"][0],
            F_A =player_shots["Finishing"][1],
            F_P = fg_percentage(player_shots["Finishing"][0],player_shots["Finishing"][1]),    
            
            IS_M =player_shots["Inside Shot"][0],
            IS_A =player_shots["Inside Shot"][1],
            
            IS_P = fg_percentage(player_shots["Inside Shot"][0],player_shots["Inside Shot"][1]),
            MR_M =player_shots["Mid-Range"][0],
            MR_A =player_shots["Mid-Range"][1],
            MR_P = fg_percentage(player_shots["Mid-Range"][0],player_shots["Mid-Range"][1]), 
            
            
            _3P_M = player_shots["3-Pointer"][0],   
            _3P_A = player_shots["3-Pointer"][1],
            _3P_P = fg_percentage(player_shots["3-Pointer"][0],player_shots["3-Pointer"][1]), 
            

            _2P_M = player_stats["FG"][0] - player_shots["3-Pointer"][0],
            _2P_A = player_stats["FG"][1] - player_shots["3-Pointer"][1],
            _2P_P = fg_percentage((player_stats["FG"][0] - player_shots["3-Pointer"][0]),(player_stats["FG"][1] - player_shots["3-Pointer"][1])),
            
            
            O_PTS = player_stats["OPTS"],
            O_FG_M = player_stats["OFG"][0],
            O_FG_A = player_stats["OFG"][1],
            O_eFG_P = eFg_percentage(player_stats["OFG"][0],player_defense["3-Pointer"][0],player_stats["OFG"][1]),
            O_3P_M = player_defense["3-Pointer"][0],
            O_3P_A = player_defense["3-Pointer"][1],
            O_3P_P = fg_percentage(player_defense["3-Pointer"][0],player_defense["3-Pointer"][1]),

            O_2P_M = player_stats["OFG"][0] - player_defense["3-Pointer"][0],
            O_2P_A = player_stats["OFG"][1] - player_defense["3-Pointer"][1],
            O_2P_P = fg_percentage((player_stats["FG"][0] - player_defense["3-Pointer"][0]),(player_stats["FG"][1] - player_defense["3-Pointer"][1])),
            

            

            O_F_M = player_defense["Finishing"][0],
            O_F_A = player_defense["Finishing"][1],
            O_F_P = fg_percentage(player_defense["Finishing"][0],player_defense["Finishing"][1]),
            
            O_IS_M = player_defense["Inside Shot"][0],
            O_IS_A = player_defense["Inside Shot"][1],
            O_IS_P = fg_percentage(player_defense["Inside Shot"][0],player_defense["Inside Shot"][1]),
            
            O_MR_M = player_defense["Mid-Range"][0],
            O_MR_A = player_defense["Mid-Range"][1],
            O_MR_P = fg_percentage(player_defense["Mid-Range"][0],player_defense["Mid-Range"][1]),
            
            O_Poss = player_stats["OPoss"],
            Min = player_stats["Min"],
            PTS = player_stats["PTS"],
            FG_M = player_stats["FG"][0],
            FG_A = player_stats["FG"][1],

            eFG_P = eFg_percentage(player_stats["FG"][0],player_shots["3-Pointer"][0],player_stats["FG"][1]),

            FT_M = player_stats["FT"][0],
            FT_A =  player_stats["FT"][1],
            FT_P =  fg_percentage(player_stats["FT"][0],player_stats["FT"][1]),
            
            Off = player_stats["Off"],
            Def = player_stats["Reb"] - player_stats["Off"],
            Rebs = player_stats["Reb"],
            AST = player_stats["AST"],
            STL = player_stats["STL"],
            BLK = player_stats["BLK"],
            TO = player_stats["TO"],
            PF = player_stats["PF"],
            PLUS = player_stats["+/-"],
            DIST = float(player_stats["DIST"]) if player_stats["DIST"] != "-" else None,
            PITP = player_stats["PITP"],
            FBP = player_stats["FBP"],
            FD = player_stats["FD"],
            Poss = player_stats["Poss"],

            OBPM = bpm_values[0], 
            DBPM = bpm_values[1], 
            BPM =  bpm_values[2],

            #Advanced Statistics
            TS = round((player_stats["PTS"]) / (2 * (player_stats["FG"][1] + 0.44 * player_stats["FT"][1])), 3) \
                if (player_stats["FG"][1] + 0.44 * player_stats["FT"][1]) != 0 else 0,

            _3PAr = round(player_shots["3-Pointer"][1] / player_stats["FG"][1], 3) if player_stats["FG"][1] != 0 else 0,

            FTr = round(player_stats["FT"][1] / player_stats["FG"][1], 3) if player_stats["FG"][1] != 0 else 0,

            # Calculations without using 'denom' as a variable
            ORB_P = round(100 * (player_stats["Off"] * (team_game_stats.Min / 5)) / 
                        (player_stats["Min"] * (team_game_stats.Off + (opp_team_game_stats.Def))), 1) \
                if (player_stats["Min"] * (team_game_stats.Off + (opp_team_game_stats.Def))) != 0 else 0,

            DRB_P = round(100 * ((player_stats["Reb"] - player_stats["Off"])* (team_game_stats.Min / 5)) / 
                        (player_stats["Min"] * (team_game_stats.Def + (opp_team_game_stats.Off))), 1) \
                if (player_stats["Min"] * (team_game_stats.Def + (opp_team_game_stats.Off))) != 0 else 0,

            TRB_P = round(100 * (player_stats["Reb"] * (team_game_stats.Min / 5)) / 
                        (player_stats["Min"] * (team_game_stats.Rebs + opp_team_game_stats.Rebs)), 1) \
                if (player_stats["Min"] * (team_game_stats.Rebs + opp_team_game_stats.Rebs)) != 0 else 0,

            AST_P = round(100 * player_stats["AST"] / 
                        (((player_stats["Min"] / (team_game_stats.Min / 5)) * team_game_stats.FG_M) - player_stats["FG"][0]), 1) \
                if (((player_stats["Min"] / (team_game_stats.Min / 5)) * team_game_stats.FG_M) - player_stats["FG"][0]) != 0 else 0,

            STL_P = round(100 * (player_stats["STL"] * (team_game_stats.Min / 5)) / 
                        (player_stats["Min"] * opp_team_game_stats.Poss), 1) \
                if (player_stats["Min"] * opp_team_game_stats.Poss) != 0 else 0,

            BLK_P = round(100 * (player_stats["BLK"] * (team_game_stats.Min / 5)) / 
                        (player_stats["Min"] * (opp_team_game_stats.FG_A - opp_team_game_stats._3P_A)), 1) \
                if (player_stats["Min"] * (opp_team_game_stats.FG_A - opp_team_game_stats._3P_A)) != 0 else 0,

            TO_P = round(100 * player_stats["TO"] / 
                        (player_stats["FG"][1] + 0.44 * player_stats["FT"][1] + player_stats["TO"]), 1) \
                if (player_stats["FG"][1] + 0.44 * player_stats["FT"][1] + player_stats["TO"]) != 0 else 0,

            USG_P = round(100 * ((player_stats["FG"][1] + 0.44 * player_stats["FT"][1] + player_stats["TO"]) * 
                                (team_game_stats.Min / 5)) / 
                        (player_stats["Min"] * (team_game_stats.FG_A + 0.44 * team_game_stats.FT_A + team_game_stats.TO)), 1) \
                if (player_stats["Min"] * (team_game_stats.FG_A + 0.44 * team_game_stats.FT_A + team_game_stats.TO)) != 0 else 0


        )
        db.session.add(player_avg)
    db.session.commit()









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

    game_data = gameAnalyzer(gameURL)
    #print(game_data)
    ####
    game_data["homeTeam"]["defense"] = transform_defense_names(game_data["homeTeam"]["defense"])
    game_data["awayTeam"]["defense"] = transform_defense_names(game_data["awayTeam"]["defense"])
    ####
    homeTeamID = game_data["homeTeam"]["teamCode"]
    awayTeamID = game_data["awayTeam"]["teamCode"]

    season_id = game_data["seasonYear"]
    game_type = game_data["gameType"]

    home_team_outcome = game_data["homeTeam"]["outcome"]
    away_team_outcome = game_data["awayTeam"]["outcome"]


    new_game = Game(game_id=game_data["gameCode"], game_type=game_type, season_id = season_id,game_date = game_data["game_date"], 
                    home_team_id = homeTeamID, away_team_id = awayTeamID)
 
    db.session.add(new_game)  # Add the new player to the session
    db.session.commit()  # Commit the transaction

    #Adds both home and away teams to the DB 
    get_or_add_team(homeTeamID)
    get_or_add_team(awayTeamID)

    #Add Game Data to Team_stats/offensive_stats/defensive_stats/player_stats
    game_data_to_team_stats(game_data)
    game_data_to_team_off_deff_stats(game_data)

    #Adds Game Data Data to playerStats
    add_player_stats(game_data)
    

    home_team_conference_id = get_team_conference(homeTeamID,season_id)
    away_team_conference_id = get_team_conference(awayTeamID,season_id)

    #Updates Team Avg
    update_team_avg(homeTeamID,season_id,game_data["gameType"],"team",home_team_outcome,game_data["homeTeam"]["totalShots"], game_data["homeTeam"]["stats"], game_data["awayTeam"]["totalShots"],home_team_conference_id)
    update_team_avg(awayTeamID,season_id,game_data["gameType"],"team",away_team_outcome,game_data["awayTeam"]["totalShots"], game_data["awayTeam"]["stats"], game_data["homeTeam"]["totalShots"],away_team_conference_id)

    #Updates Opponent Team Avg
    update_team_avg(homeTeamID,season_id,game_data["gameType"],"opponent",away_team_outcome,game_data["awayTeam"]["totalShots"], game_data["awayTeam"]["stats"], game_data["homeTeam"]["totalShots"],home_team_conference_id)
    update_team_avg(awayTeamID,season_id,game_data["gameType"],"opponent",home_team_outcome,game_data["homeTeam"]["totalShots"], game_data["homeTeam"]["stats"], game_data["awayTeam"]["totalShots"],away_team_conference_id)
    

    #Combines home and away Players for updating avg stats
    all_players = game_data["homeTeam"]["players"] + game_data["awayTeam"]["players"]

    for player in all_players:
        update_player_avg(player["playerCode"],season_id,game_type,player["position"],player["shots"],player["defense"],player["stats"],player["pos_min"])

    
    #update_player_avg(player_id,season_id,game_type,player_position,player_shots,player_defense,player_stats)

    # Exclude Exhibition and Invitational Games from Total College Stats Avg
    EXCLUDED_GAME_TYPES = {"Exhibition", "Invitational"}

    

    if game_data["gameType"] not in EXCLUDED_GAME_TYPES:
        #Updates Team Avg
        update_team_avg(homeTeamID,season_id,"College","team",home_team_outcome,game_data["homeTeam"]["totalShots"], game_data["homeTeam"]["stats"], game_data["awayTeam"]["totalShots"],home_team_conference_id)
        update_team_avg(awayTeamID,season_id,"College","team",away_team_outcome,game_data["awayTeam"]["totalShots"], game_data["awayTeam"]["stats"], game_data["homeTeam"]["totalShots"],away_team_conference_id)

        #Updates Opponent Team Avg
        update_team_avg(homeTeamID,season_id,"College","opponent",away_team_outcome,game_data["awayTeam"]["totalShots"], game_data["awayTeam"]["stats"], game_data["homeTeam"]["totalShots"],home_team_conference_id)
        update_team_avg(awayTeamID,season_id,"College","opponent",home_team_outcome,game_data["homeTeam"]["totalShots"], game_data["homeTeam"]["stats"], game_data["awayTeam"]["totalShots"],away_team_conference_id)

        #Update Stats for All players aswell
        for player in all_players:
            update_player_avg(player["playerCode"],season_id,"College",player["position"],player["shots"],player["defense"],player["stats"],player["pos_min"])



    return new_game