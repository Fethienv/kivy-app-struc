from kivy.app import App
from kivy.lang import Builder

class ScreensLoader():
    
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
                ""

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

    def _load_or_change_screen(self, class_name, screen_manager = False):
        """ load screen from registred screens data """

        # get running App
        app = App.get_running_app()

        # Screen Manger
        Screen_Manger = screen_manager if screen_manager else app.sm
            
        if not Screen_Manger.has_screen(
                app.screens_data[class_name]["screen_name"]
        ):
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
        Screen_Manger.current = str(app.screens_data[class_name]["screen_name"])

    def ChangeToScreen(self, screen_name, Child = False):

        if Child == True:
            # get running App
            app = App.get_running_app()

            # path to child screen manager
            sm = app.sm.get_screen("Dashboard").ids["dashbordbaseview"].ids['dashboard_Screen_manager_id']

            # Screen class
            screen_class = "Child" + screen_name + "Screen"

        else:
            # Screen class
            screen_class = screen_name + "Screen"

            # Main screen manager
            sm           = None

        self._load_or_change_screen(str(screen_class), screen_manager= sm)