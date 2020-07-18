# kivy Organized
kivy app for organized you project

## Features
- Organized
- Multilanguages
- Compatible with RTL direction
- Responsive
- Theme Manager
- Screen loader

## Compounds:
Compound|Type|
------------ | -------------
|Modules|folder|
|Ressources|folder|
|Screens|folder|
|Widgets|folder|
|main|py file|
|settings|py file|
|requirements|txt file|

## requirements:
- Python 3.7 recommended
- All packages in requirements.txt file

## Installation:
- Clone project
- Install requirements using: pip install -r requirements.txt
- Devlope your app

## Languages:

### Text Direction:

```

LanguagesManager().bidi()

```

### Current languages:

```

lang, locale, iso_code = LanguagesManager().get_current_language()

```

### Add Languages:
#### step 1: Extract
```

pybabel extract main.py ressources modules screens widgets -o ressources/locales/standard.pot -F ressources/locales/mapping.ini

```

#### step 2: Init
```

pybabel init -l ar_DZ -i ressources/locales/standard.pot -o ressources/locales/ar_DZ/LC_MESSAGES/main_app.po

```

#### step 3: translate file
open po file and translate it

### step 4: compile
```

pybabel compile -l ar_DZ -i ressources/locales/ar_DZ/LC_MESSAGES/main_app.po -o ressources/locales/ar_DZ/LC_MESSAGES/main_app.mo

```

for more read babel docs

## Add theme:
In ressources/themes/ create new json file and add your styles like this 
```

    "Light":
        {
            "theme_style"               : "Light",
            "primary_palette"           : "Green",
            "accent_palette"            : "Yellow",
            "primary_color"             : "6610f2",
            "secondary_color"           : "dcd5de",
            "error_text_color"          : "941212",
            "error_dialog_header_color" : "941212",
            "error_input_border_color"  : "941212",
            "progress_bar_color"        : "6610f2",
            "background_color"          : "ffffff",
            "input_border_color"        : "ffffff",
            "readbox_border_color"      : "a8a3a8",
            "Label_text_color"          : "000000",
            "dashbord_primary_color"    : "e0d5f2",
            "dashbord_secondary_color"  : "d5d2d6",
            "dashbord_icons_normal_color" : "aaa2b8",
            "dashbord_icons_normal_bkg"   : "e0d5f2",
            "dashbord_icons_active_color" : "ffffff",
            "dashbord_icons_active_bkg"   : "6610f2",            
            "font_name"                 : "ressources/fonts/KacstOne.ttf"
        },
    "Dark":
        {
            "theme_style"               : "Dark",
            "primary_palette"           : "LightGreen",
            "accent_palette"            : "Yellow",
            "primary_color"             : "6610f2",
            "secondary_color"           : "dcd5de",
            "error_text_color"          : "941212",
            "error_dialog_header_color" : "941212",
            "error_input_border_color"  : "941212",
            "progress_bar_color"        : "6610f2",
            "background_color"          : "000000",
            "input_border_color"        : "ffffff",
            "readbox_border_color"      : "a8a3a8",
            "Label_text_color"          : "ffffff",
            "dashbord_primary_color"    : "000000",
            "dashbord_secondary_color"  : "000000",
            "dashbord_icons_normal_color" : "aaa2b8",
            "dashbord_icons_normal_bkg"   : "e0d5f2",
            "dashbord_icons_active_color" : "ffffff",
            "dashbord_icons_active_bkg"   : "6610f2",            
            "font_name"                 : "ressources/fonts/KacstOne.ttf"
        }
}

```
Notes:
- You should add _color suffix if you want add a color code
- You should add 2 mode Dark and Light

than use it like this

```
app.theme.dashbord_icons_active_color

```

## Add Screens:
In screens/screens_data.json add your screen data
```
    "ClassName": {
        "subdir"      : "subdir",
        "file_name"   : "file_name",
        "screen_name" : "screen_name",
        "object": 0
    },

```

than create a subdirs like this

```

Screens/subdir/kv/file_name.kv
Screens/subdir/kv/file_name.py

```

in Screens/subdir/kv/file_name.py add class like this

```

from kivy.uix.screenmanager import Screen

class ClassName(Screen):
    pass

```

in Screens/subdir/kv/file_name.kv add class like this

```

#:kivy 1.11.1

<ClassName>:
    name: "screen_name"

```

## Add Widgets:
 
### Common widgets:

In widgets/widgets_data.json add your screen data

```
    "ClassName": {
        "file"  : "file",
        "class" : "ClassName",
        "object": 0
    },

```

than create a subdirs like this

```

widgets/ClassName/file.kv
widgets/ClassName/file.py

```

in widgets/ClassName/file.py add class like this

```

from kivy.uix.boxlayout import BoxLayout

class ClassName(BoxLayout):
    pass

```

in widgets/ClassName/file.kv add class like this

```

#:kivy 1.11.1

<ClassName>:
   

```

### Desktop widgets:

In widgets/desktop_widgets_data.json add your screen data

```
    "ClassName": {
        "file"  : "file",
        "class" : "ClassName",
        "object": 0
    },

```

than create a subdirs like this

```

widgets/ClassName/desktop/file.kv
widgets/ClassName/desktop/file.py

```

in widgets/ClassName/desktop/file.py add class like this

```

from kivy.uix.boxlayout import BoxLayout

class ClassName(BoxLayout):
    pass

```

in widgets/ClassName/desktop/file.kv add class like this

```

#:kivy 1.11.1

<ClassName>:
   

```

### Mobile widgets:

In widgets/mobile_widgets_data.json add your screen data

```
    "ClassName": {
        "file"  : "file",
        "class" : "ClassName",
        "object": 0
    },

```

than create a subdirs like this

```

widgets/ClassName/mobile/file.kv
widgets/ClassName/mobile/file.py

```

in widgets/ClassName/mobile/file.py add class like this

```

from kivy.uix.boxlayout import BoxLayout

class ClassName(BoxLayout):
    pass

```

in widgets/ClassName/mobile/file.kv add class like this

```

#:kivy 1.11.1

<ClassName>:
   

```




