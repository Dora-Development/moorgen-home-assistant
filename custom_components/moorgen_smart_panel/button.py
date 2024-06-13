from __future__ import annotations

from homeassistant.components import persistent_notification
from homeassistant.components.button import ButtonEntity, ButtonEntityDescription
from homeassistant.core import HomeAssistant
from homeassistant.const import EntityCategory
from homeassistant.helpers.typing import ConfigType, DiscoveryInfoType
from . import smart_panel
from .const import DOMAIN, BUTTON_KEYS, BUTTONS_ICON_TYPE
import logging
import asyncio

_LOGGER = logging.getLogger(__name__)

async def async_setup_entry(hass, config_entry, async_add_entities):
    new_devices = []
    
    for button_key in BUTTON_KEYS:
        if button_key == 0:
            continue
        button_desc = ButtonEntityDescription(
            key=button_key,
            translation_key=button_key
        )

        new_button_entity = TestButton(button_desc)
        new_devices.append(new_button_entity)
        hass.data[DOMAIN][button_desc.key]= new_button_entity

    async_add_entities(new_devices)

class TestButton(ButtonEntity):
    def __init__(self, button: ButtonEntityDescription):
        self._button = button
        self._attr_unique_id = f"{self._button.key}"

    @property
    def name(self):
        return f"Moorgen Smart Panel {self._attr_unique_id} button"

    async def async_press(self) -> None:
        # ограничить частоту нажатий (только 1 нажатие определенной кнопки раз в 5 секунд)
        """Send out a persistent notification."""

        persistent_notification.async_create(
            self.hass, f"Button {self._attr_unique_id}[{self._button.key}] pressed", title="Button"
        )
        self.hass.bus.async_fire(f"Moorgen_smart_panel_{self._attr_unique_id}_button_pressed")
        print(f"Button {self._attr_unique_id}[{self._button.key}] pressed")

    @property
    def device_info(self):
        return {"identifiers": {(DOMAIN, self._attr_unique_id)}}

    @property
    def icon(self):
        return BUTTONS_ICON_TYPE
