SELECT DISTINCT psk.*, pavg.*
FROM player_avg pavg
LEFT JOIN players_skills psk 
  ON psk.player_id = pavg.player_id 
  AND psk.season_id = pavg.season_id
WHERE pavg.game_type = 'College' 
  AND pavg.GP >= 20 
  AND pavg.Min >= 10
  AND (PG_Min + SG_Min + SF_Min) >= 0.75 * Min


  
  
