import streamlit as st

from user import load_single_user_detail


def set_title():
    st.write(
        """
    ## Patient Data Visualizer

    """
    )


def main():
    set_title()
    load_single_user_detail()


if __name__ == "__main__":
    main()
