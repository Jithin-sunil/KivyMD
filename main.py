from kivy.lang import Builder
from kivymd.app import MDApp
from kivy.uix.screenmanager import ScreenManager
from views.district import DistrictForm
from views.category import CategoryForm
from views.homepage import HomePage

class MainApp(MDApp):
    def build(self):
        kv_files = ['kv/district.kv', 'kv/category.kv', 'kv/homepage.kv']
        for kv in kv_files:
            try:
                Builder.load_file(kv)
                print(f"Loaded {kv}")
            except Exception as e:
                print(f"Error loading {kv}: {e}")

        self.sm = ScreenManager()
        screens = [
            (HomePage, 'homepage'),
            (DistrictForm, 'district_form'),
            (CategoryForm, 'category_form')
        ]
        
        for screen_class, screen_name in screens:
            try:
                self.sm.add_widget(screen_class(name=screen_name))
                print(f"Added {screen_name}")
            except Exception as e:
                print(f"Error adding {screen_name}: {e}")

        return self.sm

if __name__ == "__main__":
    MainApp().run()
