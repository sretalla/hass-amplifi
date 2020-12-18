"""copied from another device tracker as a starting point"""
import logging
import urllib.parse
from datetime import timedelta

import requests
import voluptuous as vol

from homeassistant.components.device_tracker import (
    PLATFORM_SCHEMA, SOURCE_TYPE_ROUTER)
from homeassistant.const import (
    CONF_DEVICES, CONF_TOKEN, CONF_URL)
import homeassistant.helpers.config_validation as cv
from homeassistant.helpers.event import track_time_interval
from homeassistant.helpers.typing import ConfigType
from homeassistant.util import slugify, Throttle

_LOGGER = logging.getLogger(__name__)

UPDATE_INTERVAL = timedelta(minutes=5)

PLATFORM_SCHEMA = PLATFORM_SCHEMA.extend({
    vol.Required(CONF_DEVICES): vol.All(cv.ensure_list, [cv.string]),
    vol.Required(CONF_TOKEN): cv.string,
	vol.Required(CONF_URL): cv.string,
})

    @Throttle(UPDATE_INTERVAL)
    def _update_info(self, now=None):
        """Update the device info."""
        _LOGGER.debug("Updating devices %s", now)
        data = requests.get(urllib.parse.urljoin(self.url, self.token)).json()
        data = data[self.token]
        for device in self.devices:
            if device not in data.keys():
                _LOGGER.info('Device %s is not available.', device)
                continue

            self.see(
                dev_id=slugify(device),
                source_type=SOURCE_TYPE_ROUTER
            )
        return True
