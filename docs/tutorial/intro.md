# Intro

This tutorial is going to help us build a real-life application using ML-style python provided by the [FunML](https://github.com/sopherapps/funml) package.

In this tutorial, we are going to build a song bank.

Its main features will be:

1. User can add a new song's lyrics.
2. User can remove a song of a given title
3. User can update a song of a given title
4. User can get a song's lyrics, given a song title.
5. User can search for any songs whose title begins with a certain phrase.

This is a basic CRUD operation.

## Dependencies

We will need the following dependencies to get up and running.

- [python +v3.7](https://www.python.org): the programming language to use.
- [poetry](https://python-poetry.org/): the python package manager.
- [funml](https://github.com/sopherapps/funml): the functional ML package for python.
- [FastAPI](https://fastapi.tiangolo.com/): the web framework to serve the app.
- [uvicorn](https://www.uvicorn.org/): the ASGI web server to serve the FastAPI app. 
- [py_scdb](https://github.com/sopherapps/py_scdb): the embedded store to act as a database.

## Install Python

Let's Get started!

Install Python of version 3.7 or above if you don't have it already.

You can install python from [the official python downloads site](https://www.python.org/downloads/).

## Install Poetry

Install Poetry to manage our packages for us.

Look at the [official installation instructions](https://python-poetry.org/docs/#installation).

## For the Impatient

You can also find the finished source code for this tutorial at 
[https://github.com/tinitto/funml-scdb-tutorial](https://github.com/tinitto/funml-scdb-tutorial).

## Create the New Project

Using Poetry, we will create a new project `funml-scdb-tutorial`

<div class="termy">

```console
$ poetry new funml-scdb-tutorial
$ cd funml-scdb-tutorial
$ poetry shell
```
</div>

A `funml-scdb-tutorial` directory is created.

```shell
funml-scdb-tutorial
├── pyproject.toml
├── README.md
├── funml_scdb_tutorial
│   └── __init__.py
└── tests
    └── __init__.py
```

## Install the Python Dependencies

Let's install [FunML](https://github.com/sopherapps/funml), [py_scdb](https://github.com/sopherapps/py_scdb)
and [FastAPI](https://fastapi.tiangolo.com/) with [uvicorn](https://www.uvicorn.org/)

<div class="termy">

```console
$ poetry add funml py_scdb fastapi "uvicorn[standard]"

---> 100%
```

</div>

## Run the Code

To run the app *when ready*, run the command below in your terminal at the root of `funml-scdb-tutorial`:

!!! note
    You must have already created the main.py file in-order for this to work.

<div class="termy">

```console
$ poetry run uvicorn main:app
INFO:     Uvicorn running on http://127.0.0.1:8000 (Press CTRL+C to quit)
INFO:     Started server process [28722]
INFO:     Waiting for application startup.
INFO:     Application startup complete.
```

</div>