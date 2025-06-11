SELECT 
    p.team_id,
    SUM(pavg.EPM * pavg.GP * pavg.Min) / SUM(pavg.GP * pavg.Min) AS EPM,
    SUM(pavg.BPM * pavg.GP * pavg.Min) / SUM(pavg.GP * pavg.Min) AS BPM,
    (1.00* tavg.GW / tavg.GP) AS WP,  -- Win Percentage (GW / GP)
    tavg.NetRtg
FROM players p
JOIN player_avg pavg ON pavg.player_id = p.player_id
JOIN team_avg tavg ON tavg.team_id = p.team_id
WHERE pavg.game_type = 'College'  
  AND pavg.season_id = 2044
  AND tavg.game_type = pavg.game_type
  AND tavg.stat_type = "team"
  AND tavg.season_id = pavg.season_id
GROUP BY p.team_id, tavg.GW, tavg.GP, tavg.NetRtg
ORDER BY EPM DESC;
