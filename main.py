import streamlit as st
from streamlit_ace import st_ace

from pandasql import sqldf
from pandasql.sqldf import PandaSQLException

from components.challenge import ChallengePanel

st.set_page_config(layout="wide")
params = st.experimental_get_query_params()

st.title("SQL Live coding tool")

if "db" in params:

    challenge, code = st.columns(2)
    with challenge:
        challenge_panel = ChallengePanel(params.get("db")[0], params.get("difficulty", [None])[0])
        challenge_panel.render()

    with code:
        st.write("""
        In the following code box you can execute your SQL code and see your results below.
        Complete the tasks given by your interviewer.
        """)

        res = st_ace(theme="tomorrow_night_blue", language="sql")

        if res:
            try:
                df = sqldf(res, challenge_panel.erd.file_dict)
                st.subheader("Result")
                st.write(df)
            except PandaSQLException as e:
                e_str = str(e)
                error_msg = e_str.split("[")[0].strip()
                error_text = f"""
                Oops! Something went wrong. Find the error message below:  
                {error_msg}
                """
                st.error(error_text, icon="🚨")
