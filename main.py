import ast

import settings

import kivy

kivy.require('1.11.1')

from kivy.config import Config

# load configuration module
from modules.config import AppConfig

# create and app config
AppConfig().load_default_config()

# kivy app
from kivy.app import App

# kivy kv builder
from kivy.lang import Builder
from kivy.utils import platform


from modules.loader import Loader

# Main application
class MainApp(App):

    device_type = "mobile"

    # loader progress
    progress_current = 0
    progress_percent = 0
    progress_total   = 1


    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        # for load screens and widgets data
        self.widgets_data          = {} 
        self.desktop_widgets_data  = {}
        self.mobile_widgets_data   = {}  
        self.screens_data          = {} 

        # detect device type
        if settings.select_device_by_distances:
            desktop_os  = ['win', 'macosx', 'linux']
            self.device_type = "desktop" if platform in desktop_os else "mobile"
        else:
            import tkinter
            self.device_type = "desktop" if tkinter.Tk().winfo_screenwidth() > 480 else "mobile"

    def build(self):
        # Only first screen
        from screens.main.py import MainScreen

        self.sm = Builder.load_file('screens/ScreenManager.kv')        
        self.sm.current = "Main"

        return self.sm
    
    def on_start(self):
        """Creates a list of items with examples on start screen."""

        # load drawables data
        print("[INFO   ] [MainApp     ] Load global widgets list ...")
        with open("widgets/widgets_data.json") as widgets_data_json:
            self.widgets_data = ast.literal_eval(widgets_data_json.read())
            widgets_data = list(self.widgets_data.keys())
            widgets_data.sort()

        if self.device_type == "desktop":
            # load desktop drawables
            print("[INFO   ] [MainApp     ] Load desktop widgets list ...")
            with open("widgets/desktop_widgets_data.json") as desktop_widgets_data_json:
                self.desktop_widgets_data = ast.literal_eval(desktop_widgets_data_json.read())
                desktop_widgets_data = list(self.desktop_widgets_data.keys())
                desktop_widgets_data.sort()
        else:
            # load mobile drawables
            print("[INFO   ] [MainApp     ] Load mobile widgets list ...")
            with open("widgets/mobile_widgets_data.json") as mobile_widgets_data_json:
                self.mobile_widgets_data = ast.literal_eval(mobile_widgets_data_json.read())
                mobile_widgets_data = list(self.mobile_widgets_data.keys())
                mobile_widgets_data.sort()

        # load screens data
        print("[INFO   ] [MainApp     ] Load screens list ...")
        with open("screens/screens_data.json") as screens_data_json:
            self.screens_data = ast.literal_eval(screens_data_json.read())
            screens_data = list(self.screens_data.keys())
            screens_data.sort()

        Loader().load_widgets()


# reset Cache
def reset():
    import kivy.core.window as window
    from kivy.base import EventLoop
    if not EventLoop.event_listeners:
        from kivy.cache import Cache
        window.Window = window.core_select_lib('window', window.window_impl, True)
        Cache.print_usage()
        for cat in Cache._categories:
            Cache._objects[cat] = {}

# run app
if __name__ == "__main__":
    reset()
    MainApp().run()