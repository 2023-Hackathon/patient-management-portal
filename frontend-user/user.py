"""Load single user detailed info."""

import time
import datetime

import streamlit as st
import pandas as pd

import req
from env import APIS_FOR_USER_DETAILED


# user_id = 1 for demo purpose
def load_single_user_detail(user_id=1):
    request_payload = {
        "id": user_id,
        "steps-day": 7,
        "anxieties-second": 15,
        "heartrates-second": 15,
    }

    details = req.get(APIS_FOR_USER_DETAILED, json=request_payload, timeout=1000)

    # 1. display bar chart
    seven_day_bar_chart(details["steps"])

    # 2. display real time
    delta_heartrate = realtime_heartrate(details["heartrates"])
    delta_anxiety = realtime_anxiety(details["anxieties"])

    # 3. real time loop starts
    while True:
        time.sleep(1)

        details = req.get(APIS_FOR_USER_DETAILED, json=request_payload, timeout=1000)
        delta_heartrate = realtime_heartrate(details["heartrates"], delta_heartrate)
        delta_anxiety = realtime_anxiety(
            details["anxieties"], delta_anxiety
        )


def seven_day_bar_chart(steps):
    steps = list(
        map(
            lambda item: [
                (
                    datetime.datetime(1970, 1, 1) + datetime.timedelta(days=item[0])
                ).strftime("%Y-%m-%d"),
                item[1],
            ],
            steps,
        )
    )

    chart_data = pd.DataFrame(steps, columns=["day", "Steps"])

    st.write(
        """
    #### Number of Steps in last 7 days

    """
    )
    st.bar_chart(chart_data, x="day", y="Steps")


def realtime_heartrate(heartrates, delta=None):
    heartrates = list(
        map(
            lambda item: [
                (
                    datetime.datetime(1970, 1, 1) + datetime.timedelta(seconds=item[0])
                ).strftime("%H:%M:%S"),
                item[1],
            ],
            heartrates,
        )
    )
    chart_data = pd.DataFrame(heartrates, columns=["timestamp", "Pulse Rate"])

    if delta is None:
        st.write(
            """
        #### Pulse rate in last 15 seconds

        """
        )
        return st.line_chart(chart_data, x="timestamp", y="Pulse Rate")

    return delta.line_chart(chart_data, x="timestamp", y="Pulse Rate")


def realtime_anxiety(anxieties, delta=None):
    anxieties = list(
        map(
            lambda item: [
                (
                    datetime.datetime(1970, 1, 1) + datetime.timedelta(seconds=item[0])
                ).strftime("%H:%M:%S"),
                item[1],
            ],
            anxieties,
        )
    )

    chart_data = pd.DataFrame(
        anxieties, columns=["timestamp", "Degree of Anxieties"]
    )

    if delta is None:
        st.write(
            """
        #### Degree of anxieties in last 15 seconds

        """
        )
        return st.line_chart(chart_data, x="timestamp", y="Degree of Anxieties")

    return delta.line_chart(chart_data, x="timestamp", y="Degree of Anxieties")
