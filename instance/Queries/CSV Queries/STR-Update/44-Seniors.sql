--Gets Everyone 
SELECT DISTINCT psk.*, pavg.*
FROM player_avg pavg
LEFT JOIN players_skills psk 
  ON psk.player_id = pavg.player_id 
  AND psk.season_id = pavg.season_id
WHERE pavg.game_type = 'College' 
  AND pavg.GP >= 20 
  AND pavg.Min >= 15
  AND psk.season_id = 2044
  AND psk.class IN ('SR', 'RS SR')
