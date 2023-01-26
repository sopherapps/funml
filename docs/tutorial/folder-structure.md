# Folder Structure

Let's start by setting up an appropriate folder structure for the app

## Add an Entry point

We need an entry point i.e. the module where the app starts.

Let's create a `main.py` file in the root folder of the project.

<div class="termy">

```console
$ touch main.py
```

</div>

This will be the module that is run using `uvicorn`. It will contain
the FastAPI app instance as this it is the way our song bank interfaces
with the outside world.

## Create the REST API App

Next we need to set up the web REST API app.

Let's create our REST API routes/views module called `api.py` within the
`funml_scdb_tutorial` folder.

<div class="termy">

```console
$ touch funml_scdb_tutorial/api.py
```

</div>

This will contain the definitions for the API, only dealing with what
HTTP clients will be interacting with i.e. the end-points and their handlers.

## Add The Song Bank

We then add the main piece of the app i.e. the song bank service itself.

Let's create a new folder `song_bank` within the `funml_scdb_tutorial` folder.
And add an `__init__.py` module in it to make it a package.

<div class="termy">

```console
$ mkdir funml_scdb_tutorial/song_bank
$ touch funml_scdb_tutorial/song_bank/__init__.py
```

</div>

Everything to do with storing, finding, removing songs internally in the app
will be handled by the `song_bank` package.

!!! info
    Whereas the REST API is a public-facing interface to interact internally with
    the `song_bank` package.
    
    We could have easily used another API e.g. a command line interface to interact with
    the `song_bank` package.

## Final Outlook

The final folder structure should now look like:

```shell

    funml-scdb-tutorial
    ├── README.md
    ├── funml_scdb_tutorial
    │   ├── __init__.py
    │   ├── api.py
    │   └── song_bank
    │       └── __init__.py
    ├── main.py
    ├── poetry.lock
    ├── pyproject.toml
    └── tests
        └── __init__.py
    
```

Next, we will look at setting up the [FastAPI app](./fastapi-app.md)
