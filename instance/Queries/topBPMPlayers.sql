SELECT 
    p.name, 
    p.player_id,
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
    pavg.BPM,
	pavg.OEPM,
	pavg.DEPM,
	pavg.EPM
FROM players p
JOIN player_avg pavg ON pavg.player_id = p.player_id
JOIN players_skills psk ON psk.player_id = p.player_id
WHERE pavg.game_type = 'College'
  AND pavg.season_id = 2044
  AND psk.season_id = 2044
  AND pavg.GP >= 20 
  AND pavg.Min >= 10
ORDER BY pavg.BPM DESC;
