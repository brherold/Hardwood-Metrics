SELECT t.team_name, p.name, pst.*
from players p 
JOIN player_stats pst on pst.player_id = p.player_id
JOIN teams t on t.team_id = p.team_id
WHERE game_id = "1035575" 
ORDER BY p.team_id and pst.Min