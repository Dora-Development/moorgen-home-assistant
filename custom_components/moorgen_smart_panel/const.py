"""Constants for the Moorgen Smart Panel integration."""
import os

DOMAIN = "moorgen_smart_panel"

BUTTON_KEYS = [
    "no_button",        # 0
    "guest",            # 1 
    "leave",            # 2
    "home",             # 3
    "movie",            # 4
    "curtain_open",     # 5
    "lamp_on",          # 6
    "lamp_off",         # 7
    "curtain_close"     # 8
] 

BUTTONS_ICON_TYPE = "mdi:button-pointer"

if os.uname().machine == "x86_64":
    FUSE_PATH = "./config/custom_components/moorgen_smart_panel/fuse"
elif os.uname().machine == "aarch64":
    FUSE_PATH = "/config/custom_components/moorgen_smart_panel/fuse"

BUTTON_ROLLBACK_TIME = 5