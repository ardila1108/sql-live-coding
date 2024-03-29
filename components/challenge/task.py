import json
import glob
import streamlit as st


class TaskDefinition:
    def __init__(self, database, difficulty):
        self.question_info = None
        self._get_question_info(database.path, difficulty)

    def _get_question_info(self, path, difficulty):
        file_list = [file.split("/")[-1] for file in glob.glob(path + "/*.json")]
        if "questions.json" in file_list:
            with open(f'{path}/questions.json', 'r') as f:
                question_info = json.load(f)
            self.question_info = question_info.get(difficulty)

    def render(self):
        if self.question_info:
            st.header("Task")
            statement = self.question_info.get("statement")
            cols = self.question_info.get("cols")
            notes = self.question_info.get("notes")
            st.write(statement)
            if notes:
                st.write("Considerations:")
                for note in notes:
                    st.markdown("- " + note)
            st.write(f"Your result table should have {len(cols)} columns:")
            for col in cols:
                st.markdown("- " + col)
