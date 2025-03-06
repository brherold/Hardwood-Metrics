SELECT tst.*
From games g 
JOIN team_stats tst on tst.game_id = g.game_id
WHERE g.game_type = "Conference" and tst.team_id = 545