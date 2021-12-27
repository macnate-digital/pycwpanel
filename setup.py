from setuptools import setup, find_packages

from pycwpanel import __version__


setup(
    name='pycwpanel',
    version=__version__,
    description='Python Library for interating with the Control Web Panel',
    author='Chris Wachira',
    author_email='chris.wachira@macnate.digital',
    url="https://macnate.digital",
    packages=find_packages(
        include=[
            'pycwpanel',
            'pycwpanel.*'
            ],
    ),
    classifiers=[
        "Programming Language :: Python :: 3.9",
        "License :: OSI Approved :: MIT License",
        "Operating System :: POSIX :: Linux",
    ],
    install_requires=[
        'boto3',
        'Click',
        'dynaconf',  # Dynamically reads config files e.g. toml, ini, .env
        'requests',
        'tomli-w',  # Writes to TOML only
        'validators',
    ],
    extras_require={
        'interactive': [
            'ipython',
        ]
    },
    entry_points={
        'console_scripts': [
            'cwp-setup=pycwpanel.cwp_setup:cwp_setup',
        ]
    },
    python_requires=">=3.9"
)
