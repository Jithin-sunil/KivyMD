from kivy.uix.screenmanager import Screen
from kivymd.uix.label import MDLabel
from kivymd.uix.textfield import MDTextField
from kivymd.uix.button import MDRaisedButton
from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.gridlayout import MDGridLayout
from kivymd.uix.button import MDRaisedButton, MDIconButton
from kivy.metrics import dp
from kivy.uix.scrollview import ScrollView
from models.db_utils import *

class DistrictForm(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        ensure_tables_exist()
        self.build_ui()
        self.populate_table()

    def build_ui(self):
        layout = MDBoxLayout(orientation='vertical', padding=dp(20), spacing=dp(10))

        # Input section
        input_layout = MDBoxLayout(orientation='horizontal', size_hint_y=None, height=dp(60), spacing=dp(10), padding=[dp(20), dp(10)])
        self.district_field = MDTextField(hint_text="Enter District Name", size_hint_x=0.8)
        submit_button = MDRaisedButton(text="Submit", on_release=lambda x: self.submit_district(), size_hint_x=0.2)

        input_layout.add_widget(self.district_field)
        input_layout.add_widget(submit_button)
        layout.add_widget(input_layout)

        # Table header
        header_layout = MDGridLayout(cols=3, size_hint_y=None, height=dp(40), padding=[dp(10), dp(10)], spacing=dp(10))
        header_layout.add_widget(MDLabel(text="ID", size_hint_x=None, width=dp(40), halign="center"))
        header_layout.add_widget(MDLabel(text="District Name", halign="center"))
        header_layout.add_widget(MDLabel(text="Actions", size_hint_x=None, width=dp(80), halign="center"))
        layout.add_widget(header_layout)

        # Scroll view for table data
        scroll_view = ScrollView()
        self.table_container = MDGridLayout(cols=3, spacing=dp(30), size_hint_y=None, padding=[dp(30), dp(30)])
        self.table_container.bind(minimum_height=self.table_container.setter('height'))
        scroll_view.add_widget(self.table_container)
        layout.add_widget(scroll_view)

        self.add_widget(layout)

    def submit_district(self):
        district_name = self.district_field.text
        if district_name.strip():
            insert_record('districts', ['name'], [district_name])
            print("District Inserted")
            self.district_field.text = ""
            self.populate_table()  # Refresh the table data
        else:
            print("District name cannot be empty!")

    def populate_table(self):
        self.table_container.clear_widgets()  # Clear previous table data

        districts = fetch_all_records('districts')
        for index, district in enumerate(districts, 1):
            self.table_container.add_widget(MDLabel(text=str(index), size_hint_x=None, width=dp(40), halign="center"))
            self.table_container.add_widget(MDLabel(text=district['name'], halign="center"))
            self.table_container.add_widget(self.create_action_buttons(district['id']))

    def create_action_buttons(self, id):
        layout = MDBoxLayout(orientation='horizontal', size_hint_x=None, width=dp(80), padding=[dp(20), 0])
        delete_button = MDIconButton(icon="delete", on_release=lambda x: self.delete_district(id))
        layout.add_widget(delete_button)
        return layout

    def delete_district(self, id):
        print(f"Attempting to delete district with ID {id}")
        delete_record('districts', id)
        print(f"District with ID {id} deleted")
        self.populate_table()  # Refresh the table data
