from flask_restful import Resource, reqparse

from database import get_db, execute_single_task


class Users(Resource):
    def get(self):
        db = get_db()
        rows = execute_single_task(db, "SELECT id FROM users", ())

        rows = list(
            map(
                lambda id: id[0],
                rows,
            )
        )

        return {"data": rows}
