"Sensor file."

from __future__ import annotations

from dataclasses import dataclass
import logging
from uuid import uuid4

from homeassistant.components.number import (
    NumberDeviceClass,
    NumberEntity,
    NumberEntityDescription,
    NumberMode,
)
from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant, callback
from homeassistant.helpers.device_registry import DeviceInfo
from homeassistant.helpers.entity_platform import AddEntitiesCallback
from homeassistant.helpers.update_coordinator import CoordinatorEntity

from .const import DOMAIN
from .coordinator import OilInformationCoordinator
from .oilinformationservice import OilInformationService

_LOGGER = logging.getLogger(__name__)


async def async_setup_entry(
    hass: HomeAssistant, entry: ConfigEntry, async_add_entities: AddEntitiesCallback
) -> bool:
    """Config entry example."""
    # assuming API object stored here by __init__.py
    oil_information_service = OilInformationService()
    oil_info_coordinator = OilInformationCoordinator(hass, oil_information_service)

    _LOGGER.info("Setup entry with oil information service and coordinator")

    await oil_info_coordinator.async_config_entry_first_refresh()

    entities: list[OilInfoEntity] = []

    entities.extend(
        [OilInfoEntity(oil_info_coordinator, 2, description) for description in NUMBER_TYPES]
    )

    async_add_entities(entities)

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


class OilInfoEntity(CoordinatorEntity, NumberEntity):
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

    @property
    def device_info(self) -> DeviceInfo:
        """Return the device info."""
        return DeviceInfo(
            identifiers={
                # Serial numbers are unique identifiers within a specific domain
                (DOMAIN, self.unique_id)
            },
            name=self.name,
            manufacturer="mechs",
            model="oildevice",
        )

    @property
    def unique_id(self):
        """Return the ID of this entity."""
        return str(uuid4())

    @callback
    def _handle_coordinator_update(self) -> None:
        """Handle updated data from the coordinator."""
        data = self.coordinator.data
        _LOGGER.info("Handling oil info update: %s entries", len(data.get("result").oil_price_dtos))
        self._attr_native_value = data.get("result").oil_price_dtos[0].price
        self.async_write_ha_state()

    async def async_set_native_value(self, value: float) -> None:
        """Update the current value."""
        await self.coordinator.async_request_refresh()
