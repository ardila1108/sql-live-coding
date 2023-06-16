import streamlit as st
from streamlit_ace import st_ace

from pandasql import sqldf
from pandasql.sqldf import PandaSQLException

from components import EntityRelationshipDiagram

params = st.experimental_get_query_params()

st.title("SQL Live coding tool")

if "db" in params:
    st.write("""
    All your assessments will be done based on the Entity Relationship Diagram presented below.
    Take your time to understand it and ask any questions you see fit.
    """)

    erd = EntityRelationshipDiagram(params.get("db")[0])
    erd.render()

    st.write("""
    In the code box below you can execute your SQL code and see your results below.
    Complete the tasks given by your interviewer.
    """)

    res = st_ace(theme="tomorrow_night_blue", language="sql")

    if res:
        try:
            df = sqldf(res, erd.file_dict)
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
