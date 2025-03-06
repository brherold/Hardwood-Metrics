// Use DBML to define your database structure
// Docs: https://dbml.dbdiagram.io/docs

Table seasons {
  season_id integer [pk]
  year integer
}

Table games {
  game_id integer [pk]
  game_type VARCHAR 
  season_id integer [ref: > seasons.season_id]
  home_team_id integer  [ref: - teams.team_id] 
  away_team_id integer [ref: - teams.team_id] 
}

Table teams {
  team_id integer [pk]
  team_name VARCHAR 
}

Table players {
  player_id integer [pk]
  team_id integer [ref: > teams.team_id]
  name VARCHAR
}

Table players_skills {
  player_id integer [ref: - players.player_id]
  season_id integer [ref: - seasons.season_id]
  height float
  weight integer
  wingspan float
  vertical float
  IS integer
  IQ integer
  OS integer
  Pass integer
  Rng integer
  Hnd integer
  Fin integer
  Drv integer
  Reb integer
  Str integer
  Idef integer
  Spd integer
  PDef integer
  Sta integer

  indexes {
    (player_id, season_id) [pk]
  }
}

Table player_stats {
  player_id integer [ref: > players.player_id]
  game_id integer [ref: > games.game_id]

  Min integer
  PTS integer
  FT_M integer 
  FT_A integer  
  Rebs integer
  AST integer
  STL integer
  BLK integer
  TO integer
  PF integer
  FD integer

  F_M integer
  F_A integer
  IS_M integer
  IS_A integer
  MR_M integer
  MR_A integer
  _3P_M integer
  _3P_A integer

  O_F_M integer
  O_F_A integer
  O_IS_M integer
  O_IS_A integer
  O_MR_M integer
  O_MR_A integer
  O_3P_M integer
  O_3P_A integer


  indexes {
    (player_id, game_id) [pk]
  }
}

Table team_stats {
    game_id integer [ref: > games.game_id]
    team_id integer [ref: > teams.team_id]

    F_M integer
    F_A integer
    IS_M integer
    IS_A integer
    MR_M integer
    MR_A integer
    _3P_M integer
    _3P_A integer
    O_F_M integer
    O_F_A integer
    O_IS_M integer
    O_IS_A integer
    O_MR_M integer
    O_MR_A integer
    O_3P_M integer
    O_3P_A integer

    indexes {
      (game_id, team_id) [pk]
  }
}

Table offense_stats {
    game_id integer [ref: > games.game_id]
    team_id integer [ref: > teams.team_id]
    
    defense_type VARCHAR

    F_M integer 
    F_A integer
    IS_M integer
    IS_A integer
    MR_M integer
    MR_A integer
    _3P_M integer
    _3P_A integer

    indexes {
      (game_id, team_id, defense_type) [pk]
  }
  
}

Table defense_stats {
    game_id integer [ref: > games.game_id]
    team_id integer [ref: > teams.team_id]
    defense_type VARCHAR

    F_M integer 
    F_A integer
    IS_M integer
    IS_A integer
    MR_M integer
    MR_A integer
    _3P_M integer
    _3P_A integer

    indexes {
      (game_id, team_id, defense_type) [pk]
  }
  
}

<: one-to-many. E.g: users.id < posts.user_id
>: many-to-one. E.g: posts.user_id > users.id
-: one-to-one. E.g: users.id - user_infos.user_id
<>: many-to-many. E.g: authors.id <> books.id