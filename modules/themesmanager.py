import settings
from kivy.utils import get_color_from_hex

class AttrDict(dict):
    def __init__(self, *args, **kwargs):
        super(AttrDict, self).__init__(*args, **kwargs)
        self.__dict__ = self

class ThemesManager():

    def get_theme(self, theme = None, mode = None):

        # default settings
        theme = "Purple" if not theme or theme == False  or theme == "False" else theme
        mode  = "Light" if not mode or mode == "OFF" or mode == "False"  else "Dark" 

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