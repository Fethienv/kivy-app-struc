
# config file
config_file = "config.ini"

# turn on profile stat
debug_profile = False

# device type selection options
select_device_by_distances = False

# list of os considerate as desktop os
desktop_os  = ['win', 'macosx', 'linux']

# Device type allways mobile
force_mobile_style = False

# loader update excluded screens
# Note: if yu add a screen name here, you should import its class when call it
excluded_screens = []

# installed themes list
Themes =  {
        'Purple' :{"file_name": "purple"},
        'Green'  :{"file_name": "green"},
    }

# Language settings
allways_use_default_language = False

# Set default language iso code
default_language = "en_US"

# Languages list
Languages = [
    {
        'name'    : "English",
        'icon'    : "flag",
        'iso_code': "en_US",
    },
    {
        'name'    : "Français",
        'icon'    : "flag",
        'iso_code': "fr_FR",
    },
    {
        'name'    : "العربية",
        'icon'    : "flag",
        'iso_code': "ar_DZ",
    },
]

# languages domain
lang_domain = "main_app"

# Themes settings

# default theme name
default_theme  = "Purple"

# allways use darkmode
force_dark_mode = False

# allways default theme
force_default_theme = False

# global url requests settings
# curl -H "X-Api-Key: GBL_API_KEY" http://192.168.1.160:8000/api/v2/blog/

API_HOST_URL = "http://localhost:8000/"
API_URL      = API_HOST_URL + "api/v2/"
API_KEY      = ""

# headers
headers = { 'content-type': 'application/json',
            "X-Api-Key": API_KEY,
        }
