#from distutils.core import setup
from setuptools import setup

setup(
    name='VolumeAffinityFilter',
    version='0.1.0',
    author='Alexey Ovchinnikov',
    author_email='aovchinnikov@mirantis.com',
    packages=['volume_affinity_filter'],
    description='Volume Affinity Filter for Openstack Nova scheduler',
    long_description=open('README.rst').read(),
)
