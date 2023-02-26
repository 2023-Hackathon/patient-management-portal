import datetime
import itertools
import random
from flask_restful import Resource, reqparse, abort

from faker import Faker

from database import (
    get_db,
    execute_single_task,
    execute_single_task_no_return,
    execute_multiple_tasks_no_return,
)


# get brief user info
# create a new user if doesn't exist
def get_brief_info(user_id):
    db = get_db()

    # make sure user exists
    faker = Faker()

    # assume binary gender now;
    # 0 => woman, 1 => man
    name, age, gender = (
        faker.name(),
        random.randint(18, 90),
        random.choice(["Male", "Female"]),
    )

    # if already exists, ignore the command
    execute_single_task_no_return(
        db,
        "INSERT OR IGNORE into users (id, name, age, gender) VALUES (?, ?, ?, ?)",
        (user_id, name, age, gender),
    )

    # guarantee to have at least one element
    name, age, gender = execute_single_task(
        db, "SELECT name, age, gender FROM users where id = ?", (user_id,)
    )[0]

    return name, age, gender


class UserStatsBrief(Resource):
    def get(self):
        parser = reqparse.RequestParser()
        parser.add_argument(
            "id", type=int, help="Expected user id. Got nothing.", required=True
        )

        args = parser.parse_args(strict=True)
        user_id = args["id"]
        name, age, gender = get_brief_info(user_id)

        def get_anxiety():
            db = get_db()
            anxieties = execute_single_task(
                db, "SELECT AVG(value) from anxieties WHERE user_id = ?", (user_id,)
            )
            return anxieties[0][0]

        return {
            "data": {
                "id": user_id,
                "name": name,
                "age": age,
                "gender": gender,
                "anxiety": get_anxiety(),
            }
        }


class UserStatsDetailed(Resource):
    def get(self):
        parser = reqparse.RequestParser()
        parser.add_argument(
            "id", type=int, help="Expected user id. Got nothing.", required=True
        )
        parser.add_argument("steps-day", type=int, default=7)
        parser.add_argument("anxieties-second", type=int, default=15)
        parser.add_argument("heartrates-second", type=int, default=15)

        args = parser.parse_args(strict=True)

        # get user info
        user_id = args["id"]
        name, age, gender = get_brief_info(user_id)

        # prepare time info
        now = datetime.datetime.now()
        timestamp = int(now.timestamp())
        cur_day = (
            datetime.datetime.fromordinal(now.toordinal())  # construct datetime
            - datetime.datetime(1970, 1, 1)  # hack: unix start time
        ).days

        db = get_db()

        def get_steps_history():
            steps_start_day = cur_day - args["steps-day"]
            return sorted(
                execute_single_task(
                    db,
                    "SELECT day, value from steps WHERE user_id = ? AND day > ?",
                    (user_id, steps_start_day),
                )
            )

        def get_anxieties_history():
            anxieties_start_timestamp = timestamp - args["anxieties-second"]
            return sorted(
                execute_single_task(
                    db,
                    "SELECT timestamp, value from anxieties WHERE user_id = ? AND timestamp > ?",
                    (user_id, anxieties_start_timestamp),
                )
            )

        def get_heartrates_history():
            heartrates_start_timestamp = timestamp - args["anxieties-second"]
            return sorted(
                execute_single_task(
                    db,
                    "SELECT timestamp, value from heartrates WHERE user_id = ? AND timestamp > ?",
                    (user_id, heartrates_start_timestamp),
                )
            )

        return {
            "data": {
                "id": user_id,
                "name": name,
                "age": age,
                "gender": gender,
                "steps": get_steps_history(),
                "anxieties": get_anxieties_history(),
                "heartrates": get_heartrates_history(),
            }
        }

    @staticmethod
    def __check_format(arg, time_checker, argname: str):
        if not all(map(lambda item: len(item) == 2, arg)):
            abort(400, message=f"Expected {argname} to be a list [timestamp, value].")
        if not all(
            map(
                lambda item: isinstance(item[0], (int, float))
                and isinstance(item[1], int),
                arg,
            )
        ):
            abort(
                400,
                message="Type mismatch. 1st element should be either int or float. 2nd element should be int.",
            )
        if not all(map(time_checker, arg)):
            abort(400, message="timestamp should be less than the current timestamp.")

    def patch(self):
        parser = reqparse.RequestParser()
        parser.add_argument(
            "id", type=int, help="Expected user id. Got nothing.", required=True
        )
        parser.add_argument("steps", type=list, default=[], action="append")
        parser.add_argument("heartrates", type=list, default=[], action="append")
        parser.add_argument("anxieties", type=list, default=[], action="append")

        args = parser.parse_args(strict=True)

        # Check arguments
        # Format: [[timestamp, value]]
        now = datetime.datetime.now()
        timestamp = int(now.timestamp())
        cur_day = (
            datetime.datetime.fromordinal(now.toordinal())  # construct datetime
            - datetime.datetime(1970, 1, 1)  # hack: unix start time
        ).days

        def timestamp_checker(x):
            return x[0] <= timestamp

        def day_checker(x):
            return x[0] <= cur_day

        UserStatsDetailed.__check_format(args["steps"], day_checker, "steps")
        UserStatsDetailed.__check_format(
            args["heartrates"], timestamp_checker, "heartrates"
        )
        UserStatsDetailed.__check_format(
            args["anxieties"], timestamp_checker, "anxieties"
        )

        user_id = args["id"]
        db = get_db()

        def update_steps(steps: list):
            execute_multiple_tasks_no_return(
                db,
                itertools.repeat(
                    "INSERT or REPLACE into steps (user_id, day, value) VALUES (?, ?, ?)",
                    len(steps),
                ),
                map(lambda step: (user_id, step[0], step[1]), steps),
            )

        def update_heartrates(heartrates: list):
            execute_multiple_tasks_no_return(
                db,
                itertools.repeat(
                    "INSERT or REPLACE into heartrates (user_id, timestamp, value) VALUES (?, ?, ?)",
                    len(heartrates),
                ),
                map(
                    lambda heartrate: (user_id, int(heartrate[0]), heartrate[1]),
                    heartrates,
                ),
            )

        def update_anxieties(anxieties: list):
            execute_multiple_tasks_no_return(
                db,
                itertools.repeat(
                    "INSERT or REPLACE into anxieties (user_id, timestamp, value) VALUES (?, ?, ?)",
                    len(anxieties),
                ),
                map(lambda current: (user_id, int(current[0]), current[1]), anxieties),
            )

        update_steps(args["steps"])
        update_heartrates(args["heartrates"])
        update_anxieties(args["anxieties"])

        return {}
