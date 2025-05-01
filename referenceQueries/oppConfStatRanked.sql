WITH context AS (
    SELECT DISTINCT conference_id, season_id, game_type, stat_type
    FROM team_avg
    WHERE team_id = ?
      AND season_id = ?
      AND game_type = ?
      AND stat_type = 'opponent'
),
ranked AS (
    SELECT 
        t.team_id,
        
        -- Playing time
        RANK() OVER (PARTITION BY t.conference_id, t.season_id, t.game_type, t.stat_type ORDER BY t.GW ASC) AS GW,
        RANK() OVER (PARTITION BY t.conference_id, t.season_id, t.game_type, t.stat_type ORDER BY (t.GP - t.GW) DESC) AS GL,
        RANK() OVER (PARTITION BY t.conference_id, t.season_id, t.game_type, t.stat_type ORDER BY t.Min DESC) AS Min,
        
        -- Scoring
        RANK() OVER (PARTITION BY t.conference_id, t.season_id, t.game_type, t.stat_type ORDER BY t.PTS ASC) AS PTS,
        RANK() OVER (PARTITION BY t.conference_id, t.season_id, t.game_type, t.stat_type ORDER BY t.FG_M ASC) AS FG_M,
        RANK() OVER (PARTITION BY t.conference_id, t.season_id, t.game_type, t.stat_type ORDER BY t.eFG_P ASC) AS eFG_P,
        RANK() OVER (PARTITION BY t.conference_id, t.season_id, t.game_type, t.stat_type ORDER BY t._3P_M ASC) AS _3P_M,
        RANK() OVER (PARTITION BY t.conference_id, t.season_id, t.game_type, t.stat_type ORDER BY t._3P_P ASC) AS _3P_P,
        RANK() OVER (PARTITION BY t.conference_id, t.season_id, t.game_type, t.stat_type ORDER BY t._2P_M ASC) AS _2P_M,
        RANK() OVER (PARTITION BY t.conference_id, t.season_id, t.game_type, t.stat_type ORDER BY t._2P_P ASC) AS _2P_P,
        RANK() OVER (PARTITION BY t.conference_id, t.season_id, t.game_type, t.stat_type ORDER BY t.FT_M ASC) AS FT_M,
        RANK() OVER (PARTITION BY t.conference_id, t.season_id, t.game_type, t.stat_type ORDER BY t.FT_P ASC) AS FT_P,
        
        -- Efficiency
        RANK() OVER (PARTITION BY t.conference_id, t.season_id, t.game_type, t.stat_type ORDER BY t.PLUS ASC) AS PLUS,
        RANK() OVER (PARTITION BY t.conference_id, t.season_id, t.game_type, t.stat_type ORDER BY t.PITP ASC) AS PITP,
        RANK() OVER (PARTITION BY t.conference_id, t.season_id, t.game_type, t.stat_type ORDER BY t.FBP ASC) AS FBP,
        
        -- Rebounding
        RANK() OVER (PARTITION BY t.conference_id, t.season_id, t.game_type, t.stat_type ORDER BY t.Off ASC) AS Off,
        RANK() OVER (PARTITION BY t.conference_id, t.season_id, t.game_type, t.stat_type ORDER BY t.Def ASC) AS Def,
        RANK() OVER (PARTITION BY t.conference_id, t.season_id, t.game_type, t.stat_type ORDER BY t.Rebs ASC) AS Rebs,
        
        -- Playmaking
        RANK() OVER (PARTITION BY t.conference_id, t.season_id, t.game_type, t.stat_type ORDER BY t.AST ASC) AS AST,
        RANK() OVER (PARTITION BY t.conference_id, t.season_id, t.game_type, t.stat_type ORDER BY t.STL ASC) AS STL,
        
        -- Defense
        RANK() OVER (PARTITION BY t.conference_id, t.season_id, t.game_type, t.stat_type ORDER BY t.BLK ASC) AS BLK,
        RANK() OVER (PARTITION BY t.conference_id, t.season_id, t.game_type, t.stat_type ORDER BY t.FD ASC) AS FD,
        
        -- Attempts
        RANK() OVER (PARTITION BY t.conference_id, t.season_id, t.game_type, t.stat_type ORDER BY t.FG_A ASC) AS FG_A,
        RANK() OVER (PARTITION BY t.conference_id, t.season_id, t.game_type, t.stat_type ORDER BY t._3P_A ASC) AS _3P_A,
        RANK() OVER (PARTITION BY t.conference_id, t.season_id, t.game_type, t.stat_type ORDER BY t._2P_A ASC) AS _2P_A,
        RANK() OVER (PARTITION BY t.conference_id, t.season_id, t.game_type, t.stat_type ORDER BY t.FT_A ASC) AS FT_A,
        
        -- Negative stats
        RANK() OVER (PARTITION BY t.conference_id, t.season_id, t.game_type, t.stat_type ORDER BY t."TO" DESC) AS "TO",
        RANK() OVER (PARTITION BY t.conference_id, t.season_id, t.game_type, t.stat_type ORDER BY t.PF DESC) AS PF,
        
        -- Neutral stats
        RANK() OVER (PARTITION BY t.conference_id, t.season_id, t.game_type, t.stat_type ORDER BY t.DIST DESC) AS DIST,
        RANK() OVER (PARTITION BY t.conference_id, t.season_id, t.game_type, t.stat_type ORDER BY t.Poss DESC) AS Poss,
        RANK() OVER (PARTITION BY t.conference_id, t.season_id, t.game_type, t.stat_type ORDER BY t._3PAr DESC) AS _3PAr,
        RANK() OVER (PARTITION BY t.conference_id, t.season_id, t.game_type, t.stat_type ORDER BY t.FTr ASC) AS FTr

    FROM team_avg t
    JOIN context c
      ON t.conference_id = c.conference_id
     AND t.season_id = c.season_id
     AND t.game_type = c.game_type
     AND t.stat_type = c.stat_type
)
SELECT *
FROM ranked
WHERE team_id = ?;
