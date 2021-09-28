<img src="./frontend/app/images/se-logo.png" alt="Logo of the project" align="right">

# HUS &middot; [![GitHub license](https://img.shields.io/badge/license-MIT-blue.svg?style=flat-square)](https://github.com/your/your-project/blob/master/LICENSE)
> HUS is abbreviation which stands for the collaboration between Hogeschool Utrecht and Schneider Electric

This application is mainly used for monitoring sensordata which is used by the [Logic Controller (Wiser for KNX).](https://www.se.com/nl/nl/product/LSS100100/wiser-for-knx---homelynk-logic-controller/)

It's made by 5 students of Hogeschool Utrecht.

## Installing / Getting started

A quick introduction of what you need to do in order to get the server up &
running.

```shell
clone https://github.com/florisgravendeel/HUS
cd backend / frontend
docker build -t [name] .
```

The code above creates a copy of the application and builds an image.
Here you should say what actually happens when you execute the code above.

## Developing

### Built With
List main libraries, frameworks used including versions (React, Angular etc...)

### Prerequisites
What is needed to set up the dev environment. For instance, global dependencies or any other tools. include download links.

```
C:
│ 
├───backend # everything that has to do with the backend is in this folder
│   ├───app
│   └───Dockerfile # use this Dockerfile to build the backend-image for Docker
│       ├───libary  # Python subpackage containing all the required libraries
│       ├───routers # Python subpackage for routing internet traffic
│       ├───sql_app # Python subpackage for everything that belongs to the database 
│       ├───main.py # The main function is executed in this class
│       └───requirements.txt # contains a list all the packages needed by the backend 
│ 
├───frontend # everything that has to do with the frontend is in this folder
│   ├───app
│   ├───Dockerfile # use this Dockerfile to build the frontend-image for Docker
│   ├───__init__.py # The main function is executed in this file
│   └───requirements.txt # contains a list all the packages needed by the backend 
│       ├───libary  # Python subpackage containing all the required libraries
│       ├───routers # Python subpackage for routing internet traffic
│       └───sql_app # Python subpackage for everything that belongs to the database 
└───venv # This folder is invisible and it's used by the Python Interpreter. 
```
### Setting up Dev

Here's a brief intro about what a developer must do in order to start developing
the project further:

```shell
git clone https://github.com/your/your-project.git
cd your-project/
packagemanager install
```

And state what happens step-by-step. If there is any virtual environment, local server or database feeder needed, explain here.

### Building

If your project needs some additional steps for the developer to build the
project after some code changes, state them here. for example:

```shell
./configure
make
make install
```

Here again you should state what actually happens when the code above gets
executed.

### Deploying / Publishing
give instructions on how to build and release a new version
In case there's some step you have to take that publishes this project to a
server, this is the right time to state it.

```shell
packagemanager deploy your-project -s server.com -u username -p password
```

And again you'd need to tell what the previous code actually does.

## Versioning

We can maybe use [SemVer](http://semver.org/) for versioning. For the versions available, see the [link to tags on this repository](/tags).


## Configuration

Here you should write what are all of the configurations a user can enter when using the project.

## Tests

Describe and show how to run the tests with code examples.
Explain what these tests test and why.

```shell
Give an example
```

## Style guide

Explain your code style and show how to check it.

## Api Reference

If the api is external, link to api documentation. If not describe your api including authentication methods as well as explaining all the endpoints with their required parameters.


## Database

Explaining what database (and version) has been used. Provide download links.
Documents your database design and schemas, relations etc... 

## Licensing

State what the license is and how to find the text version of the license.
