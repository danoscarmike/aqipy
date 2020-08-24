from setuptools import setup

with open("README.md", "r") as fh:
    long_description = fh.read()

setup(
    name='aqipy',
    version='0.3.0',
    author='Dan O\'Meara',
    author_email='omeara.dan@gmail.com',
    description='A simple CLI to get live Air Quality Indices',
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/danoscarmike/aqipy",
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
        'Programming Language :: Python :: 3',
        'Development Status :: 3 - Alpha',
        'License :: OSI Approved :: MIT License',
    ]
)
