from homeassistant.core import HomeAssistant
from .const import DOMAIN, BUTTON_KEYS, FUSE_PATH
import asyncio
import logging
import subprocess
import threading
import time
import os

from . import file_watchdog

_LOGGER = logging.getLogger(__name__)

# def turn_on_lamp(hass):
#     print("lamp on")
#     hass.states.set("moorgen_smart_panel.test", "lamp on")
#     hass.bus.fire("moorgen_smart_panel_lamp_on")

# def turn_off_lamp(hass):
#     print("lamp off")
#     hass.states.set("moorgen_smart_panel.test", "lamp off")
#     hass.bus.fire("moorgen_smart_panel_lamp_off")

def StartSerial(serial_port: str):
    if os.uname().machine == "x86_64":
        arch = "x86_64"
    elif os.uname().machine == "aarch64":
        arch = "aarch64"

    p = subprocess.Popen([f"./config/custom_components/moorgen_smart_panel/remoorgen_{arch}", "--mount", FUSE_PATH, "--serial", serial_port])
    _LOGGER.info("Serial started")
    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        p.terminate()
        time.sleep(3)
        if p.poll()==None:
            p.kill()

class MoorgenSmartPanel:

    def __init__(self, hass: HomeAssistant, logger: logging.Logger, serial_port: str) -> None:
        self._serial_port = serial_port
        self.hass:HomeAssistant = hass

        # Run go binary for serial
        threading.Thread(target=StartSerial, args=[serial_port]).start()

        threading.Thread(target=file_watchdog.StartMonitoringFuse, args=(logger, self)).start()

    def button_pressed(self, button_num):
        if button_num !=0 and button_num < len(BUTTON_KEYS):
            self.hass.states.set("moorgen_smart_panel.test", button_num)
        
            but = self.hass.data[DOMAIN][BUTTON_KEYS[button_num]]
            asyncio.run_coroutine_threadsafe(but._async_press_action(), self.hass.loop)
        