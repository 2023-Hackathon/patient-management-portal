from flask import Flask
from flask_restful import Api

from _profile import UserProfile
from _stats import UserStats

app = Flask(__name__)
api = Api(app)


def add_resources():
    resources = [
        (UserProfile, "/user/profile"),
        (UserStats, "/user/stats"),
    ]

    for handler_cls, path in resources:
        api.add_resource(handler_cls, path)


add_resources()


if __name__ == "__main__":
    app.run(debug=True)
