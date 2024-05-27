from .const import DOMAIN

def turn_on_lamp(hass):
    print("lamp on")
    hass.states.set("moorgen_smarp_panel.test", "lamp on")

def turn_off_lamp(hass):
    print("lamp off")
    hass.states.set("moorgen_smarp_panel.test", "lamp off")

def button_pressed(hass, button_num):
    if button_num == 6:
        turn_on_lamp(hass)
    if button_num !=0:
        hass.states.set("moorgen_smarp_panel.test", button_num)