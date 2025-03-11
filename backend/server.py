from flask import Flask, request, jsonify
from scripts.pygetPlayerInfo import *
from scripts.dbOperations import *
from scripts.pygameAnalyzerAPI import *
from scripts.helperFunctions import *
from scripts.teamRosterInfo import *
from scripts.getRequest import *

from models import *
import os

BASE_DIR = os.path.abspath(os.path.dirname(__file__))
DB_PATH = os.path.join(BASE_DIR, '..', 'instance', 'basketball.db')

SQLALCHEMY_DATABASE_URI = f'sqlite:///{DB_PATH}'

# Initialize Flask app and SQLAlchemy
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = SQLALCHEMY_DATABASE_URI #'sqlite:///basketball.db' 
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db.init_app(app)




#API Build
@app.route('/')
def home():
    return "Welcome to the Hardwood API!"

#Add season
@app.route('/seasons',methods=["POST"])
def add_season():
    url = request.json.get('url')
    if "http://onlinecollegebasketball.org" not in url:
        return jsonify({"error": "URL is not for Hardwood"})
    else:
        current_season = find_current_season()
        existing_season = Season.query.filter_by(season_id=current_season).first()
        if not existing_season:
            new_season = Season(season_id = current_season ,year = current_season)

            db.session.add(new_season)  
            db.session.commit() 

        return jsonify({"message": "Season found or added successfully",
                        "season_id": current_season}), 200

#Add conferences
@app.route('/conferences',methods=['POST'])
def add_conferences():
    url = request.json.get('url')
    if "http://onlinecollegebasketball.org" not in url:
        return jsonify({"error": "URL is not for Hardwood"})
    else:
        conference_adder()

        return jsonify({"message": "Conferences added successfully",
                        }), 200
    
    
        

#Add player 
@app.route('/players',methods=["PUT","POST", "GET"])
def player():
    player_url = request.json.get('player_url')

    if not player_url:
        return jsonify({"error":"Player URL not found"})
    
    player_id = int(player_url.split("/")[-1])

    if request.method == "GET":
        player = Player.query.get(player_id)
        if player:
            return jsonify({
                "message": "GET Player found or added successfully",
                "player_id": player.player_id,
                "player_name": player.name,
                "team_id": player.team_id
            }), 200 
        else:
            return jsonify({
                "message": "Failed to find player"
            })
        pass
    else:
        if request.method == "POST":
            player = get_or_add_player(player_id)
        elif request.method == "PUT":
            player = update_player_helper(player_id)

        if player:
            return jsonify({
                "message": "Player found or added successfully",
                "player_id": player.player_id,
                "player_name": player.name,
                "team_id": player.team_id
            }), 200  # HTTP 200 OK
        else:
            return jsonify({
                "message": "Failed to add player"
            }), 400  # HTTP 400 Bad Request

#Get player Game Logs
@app.route('/players/<int:player_id>/gamelog/<int:season_id>',methods=["GET"])
def get_player_gamelog(player_id,season_id):
    game_log = game_log_finder(player_id,season_id)
    if not game_log:
        return jsonify({"error": "No game log for the player for that given season"})
    else:
        return jsonify({
            "player_id": player_id,
            "season_id": season_id,
            "gamelog": game_log
        })

#Get player Averages in particular season and gametype
@app.route("/players/<int:player_id>/avg/<int:season_id>/<game_type>")
def get_player_avg(player_id,season_id,game_type):
    player_avg = avg_stats_finder(player_id,season_id,game_type)
    if not player_avg:
        return jsonify({"error": "No averages for the player for that given season"})
    else:
        return jsonify({
            "player_id": player_id,
            "season_id": season_id,
            "game_type": game_type,
            "playerAvg": player_avg
        })



#Add team to DB 
@app.route('/teams',methods=["GET","POST"])
def team():
    if request.method == "POST":
        team_url = request.json.get('team_url')

        if not team_url:
            return jsonify({"error":"Team URL not found"})
        
        team_id = int(team_url.split("/")[-1])

        
        if team_id > 1010:
            return jsonify({
                "message": "Not a team Code"
            }), 400  # HTTP 400 Bad Request

        team = get_or_add_team(team_id)

        if team:
            return jsonify({
                "message": "Team found or added successfully",
                "team_id": team.team_id,
                "team_name": team.team_name
            }), 200  # HTTP 200 OK
        else:
            return jsonify({
                "message": "Failed to add Team"
            }), 400  # HTTP 400 Bad Request
    
    elif request.method == "GET":
        pass


#Add Game to DB
@app.route("/games",methods=["GET","POST"])
def game():
    game_url = request.json.get("game_url")
    game_id = int(game_url.split("/")[-1])

    if request.method == "POST":
        game = add_game_helper(game_id) #Adds game & teams to DB
        
        
    
        if game:
            return jsonify({
                "message": "Game found or added successfully",
                "game_id": game.game_id,
                "game_type": game.game_type,
                "season_year": game.season_id,
                "home_team_id": game.home_team_id,
                "away_team_id" : game.away_team_id
            }), 200  # HTTP 200 OK
        else:
            return jsonify({
                "message": "Failed to add Game"
            }), 400  # HTTP 400 Bad Request
        
    #GET request for getting data from a game
    elif request.method == "GET":
        
        pass




#Test Get Request for Game 
#






if __name__ == '__main__':
    # Create all tables based on the models
    with app.app_context():
        db.create_all()

    app.run(debug=True)