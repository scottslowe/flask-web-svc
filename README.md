# A Simple Flask Web Service

A simple but flexible Flask web service used to demonstrate microservices architectures. It is designed to operate across three different containers:

* A "front-end" container that provides an HTML response based on information gathered from two "back-end" JSON-based web services
* The "users" API, which is a JSON-based web service queried by the front-end container(s)
* The "orders" API, which is a JSON-based web service queried by the front-end container(s)

## Usage

This web service is a single application designed to run in three separate containers.

### Using Docker Compose

The easiest way to spin up the application is to use Docker Compose. A `docker-compose.yml` file is provided in the repository.

```
docker-compose up -d
```

### Running the Containers Manually

Running the containers manually is a bit more difficult, but certainly possible.

1. First, launch the "users" API container:

        docker run -d -e PORT=6000 -p 6000:6000 slowe/flask-web-svc:latest

    Make note of the IP address where the container is running, as you'll need it later.

2. Next, launch the "orders" API container:

        docker run -d -e PORT=7000 -p 7000:7000 slowe/flask-web-svc:latest

    As with the previous step, make note of the IP address where this container is scheduled.

3. Before proceeding, ensure that the back-end containers are working properly. Use `curl` or a web browser to access the URL for the containers:

        http://<IP address from step 1>:6000/users/json/
        http://<IP address from step 2>:7000/users/json/

    You should get back a JSON-formatted response that contains information about the request. If this doesn't work, resolve the issue before continuing.

4. Finally, launch the front-end container:

        docker run -d -e USER_API_HOST=<IP address from step 1> -e USER_API_PORT=6000 -e ORDER_API_HOST=<IP address from step 2> -e ORDER_API_PORT=7000 -p 5000:5000 slowe/flask-web-svc:latest

    If you want the front-end container to listen on a port _other_ than 5000, change the `-p` parameter and add an additional environment parameter in the form `-e PORT=<desired port>`.

The application is now running and ready to use. You can use `curl` or a web browser to access the application:

    http://<IP address from step 4>:5000/

This will provide an HTML-formatted response that contains information about the request and the requests/responses from the back-end JSON-based web services. You can use this information to see how various container orchestration systems and other technologies affect the communications between containers.

## License

This material is licensed under the MIT License.
