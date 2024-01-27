"Config flow file."

import logging
from typing import Any

import voluptuous as vol

from homeassistant import config_entries
from homeassistant.const import CONF_API_KEY, CONF_ENTITY_ID, CONF_ROOM
from homeassistant.core import callback
from homeassistant.data_entry_flow import FlowResult
from homeassistant.helpers.schema_config_entry_flow import (
    SchemaFlowFormStep,
    SchemaOptionsFlowHandler,
)

from .const import DEFAULT_NAME, DEFAULT_ROOM, DOMAIN

_LOGGER = logging.getLogger(__name__)

STEP_USER_DATA_SCHEMA = vol.Schema(
    {
        vol.Required(CONF_API_KEY, description="Api Key"): str,
        vol.Required(CONF_ENTITY_ID, default=DEFAULT_NAME, description="Entity Id"): str,
        vol.Required(CONF_ROOM, default=DEFAULT_ROOM, description="Room"): str
    }
)

OPTIONS_FLOW = {
    "init": SchemaFlowFormStep(STEP_USER_DATA_SCHEMA),
}


class ConfigFlow(config_entries.ConfigFlow, domain=DOMAIN):
    """Handle a config flow for oil information checker."""

    VERSION = 1

    async def async_step_user(
        self, user_input: dict[str, Any] | None = None
    ) -> FlowResult:
        """Handle the initial configuration step."""
        errors: dict[str, str] = {}

        _LOGGER.info("Setup config with parameters")

        if user_input is not None:
            if not errors:
                    return self.async_create_entry(
                        title=user_input[CONF_ENTITY_ID], data=user_input
                    )

        return self.async_show_form(
            step_id="user", data_schema=STEP_USER_DATA_SCHEMA, errors=errors
        )


    @staticmethod
    @callback
    def async_get_options_flow(
        config_entry: config_entries.ConfigEntry,
    ) -> SchemaOptionsFlowHandler:
        """Get the options flow for this handler."""
        return SchemaOptionsFlowHandler(config_entry, OPTIONS_FLOW)
