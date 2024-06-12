from kivy.uix.screenmanager import Screen
from kivymd.uix.datatables import MDDataTable
from kivy.metrics import dp
from kivymd.uix.button import MDIconButton

from kivy.uix.relativelayout import RelativeLayout
from models.db_utils import *

class CategoryForm(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        ensure_tables_exist()
        self.populate_table()

    def submit_category(self):
        category_name = self.ids.category_field.text
        if category_name.strip():
            insert_record('tbl_category', ['name'], [category_name])
            print("Category Inserted")
            self.ids.category_field.text = ""
            self.populate_table()  # Refresh the table data
        else:
            print("Category name cannot be empty!")

    def populate_table(self):
        categories = fetch_all_records('tbl_category')
        table_data = [
            (
                str(index),
                category['name'],
                self.create_action_buttons(category['category_id'])
            )
            for index, category in enumerate(categories, 1)
        ]

        # Create MDDataTable if it doesn't exist
        if not hasattr(self, 'data_table'):
            self.data_table = MDDataTable(
                size_hint=(1, 0.8),
                pos_hint={'center_x': 0.5},
                rows_num=10,
                column_data=[
                    ("ID", dp(40)),
                    ("Category Name", dp(40)),
                    ("Actions", dp(40)),
                ],
                row_data=table_data,
                use_pagination=True,
            )
            self.ids.table_container.add_widget(self.data_table)
        else:
            self.data_table.row_data = table_data

    def create_action_buttons(self, category_id):
        layout = RelativeLayout(size_hint_x=None, width=dp(30))
        delete_button = MDIconButton(icon="delete", on_release=lambda x: self.delete_category(category_id))
        layout.add_widget(delete_button)
        return layout

    def delete_category(self, category_id):
        delete_record('tbl_category', category_id)
        print(f"Category with ID {category_id} deleted")
        self.populate_table()  # Refresh the table data
