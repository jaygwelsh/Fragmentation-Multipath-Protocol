# setup.py

from setuptools import setup, find_packages

setup(
    name='fmp',  # Updated package name to reflect FMP
    version='0.1.0',
    packages=find_packages(),
    install_requires=[
        'msgpack',
        'cryptography',
        # Add other dependencies here if necessary
    ],
    entry_points={
        'console_scripts': [
            'fmp-sender=fmp.scripts.sender:main',      # Updated entry point
            'fmp-receiver=fmp.scripts.receiver:main',  # Updated entry point
        ],
    },
)
