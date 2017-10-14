# A Simple Flask Web Service

A simple but flexible Flask web service used to demonstrate microservices architectures.

## Usage

This web service does nothing other than respond, either in HTML or JSON, with information about the web request, the system making the request, and the system handling the request.

To run the web service, simply execute the Python script in the `app` directory, like this:

```
python app/main.py
```

Or, as a Docker container:

```
docker run -d -p 5000:5000 slowe/flask-web-svc:latest
```

Specify the `PORT` environment variable to have the web service listen on a port _other_ than 5000, like this:

```
PORT=7000 python app/main.py
```

Or, when using a Docker container:

```
docker run -d -e PORT=7000 -p 7000:7000 slowe/flask-web-svc:latest
```

Once the application is running, make web requests to it (using `curl` or a web browser). _Any_ top-level URL is supported, and will all return the same information. Assuming you have the application listening on port 5000 on IP address 192.168.99.100, these requests would all return a valid HTML response:

```
http://192.168.99.100:5000/auth
http://192.168.99.100:5000/api
http://192.168.99.100:5000/test
```

The web service will **not** respond to multi-level paths, like `/auth/user` or `/api/object`. Only a single-level path is currently supported.

Appending `/json` to the URL will cause the web service to respond in JSON instead of HTML.

## License

This material is licensed under the MIT License.
