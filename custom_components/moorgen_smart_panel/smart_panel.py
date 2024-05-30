from homeassistant.core import HomeAssistant
from .const import DOMAIN, BUTTON_KEYS
import asyncio

from . import massegeFFI

# def turn_on_lamp(hass):
#     print("lamp on")
#     hass.states.set("moorgen_smart_panel.test", "lamp on")
#     hass.bus.fire("moorgen_smart_panel_lamp_on")

# def turn_off_lamp(hass):
#     print("lamp off")
#     hass.states.set("moorgen_smart_panel.test", "lamp off")
#     hass.bus.fire("moorgen_smart_panel_lamp_off")

class MoorgenSmartPanel:

    def __init__(self, hass: HomeAssistant, serial_port) -> None:
        self._serial_port = serial_port
        # self.buttons = []
        self.hass:HomeAssistant = hass

        # self.buttons.append()

        massegeFFI.StartMessageHandler(self, serial_port)

    def button_pressed(self, button_num):
        if button_num !=0 & button_num < len(BUTTON_KEYS):
            self.hass.states.set("moorgen_smart_panel.test", button_num)
        
            but = self.hass.data[DOMAIN][BUTTON_KEYS[button_num]]
            asyncio.run_coroutine_threadsafe(but._async_press_action(), self.hass.loop)
        