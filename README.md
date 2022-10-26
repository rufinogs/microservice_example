# With docker
# microservice_example
microservices_example with Python using Django as the framework and using Docker

In this brach we can see the app using docker.

To launch the environment and the containers:

1.- Install docker desktop

2.- run in terminal this command: docker-compose --env-file .env up --build django_app

3.- To finish the containers you should use this command: docker-compose down -v

# Local Option
# Microservice Example
Example of a costumer microservice with Python using Django as the framework 

To run the microservice first you have to write in the terminal: 

python manage.py makemigrations

python manage.py migrate customer 

python manage.py startapp
