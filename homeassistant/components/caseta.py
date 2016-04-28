"""
Support for caseta lights.
For more details about this platform, please refer to the documentation at
https://home-assistant.io/components/light.caseta/
"""
import logging
import json
from homeassistant import bootstrap
from homeassistant.const import (
    ATTR_DISCOVERED, ATTR_SERVICE, CONF_ACCESS_TOKEN,
    EVENT_PLATFORM_DISCOVERED)
from homeassistant.helpers import validate_config
from homeassistant.helpers.entity import ToggleEntity
from homeassistant.loader import get_component
from homeassistant.components.light import ATTR_BRIGHTNESS, Light
from homeassistant.loader import get_component

REQUIREMENTS = ['python-caseta']
DOMAIN = "light"

def setup(hass, config):
    """Setup the Caseta component."""
    global lutronapi
    logger = logging.getLogger(__name__)

    import pycaseta

    config = config['caseta']
    host = config.get('host')
    port = config.get('port',23)
    user = config.get('user','lutron')
    pw = config.get('password','integration')
    ir_file = config.get('integration_report')
    logging.info('Setting credentials for pycaseta')

    pycaseta.set_credentials(host, port, user, pw)

    integration_report = hass.config.config_dir + '/{}'.format(ir_file)

    with open(integration_report) as f:
        integration_dict = json.load(f)

    # Load components for the devices
    for component_name, func_exists, discovery_type in (
            ('light', pycaseta.get_devices(integration_dict), 'light_bulb'),

            ):



        component = get_component(component_name)

        # Ensure component is loaded
        bootstrap.setup_component(hass, component.DOMAIN, config)

        # Fire discovery event
        hass.bus.fire(EVENT_PLATFORM_DISCOVERED, {
            ATTR_SERVICE: discovery_type,
            ATTR_DISCOVERED: {}
        })

    return True

