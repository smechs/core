"""Initializing oil information service."""
import logging

import requests
from requests import Response

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
        "deliveryTimes": "normal",
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

    oil_price_dtos: list[OilPriceDto] = []


class OilInformationService:
    """Oil information service."""

    oil_information_configuration: OilInformationConfiguration = (
        OilInformationConfiguration()
    )

    def __init__(self) -> None:
        """Initialize oil information service."""
        self.name: str = "oilservice2"

    def request_oil_information(self) -> OilPriceInformationDto:
        """Request oil info."""
        # response: Response = self._send_request()
        oilpricedto: OilPriceInformationDto = OilPriceInformationDto()
        oilpricedto.oil_price_dtos.append(OilPriceDto(22, "dealer"))

        _LOGGER.info("Oil price retrieved from: %s", oilpricedto.oil_price_dtos[0].dealer)
        return oilpricedto

        # return self._map_response(response=response)

    def _map_response(self, response: Response) -> OilPriceInformationDto:
        oil_price_information_dto: OilPriceInformationDto = OilPriceInformationDto()

        oil_price_list: list = response.json()["data"]

        for oil_price in oil_price_list:
            oil_price_dto: OilPriceDto = OilPriceDto(
                price=oil_price["pricing"]["total"]["brutto"],
                dealer=oil_price["dealer"]["name"],
            )
            oil_price_information_dto.oil_price_dtos.append(oil_price_dto)

        return oil_price_information_dto

    def _send_request(self) -> Response:
        return requests.post(
            url=self.oil_information_configuration.url,
            json=self.oil_information_configuration.payload,
            timeout=15,
        )
