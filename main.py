import json
import streamlit as st
from streamlit_ace import st_ace

from pandasql import sqldf
from pandasql.sqldf import PandaSQLException

from core.database import Database

from components.challenge import ChallengePanel

st.set_page_config(layout="wide")
params = st.experimental_get_query_params()

practice_mode = True

if "db" in params:
    practice_mode = False

if practice_mode:
    st.title("SQL Live coding practice tool")
    db_col, diff_col = st.columns(2)
    with open(f'data/config.json', 'r') as f:
        practice_list = json.load(f).get("practice")

    with db_col:
        db = st.selectbox(
            "Pick a database",
            practice_list,
            format_func=lambda x: x.title()
        )

    try:
        with open(f"data/{db}/questions.json", 'r') as f:
            diff_list = list(json.load(f).keys())
    except FileNotFoundError:
        diff_list = []

    with diff_col:
        difficulty = st.radio(
            "Select a difficulty level",
            ["playground"] + diff_list,
            format_func=lambda x: x.title(),
            horizontal=True
        )
else:
    st.title("SQL Live coding interview tool")
    db = params.get("db")[0]
    difficulty = params.get("difficulty", [None])[0]

database = Database(db)

st.markdown("""---""")

challenge, code, result = st.columns(3)
with challenge:
    challenge_panel = ChallengePanel(database, difficulty)
    challenge_panel.render()

with code:
    st.write("""
    In the following code box you can execute your SQL code and see your results below.
    Complete the tasks given by your interviewer.
    """)

    res = st_ace(theme="tomorrow_night_blue", language="sql")

with result:
    st.subheader("Result")
    if res:
        try:
            df = sqldf(res, database.file_dict)
            st.write(df)
        except PandaSQLException as e:
            e_str = str(e)
            error_msg = e_str.split("[")[0].strip()
            error_text = f"""
            Oops! Something went wrong. Find the error message below:  
            {error_msg}
            """
            st.error(error_text, icon="🚨")
        except ValueError as e:
            e_str = str(e).lower()
            if "duplicate" in e_str:
                st.error("You cannot have two columns with the same name", icon="🚨")
