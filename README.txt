================================
OpenStack Volume Affinity Filter
================================

OpenStack Volume Affinity Filter  provides an extra  filter for
Nova scheduler. This filter allows to select hosts on the basis
of volume affinity, i.e. those hosts to which specified volumes
belongs physicaly.

The current version was tested  with Grizzly OpenStack version.
It won't work with Folsom OpenStack or any earlier versions.


FILTER USAGE
============

To use the filter you need to perform the following steps:

1. Install the package  using either pip or easyinstall.

2. Add module name to /etc/nova/nova.conf::

    scheduler_available_filters = volume_affinity_filter.volume_affinity_filter.SameWithVolumeHostFilter

3. Add filter name to the list of available filters::

    scheduler_default_filters=SameWithVolumeHostFilter*<, OtherFilterYouAreToUse, ...>*

4. Restart nova-scheduler.

5. Provide id of a volume you want to use as a hint to nova when booting
a new instance as **same_host_volume_id**. A command to boot an instance
should look like this one::

    nova boot --image=*image_id*  --flavor=*flavor_id* *server_name*
              --hint same_host_volume_id=*volume_id*

This should select a host to which specified volume belongs and run an instance
on it.
