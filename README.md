<img src="./frontend/app/images/se-logo.png" alt="Logo of the project" align="right">

# HUS &middot; [![GitHub license](https://img.shields.io/badge/license-MIT-blue.svg?style=flat-square)](https://github.com/your/your-project/blob/master/LICENSE)
> HUS is abbreviation which stands for the collaboration between Hogeschool Utrecht and Schneider Electric

This application is mainly used for monitoring sensordata which is used by the [Logic Controller (Wiser for KNX).](https://www.se.com/nl/nl/product/LSS100100/wiser-for-knx---homelynk-logic-controller/)

It's made by 5 students of Hogeschool Utrecht.

#### Built with:
* FastAPI
* Uvicorn
* SQLAlchemy
* Vue
* Docker

## Installing / Getting started

A quick introduction of what you need to do in order to get the server up &
running.

Step 1. Copy the project.
```shell
clone https://github.com/florisgravendeel/HUS.git
```
Step 2. Change directory into backend or frontend
```shell
cd backend OR cd frontend
```
Step 3. Create an image with Docker  [(click here if you don't have Docker installed)](https://docs.docker.com/get-docker/)
```shell
docker build -t [name] .
```
Step 4. Open Docker Desktop and run the application.

## API Reference

To check out [live examples](https://www.youtube.com/watch?v=wpV-gGA4PSk) and docs, visit [our website](https://www.youtube.com/watch?v=wpV-gGA4PSk).

## Database

We currently use PostgreSQL. 

### Directory Layout
```
.
│ 
├───backend                  # Everything that has to do with the backend is in this folder
│   ├───app
│   └───Dockerfile           # Use this Dockerfile to build the backend-image for Docker
│       ├───libary           # Python subpackage containing all the required libraries
│       ├───routers          # Python subpackage for routing internet traffic
│       ├───sql_app          # Python subpackage for everything that belongs to the database 
│       ├───main.py          # The main function is executed in this class
│       └───requirements.txt # Contains a list all the packages needed by the backend 
│ 
├───frontend                 # everything that has to do with the frontend is in this folder
│   ├───app
│   ├───Dockerfile           # Use this Dockerfile to build the frontend-image for Docker
│   ├───__init__.py          # The main function is executed in this file
│   └───requirements.txt     # contains a list all the packages needed by the backend 
│       ├───libary           # Python subpackage containing all the required libraries
│       ├───routers          # Python subpackage for routing internet traffic
│       └───sql_app          # Python subpackage for everything that belongs to the database 
└───venv                     # This folder is invisible and it's used by the Python Interpreter. 
```

This is our directory layout, nothing special about. Make sure, you add the right files to the right folder.
- [ ] Diego navragen om de nieuwe mappen opnieuw op te noemen

## Style guide

- [x] uitzoeken welke style wij willen gaan gebruiken? 
- [ ] dat verdomde document terugvinden
- [ ] naming conventions toevoegen
- [ ] expain the code style
- [ ] how to check it

## License

[MIT](https://opensource.org/licenses/MIT)

Copyright (c) 2021 by Floris, Tijmen, Seger, Sven and Diego