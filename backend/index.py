from flask import Flask, g
from flask_restful import Api

from database import init_db
from user_stats import UserStatsBrief, UserStatsDetailed
from users import Users

app = Flask(__name__)
api = Api(app)


def add_resources():
    resources = [
        (UserStatsBrief, "/user/stats/brief"),
        (UserStatsDetailed, "/user/stats/detailed"),
        (Users, "/users"),
    ]

    for handler_cls, path in resources:
        api.add_resource(handler_cls, path)


@app.teardown_appcontext
def close_connection(_):
    db = getattr(g, "_database", None)
    if db is not None:
        db.close()


def main():
    init_db()
    add_resources()


if __name__ == "__main__":
    main()
    app.run(host="0.0.0.0", port=8443, debug=True)
