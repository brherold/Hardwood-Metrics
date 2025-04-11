SELECT 
	DISTINCT
    p.name, 
    p.player_id,
	t.team_name,
    CASE 
        WHEN pavg.PG_Min >= pavg.SG_Min AND pavg.PG_Min >= pavg.SF_Min AND pavg.PG_Min >= pavg.PF_Min AND pavg.PG_Min >= pavg.C_Min THEN 'PG'
        WHEN pavg.SG_Min >= pavg.PG_Min AND pavg.SG_Min >= pavg.SF_Min AND pavg.SG_Min >= pavg.PF_Min AND pavg.SG_Min >= pavg.C_Min THEN 'SG'
        WHEN pavg.SF_Min >= pavg.PG_Min AND pavg.SF_Min >= pavg.SG_Min AND pavg.SF_Min >= pavg.PF_Min AND pavg.SF_Min >= pavg.C_Min THEN 'SF'
        WHEN pavg.PF_Min >= pavg.PG_Min AND pavg.PF_Min >= pavg.SG_Min AND pavg.PF_Min >= pavg.SF_Min AND pavg.PF_Min >= pavg.C_Min THEN 'PF'
        ELSE 'C'
    END AS Primary_Position,
    pavg.Min,
    pavg.OBPM, 
    pavg.DBPM, 
    pavg.BPM
FROM players p
JOIN player_avg pavg ON pavg.player_id = p.player_id
JOIN teams t on t.team_id = p.team_id
JOIN team_avg tavg on tavg.team_id = t.team_id
WHERE pavg.game_type = 'Conference'
  AND pavg.season_id = 2044
  AND pavg.GP >= 20 
  AND pavg.Min >= 20
  and tavg.conference_id <= 15
 
ORDER BY pavg.BPM DESC;
