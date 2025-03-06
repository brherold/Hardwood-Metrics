SELECT DISTINCT p.name, t.team_name, pavg.GP, pavg.OBPM, pavg.DBPM, pavg.BPM
from player_avg pavg
JOIN players p on p.player_id = pavg.player_id
JOIN teams t on t.team_id = p.team_id
JOIN team_avg tavg on tavg.team_id = t.team_id
WHERE tavg.conference_id = 8 and  pavg.game_type = "Conference" and pavg.gp >= 7 and pavg.Min >= 20
ORDER BY pavg.BPM desc
