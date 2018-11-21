# AQIPY  

A simple tool to get Air Quality Indices from around the world.

## Installation    
1. Get an API token [here](https://aqicn.org/data-platform/token/#/).    
1. Create an environment variable with your token:    
`export AQIPY_TOKEN='<your_new_token>'`    
1. Clone this repository.
1. From your new directory:    
`pip3 install -e .`

## Usage
To get the AQI for your current location (IP based):    
`aqipy`

To get the AQI for a specific location (latitude longitude):    
`aqipy geo [--latlon / -l <lat lon>]`    

## Attribution     
This tool uses APIs provided by the [World Air Quality Index Project](http://waqi.info/).   
