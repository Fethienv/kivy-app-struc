from kivy.uix.boxlayout import BoxLayout
from kivy.uix.stacklayout import StackLayout
from kivy.properties import ObjectProperty, ListProperty

class DashbordBaseView(StackLayout):

    top_left_items        = ListProperty() #["menu", lambda x: nav_drawer.set_state("open")]
    top_right_items       = ListProperty() #[["dots-vertical", lambda x: root.callback_1()], ["flag", lambda x: root.callback_2()]]
    bottom_action_button  = ObjectProperty() 
    bottom_left_items     = ListProperty()   #[["menu", lambda x: x]]
    bottom_right_items    = ListProperty()   #[["dots-vertical", lambda x: x], ["clock", lambda x: x]]

    def callback(self):
        pass
    