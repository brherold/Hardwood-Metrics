select p.name, psk.*
from players p 
join players_skills psk on p.player_id = psk.player_id
WHERE p.team_id = 533
ORDER BY psk.SI desc