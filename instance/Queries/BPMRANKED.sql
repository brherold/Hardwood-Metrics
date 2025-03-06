SELECT t.team_name, t.team_id, tavg.OBPM, tavg.DBPM, tavg.BPM
FROM teams t
JOIN team_avg tavg on tavg.team_id = t.team_id
WHERE tavg.stat_type = "team" and tavg.game_type = "College"
ORDER BY tavg.BPM DESC

