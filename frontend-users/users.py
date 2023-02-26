"""Load all users brief info."""

import pandas as pd
import streamlit as st

import req
from env import APIS_FOR_USERS_ID, APIS_FOR_USER_BRIEF


def plot_users():
    user_ids = req.get(APIS_FOR_USERS_ID, timeout=1000)

    pd_dataframe = {"id": [], "name": [], "age": [], "gender": [], "anxiety": []}

    for user_id in user_ids:
        request_payload = {"id": user_id}

        resp = req.get(APIS_FOR_USER_BRIEF, timeout=1000, json=request_payload)
        pd_dataframe["id"].append(resp["id"])
        pd_dataframe["name"].append(resp["name"])
        pd_dataframe["age"].append(resp["age"])
        pd_dataframe["gender"].append(resp["gender"])
        pd_dataframe["anxiety"].append(resp["anxiety"])

    pd_dataframe = pd.DataFrame(pd_dataframe)

    plot_serious_users(pd_dataframe)
    plot_users_brief(pd_dataframe)


def plot_users_brief(dataframe):
    st.write(
        """
    #### Patients

    """
    )
    st.dataframe(dataframe)


def plot_serious_users(dataframe):
    st.write(
        """
    #### Patients with serious mental problems

    """
    )

    # for demo purpose,
    # choose n == 5
    TOP_N = 5

    dataframe = dataframe.sort_values(by="anxiety", ascending=False)[:TOP_N]
    st.dataframe(dataframe)
