"Sensor file."

from __future__ import annotations

from dataclasses import dataclass
import logging

from homeassistant.components.number import (
    NumberDeviceClass,
    NumberEntity,
    NumberEntityDescription,
    NumberMode,
)
from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant, callback
from homeassistant.helpers.entity_platform import AddEntitiesCallback
from homeassistant.helpers.update_coordinator import CoordinatorEntity

from .coordinator import MyCoordinator
from .oilinformationservice import OilInformationService

_LOGGER = logging.getLogger(__name__)

async def async_setup_entry(
    hass: HomeAssistant, entry: ConfigEntry, async_add_entities: AddEntitiesCallback
) -> bool:
    """Config entry example."""
    # assuming API object stored here by __init__.py
    my_api = OilInformationService()  # hass.data[DOMAIN][entry.entry_id]
    coordinator = MyCoordinator(hass, my_api)

    _LOGGER.info("Setup entry with my_api and coordinator")

    # Fetch initial data so we have data when entities subscribe
    #
    # If the refresh fails, async_config_entry_first_refresh will
    # raise ConfigEntryNotReady and setup will try again later
    #
    # If you do not want to retry setup on failure, use
    # coordinator.async_refresh() instead
    #
    await coordinator.async_config_entry_first_refresh()

    entities: list[MyEntity] = []

    entities.extend(
            [
                MyEntity(coordinator, 2, description)
                for description in NUMBER_TYPES
            ]
        )

    async_add_entities(
        entities
    )

    return True

@dataclass(frozen=True)
class OilInfoNumberEntityDescription(NumberEntityDescription):
    """Describes BMW number entity."""


NUMBER_TYPES: list[OilInfoNumberEntityDescription] = [
    OilInfoNumberEntityDescription(
        key="oil_info",
        translation_key="oil_info",
        device_class=NumberDeviceClass.VOLUME,
        native_max_value=5000.0,
        native_min_value=1000.0,
        native_step=50.0,
        mode=NumberMode.SLIDER,
        icon="mdi:battery-charging-medium",
    ),
]

class MyEntity(CoordinatorEntity, NumberEntity):
    """An entity using CoordinatorEntity.

    The CoordinatorEntity class provides:
      should_poll
      async_update
      async_added_to_hass
      available

    """

    def __init__(self, coordinator, idx, description) -> None:
        """Pass coordinator to CoordinatorEntity."""
        super().__init__(coordinator, context=idx)
        self.idx = idx
        self.name = "OilInfo"
        self.coordinator = coordinator
        self.device_class = NumberDeviceClass.VOLUME_STORAGE
        self.entity_description = description

    @callback
    def _handle_coordinator_update(self) -> None:
        """Handle updated data from the coordinator."""
        data = self.coordinator.data
        _LOGGER.info("Handling update: %s", len(data.get("result").oil_price_dtos))
        self._attr_native_value = data.get("result").oil_price_dtos[0].price
        self.async_write_ha_state()

    async def async_set_native_value(self, value: float) -> None:
        """Update the current value."""
        # Do the turning on.
        # ...

        # Update the data
        await self.coordinator.async_request_refresh()
