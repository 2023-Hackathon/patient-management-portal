from flask_restful import Resource, reqparse


class UserProfile(Resource):
    def patch(self):
        parser = reqparse.RequestParser()
        parser.add_argument("id", type=int, help="Expected user id. Got nothing.", required=True)

        args = parser.parse_args(strict=True)
        print(args)

        return {}
