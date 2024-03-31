from flask import Flask, Response
from PySQLiteDBConnection import Connect
from json import dumps
from os import environ

app = Flask("Fun Seekers Tournament API")

environ["FLASK_APP"] = "main.py"
environ["FLASK_ENV"] = "production"

database = Connect("database.sqlite3")


def get_data(table: str) -> dict:
    players = database.read_table(table)
    data = {}
    for player in players:
        data[player[0]] = {
            "summoner_name": player[1],
            "level": player[2]
        }
    return data


def add_access_controls(response: Response) -> Response:
    response.headers["Access-Control-Allow-Origin"] = "*"
    response.headers["Access-Control-Allow-Methods"] = "GET"
    return response


@app.errorhandler(404)
def resouerce_not_found(error):
    return Response(status=404, response=dumps({"error": 404, "message": "Resource not found"}), content_type="application/json")


@app.route("/test", methods=["GET"])
def test():
    database.connect()
    data = get_data("players_test")
    return add_access_controls(Response(status=200, response=dumps(data), content_type="application/json"))


@app.route("/", methods=["GET"])
def home():
    database.connect()
    data = get_data("players")
    return add_access_controls(Response(status=200, response=dumps(data), content_type="application/json"))


if __name__ == "__main__":
    app.run()
