import settings
import gettext

import arabic_reshaper
import bidi.algorithm as alg_bidi
import locale as PLocale

from kivy.app import App
from babel import Locale as BLocale

from modules.config import AppConfig

class LanguagesManager:

    languages_dir = 'ressources/locales'

    def get_current_language(self):
        ''' method use to get current language from config.ini file, os or from settings '''

        config_language  = AppConfig().get_config('localization', 'language')
        current_language = PLocale.getdefaultlocale()[0] if not config_language else config_language # get language from config ini or auto detect os language
        App.get_running_app().current_language = current_language if current_language else settings.default_language # if get os or config laguage faild get current language

        locale   = BLocale.parse(App.get_running_app().current_language)
        lang     = gettext.translation(settings.lang_domain, localedir=self.languages_dir, languages=[App.get_running_app().current_language], fallback=True)
        iso_code = App.get_running_app().current_language

        return lang, locale, iso_code
    
    def get_current_language_as_dict(self):
        ''' method use to return a dict contain the selected language '''

        flag = "earth"
        for language in settings.Languages:
            if language['name'] == App.get_running_app().locale.get_language_name(App.get_running_app().current_language):
                flag = language['icon']

        CurrentSelectedLanguage = [{"text":alg_bidi.get_display(arabic_reshaper.reshape(App.get_running_app().locale.get_language_name(App.get_running_app().current_language))), 'icon':flag}]
        return CurrentSelectedLanguage

    def ChangeToLanguage(self, selected_Language_iso_code):
        ''' method use to change between languages '''

        locale   = BLocale.parse(selected_Language_iso_code)
        lang     = gettext.translation(settings.lang_domain, localedir=self.languages_dir, languages=[selected_Language_iso_code], fallback=True)
        iso_code = selected_Language_iso_code
        App.get_running_app().current_language = selected_Language_iso_code
        return lang, locale, iso_code

    def translate(self, *args):
        ''' method use to translate '''
        text = alg_bidi.get_display(arabic_reshaper.reshape(App.get_running_app().lang.gettext(*args)))
        return text

    def bidi(self):
        ''' method use to get direction by language '''
        bidi = {"left-to-right":"ltr","right-to-left":"rtl"}
        return bidi[App.get_running_app().locale.character_order]

    def set_app_language(self, selected_Language_iso_code):
        app = App.get_running_app()

        app.lang, app.locale, app.iso_code = self.ChangeToLanguage(selected_Language_iso_code)
        _ = app.lang.gettext #The 'u' in 'ugettext' is for Unicode - use this to keep Unicode from breaking the app

        # save config ini
        AppConfig().save_config('localization', 'language', app.iso_code)


    def settings_json(self, translator):

        _ = translator

        languages = []

        for language in settings.Languages:
           languages.append(language["iso_code"])

        Multilingual_settings = '''
                                    [
                                        {
                                            "type": "title",
                                            "title": "'''+_("Themes Settings")+'''"
                                        },
                                        { 
                                            "type"   : "options", 
                                            "title"  : "'''+_("Language Settings")+'''",
                                            "desc"   : "'''+_("Choose which language to translate the text of this app into")+'''",
                                            "section": "localization", "key": "language",
                                            "options": [ "''' + ('", "').join(languages) + '''" ]
                                        }
                                    ]
                                '''

        return Multilingual_settings
 
def _(*args):
    ''' translation function'''
    return LanguagesManager().translate(*args)




    




