import glob
import json
import streamlit as st
import pandas as pd
from pandaserd import ERD


class EntityRelationshipDiagram(ERD):
    def __init__(self, path):
        super().__init__()
        self.path = path
        self.file_dict = self._build_file_dict()

    def render(self):
        self._add_tables()
        self._add_relationships()
        dot_string = self._format_dot_string()
        st.graphviz_chart(dot_string, use_container_width=False)

    def _build_file_dict(self):
        file_list = glob.glob(self.path + "/*.csv")
        return {
            file.split("/")[-1].replace(".csv", ""): pd.read_csv(file) for file in file_list
        }

    def _add_tables(self):
        for name, df in self.file_dict.items():
            self.add_table(df, name)

    def _add_relationships(self):
        with open(f'{self.path}/relationships.json', 'r') as f:
            relationships = json.load(f)
        for rel in relationships:
            self.create_rel(**rel)

    def _format_dot_string(self):
        gen_code = self.table_gen_code
        if '\t}' in set(gen_code):
            gen_code.remove('\t}')
        gen_code.append('\t}')
        tmp = gen_code
        return '\n'.join(tmp)
