with app.app_context():

    ############################################################################################
    #From Player Table 

    player = Player.query.get(202447)
    
    for stat in player.player_stats:
        print(stat.Min)
    
    for skill in player.player_skills:
        print(player.name, skill.height, skill.weight)
    
    
    #Since backref, can get information from both ways (from player can get the team name)
    player = Player.query.get(202447)
    print(player.team.team_name)

    #Gets Box score of all games the player has played
    player = Player.query.get(205173)
    for stats in player.player_stats:
        print({column.name: getattr(stats, column.name) for column in PlayerStats.__table__.columns})

    #Gets Game Log of all games the player has played in season 2044 that are not Exhibition games (also prints out the player's name and team name)
    player = Player.query.get(205173)
    print(player.name, player.team.team_name)
    for stats in player.player_stats:
        game = stats.game
        if game.season_id == 2044 and game.game_type != "Exhibition":
            print({column.name: getattr(stats, column.name) for column in PlayerStats.__table__.columns})

#Function that inputs playerID and seasonCode and ouputs avg mins played
def avg_stats_finder(player_id, season_id, game_type):
    averages = {}
    with app.app_context(): # Ensure the app context is active
        stats = [
    "Min", "PTS", "FG_M","FG_A", "_3P_M", "_3P_A", "FT_M", "FT_A", "Off" ,"Rebs", "AST", "STL", "BLK", "TO", "PF", "FD",
    "F_M", "F_A", "IS_M", "IS_A", "MR_M", "MR_A", 
    "O_F_M", "O_F_A", "O_IS_M", "O_IS_A", "O_MR_M", "O_MR_A", "O_3P_M", "O_3P_A"
]  # List of columns you want the average for
        for stat in stats:
            if game_type == "College":
                avg =  (
                db.session.query(func.avg(getattr(PlayerStats, stat)))
                .join(Game, PlayerStats.game_id == Game.game_id)
                .filter(PlayerStats.player_id == player_id, Game.season_id == season_id, (~Game.game_type.in_(["Exhibition", "Invitational"]) # does not include "Exhbiiton or Invitational"
))
                .scalar()
                )
            else:    
                avg =  (
                    db.session.query(func.avg(getattr(PlayerStats, stat)))
                    .join(Game, PlayerStats.game_id == Game.game_id)
                    .filter(PlayerStats.player_id == player_id, Game.season_id == season_id, Game.game_type == game_type)
                    .scalar()
                )
                
            averages[stat] = round(avg,1) if avg is not None else None
    return averages

avg = avg_stats_finder(205173, 2044,"College")

print(avg)

#Function that gets game logs of a player in a season
def game_log_finder(player_id, season_id):
    gameCount = 1
    gameLogDic = {}
    with app.app_context():
        player = Player.query.get(player_id)
        for stat in player.player_stats:
            gameInfo = stat.game
            if gameInfo.season_id == 2044:
                gameLogDic[gameCount] = {column.name: getattr(stat, column.name) for column in PlayerStats.__table__.columns}
                gameCount += 1
        return gameLogDic

glf = game_log_finder(205173,2044)
print(glf)


    ######################################################################################################
    #From Team Table

        
    #Gets all playerIDs in a given team
    team = Team.query.get(533)
    for player in team.players:
        print(player.player_id)
    
    
    #Gets all player name, height, weight from team code 533 in season 2044
    team = Team.query.get(533)
    for player in team.players:
        for skill in player.player_stats:
            if skill.season_id == 2044:
                print(player.name, skill.height, skill.vertical)

    #Gets all team_stats 
    team = Team.query.get(533)
    print(team.team_name)
    for team_stats in team.team_stats:
        print({column.name: getattr(team_stats, column.name) for column in TeamStats.__table__.columns})
    
    ##################################################################################################
    #From TeamStats Table
    
    #Gets the season_id and game_type from teamStats table of gameID 1029591 and teamID 533
    team_stats = TeamStats.query.get((1029591,533))
    print(team_stats.game.season_id, team_stats.game.game_type)

    #Gets Team_Stats from teamID 533 in season 2044 that are not exhibition games
    team = Team.query.get(533)
    print(team.team_name)
    for team_stats in team.team_stats:
        game_info = team_stats.game
        if game_info.season_id == 2044 and game_info.game_type != "Exhibition":
            print({column.name: getattr(team_stats, column.name) for column in TeamStats.__table__.columns})

    #Gets Avgs of All players in a Team in a given season and game_Type
    def avg_player_stats_from_Team(team_id,season_id,game_type):
        stats = []
        with app.app_context():
            team = Team.query.get(team_id)
            players = team.players
            for player in players:
                player_skills = player.player_skills
                for player_skill in player_skills:
                    if player_skill.season_id == season_id:
                        stats.append((player.name,avg_stats_finder(player.player_id,season_id,game_type)))
        
        return stats

