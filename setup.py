from setuptools import setup

setup(
    name='weatherstation',
    version='1.0',
    description='Tinkerforge RasPi Weatherstation',
    author='Franz Graf',
    author_email='code@Locked.de',
    packages=['weatherstation'],
    install_requires=['tinkerforge']
)