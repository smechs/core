"""The "hello world" custom component.

This component implements the bare minimum that a component should implement.

Configuration:

To use the oilchecking component you will need to add the following to your
configuration.yaml file.

oilchecking:
"""
from __future__ import annotations

from asyncio import timeout
from datetime import timedelta
import logging

from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant, callback
from homeassistant.const import Platform


from .sensor import MyEntity
from .coordinator import MyCoordinator

from .oilinformationservice import OilInformationService
from .const import DOMAIN

_LOGGER = logging.getLogger(__name__)

PLATFORMS = [Platform.SENSOR]

async def async_setup_entry(hass: HomeAssistant, entry: ConfigEntry) -> bool:
    """Set up Oil Info as config entry."""
    my_api = OilInformationService()  # hass.data[DOMAIN][entry.entry_id]
    coordinator = MyCoordinator(hass, my_api)

    await coordinator.async_config_entry_first_refresh()

    hass.data.setdefault(DOMAIN, {})
    hass.data[DOMAIN][entry.entry_id] = coordinator

    await hass.config_entries.async_forward_entry_setups(entry, PLATFORMS)

    return True



