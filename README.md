Notes Management System — README

From the project root, start everything with a single command:

docker compose up --build

This builds and runs two containers: the Django backend (django_backend) and the PostgreSQL database. While the containers start, the backend runs the automated steps defined in the entrypoint (migrations, etc.). When it’s done, the app is ready.

Open your browser at http://localhost:8000

You’ll see the login page. A default superuser is already available:

username: admin

password: pass

Log in and you’ll be redirected to the Swagger documentation. From there you can try the Notes APIs, register new users, and use the endpoint that returns a JWT access token. If you want to call protected endpoints from Swagger, click Authorize and paste the access token as:

    Bearer <ACCESS_TOKEN>

The same token works in Postman: set Authorization → Bearer Token (or add the header Authorization: Bearer <ACCESS_TOKEN>), and you can make calls to the APIs outside of Swagger as well.

Note (Windows hosts): ensure all shell scripts use Unix line endings (LF). In particular, verify that docker/entrypoint.sh is saved with LF (not CRLF) and is executable or the container will crash with error: django_backend exited with code 255. If your working copy is mounted into the container, Git on Windows may introduce CRLF line endings, which can cause /bin/bash^M “bad interpreter” errors. To avoid this, if it’s saved with CRLF, convert it to LF from your editor.

What the app does:

Authentication:

    Register a new user (public).

    JWT login to get access/refresh tokens.

    Protected APIs require: Authorization: Bearer <ACCESS_TOKEN>.

    Optional session login for browsing the docs in the browser.

    Current user endpoint to fetch your profile once authenticated.

Notes API

    Full CRUD (create, read, update, delete).

    Each user can see and manage only their own notes.

    Notes have tags (list of strings, normalized).

    Filter by tags: ?tags=report,meeting

    Search in title/content: ?search=... (DRF SearchFilter)

API Docs

    Swagger UI included at localhost:8000/swagger/docs/

    Click Authorize and paste Bearer <ACCESS_TOKEN> to call protected endpoints.

    API endpoints can be accessed also from logged user.
