"""Initializing oil information service."""
import logging

import httpx
from httpx import Response

_LOGGER = logging.getLogger(__name__)

class OilInformationConfiguration:
    """Oil information configuration."""

    url: str = "https://backbone.esyoil.com/heating-oil-calculator/v1/calculate"
    payload: dict = {
        "zipcode": "90522",
        "amount": 3000,
        "unloading_points": 1,
        "payment_type": "ec",
        "prod": "normal",
        "hose": "fortyMetre",
        "short_vehicle": "withTrailer",
        "deliveryTimes": "normal"
    }


class OilPriceDto:
    """Oil price dto."""

    price: int
    dealer: str

    def __init__(self, price: int, dealer: str) -> None:
        """Initialize dto."""
        self.price = price
        self.dealer = dealer

class OilPriceInformationDto:
    """Oil price information dto."""

    def __init__(self) -> None:
        """Init."""
        self.oil_price_dtos: list[OilPriceDto] = []


class OilInformationService:
    """Oil information service."""

    oil_information_configuration: OilInformationConfiguration = (
        OilInformationConfiguration()
    )

    def __init__(self) -> None:
        """Initialize oil information service."""
        self.name: str = "oilservice2"

    async def request_oil_information(self) -> OilPriceInformationDto:
        """Request oil info."""
        oilpricedto: OilPriceInformationDto = self._map_response(await self._send_request())

        _LOGGER.info("Oil price information retrieved with %s entries", str(len(oilpricedto.oil_price_dtos)))
        return oilpricedto

    def _map_response(self, response: Response) -> OilPriceInformationDto:
        oil_price_information_dto: OilPriceInformationDto = OilPriceInformationDto()

        oil_price_list: list = response.json()["data"]

        for oil_price in oil_price_list:
            oil_price_dto: OilPriceDto = OilPriceDto(
                price=oil_price["pricing"]["total"]["brutto"],
                dealer=oil_price["dealer"]["name"],
            )
            oil_price_information_dto.oil_price_dtos.append(oil_price_dto)

        _LOGGER.info("Mapped response")

        return oil_price_information_dto

    async def _send_request(self) -> Response:
        async with httpx.AsyncClient() as client:
            _LOGGER.info("Sending request with url %s", self.oil_information_configuration.url)
            response = await client.post(url=self.oil_information_configuration.url, json=self.oil_information_configuration.payload)
            _LOGGER.info("Receiving data")

            return response
