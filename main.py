from flask import Flask, Response
from PySQLiteDBConnection import Connect
from json import dumps
from os import environ

app = Flask("Fun Seekers Tournament API")

environ['FLASK_ENV'] = 'production'

database = Connect("database.sqlite3")


@app.route("/test")
def test():
    database.connect()
    players = database.read_table("players_test")
    data = {}
    for player in players:
        data[player[0]] = {
            "summoner_name": player[1],
            "level": player[2]
        }
    return Response(status=200, response=dumps(data), content_type="application/json")


@app.route("/")
def home():
    database.connect()
    players = database.read_table("players")
    data = {}
    for player in players:
        data[player[0]] = {
            "summoner_name": player[1],
            "level": player[2]
        }
    return Response(status=200, response=dumps(data), content_type="application/json")


if __name__ == "__main__":
    app.run(port=1000)
