from flask_restful import Resource, reqparse


class UserStats(Resource):
    def patch(self):
        parser = reqparse.RequestParser()
        parser.add_argument("id", type=int, help="Expected user id. Got nothing.", required=True)
        parser.add_argument("steps", type=list, required=False, action="append")
        parser.add_argument("heartrates", type=list, required=False, action="append")
        parser.add_argument("currents", type=list, required=False, action="append")
        parser.add_argument("curetimes", type=list, required=False, action="append")

        # Check arguments

        args = parser.parse_args(strict=True)
        print(args)

        return {}
