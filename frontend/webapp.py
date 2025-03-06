from flask import Flask, render_template, request, redirect, url_for, jsonify
import requests

api_url = "http://127.0.0.1:5000"


app = Flask(__name__)

@app.route("/", methods=["GET","POST"])
def home():
    if request.method == "GET":
        code = int(request.args.get("code"))
        if code > 1010 and code < 1000000:
            #Player Code
            response = requests.get(f"{api_url}/players/{code}/avg/2044/Conference")
        elif code > 1010:
            #Game Code
            response = requests.get(f"{api_url}/games")
        else:
            response = requests.get(f"{api_url}/teams")
        if response.status_code == 200:
            data = response.json()
            print("worked")
        else:
            print("error")
        return data
    return render_template('home.html')


if __name__ == '__main__':
    app.run(port=3000)
    app.run(debug=True)