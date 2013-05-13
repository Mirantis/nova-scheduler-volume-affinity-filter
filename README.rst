================================
OpenStack Volume Affinity Filter
================================

OpenStack Volume Affinity Filter provides an extra filter for
Nova scheduler. This filter allows to select hosts on the basis
of volume affinity, i.e. those hosts to which specified volumes
belong physicaly.

The current version was tested with Grizzly OpenStack version.
It won't work with Folsom OpenStack or any earlier versions.

FILTER USAGE
============

To use the filter you need to perform the following steps:

1. Install the package using either pip or easyinstall.

2. Add module name to /etc/nova/nova.conf:

.. parsed-literal::

    scheduler_available_filters = volume_affinity_filter.volume_affinity_filter.SameWithVolumeHostFilter
3. Add filter name to the list of available filters:

.. parsed-literal::

    scheduler_default_filters = SameWithVolumeHostFilter\ *<, OtherFilterYouAreToUse, ...>*

4. Restart nova-scheduler.
5. Provide id of a volume you want to use as a hint to nova when booting
a new instance as **same_host_volume_id**. A command to boot an instance
should look like this one:

.. parsed-literal::

    nova boot --image=\ *<image_id>*  --flavor=\ *<flavor_id>* *<server_name>*
              --hint same_host_volume_id=\ *<volume_id>*

This should select a host to which specified volume belongs and run an instance
on it.

Note, that to be able to write logging data you must provide proper
logging.conf as well as a reference to it in nova.conf. You can use
standard logging.conf template shipped with nova as a starting point.
In logging.conf you must provide an extra entry describing the logger
used for the filter::

    [logger_vaf]
    level = INFO
    handlers = stderr
    qualname = volume_affinity_filter
