from kivy.uix.screenmanager import Screen
from kivymd.uix.datatables import MDDataTable
from kivy.metrics import dp
from kivymd.uix.button import MDIconButton

from kivy.uix.relativelayout import RelativeLayout
from models.db_utils import *

class DistrictForm(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        ensure_tables_exist()
        self.populate_table()

    def submit_district(self):
        district_name = self.ids.district_field.text
        if district_name.strip():
            insert_record('districts', ['name'], [district_name])
            print("District Inserted")
            self.ids.district_field.text = ""
            self.populate_table()  # Refresh the table data
        else:
            print("District name cannot be empty!")

    def populate_table(self):
        districts = fetch_all_records('districts')
        table_data = [
            (
                str(index),
                district['name'],
                self.create_action_buttons(district['district_id'])
            )
            for index, district in enumerate(districts, 1)
        ]

        # Create MDDataTable if it doesn't exist
        if not hasattr(self, 'data_table'):
            self.data_table = MDDataTable(
                size_hint=(1, 0.8),
                pos_hint={'center_x': 0.5},
                rows_num=10,
                column_data=[
                    ("ID", dp(40)),
                    ("District Name", dp(40)),
                    ("Actions", dp(40)),
                ],
                row_data=table_data,
                use_pagination=True,
            )
            self.ids.table_container.add_widget(self.data_table)
        else:
            self.data_table.row_data = table_data

    def create_action_buttons(self, district_id):
        layout = RelativeLayout(size_hint_x=None, width=dp(30))
        delete_button = MDIconButton(icon="delete", on_release=lambda x: self.delete_district(district_id))
        layout.add_widget(delete_button)
        return layout

    def delete_district(self, district_id):
        delete_record('districts', district_id)
        print(f"District with ID {district_id} deleted")
        self.populate_table()  # Refresh the table data
