import settings
from kivy.app import App
from kivy.utils import get_color_from_hex

from modules.config import AppConfig

class AttrDict(dict):
    def __init__(self, *args, **kwargs):
        super(AttrDict, self).__init__(*args, **kwargs)
        self.__dict__ = self

class ThemesManager:

    def get_theme(self):

        # load themes config
        theme_name = AppConfig().get_config('Apparence', 'theme_name')
        dark_mode  = AppConfig().get_config('Apparence', 'theme_mode')

        # default settings
        theme = settings.default_theme if not theme_name or theme_name == False  or theme_name == "False" else theme_name
        mode  = "Light" if (not dark_mode or dark_mode == "OFF" or dark_mode == "False") and not settings.force_dark_mode  else "Dark" 

        # force settings
        theme = settings.default_theme if settings.force_default_theme else theme
        mode  = "Dark" if settings.force_dark_mode else mode

        # load theme file
        import ast
        with open(f"ressources/themes/{settings.Themes[theme]['file_name']}.json") as read_file:
                theme_data = ast.literal_eval(read_file.read())

        def add_get_color(key, code):
            if "_color" in str(key): 
                return get_color_from_hex('#'+str(code))
            else:
                return code

        # load theme data
        theme_data[mode] = {k: add_get_color(k, v) for k, v in theme_data[mode].items()}

        # convert theme as objects.attributes
        d = AttrDict()
        d.update(theme_data[mode])
        return d

    def set_app_theme(self, theme):

        # save theme settings
        AppConfig().save_config('Apparence', 'theme_name', theme)
 
        app = App.get_running_app()
        app.theme = self.get_theme()            
        
    def set_app_theme_mode(self, theme_mode):

        # save theme settings
        AppConfig().save_config('Apparence', 'theme_mode', theme_mode)
 
        app       = App.get_running_app()
        app.theme = self.get_theme()            
        
    def settings_json(self, translator):

        _ = translator

        Themes    = []
        for theme in settings.Themes.keys():
           Themes.append(theme)

        Apparence_settings ='''
                            [
                                {
                                    "type": "title",
                                    "title": "''' + _("Themes Settings") + '''"
                                },
                                { 
                                    "type"   : "options", 
                                    "title"  : "''' + _("Theme") + '''",
                                    "desc"   : "''' + _("Choose your theme") + '''",
                                    "section": "Apparence", "key": "theme_name",
                                    "options": [ "''' + ('", "').join(Themes) + '''" ]
                                },
                                { 
                                    "type"   : "bool", 
                                    "title"  : "''' + _("Dark mode") + '''",
                                    "desc"   : "''' + _("Turn on/off darkmode") + '''",
                                    "section": "Apparence", "key": "theme_mode",
                                    "values" : ["''' + _("OFF") + '''", "''' + _("ON") + '''"]
                                }
                            ]
                            '''
        return Apparence_settings