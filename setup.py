"""Setup file for minfluxdbconvert."""
from setuptools import setup, find_packages
from minflux.const import (__version__, PROJECT_NAME, PROJECT_LICENSE,
                           PROJECT_EMAIL, PROJECT_URL, PROJECT_AUTHOR)

REQUIRES = [
    'pyyaml==3.12',
    'influxdb==4.1.1',
    'voluptuous==0.10.5',
    'coloredlogs==7.3',
    'pytz==2017.2',
    'typing>=3,<4'
]

PACKAGES = find_packages()

setup(
    name=PROJECT_NAME,
    version=__version__,
    url=PROJECT_URL,
    author=PROJECT_AUTHOR,
    author_email=PROJECT_EMAIL,
    license=PROJECT_LICENSE,
    packages=PACKAGES,
    include_package_data=True,
    platforms='any',
    install_requires=REQUIRES,
    entry_points={
        'console_scripts': [
            'minflux = minflux.__main__:main'
        ]
    }
)
