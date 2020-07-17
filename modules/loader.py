from kivy.app import App
from kivy.lang import Builder

class Loader():
    
    def load_widgets(self):

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
        _load_widgets(app.widgets_data, app)
        _load_widgets(spec_widgets, app, app.device_type)


    def _load_widgets(self, widgets_data, app, device_type = None):

        for ItemName in widgets_data:
            # Print status
            if device_type:
                print(f"[INFO   ] [MainApp     ] load {device_type} widgets: ", ItemName)
            else:
                print(f"[INFO   ] [MainApp     ] load widgets: ", ItemName)

            # get file name
            widgets_file_name   = widgets_data[ItemName]["name"]

            # load py file if exist
            try:
                if device_type:
                    py_class = "from widgets." + str(widgets_file_name) + "." + str(device_type)  +" import " + str(widgets_file_name)
                else:
                    py_class = "from widgets." + str(widgets_file_name) + "." + str(device_type)  +" import " + str(widgets_file_name)

                exec(py_class)
                     
                Factory = str(widgets_file_name) + "()"
                widgets_object = eval(Factory)

                widgets_data[ItemName]["object"] = widgets_object

            except ModuleNotFoundError:
                ""

            # load kv file if exist
            if device_type:  
                Builder.load_file(
                    f"widgets/{widgets_file_name}/{device_type}/{widgets_file_name}.kv"
                )
            else:
                Builder.load_file(
                    f"widgets/{widgets_file_name}/{widgets_file_name}.kv"
                )

            # set current progress
            app.progress_current += 1
            app.progress_percent = (app.progress_current / app.progress_total) * 100
