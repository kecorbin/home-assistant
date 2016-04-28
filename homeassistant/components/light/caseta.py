"""
Support for caseta lights.

"""
import logging
import json
from homeassistant.components.light import ATTR_BRIGHTNESS, Light


DEPENDENCIES = ['caseta']
DOMAIN = "light"


def setup_platform(hass, config, add_devices_callback, discovery_info=None):
    """Setup caseta lights."""
    import pycaseta

    # TODO static file reference here
    integration_report = hass.config.config_dir + '/{}'.format('caseta.json')

    with open(integration_report) as f:
        integration_dict = json.load(f)
    print("setup_plaform received: {}".format(integration_dict))
    if len(pycaseta.get_devices(integration_dict=integration_dict)) > 0:
        for device in pycaseta.get_devices(integration_dict=integration_dict):
            add_devices_callback([CasetaDimmer(device)])



class CasetaDimmer(Light):
    """Representation of a caseta lamp dimmer module."""

    def __init__(self, caseta):
        """Initialize the light."""
        self.caseta = caseta

        logging.info('creating new caseta switch')
    @property
    def unique_id(self):
        """Return the ID of this caseta light."""
        return "{}.{}".format(self.__class__, self.caseta.device_id())

    @property
    def name(self):
        """Return the name of the light if any."""
        return self.caseta.name()

    @property
    def is_on(self):
        """Return true if light is on."""
        return self.caseta.state()
    #
    # @property
    # def brightness(self):
    #     """Return the brightness of the light."""
    #     return int(self.caseta.brightness() * 255)

    @property
    def available(self):
        """True if connection == True."""
        return self.caseta.available

    # pylint: disable=too-few-public-methods
    def turn_on(self, **kwargs):
        """Turn the switch on."""
        brightness = kwargs.get(ATTR_BRIGHTNESS)

        if brightness is not None:
            self.caseta.set_state(True, brightness=brightness / 255)
        else:
            self.caseta.set_state(True)

    def turn_off(self):
        """Turn the switch off."""
        self.caseta.set_state(False)

    def update(self):
        """Update state of the light."""
        self.caseta.update_state()