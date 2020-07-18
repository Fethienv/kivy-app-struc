import settings

from kivy.app import App
from kivy.lang import Builder

class ScreensLoader:
    
    def load_widgets(self):
        """ load widgets from registred screens data """

        # get running App
        app = App.get_running_app()

        # get widgets by device
        spec_widgets = app.desktop_widgets_data if app.device_type == "desktop" else app.mobile_widgets_data

        # count how many widgets ?
        count_widgets      = len(app.widgets_data)
        count_spec_widgets = len(spec_widgets)

        # set total progress
        app.progress_total += count_widgets
        app.progress_total += count_spec_widgets

        # load widgets
        self._load_widgets(app.widgets_data, app)
        self._load_widgets(spec_widgets, app, app.device_type)

    def _load_widgets(self, widgets_data, app, device_type = None):

        for ItemName in widgets_data:
            # Print status
            if device_type:
                print(f"[INFO   ] [SCSLoader   ] load {device_type} widgets: ", ItemName)
            else:
                print(f"[INFO   ] [SCSLoader   ] load widgets: ", ItemName)

            # get file name
            widgets_file_name = widgets_data[ItemName]["file"]
            widgets_class     = widgets_data[ItemName]["class"]

            # load py file if exist
            try:
                if device_type:
                    py_class = "from widgets." + str(ItemName) + "." + str(device_type)  + "." + str(widgets_file_name) + " import " + str(widgets_class)
                else:
                    py_class = "from widgets." + str(ItemName) + "." + str(widgets_file_name) + " import " + str(widgets_class)

                exec(py_class)
                     
                Factory = str(widgets_class) + "()"
                widgets_object = eval(Factory)

                widgets_data[ItemName]["object"] = widgets_object

            except ModuleNotFoundError:
                print(f"[ERROR  ] [SCSLoader   ] Class not found: ", ItemName)

            except Exception as e:
                import traceback
                track = traceback.format_exc()
                print("[ERROR  ] [SCSLoader   ] Exception: ", getattr(e, 'message', repr(e)), track ) 

            # load kv file if exist
            if device_type:  
                Builder.load_file(
                    f"widgets/{ItemName}/{device_type}/{widgets_file_name}.kv"
                )
            else:
                Builder.load_file(
                    f"widgets/{ItemName}/{widgets_file_name}.kv"
                )

            # set current progress
            app.progress_current += 1
            app.progress_percent = (app.progress_current / app.progress_total) * 100
    
    def _unload_widgets(self, widgets_data, device_type = None):
        """ unload widgets """

        for ItemName in widgets_data:
            widgets_file_name = widgets_data[ItemName]["file"]

            if device_type: 
                Builder.unload_file(
                    f"widgets/{ItemName}/{device_type}/{widgets_file_name}.kv"
                )
            else:
                Builder.unload_file(
                    f"widgets/{ItemName}/{widgets_file_name}.kv"
                )

            widgets_data[ItemName]["object"] = 0

            # Print status
            if device_type:
                print(f"[INFO   ] [SCSLoader   ] unload {device_type} widgets: ", ItemName)
            else:
                print(f"[INFO   ] [SCSLoader   ] unload widgets: ", ItemName)
        
        return widgets_data


    def _load_or_change_screen(self, class_name, screen_manager = False):
        """ load screen from registred screens data """

        # get running App
        app = App.get_running_app()

        # Screen Manger
        Screen_Manger = screen_manager if screen_manager else app.sm
            
        if not Screen_Manger.has_screen( app.screens_data[class_name]["screen_name"]) and not app.screens_data[class_name]["screen_name"] in app.excluded_screens:

            file_name = app.screens_data[class_name]["file_name"]
            subdir    = app.screens_data[class_name]["subdir"]

            Builder.load_file(
                        f"screens/{subdir}/kv/{file_name}.kv"
            )

            py_class = "from screens." + str(app.screens_data[class_name]["subdir"]) + '.py.' + str(app.screens_data[class_name]["file_name"]) +" import " + str(class_name)
            exec(py_class)

            Factory = str(class_name) + "(name='"+str(app.screens_data[class_name]["screen_name"])+"')"

            screen_object = eval(Factory)

            app.screens_data[class_name]["object"] = screen_object

            Screen_Manger.add_widget(app.screens_data[class_name]["object"])

        manager_name = "in Main Manger" if not screen_manager else "in Dashboard Manger"
                          
        print("[INFO   ] [SCSLoader   ] load screen " + manager_name + ": ", app.screens_data[class_name]["screen_name"])

        app.isDashboard    = False if not screen_manager else True

        app.LastScreen     = str(Screen_Manger.current) if not screen_manager else ""
        app.CurrentScreen  = str(app.screens_data[class_name]["screen_name"])

        Screen_Manger.current = str(app.screens_data[class_name]["screen_name"])

    def ChangeToScreen(self, screen_name, Child = False):

        if Child == True:
            # get running App
            app = App.get_running_app()

            # path to child screen manager
            sm = app.sm.get_screen("Dashboard").ids["dashbordbaseview"].ids['dashboard_Screen_manager_id']

            # Screen class
            screen_class = "Dashboard" + screen_name + "Screen"

        else:
            # Screen class
            screen_class = screen_name + "Screen"

            # Main screen manager
            sm           = None

        self._load_or_change_screen(str(screen_class), screen_manager= sm)

    def DashboardChangeToScreen(self, screen_name, All = False):

        if All == True: 
            self.ChangeToScreen(screen_name= "Dashboard")

        self.ChangeToScreen(screen_name= screen_name, Child = True )

    def _unload_Screens(self, app, screen_manager = None):

        from kivy.uix.screenmanager import Screen

        sm = screen_manager if screen_manager else app.sm

        for class_name in app.screens_data:
            
            if not app.screens_data[class_name]["screen_name"] in app.excluded_screens:
                

                if isinstance(app.screens_data[class_name]["object"], Screen) and app.screens_data[class_name]["object"] != 0:

                    # remove screen
                    sm.remove_widget(app.screens_data[class_name]["object"])

                    # unload string files
                    file_name = app.screens_data[class_name]["file_name"]
                    subdir    = app.screens_data[class_name]["subdir"]

                    Builder.unload_file(
                            f"screens/{subdir}/kv/{file_name}.kv"
                    )

                    app.screens_data[class_name]["object"] == 0

                    print("[INFO   ] [SCSLoader   ] Update screen: ", app.screens_data[class_name]["screen_name"])

        return app.screens_data

    def UpdateScreens(self):

        # get running App
        app = App.get_running_app()

        # remove all widgets in screen manager
        app.sm.clear_widgets()
        Builder.unload_file(app.first_screen_kv)
        Builder.unload_file('screens/ScreenManager.kv')
        Builder.load_file('screens/ScreenManager.kv') 

        # unload common widgets
        app.widgets_data = self._unload_widgets(app.widgets_data)

        # unload specific widgets
        if app.device_type == "desktop": 
            app.desktop_widgets_data = self._unload_widgets(app.desktop_widgets_data, device_type=app.device_type)
        else: 
            app.mobile_widgets_data = self._unload_widgets(app.mobile_widgets_data, device_type=app.device_type)
        
        # remove old language screens
        self._unload_Screens(app)

        # reload widgets and screens 
        self.load(reload=True)

        # load last screen
        if app.isDashboard == True:
            self.DashboardChangeToScreen(screen_name=app.CurrentScreen[9:], All = True)
        else:
            self.ChangeToScreen(screen_name= app.CurrentScreen)

    # Screens and widgets Load data
    def SWloader(self, path):
        ''' method used to read and get screens and widgets data from json file'''
        import ast
        with open(str(path)) as data_dict_json:
            data_dict    = ast.literal_eval(data_dict_json.read())
            data_dict_list = list(data_dict.keys())
            return data_dict, data_dict_list.sort()

    def load(self, reload=False):
        ''' method used to load widgets and screens data '''

        # get running App
        app = App.get_running_app()

        # load widgets data
        print("[INFO   ] [SCSLoader   ] Load global widgets list ...")
        app.widgets_data, app.widgets_data_list = self.SWloader( "widgets/widgets_data.json")

        if app.device_type == "desktop":
            # load desktop widgets
            print("[INFO   ] [SCSLoader   ] Load desktop widgets list ...")
            app.desktop_widgets_data, app.desktop_widgets_data_list = self.SWloader("widgets/desktop_widgets_data.json")

        else:
            # load mobile widgets
            print("[INFO   ] [SCSLoader   ] Load mobile widgets list ...")
            app.mobile_widgets_data, app.mobile_widgets_data_list = self.SWloader("widgets/mobile_widgets_data.json")

        # load screens data
        print("[INFO   ] [SCSLoader   ] Load screens list ...")
        app.screens_data, app.screens_data_list = self.SWloader("screens/screens_data.json")

        if reload == False:
            app.screens_data[app.first_screen_class.name + 'Screen']['object'] = app.first_screen_class

        # load widgets
        self.load_widgets()
