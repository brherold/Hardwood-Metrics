-- Slight change to 2044 Bigs.sql (more standaridized like other Position.sql

SELECT DISTINCT psk.*, pavg.*
FROM player_avg pavg
LEFT JOIN players_skills psk 
  ON psk.player_id = pavg.player_id 
  AND psk.season_id = pavg.season_id
WHERE pavg.game_type = 'College'
  AND pavg.season_id = 2045
  AND pavg.GP >= 20 
  AND pavg.Min >= 15 
  AND (PF_Min + C_Min) >= 0.75 * Min
  