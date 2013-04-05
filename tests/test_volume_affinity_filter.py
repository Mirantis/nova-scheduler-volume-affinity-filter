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
Tests For Volume Affinity Filter For Nova-Scheduler.
"""

import mox

from nova import context
from nova import exception
from nova.openstack.common import importutils
from nova.scheduler import filters
from nova import test
from nova.tests.scheduler import fakes
import nova.volume.cinder


class HostFiltersTestCase(test.TestCase):
    """Test case for volume affinity filter for nova-scheduler."""

    def setUp(self):
        super(HostFiltersTestCase, self).setUp()
        self.filter_instance = importutils.import_class(
            'volume_affinity_filter.volume_affinity_filter.'
            'SameWithVolumeHostFilter')()
        self.context = context.get_admin_context()

        self.mockReturn = self.mox.CreateMockAnything()
        setattr(self.mockReturn, 'os-vol-host-attr:host', 'host1')
        self.mockObj = self.mox.CreateMockAnything()
        self.mockObj.volumes = self.mox.CreateMockAnything()

    def test_affinity_same_filter_passes(self):
        host = fakes.FakeHostState('host1', 'compute', {})
        filter_properties = {'context': self.context,
                             'scheduler_hints': {
                                 'same_host_volume_id': 'ID', }}
        self.mox.StubOutWithMock(nova.volume.cinder, 'cinderclient')
        self.mockObj.volumes.get('ID').AndReturn(self.mockReturn)
        nova.volume.cinder.cinderclient(self.context).AndReturn(self.mockObj)
        self.mox.ReplayAll()
        self.assertTrue(self.filter_instance.host_passes
                       (host, filter_properties))

    def test_affinity_same_filter_fails(self):
        host = fakes.FakeHostState('host2', 'compute', {})
        filter_properties = {'context': self.context,
                             'scheduler_hints': {
                                 'same_host_volume_id': 'ID', }}
        self.mox.StubOutWithMock(nova.volume.cinder, 'cinderclient')
        self.mockObj.volumes.get('ID').AndReturn(self.mockReturn)
        nova.volume.cinder.cinderclient(self.context).AndReturn(self.mockObj)
        self.mox.ReplayAll()
        self.assertFalse(self.filter_instance.host_passes
                        (host, filter_properties))

    def test_affinity_volume_not_found(self):
        host = fakes.FakeHostState('host1', 'compute', {})
        filter_properties = {'context': self.context,
                             'scheduler_hints': {
                                 'same_host_volume_id': 'WRONG_ID', }}
        self.mox.StubOutWithMock(nova.volume.cinder, 'cinderclient')
        self.mockObj.volumes.get('WRONG_ID').AndRaise(exception.VolumeNotFound(
            volume_id='WORNG_ID'))
        nova.volume.cinder.cinderclient(self.context).AndReturn(self.mockObj)
        self.mox.ReplayAll()
        self.assertFalse(self.filter_instance.host_passes
                        (host, filter_properties))

    def test_affinity_no_hint_supplied(self):
        host = fakes.FakeHostState('host1', 'compute', {})
        filter_properties = {'context': self.context,
                             'scheduler_hints': {}}
        self.assertTrue(self.filter_instance.host_passes
                        (host, filter_properties))
