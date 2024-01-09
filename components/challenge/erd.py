import glob
import json
import streamlit as st
import pandas as pd
from pandaserd import ERD


class EntityRelationshipDiagram(ERD):
    def __init__(self, path):
        super().__init__()
        self.path = path

    def render(self):
        erd_image = self._get_erd_image()
        if erd_image:
            with st.expander("Entity Relationship Diagram"):
                st.image(erd_image)
        else:
            file_dict = self._build_file_dict()
            self._add_tables(file_dict)
            self._add_relationships()
            dot_string = self._format_dot_string()
            with st.expander("Entity Relationship Diagram"):
                st.graphviz_chart(dot_string, use_container_width=False)

    def _build_file_dict(self):
        file_list = glob.glob(self.path + "/*.csv")
        return {
            file.split("/")[-1].replace(".csv", ""): pd.read_csv(file) for file in file_list
        }

    def _get_erd_image(self):
        erd_image = glob.glob(self.path + "/erd.*")
        if erd_image:
            return erd_image[0]
        else:
            return None

    def _add_tables(self, file_dict):
        for name, df in file_dict.items():
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
