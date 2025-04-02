SELECT p.name, psk.Pos,pavg.*
FROM players p
JOIN player_avg pavg on pavg.player_id = p.player_id
JOIN players_skills psk on psk.player_id = p.player_id
WHERE team_id = 533 AND pavg.game_type = "Conference"  and pavg.GP > 10 and pavg.Min > 10
ORDER BY pavg.BPM desc