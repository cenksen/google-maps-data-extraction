from setuptools import setup, find_packages

setup(
    name='google-maps-data-extraction',
    version='0.1.0',
    description='Google Maps Data Extraction',
    author='Cenk Sen',
    author_email='dev@cenksen.com',
    packages=find_packages(),
    install_requires=[
        'pandas',
        'playwright',
    ],
    entry_points={
        'console_scripts': [
            'google-maps-extract=google_maps_data_extraction.main:main',
        ],
    },
)
