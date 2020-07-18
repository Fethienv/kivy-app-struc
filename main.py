import settings

import cProfile
import pstats

import kivy

kivy.require('1.11.1')

from kivy.config import Config
from kivy.uix.settings import SettingsWithSidebar, SettingsWithNoMenu, SettingsWithSpinner

# load configuration module
from modules import AppConfig

# create and app config
AppConfig().load_default_config()

# kivy app
from kivy.app import App

# kivy kv builder
from kivy.lang import Builder

# modules
from modules import ScreensLoader, ThemesManager, LanguagesManager

# load string translator
_ = LanguagesManager().translate


# Main application
class MainApp(App):

    # device
    device_type = "mobile"

    # loader progress
    progress_current = 0
    progress_percent = 0
    progress_total   = 1

    # laguages
    current_language = ""

    use_kivy_settings = False

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        # for load screens and widgets data
        self.widgets_data          = {} 
        self.desktop_widgets_data  = {}
        self.mobile_widgets_data   = {}  
        self.screens_data          = {} 

        # loader update excluded screens
        self.excluded_screens = settings.excluded_screens

        # detect device type
        if not settings.select_device_by_distances:
            from kivy.utils import platform
            self.device_type = "desktop" if platform in settings.desktop_os and not settings.force_mobile_style else "mobile"
        else:
            import tkinter
            self.device_type = "desktop" if tkinter.Tk().winfo_screenwidth() > 480 and not settings.force_mobile_style else "mobile"

        # load language
        self.lang, self.locale, self.iso_code = LanguagesManager().get_current_language() 

        # load theme
        self.theme = ThemesManager().get_theme()

        # app title
        self.title = _("Kivy Organisation")

        # setting panel style
        if self.device_type == "desktop":
            self.settings_cls = SettingsWithSpinner # SettingsWithSidebar : only with python 3.7
        else:
            self.settings_cls = SettingsWithSpinner # after will be: SettingsWithNoMenu  

    def build(self):
        ''' build method '''

        # create screen manager
        self.sm = Builder.load_file('screens/ScreenManager.kv') 

        # Only first screen and it
        from screens.main.py.main import MainScreen

        self.first_screen_kv = 'screens/main/kv/main.kv'
        Builder.load_file(self.first_screen_kv) 
        self.first_screen_class = MainScreen(name="Main")

        self.sm.add_widget(self.first_screen_class)

        # change to first screen
        self.sm.current = str(self.first_screen_class.name)

        # set last screen name
        self.CurrentScreen = self.sm.current
        self.LastScreen    = self.sm.current
        self.isDashboard   = False

        return self.sm
    
    def on_start(self):
        """Creates a list of items with examples on start screen."""

        # for debug
        if settings.debug_profile:
            self.profile = cProfile.Profile()
            self.profile.enable()

        # load screens and widgets
        ScreensLoader().load()

    def on_stop(self):
        ''' on stop method '''

        # for debug
        if settings.debug_profile:
            self.profile.disable()
            self.profile.dump_stats('app.profile')
            p = pstats.Stats('app.profile')
            p.strip_dirs().sort_stats(-1).print_stats()

    
    ## Settings
    def build_config(self, config):
        ''' build configuration method '''

        self.config = Config
        AppConfig().build_config('localization', 'language', self.iso_code)
        AppConfig().build_config('Apparence', 'theme_name', "Purple")
        AppConfig().build_config('Apparence', 'theme_mode', "OFF")

    def build_settings(self, settings):
        ''' build settings method '''

        settings.add_json_panel(_('Multilingual'), self.config, data=LanguagesManager().settings_json(translator=_))
        settings.add_json_panel(_('Apparence'), self.config, data=ThemesManager().settings_json(translator=_))
        

    def on_config_change(self, config, section, key, value):
        ''' on config change method '''

        if config is not self.config:
            return
        token = (section, key)
        if token == ('localization', 'language'):
            print("[INFO   ] [AppConfig   ] Set language to : ", value)
            LanguagesManager().set_app_language(value)
            
        if token == ('Apparence', 'theme_mode'):
            print("[INFO   ] [AppConfig   ] Set theme mode : ", value)
            ThemesManager().set_app_theme_mode(theme_mode = str(value))
            
        if token == ('Apparence', 'theme_name'):
            print("[INFO   ] [AppConfig   ] Set theme : ", value)
            ThemesManager().set_app_theme(theme=str(value))

        # live apply changes
        ScreensLoader().UpdateScreens()
        reset()

        
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