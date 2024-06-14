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
    INTEGRATION_PATH = "./config/custom_components/moorgen_smart_panel"
    FUSE_PATH = INTEGRATION_PATH + "/fuse"
    REMOORGEN_BIN_PATH = INTEGRATION_PATH + "/remoorgen_x86_64"
elif os.uname().machine == "aarch64":
    INTEGRATION_PATH = "/config/custom_components/moorgen_smart_panel"
    FUSE_PATH = INTEGRATION_PATH + "/fuse"
    REMOORGEN_BIN_PATH = INTEGRATION_PATH + "/remoorgen_aarch64"

BUTTON_ROLLBACK_TIME = 5