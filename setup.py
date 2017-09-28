from setuptools import setup, find_packages
from minfluxdbconvert.const import (__version__, PROJECT_NAME, PROJECT_LICENSE,
                                  PROJECT_EMAIL, PROJECT_URL, PROJECT_AUTHOR)

with open('./requirements.txt', 'r') as infile:
    REQUIRES = infile.readlines()

PACKAGES = find_packages()

setup(
    name=PROJECT_NAME,
    version=__version__,
    url=PROJECT_URL,
    author=PROJECT_AUTHOR,
    author_email=PROJECT_EMAIL,
    packages=PACKAGES,
    include_package_data=True,
    platforms='any',
    install_requires=REQUIRES,
    entry_points={
        'console_scripts': [
            'mfdb = minfluxdbconvert.__main__:main'
        ]
    }
)
