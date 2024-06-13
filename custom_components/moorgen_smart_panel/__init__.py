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
from homeassistant.const import EVENT_HOMEASSISTANT_STOP
import asyncio
# from . import sst
from .const import DOMAIN
import logging
import subprocess
import os

from . import smart_panel
from .package_manager import ManagePackages

_LOGGER = logging.getLogger(__name__)
PLATFORMS: list[str] = ["button"]

async def async_setup_entry(hass: HomeAssistant, entry: ConfigEntry) -> bool:
    # asyncio.run_coroutine_threadsafe(hass.bus.listen_once(EVENT_HOMEASSISTANT_STOP, sp.shutdown), hass.loop)

    if subprocess.call(["which", "fusermount3"]) != 0:
        _LOGGER.info("cannot found package fusermount3, trying to install")
        if ManagePackages("install", "fuse3") != True:
            _LOGGER.info("Failed to install required package 'fuse3'")
            return
        _LOGGER.info("Sucsess install fuse3!")
    else:
        _LOGGER.info("fusermount3 installed")

    if os.uname().machine == "aarch64":
        subprocess.call(["chmod", "+X", "/config/custom_components/moorgen_smart_panel", "-R"])
    
    # проверить и исправить права доступа для бинарников
    
    sp = smart_panel.MoorgenSmartPanel(hass, _LOGGER, entry.data["serial_port"])
    hass.data.setdefault(DOMAIN, {})[entry.entry_id] = sp

    await hass.config_entries.async_forward_entry_setups(entry, PLATFORMS)
    return True

async def async_unload_entry(hass: HomeAssistant, entry: ConfigEntry) -> bool:
    unload_ok = await hass.config_entries.async_unload_platforms(entry, PLATFORMS)
    if unload_ok:
        hass.data[DOMAIN].pop(entry.entry_id)

    return unload_ok