# Recipe App backend
This is a study project in which I'll design a backend system using Python, Django, Postgresql and Docker.

In order to run the project, simply run the command bellow. It will create the docker build and the image and then run the container. 
```commandline
docker compose up
```

In order to see the APIs documentations, you can enter the following address in your browser with the api up and running
```commandline
http://127.0.0.1:8000/api/docs/
```

# Project structure
The project is structured in a way that separates the concerns of different components. The main components are:
- **Django project modules**: 
  - **app**: Contains the Django applications, each responsible for a specific part of the project. Each app has its own models, views, serializers, and URLs.
  - **core**: Contains the core functionality of the project, such as commands, utilities, and settings.
  - **user**: Contains the user resource's code
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

# Resources

### User
The user model is a custom user model that extends the AbstractBaseUser class from Django, since it does not support email fields. The custom user model includes fields for email, name, is_active and is_staff statuses. The user model also includes methods for creating users and superusers.

In order to access private resources in the app, you'll need to create a user using the endpoint `POST /api/user/`. With the user created, you'll need to call the `POST /api/user/token` endpoint to create a token and use this token to authenticate to the private endpoints.

The endpoints from the path `/api/user/me` are used to manage your user's information.

### Recipe