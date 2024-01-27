"""My custom coordinator."""

from __future__ import annotations

from asyncio import timeout
from datetime import timedelta
import logging

from homeassistant.core import HomeAssistant
from homeassistant.helpers.update_coordinator import DataUpdateCoordinator, UpdateFailed

from .oilinformationservice import OilInformationService, OilPriceInformationDto

_LOGGER = logging.getLogger(__name__)


class OilInformationCoordinator(DataUpdateCoordinator):
    """My custom coordinator."""

    def __init__(self, hass: HomeAssistant, oil_information_service: OilInformationService) -> None:
        """Initialize my coordinator."""
        super().__init__(
            hass,
            _LOGGER,
            # Name of the data. For logging purposes.
            name="OilInfoSensor",
            # Polling interval. Will only be polled if there are subscribers.
            update_interval=timedelta(seconds=60),
        )
        self.my_api: OilInformationService = oil_information_service

    async def _async_update_data(self) -> dict[str, OilPriceInformationDto]:
        """Fetch data from API endpoint.

        This is the place to pre-process the data to lookup tables
        so entities can quickly look up their data.
        """
        try:
            async with timeout(10):
                results: OilPriceInformationDto = await self.my_api.request_oil_information()
                return {"result": results}
        except Exception as err:
            raise UpdateFailed(f"Error communicating with API: {err}") from err
