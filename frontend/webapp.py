from flask import Flask, render_template, request, redirect, url_for, jsonify
from getData import *

app = Flask(__name__)

@app.route("/", methods=["GET", "POST"])
def home():
    if request.method == "POST":
        team_id = request.form["code"]
        season_id = 2045
        return redirect(url_for('teamStats', code=team_id, season_year=season_id))
    
    return render_template('home.html')

#Route to get to Team Stats for Given year
@app.route("/teams/<code>/<season_year>/<game_type>")
@app.route('/teams/<code>/<season_year>', methods=['GET', 'POST'], defaults={'game_type': 'College'})
def teamStats(code, season_year, game_type):
    team_id = int(code)
    season_id = int(season_year)

    roster = getRoster(team_id, season_id)
    team_avg = getTeamAvg(team_id, season_id, game_type)
    opp_avg = getOppAvg(team_id, season_id, game_type)
    team_player_avg = getTeamPlayerAvg(team_id, game_type, season_id)
    team_offense = getTeamOffense(team_id,season_id,game_type)
    team_defense = getTeamDefense(team_id,season_id,game_type)
    team_rank = getTeamRank(team_id,season_id,game_type)
    opp_rank = getOppRank(team_id,season_id,game_type)

    team_avg['ORB_P'] = 100 * (team_avg['Off'] / (team_avg['Off'] + opp_avg['Def']))
    team_avg['DRB_P'] = 100 * (team_avg['Def'] / (team_avg['Def'] + opp_avg['Off']))

    team_avg["TO_P"] = 100 * (team_avg["TO"] / (team_avg["FG_A"] + .44 * (team_avg["FT_A"] + team_avg["TO"])))
    opp_avg["TO_P"] = 100 * (opp_avg["TO"] / (opp_avg["FG_A"] + .44 * (opp_avg["FT_A"] + opp_avg["TO"])))

    team_avg["ORtg"] = 100 * (team_avg["PTS"] / team_avg["Poss"])
    team_avg["DRtg"] = 100 * (opp_avg["PTS"] / opp_avg["Poss"])

    return render_template('teamPage.html', roster=roster, team_stats=team_avg, opp_stats=opp_avg, player_stats=team_player_avg, team_offense = team_offense, team_defense=team_defense, team_rank=team_rank, opp_rank=opp_rank)

#Route to get to Game Log for given year
@app.route('/teams/<code>/<season_year>/gamelog')
def gameLog(code, season_year):
    team_id = int(code)
    season_id = int(season_year)

    game_log = getTeamGameLog(team_id,season_id)

    return render_template('teamGameLog.html', game_log = game_log, season_id = season_id)



if __name__ == '__main__':
    app.run(port=3000, debug=True)
