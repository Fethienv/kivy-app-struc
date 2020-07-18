# Orgaized
kivy app for organized you project

## Features
- Organized
- Multilanguages
- Compatible with RTL direction
- Responsive

## Compounds:
Compound|Type|
--------------
|Modules|folder|
|Ressources|folder|
|Screens|folder|
|Widgets|folder|
|main|py file|

## Installation:
- python 3.7 recommended
- use pip install -r requirements.txt

## Languages:
### step 1: Extract
'''
pybabel extract main.py ressources modules screens widgets -o ressources/locales/standard.pot -F ressources/locales/mapping.ini
'''

### step 2: Init
'''
pybabel init -l ar_DZ -i ressources/locales/standard.pot -o ressources/locales/ar_DZ/LC_MESSAGES/main_app.po
'''
### step 3: translate file
open po file and translate it

### step 4: compile
'''
pybabel compile -l ar_DZ -i ressources/locales/ar_DZ/LC_MESSAGES/main_app.po -o ressources/locales/ar_DZ/LC_MESSAGES/main_app.mo
'''

for more read babel docs


