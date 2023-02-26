import streamlit as st

from users import plot_users


def set_title():
    st.write(
        """
    ## Music Therapy Patient Management Portal

    """
    )


def main():
    set_title()
    plot_users()


if __name__ == "__main__":
    main()
