# Popular Service

A service to check whether a given github repo is popular or not.

## Tech stack

The service is written in python 3 using FastAPI/Pydantic to serve its REST API and PyGithub to communicate with github. It uses a Personal access token from Github to retreive the data it needs.

## How to

### Build

#### virtualenv

```sh
$ virtualenv venv
$ . venv/bin/activate
# prod environment
$ pip install -r requirements.txt
# or dev environment
$ pip install -r requirements-dev.txt
```

#### docker

```sh
# build
$ docker build -t popular .
```

### Run Tests

```sh
# only in dev
$ pytest
```

### Run the service locally

Create a personal access token from Github (Token settings can be found here: https://github.com/settings/tokens).

Update the .env file with your GITHUB_TOKEN env var or export it in your shell.

#### virtualenv

```sh
$ python -m uvicorn main:app
```

#### docker

```sh
$ docker run --env-file .env -p 8000:8000 --name pop --rm popular
```

#### docker-compose

```sh
$ docker-compose up -d
```

After starting the service navigate to http://localhost:8000/docs in your browser to see the swagger docs and try out the endpoints.
