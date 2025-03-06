SELECT p.name, psk.Pos, psk.height, psk.vertical, pavg.*
FROM players p 
JOIN players_skills psk on psk.player_id = p.player_id
JOIN player_avg pavg on pavg.player_id = p.player_id
WHERE p.team_id = 58 and pavg.game_type = "Conference"
ORDER BY pavg.Min desc