"""The Moorgen Smart Panel integration."""

# from .massegeFFI import StartMessageHandler
# from .const import DOMAIN

# def setup(hass, config):
#     """Initialise the panel."""
#     print("initing")
#     hass.states.set("moorgen_smarp_panel.test", "init")

#     StartMessageHandler(hass, config)
#     return True

from __future__ import annotations

from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant
import asyncio
# from . import sst
from .const import DOMAIN
import logging

from . import smart_panel

_LOGGER = logging.getLogger(__name__)
PLATFORMS: list[str] = ["button"]

async def async_setup_entry(hass: HomeAssistant, entry: ConfigEntry) -> bool:
    #Создать объект с подключением к сервису
    # sst1 = sst.SST(hass, entry.data["username"], entry.data["password"])
    
    sp = smart_panel.MoorgenSmartPanel(hass, _LOGGER, entry.data["serial_port"])
    
    hass.data.setdefault(DOMAIN, {})[entry.entry_id] = sp
    # await hass.async_add_executor_job(
    #          sst1.pull_data
    #      )

    await hass.config_entries.async_forward_entry_setups(entry, PLATFORMS)
    return True

async def async_unload_entry(hass: HomeAssistant, entry: ConfigEntry) -> bool:
    unload_ok = await hass.config_entries.async_unload_platforms(entry, PLATFORMS)
    if unload_ok:
        hass.data[DOMAIN].pop(entry.entry_id)

    return unload_ok