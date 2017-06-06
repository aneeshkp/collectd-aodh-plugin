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

"""Aodh collectd plugin implementation."""

from __future__ import unicode_literals

from collectd_aodh.sender import Sender

import datetime
import logging
import collectd
LOGGER = logging.getLogger(__name__)


class Writer(object):
    """Aodh writer."""

    def __init__(self, meters, config):
        """Initialize Writer."""
        self._meters = meters
        self._sender = Sender()
        self._config = config

    def write(self, vl, data):
        """Collect data from collectd."""
        # take the plugin (specialized or default) for parsing the data
        notification = self._meters.get(vl.plugin)
        #for v in vl.values:
        #   collectd.info("*************************spam: Writing %s (%s): %f" % (vl.plugin, vl.type, v))
        if vl.plugin == "connectivity":
            collectd.info("@@@@@@@@@@@@@@")
            collectd.info("plugin: %s" %(vl.plugin))
            collectd.info("plugin instance:  %s" %(vl.plugin_instance))
            collectd.info("type :  %s" %(vl.type))
            collectd.info("type instanc: %s" %(vl.type_instance))
            collectd.info("host :%s" %(vl.host))
            collectd.info("values: %s" %(vl.values))
            collectd.info("Metername : %s" %(notification.meter_name(vl)))
            collectd.info("resource id :%s" %(notification.resource_id(vl)))

        # prepare all data related to the sample
            metername = notification.meter_name(vl)
            #metername=notification.resource_id(vl)
            meter_value=int(vl.values[0])
            collectd.info("Meter values: %d" %(meter_value))
 
            if  meter_value>=1:
                 message = "Interface "+ vl.type +" is up : within"
                 severity="low"
            else:
                 message = "Interface "+ vl.type +" is down : above"
                 severity="critical"
 
            # message = "Interface" #notification.message(vl)
            #severity = "low" #notification.severity(vl)
            resource_id = notification.resource_id(vl)
            timestamp = datetime.datetime.utcfromtimestamp(vl.time).isoformat()
                
            collectd.info(
                'Writing: plugin="%s", message="%s", severity="%s", time="%s'
                  %(vl.plugin, message, severity, timestamp))

            self._send_data(metername, severity, resource_id, message)

    def _send_data(self, metername, severity, resource_id, message):
        """Send data to Aodh."""
        LOGGER.debug('Sending alarm for %s',  metername)
        self._sender.send(metername, severity, resource_id, message)

