from setuptools import setup

setup(
    name='aqipy',
    version='0.1.0',
    author='Dan O\'Meara',
    author_email='omeara.dan@gmail.com',
    packages=['aqipy'],
    entry_points={
        'console_scripts': [
            'aqipy = aqipy.__main__:main'
        ]},
    install_requires=[
        'click',
        'requests',
    ],
    classifiers=[
        'Development Status :: 1 - Planning',
    ]
)
