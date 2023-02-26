"""Populate the data in the database."""

import random
import datetime
import time

import requests

from env import APIS_FOR_USER_BRIEF, APIS_FOR_USER_DETAILED


def clamp(val, minv, maxv):
    return max(min(val, maxv), minv)


def fill_steps(user_id):
    # prepare time info
    now = datetime.datetime.now()
    cur_day = (
        datetime.datetime.fromordinal(now.toordinal())  # construct datetime
        - datetime.datetime(1970, 1, 1)  # hack: unix start time
    ).days

    for i in range(cur_day - 6, cur_day + 1):
        payload = {"id": user_id, "steps": [[i, random.randint(1000, 10000)]]}
        requests.patch(APIS_FOR_USER_DETAILED, json=payload, timeout=1000)


def create_user(user_id):
    payload = {
        "id": user_id,
    }
    requests.get(APIS_FOR_USER_BRIEF, json=payload, timeout=1000)


def fill_heartrates(user_id):
    # prepare time info
    now = datetime.datetime.now()
    timestamp = now.timestamp() - 1
    payload = {"id": user_id, "heartrates": [[timestamp, random.randint(55, 65)]]}
    requests.patch(APIS_FOR_USER_DETAILED, json=payload, timeout=1000)


def fill_anxieties(user_id):
    # prepare time info
    now = datetime.datetime.now()
    timestamp = now.timestamp() - 1
    payload = {"id": user_id, "anxieties": [[timestamp, random.randint(0, 4)]]}
    requests.patch(APIS_FOR_USER_DETAILED, json=payload, timeout=1000)


def main():
    user_ids = range(1, 11)
    for user_id in user_ids:
        create_user(user_id)
        fill_steps(user_id)

    # real time rendering
    while True:
        for user_id in user_ids:
            fill_heartrates(user_id)
            fill_anxieties(user_id)

        time.sleep(1)


if __name__ == "__main__":
    main()
