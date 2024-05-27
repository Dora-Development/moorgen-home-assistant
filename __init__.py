"""The Moorgen Smart Panel integration."""

from .massegeFFI import StartMessageHandler
from .const import DOMAIN

def setup(hass, config):
    """Initialise the panel."""
    print("initing")
    hass.states.set("moorgen_smarp_panel.test", "init")

    StartMessageHandler(hass, config)
    return True