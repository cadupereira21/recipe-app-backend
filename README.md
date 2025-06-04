# Recipe App backend
This is a study project in which I'll design a backend system using Python, Django, Postgresql and Docker.

In order to run the project, simply run the command bellow. It will create the docker build and the image and then run the container. 
```commandline
docker compose up
```

# Project structure
The project is structured in a way that separates the concerns of different components. The main components are:
- **Django project modules**: 
  - **app**: Contains the Django applications, each responsible for a specific part of the project. Each app has its own models, views, serializers, and URLs.
  - **core**: Contains the core functionality of the project, such as commands, utilities, and settings.
  - ***/tests**: Each module has its own tests directory, which contains unit tests for that module.
- **Docker**: In the root, we have the Dockerfile and docker-compose.yml file for building and running the application in a containerized environment.
- **Requirements**: The requirements.txt contains the list of Python packages required for the project.

# Running tests

To run the tests, you can use the following command:
```commandline
docker compose run --rm app python manage.py test
```
OR
```commandline
docker compose run --rm app sh -c "python manage.py test"
```