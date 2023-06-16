import streamlit as st
from components.challenge import EntityRelationshipDiagram, TaskDefinition


class ChallengePanel:
    def __init__(self, db, difficulty):
        path = f"data/{db}"
        self.erd = EntityRelationshipDiagram(path)
        self.task_definition = TaskDefinition(path, difficulty)

    def render(self):
        st.write("""
        All your assessments will be done based on the Entity Relationship Diagram presented below.
        Take your time to understand it and ask any questions you see fit.
        """)

        self.erd.render()
        self.task_definition.render()
