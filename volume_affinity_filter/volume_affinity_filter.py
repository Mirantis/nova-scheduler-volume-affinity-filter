# Copyright 2011 OpenStack LLC.  # All Rights Reserved.
#
#    Licensed under the Apache License, Version 2.0 (the "License"); you may
#    not use this file except in compliance with the License. You may obtain
#    a copy of the License at
#
#         http://www.apache.org/licenses/LICENSE-2.0
#
#    Unless required by applicable law or agreed to in writing, software
#    distributed under the License is distributed on an "AS IS" BASIS, WITHOUT
#    WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the
#    License for the specific language governing permissions and limitations
#    under the License.
"""
Volume Affinity Filter For Nova-Scheduler.

This filter selects only that host to which specified volume
belongs. Other hosts get rejected.
"""

from nova import exception
from nova.openstack.common import log as logging
from nova.scheduler import filters
import nova.volume.cinder as brick

LOG = logging.getLogger(__name__)


class SameWithVolumeHostFilter(filters.BaseHostFilter):
    """Schedule the instance on the same host as given volume_id."""
    hint_name = 'same_host_volume_id'

    def host_passes(self, host_state, filter_properties):
        """Processes same_host_volume_id hint if given."""

        context = filter_properties['context']
        scheduler_hints = filter_properties['scheduler_hints']
        volume_id = scheduler_hints.get(self.hint_name, False)
        if volume_id:
            try:
                host = host_state.host
                the_brick = brick.cinderclient(context).volumes.get(volume_id)
                vol_host = getattr(the_brick, 'os-vol-host-attr:host', None)
                return host == vol_host
            except exception.VolumeNotFound:
                LOG.warning('volume with provided id ("%s") was not found',
                            volume_id)
                return False
        # With no same_volume_host key
        LOG.debug('no %s hint provided, filter passes', self.hint_name)
        return True
