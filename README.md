Notes Management System — README

From the project root, start everything with a single command:

docker compose up --build

This builds and runs two containers: the Django backend (django_backend) and the PostgreSQL database. While the containers start, the backend runs the automated steps defined in the entrypoint (migrations, etc.). When it’s done, the app is ready.

Open your browser at http://localhost:8000

You’ll see the login page. A default superuser is already available:

username: admin

password: pass

Log in and you’ll be redirected to the Swagger documentation. From there you can try the Notes APIs, register new users, and use the endpoint that returns a JWT access token. If you want to call protected endpoints from Swagger, click Authorize and paste the token as:

    Bearer <ACCESS_TOKEN>

The same token works in Postman: set Authorization → Bearer Token (or add the header Authorization: Bearer <ACCESS_TOKEN>), and you can make calls to the APIs outside of Swagger as well.

That’s it: one command to start, log in at localhost:8000, then explore and test the APIs directly from the docs.