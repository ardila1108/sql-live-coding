import json
import streamlit as st


class TaskDefinition:
    def __init__(self, path, difficulty):
        self.accepted_difficulties = ["low", "medium", "high"]
        self.question_info = None
        if difficulty not in self.accepted_difficulties:
            self.question_info = self._get_question_info(path, difficulty)

    @staticmethod
    def _get_question_info(path, difficulty):
        with open(f'{path}/questions.json', 'r') as f:
            question_info = json.load(f)

        return question_info.get(difficulty)

    def render(self):
        if self.question_info:
            st.header("Task")
            statement = self.question_info.get("statement")
            cols = self.question_info.get("cols")
            st.write(statement)
            st.write(f"Your result table should have {len(cols)} columns:")
            for col in cols:
                st.markdown("- " + col)
