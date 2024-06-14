from homeassistant.core import HomeAssistant, Event
from homeassistant.const import EVENT_HOMEASSISTANT_STOP
from .const import DOMAIN, BUTTON_KEYS, FUSE_PATH, BUTTON_ROLLBACK_TIME
import asyncio
import logging
import subprocess
import threading
import time
import os
import pwd
import datetime

from homeassistant.util import dt as dt_util

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
    
class MoorgenSmartPanel:

    def __init__(self, hass: HomeAssistant, logger: logging.Logger, serial_port: str) -> None:
        self.logger = logger
        self._serial_port = serial_port
        self.hass:HomeAssistant = hass
        self._shutdown = False

        if os.uname().machine == "x86_64":
            path = "./config/custom_components/moorgen_smart_panel/remoorgen_x86_64"
        elif os.uname().machine == "aarch64":
            path = "/config/custom_components/moorgen_smart_panel/remoorgen_aarch64"

        self.serial_process = subprocess.Popen([path, "--mount", FUSE_PATH, "--serial", serial_port])
        self.logger.info("Serial started")

        self.hass.bus.async_listen_once(EVENT_HOMEASSISTANT_STOP, self.shutdown)

        self.file_watchdog = file_watchdog.FileWatchdog(self.logger, self)
        self.file_watchdog.startMonitoringFuse()

    def button_pressed(self, button_num):
        if button_num !=0 and button_num < len(BUTTON_KEYS):
            but = self.hass.data[DOMAIN][BUTTON_KEYS[button_num]]
            if but.state != 'unknown' and (dt_util.utcnow() - datetime.datetime.fromisoformat(but.state)).seconds < BUTTON_ROLLBACK_TIME:
                return
            
            self.hass.states.set("moorgen_smart_panel.test", button_num)
            asyncio.run_coroutine_threadsafe(but._async_press_action(), self.hass.loop)
        
    def shutdown(self, event: Event | None = None) -> None:
        """Graceful shutdown."""
        if self._shutdown:
            return

        self.logger.info("Graceful shutdown")
        self.file_watchdog.stopMonitoringFuse()
        self.serial_process.terminate()
        try:
            self.serial_process.wait(3)
        except subprocess.TimeoutExpired:
            pass
        if self.serial_process.poll()==None:
            self.serial_process.kill()
        self._shutdown = True