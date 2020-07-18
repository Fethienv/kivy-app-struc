
import settings
import configparser

from kivy.config import Config

class AppConfig:

    def build_config(self,section, key, value):
        Config.read(settings.config_file)
        try:
            Config.get(section, key)
        except configparser.NoSectionError:
            Config.add_section(section)
            Config.set(section, key, value)
        except configparser.NoOptionError:
            Config.set(section, key, value)

    def get_config(self, section, key):
        Config.read(settings.config_file)
        try:
            return Config.get(section, key)
        except configparser.NoSectionError:
            return False
        except configparser.NoOptionError:
            return False

    def save_config(self, section, key, value):
        Config.read(settings.config_file)
        try:
            Config.get(section, key)
        except configparser.NoSectionError:
            Config.add_section(section)

        Config.set(section, key, value)
        Config.write()
    
    def add_config(self, section, key, value):
        Config.read(settings.config_file)
        try:
            Config.get(section, key)
        except configparser.NoSectionError:
            Config.add_section(section)

        Config.set(section, key, value)
    
    def load_default_config(self):

        #self.add_config('kivy', 'window_icon', 'ressources/images/icon.ico')

        font = ['Kacst', 'ressources/fonts/KacstLetter.ttf', 'ressources/fonts/KacstLetter.ttf', 'ressources/fonts/KacstOne.ttf', 'ressources/fonts/KacstOne.ttf']  
        
        self.add_config('kivy', 'default_font', font)

        # detect device type
        if not settings.select_device_by_distances:
            from kivy.utils import platform
            device_type = "desktop" if platform in settings.desktop_os and not settings.force_mobile_style else "mobile"
        else:
            import tkinter
            device_type = "desktop" if tkinter.Tk().winfo_screenwidth() > 480 and not settings.force_mobile_style else "mobile"

        if device_type == 'desktop' :

            self.add_config('kivy', 'desktop', 1)

            if not settings.select_device_by_distances:
                import tkinter

            # Screen size detection
            tkinter_framework = tkinter.Tk()
            screen_width  = tkinter_framework.winfo_screenwidth()
            screen_height = tkinter_framework.winfo_screenheight()

            # set splash screen width & height
            window_height = int(screen_height / 2)
            window_width  = int(screen_width / 2)

            window_left = int((screen_width/2) - (window_width/2))
            window_top  = int((screen_height/2) - (window_height/2))

            self.add_config('graphics', 'height', window_height)
            self.add_config('graphics', 'width', window_width)

            self.add_config('graphics', 'minimum_width', window_width)
            self.add_config('graphics', 'minimum_height', window_height)

            self.add_config('graphics', 'position', "custom")

            self.add_config('graphics', 'top', window_top)
            self.add_config('graphics', 'left', window_left)

        elif  device_type == 'mobile':
            self.build_config('kivy', 'desktop', 0)
            self.save_config('graphics', 'fullscreen', 1)


