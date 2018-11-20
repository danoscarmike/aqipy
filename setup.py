from setuptools import setup

setup(
    name='aqipy',
    version='0.1.0',
    packages=['aqipy'],
    entry_points={
        'console_scripts': [
            'aqipy = aqipy.__main__:main'
        ]}
)
