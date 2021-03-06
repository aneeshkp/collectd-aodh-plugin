# -*- coding: utf-8 -*-

# Licensed under the Apache License, Version 2.0 (the "License"); you may
# not use this file except in compliance with the License. You may obtain
# a copy of the License at
#
#      http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS, WITHOUT
# WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the
# License for the specific language governing permissions and limitations
# under the License.

"""Aodh collectd plugin."""

import logging

try:
    # pylint: disable=import-error
    import collectd
    # pylint: enable=import-error
except ImportError:
    collectd = None  # when running unit tests collectd is not avaliable

import collectd_ceilometer
from collectd_aodh.writer import Writer
from collectd_common.logger import CollectdLogHandler
from collectd_common.meters import MeterStorage
from collectd_common.settings import Config


LOGGER = logging.getLogger(__name__)
ROOT_LOGGER = logging.getLogger(collectd_.aodh__name__)


def register_plugin(collectd):
    """Bind plugin hooks to collectd and viceversa."""
    config = Config.instance()

    # Setup loggging
    log_handler = CollectdLogHandler(collectd=collectd)
    log_handler.cfg = config
    ROOT_LOGGER.addHandler(log_handler)
    ROOT_LOGGER.setLevel(logging.NOTSET)

    # Creates collectd plugin instance
    instance = Plugin(collectd=collectd, config=config)

    # Register plugin callbacks
    collectd.register_config(instance.config)
    collectd.register_shutdown(instance.shutdown)
    collectd.register_write(instance.write)

class Plugin(object):
    """Aodh plugin with collectd callbacks."""

    # NOTE: this is a multithreaded class

    def __init__(self, collectd, config):
        """Plugin instance."""
        self._config = config
        self._meters = MeterStorage(collectd=collectd)
        self._writer = Writer(self._meters, config=config)

    def config(self, cfg):
        """Configuration callback.

        @param cfg configuration node provided by collectd
        """
        self._config.read(cfg)

    def write(self, vl, data=None):
        """write callback."""
        LOGGER.info("AODH ***********************Notification")
        self._writer.write(vl, data)

    def shutdown(self):
        """Shutdown callback."""
        LOGGER.info("SHUTDOWN")


if collectd:
    register_plugin(collectd=collectd)

