SELECT DISTINCT 
    p.name, 
    p.team_id, 
    tavg.conference_id, 
	tavg.SOS,
    psk.*, 
    pavg.*
FROM players p
JOIN players_skills psk
  ON psk.player_id = p.player_id
  AND psk.season_id = 2045
JOIN (
    SELECT DISTINCT team_id, season_id, conference_id, SOS
    FROM team_avg
    WHERE season_id = 2045
      AND game_type = 'College'
	  and stat_type = "team"
) tavg ON tavg.team_id = p.team_id
JOIN player_avg pavg
  ON pavg.player_id = p.player_id
  AND pavg.game_type = 'College'
  AND pavg.season_id = 2045    -- <== Added season filter here
WHERE pavg.GP >= 20
  AND pavg.Min >= 15
ORDER BY tavg.conference_id;
